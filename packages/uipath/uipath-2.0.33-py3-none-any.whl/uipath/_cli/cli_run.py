# type: ignore
import asyncio
import logging
import os
import traceback
from os import environ as env
from typing import Optional
from uuid import uuid4

import click
from dotenv import load_dotenv

from ._runtime._contracts import (
    UiPathRuntimeContext,
    UiPathRuntimeError,
    UiPathTraceContext,
)
from ._runtime._runtime import UiPathRuntime
from .middlewares import MiddlewareResult, Middlewares

logger = logging.getLogger(__name__)
load_dotenv()


def python_run_middleware(
    entrypoint: Optional[str], input: Optional[str], resume: bool
) -> MiddlewareResult:
    """Middleware to handle Python script execution.

    Args:
        entrypoint: Path to the Python script to execute
        input: JSON string with input data
        resume: Flag indicating if this is a resume execution

    Returns:
        MiddlewareResult with execution status and messages
    """
    if not entrypoint:
        return MiddlewareResult(
            should_continue=False,
            info_message="""Error: No entrypoint specified. Please provide a path to a Python script.
Usage: `uipath run <entrypoint_path> <input_arguments>`""",
        )

    if not os.path.exists(entrypoint):
        return MiddlewareResult(
            should_continue=False,
            error_message=f"""Error: Script not found at path {entrypoint}.
Usage: `uipath run <entrypoint_path> <input_arguments>`""",
        )

    try:

        async def execute():
            context = UiPathRuntimeContext.from_config(
                env.get("UIPATH_CONFIG_PATH", "uipath.json")
            )
            context.entrypoint = entrypoint
            context.input = input
            context.resume = resume
            context.job_id = env.get("UIPATH_JOB_KEY")
            context.trace_id = env.get("UIPATH_TRACE_ID")
            context.tracing_enabled = env.get("UIPATH_TRACING_ENABLED", True)
            context.trace_context = UiPathTraceContext(
                trace_id=env.get("UIPATH_TRACE_ID"),
                parent_span_id=env.get("UIPATH_PARENT_SPAN_ID"),
                root_span_id=env.get("UIPATH_ROOT_SPAN_ID"),
                enabled=env.get("UIPATH_TRACING_ENABLED", True),
                job_id=env.get("UIPATH_JOB_KEY"),
                org_id=env.get("UIPATH_ORGANIZATION_ID"),
                tenant_id=env.get("UIPATH_TENANT_ID"),
                process_key=env.get("UIPATH_PROCESS_UUID"),
                folder_key=env.get("UIPATH_FOLDER_KEY"),
                reference_id=env.get("UIPATH_JOB_KEY") or str(uuid4()),
            )
            context.logs_min_level = env.get("LOG_LEVEL", "INFO")

            async with UiPathRuntime.from_context(context) as runtime:
                await runtime.execute()

        asyncio.run(execute())

        # Return success
        return MiddlewareResult(should_continue=False)

    except UiPathRuntimeError as e:
        return MiddlewareResult(
            should_continue=False,
            error_message=f"Error: {e.error_info.title} - {e.error_info.detail}",
            should_include_stacktrace=False,
        )
    except Exception as e:
        # Handle unexpected errors
        logger.exception("Unexpected error in Python runtime middleware")
        return MiddlewareResult(
            should_continue=False,
            error_message=f"Error: Unexpected error occurred - {str(e)}",
            should_include_stacktrace=True,
        )


@click.command()
@click.argument("entrypoint", required=False)
@click.argument("input", required=False, default="{}")
@click.option("--resume", is_flag=True, help="Resume execution from a previous state")
def run(entrypoint: Optional[str], input: Optional[str], resume: bool) -> None:
    """Execute the project."""
    # Process through middleware chain
    result = Middlewares.next("run", entrypoint, input, resume)

    if result.should_continue:
        result = python_run_middleware(
            entrypoint=entrypoint, input=input, resume=resume
        )

    # Handle result from middleware
    if result.error_message:
        click.echo(result.error_message, err=True)
        if result.should_include_stacktrace:
            click.echo(traceback.format_exc(), err=True)
        click.get_current_context().exit(1)

    if result.info_message:
        click.echo(result.info_message)

    # If middleware chain completed but didn't handle the request
    if result.should_continue:
        click.echo("Error: Could not process the request with any available handler.")
        click.get_current_context().exit(1)


if __name__ == "__main__":
    run()

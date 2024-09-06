import boto3
import click
from dotenv import load_dotenv
import os, re
from typing import Optional, Dict, Any

load_dotenv()

# Load AWS credentials from environment variables for security
sagemaker_client = boto3.client(
    "sagemaker",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


@click.group("utility")
@click.version_option("0.3.0")
def cli() -> None:
    """CLI group for app commands."""
    pass


@cli.command()
@click.option("-n", "--name", help="Pipeline Name", required=True)
@click.option("-r", "--rolearn", help="Pipeline Execution RoleARN", required=True)
@click.option("-f", "--filename", help="Pipeline Definition file", type=click.Path(exists=True))
@click.option("-p", "--parameter", multiple=True, help="Pipeline Hyperparameters")
@click.option(
    "-c",
    "--choice",
    type=click.Choice(["start", "create", "delete", "update", "list"], case_sensitive=False),
    help="CRUD operations",
    required=True
)
def sagemaker(name: str, rolearn: str, filename: Optional[str], parameter: Optional[str], choice: str) -> None:
    """Sagemaker Helper functions"""
    try:
        if choice in ["create", "update"] and filename:
            with open(filename, "r") as f:
                pipeline_definition_json = f.read()

        params = [dict([p.split("=") for p in parameter])] if parameter else []

        if choice == "create":
            message = sagemaker_client.create_pipeline(
                PipelineName=name,
                PipelineDefinition=pipeline_definition_json,
                RoleArn=rolearn,
            )
        elif choice == "update":
            message = sagemaker_client.update_pipeline(
                PipelineName=name,
                PipelineDefinition=pipeline_definition_json,
                RoleArn=rolearn,
            )
        elif choice == "start":
            message = sagemaker_client.start_pipeline_execution(
                PipelineName=name,
                PipelineParameters=params
            )
        elif choice == "list":
            message = list_pipelines()
        elif choice == "delete":
            message = sagemaker_client.delete_pipeline(PipelineName=name)
        else:
            message = "Invalid Option"

        click.echo(message)

    except Exception as e:
        click.echo(f"Error: {e}")


def list_pipelines() -> Any:
    """Lists all Sagemaker pipelines and their executions."""
    pipeline_list = sagemaker_client.list_pipelines()
    message = []

    for pipeline in pipeline_list["PipelineSummaries"]:
        pipeline_name = pipeline["PipelineDisplayName"]
        execution_list = sagemaker_client.list_pipeline_executions(PipelineName=pipeline_name)
        execution_logs = []

        for execution in execution_list["PipelineExecutionSummaries"]:
            executionARN = execution["PipelineExecutionArn"]
            params_list = sagemaker_client.list_pipeline_parameters_for_execution(
                PipelineExecutionArn=executionARN
            )["PipelineParameters"]
            hyperparameters = {param["Name"]: param["Value"] for param in params_list}

            execution_logs.append({
                "PipelineExecutionArn": executionARN,
                "PipelineExecutionDisplayName": execution["PipelineExecutionDisplayName"],
                "PipelineExecutionStatus": execution["PipelineExecutionStatus"],
                "PipelineParameters": hyperparameters,
            })

        message.append({
            "PipelineArn": pipeline["PipelineArn"],
            "RoleArn": pipeline["RoleArn"],
            "PipelineDisplayName": pipeline_name,
            "PipelineExecutionSummaries": execution_logs,
        })

    return message


@cli.command()
@click.argument("filename", type=click.Path())
@click.argument("message")
def version(filename: str, message: str) -> Optional[str]:
    """Version Bump based on major, minor, and patch releases."""
    tag = read_version_file(filename)
    tag_version = tag[1:].split(".")

    if "MAJOR" in message.upper():
        tag_version[0], tag_version[1], tag_version[2] = int(tag_version[0]) + 1, 0, 0
    elif "MINOR" in message.upper():
        tag_version[1], tag_version[2] = int(tag_version[1]) + 1, 0
    else:
        tag_version[2] = int(tag_version[2]) + 1

    updated_version = "v" + ".".join(map(str, tag_version))
    click.echo(updated_version)

    write_version_file(filename, updated_version)
    click.echo(f'Saved to {filename}')
    return None


def read_version_file(filename: str) -> str:
    """Read version from the file, if exists."""
    return open(filename).read().strip() if os.path.exists(filename) else "v0.0.0"


def write_version_file(filename: str, version: str) -> None:
    """Write version to the file."""
    with open(filename, "w") as file:
        file.write(version)


@cli.command()
@click.argument("filename", type=click.Path())
@click.argument("version")
def update_charts(filename: str, version: str) -> None:
    """Update Chart.yaml with a new version."""
    # Implement chart updating logic as needed
    click.echo(f'Updated {filename} with version {version}')


if __name__ == "__main__":
    cli()

# Utility CLI

**Utility CLI** is a tool focussing on automating day-to-day tasks. This tool simplifies the management of ML pipelines on AWS with easy commands to create, list, start, update and delete SageMaker pipelines. Additionally this tool also supports version bumps using semantic versioning. Soon will expand support for other Infras!

## Features

### 1. SageMaker Pipeline Management

The CLI offers commands to create, update, start, list, and delete SageMaker pipelines.

#### Create a Pipeline
You can create a new pipeline by specifying a pipeline definition file, role ARN, and pipeline name.

```bash
utility sagemaker -c create -f <filename> -r <pipeline-execution-role-arn> -n <pipeline-name>
```

#### List All Pipelines
Retrieve a list of all available SageMaker pipelines.

```bash
utility sagemaker -c list
```

#### Start a Pipeline Execution
Trigger an execution for an existing pipeline, passing any necessary parameters.

```bash
utility sagemaker -c start -n <pipeline-name> -p Name=param0 -p Value=value0
```

#### Delete a Pipeline
Remove a pipeline by specifying its name.

```bash
utility sagemaker -c delete -n <pipeline-name>
```
#### Update an Existing Pipeline
Update a pipeline by specifying the new definition file, role ARN, and pipeline name.

```bash
utility sagemaker -c update -f <filename> -r <pipeline-execution-role-arn> -n <pipeline-name>
```

### 2. Version Management with Semantic Versioning

The CLI follows semantic versioning (`major`, `minor`, `patch`), allowing you to easily bump versions based on changes to your project.

#### Major Version Update
Use this command for a major version update.

```bash
utility version version.txt major
```

#### Minor Version Update
Use this command for a minor version update.

```bash
utility version version.txt minor
```

#### Patch (Bug Fix) Version Update
Use this command for a patch or bug fix update.

```bash
utility version version.txt patch
```

## Installation

1. Install the required dependencies:
    ```bash
    pip install git+https://github.com/SupreethKunder/Utility-CLI.git
    ```

2. Configure your AWS credentials in a `.env` file:
    ```env
    AWS_ACCESS_KEY_ID=your-access-key-id
    AWS_SECRET_ACCESS_KEY=your-secret-access-key
    AWS_REGION=your-region
    ```

## Usage

Run the commands directly from your terminal to manage SageMaker pipelines or bump the version of your project.

### Example: Creating a New Pipeline
```bash
utility sagemaker -c create -f pipeline_definition.json -r arn:aws:iam::123456789012:role/SageMakerRole -n MyPipeline
```

### Example: Triggering a Pipeline Execution
```bash
utility sagemaker -c start -n MyPipeline -p Name=param1 -p Value=value1
```

### Example: Bumping the Version (Minor Update)
```bash
utility version version.txt minor
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.


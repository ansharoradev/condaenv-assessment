# Packages and CLI automation
* Task: Automate creating 2 conda environments, search and install different packages in
both environments. Finally verify the packages are installed successfully.
  * Task Description: The candidate should write the test cases preferably in Python
  using Pytest and required python libraries to run the CLI commands.
  * Task Requirement: The packages installation run in Linux, Windows and MacOS
  correspondingly. Add required validations and a test execution report for the
  developed tests.

## Project Structure
- `tests/test_envs.py`: Contains the test cases for creating conda environments and installing packages.
- `tests/env.py`: Contains the helper functions for creating and managing conda environments.
- `tests/packages.py`: Contains the helper functions for installing and verifying packages in conda environments.
- `requirements.txt`: Lists the dependencies required for the project.
- `.github/workflows/multiple_conda_envs.yml`: GitHub Actions workflow for running the tests on multiple operating systems.

Included but not used since `conda_cli` provides a better interface for automating existing `conda` operations.
- `tests/env_subprocess.py`: Contains the helper functions for creating and managing conda environments using subprocess.

## Setup
1. Clone the repository:
```
git clone git@github.com:anshooarora/condaenv-assessment.git
cd condaenv-assessment
```

2. Create a conda environment and install the dependencies:
```
conda create --name condaenvtests -y
conda activate condaenvtests
conda install -y --file requirements.txt
```

## Running Tests
To run the tests, use the following command:
```
pytest tests/test_envs.py
```

To view a detailed report of the test results, you can use the `--html=reports/pytest_report.html` option. This will generate an HTML report of the test results in the `reports` directory.

```
pytest tests/test_envs.py --html=reports/pytest_report.html
```

## GitHub Actions
The project is configured to run tests on multiple operating systems using GitHub Actions. The workflow file is located at `.github/workflows/multiple_conda_envs.yml`.

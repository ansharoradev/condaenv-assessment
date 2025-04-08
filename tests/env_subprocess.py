import logging as log
import subprocess
from conda_subprocess import run

from .commands import Commands
from .utils import current_millis


class Env:
    """
    A class to manage conda environments, including creation, activation, package installation, and removal.

    Attributes:
    env_name (str): The name of the conda environment.
    prefix_path (str): The file system path where the conda environment is located.
    """

    def __init__(self, env_name=None, prefix_path=None):
        """
        Initialize the Env class with an optional environment name and prefix path.

        Parameters:
        env_name (str): The name of the conda environment. Defaults to None.
        prefix_path (str): The file system path where the conda environment is located. Defaults to None.
        """
        self.env_name = env_name
        self.prefix_path = prefix_path

    def name(self):
        """
        Get the name of the conda environment. If the name is not set, generate a new one based on the current time.

        Returns:
        str: The name of the conda environment.
        """
        if self.env_name is None or self.env_name == "":
            self.env_name = f"env_{current_millis()}"
        return self.env_name

    def create(self, packages=None, install_default_packages=False):
        """
        Create a new conda environment with the specified packages.

        Parameters:
        packages (str): A comma-separated string of packages to install in the environment.
        install_default_packages (bool): Flag to determine whether to install default packages. Defaults to False.

        Returns:
        subprocess.CompletedProcess: The result of the package installation process.

        Raises:
        Exception: If the environment creation or package installation fails.
        """
        install_default_packages_flag = '' if install_default_packages else '--no-default-packages'

        create_args = ['conda', Commands.CREATE, install_default_packages_flag, '-y', '-n', self.name()]
        if self.prefix_path:
            create_args = ['conda', Commands.CREATE, '-y', install_default_packages_flag, '--prefix', self.prefix_path]

        package_list = []
        if packages:
            package_list = packages.split(",")
        for package in package_list:
            create_args.append(package)
        result = subprocess.run(create_args, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to create environment name={self.name()}, prefix_path={self.prefix_path}: {result.stdout} {result.stderr}")

        if package_list:
            self.list_packages()
            for package in package_list:
                pkg_result = self.is_package_installed(package)
                if pkg_result is None or pkg_result.returncode != 0:
                    log.error("Failed to list packages in environment: %s", pkg_result.stderr)
                return pkg_result

    def is_package_installed(self, package):
        """
        Check if a package is installed in the conda environment.

        Parameters:
        package (str): The name of the package to check.

        Returns:
        subprocess.CompletedProcess: The result of the package import check process.

        Raises:
        Exception: If the package import check fails.
        """
        package_name = package.split("=")[0]
        import_args = ["python", "-c", f"import {package_name}"]
        try:
            if self.prefix_path:
                is_import_success = run(import_args, prefix_path=self.prefix_path, capture_output=True, text=True)
            else:
                is_import_success = run(import_args, prefix_name=self.env_name, capture_output=True, text=True)
            if is_import_success.returncode != 0:
                log.error("Failed to list packages in environment: %s", is_import_success.stderr)
            return is_import_success
        except Exception as e:
            log.error("Failed to import package: %s", e)
        return None

    def list_packages(self):
        """
        List all packages installed in the conda environment.

        Returns:
        subprocess.CompletedProcess: The result of the package listing process.

        Raises:
        Exception: If the package listing fails.
        """
        try:
            if self.prefix_path:
                conda_list = run(f"conda {Commands.LIST}", prefix_path=self.prefix_path, capture_output=True, text=True)
            else:
                conda_list = run(f"conda {Commands.LIST}", prefix_name=self.env_name, capture_output=True, text=True)
            if conda_list.returncode != 0:
                log.error("Failed to list packages in environment: %s", conda_list.stderr)
            return conda_list
        except Exception as e:
            log.error("Failed to list packages in environment: %s", e)
        return None

    def activate(self):
        """
        Activate the conda environment.

        Returns:
        subprocess.CompletedProcess: The result of the environment activation process.

        Raises:
        Exception: If the environment activation fails.
        """
        result = subprocess.run(['conda', Commands.ACTIVATE, self.name()], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to activate environment {self.name()}: {result.stderr}")
        return result

    def remove(self):
        """
        Remove the conda environment.

        Returns:
        subprocess.CompletedProcess: The result of the environment removal process.

        Raises:
        Exception: If the environment removal fails.
        """
        if self.prefix_path:
            result = subprocess.run(['conda', Commands.REMOVE, '--prefix', self.prefix_path, '--all', '-y'], capture_output=True, text=True)
        else:
            result = subprocess.run(['conda', Commands.REMOVE, '--name', self.name(), '--all', '-y'], capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to remove environment {self.name()}: {result.stderr}")
        return result

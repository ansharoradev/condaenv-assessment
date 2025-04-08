from __future__ import annotations
from conda.testing.fixtures import CondaCLIFixture, TmpEnvFixture
import logging as log

from .commands import Commands


class Env:
    """
    A class to manage Conda environments and packages.
    """

    def __init__(self, conda_cli: CondaCLIFixture, env_name: str = None, prefix_path: str = None):
        log.debug("Initiating class::Env with env_name: %s, prefix_path: %s", env_name, prefix_path)
        self.conda_cli = conda_cli
        self.env_name = env_name
        self.prefix_path = prefix_path

    def is_env_exists(self) -> bool:
        """
        Check if a Conda environment exists.

        :return: True if the environment exists, False otherwise.
        """
        log.debug("Checking if environment %s exists", self.env_name)
        out, err, code = self.conda_cli("env", Commands.LIST)
        log.debug("Output: %s", out)
        if not code is None and code != 0:
            log.error("Failed to list environments: %s", err)
            return False
        return any(self.env_name + " " in line for line in out.splitlines())

    def remove_env(self):
        """
        Remove a Conda environment.
        """
        log.debug("Removing environment %s", self.env_name)
        out, err, code = self.conda_cli("remove", "--name", self.env_name, "--all", "-y")
        if not code is None and code != 0:
            log.error("Failed to remove environment %s: %s", self.env_name, err)
        log.debug("Output: %s", out)

    def create_env(self):
        """
        Create a new Conda environment.

        :return: The output of the environment creation command.
        """
        log.info("Creating environment %s", self.env_name)
        out, err, code = self.conda_cli(Commands.CREATE, "-y", "-n", self.env_name)
        if not code is None and code != 0:
            log.error("Failed to create environment %s: %s", self.env_name, err)
        log.info("Output: %s", out)
        return out, err, code

    def install_package(self, package: str):
        """
        Install a package in a Conda environment.

        :param package: Name of the package to install.
        """
        log.info("Installing package %s in environment %s", package, self.env_name)
        out, err, code = self.conda_cli(Commands.INSTALL, package, "-n", self.env_name, "-y")
        log.info("Output: %s", out)
        return out, err, code

    def is_package_installed(self, package: str) -> bool:
        """
        Check if a package is installed in a Conda environment.

        :param package: Name of the package to check.
        :return: True if the package is installed, False otherwise.
        """
        log.debug("Checking if package %s is installed in environment %s", package, self.env_name)
        package_name = package.split("=")[0]
        version = package.split("=")[1] if "=" in package else None
        out, err, code = self.conda_cli(Commands.LIST, "-n", self.env_name)
        log.debug("Output: %s", out)

        if code != 0:
            log.error("Failed to list packages in environment %s: %s", self.env_name, err)
            return False

        if version:
            return any(line.startswith(package_name) and version in line for line in out.splitlines())

        return any(line.startswith(package_name) for line in out.splitlines())

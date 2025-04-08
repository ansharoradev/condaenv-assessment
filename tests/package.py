from conda.testing.fixtures import CondaCLIFixture, TmpEnvFixture


class Package:

    def __init__(self, conda_cli: CondaCLIFixture):
        self.conda_cli = conda_cli

    def search(self, package: str):
        """
        Search for a package in Conda repositories.

        :param package: Name of the package to search for.
        """
        package = package.split("=")[0]
        out, err, code = self.conda_cli("search", package)
        return out, err, code

    def is_package_available(self, package: str) -> bool:
        """
        Check if a package is available in Conda repositories.

        :param package: Name of the package to check.
        :return: True if the package is available, False otherwise.
        """
        package_name = package.split("=")[0]
        version = package.split("=")[1] if "=" in package else None
        out, err, code = self.search(package)
        if code != 0:
            return False
        if version:
            return any(line.startswith(package_name) and version in line for line in out.splitlines())
        return any(line.startswith(package_name) for line in out.splitlines())

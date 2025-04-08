from __future__ import annotations
from conda.testing.fixtures import CondaCLIFixture
import logging as log
import pytest

from .env import Env
from .package import Package


pytest_plugins = "conda.testing.fixtures"


test_cases = [
    {
        "name": "api",
        "packages": [ "requests" ]
    }, {
       "name": "datascience",
        "packages": ["numpy", "pandas", "matplotlib"]
    }, {
        "name": "api",
        "packages": [ "requests=2.32.3" ]
    }, {
       "name": "datascience",
        "packages": ["numpy=2.2.4", "pandas=2.2.3", "matplotlib=3.10.1"]
    }
]


@pytest.mark.parametrize("test_case", test_cases)
def test_conda_create(conda_cli: CondaCLIFixture, test_case):
    log.info("Running test_conda_create with test_case: %s", test_case)

    env_name = test_case["name"]
    env = Env(conda_cli, env_name)
    package = Package(conda_cli)

    if env.is_env_exists():
        env.remove_env()

    out, err, code = env.create_env()
    assert code is None or code == 0, f"Failed to create environment {env_name} with code {code}"
    assert f"conda activate {env_name}" in out, f"Activation message not found in output for {env_name}"

    for pkg in test_case["packages"]:
        is_package_available = package.is_package_available(pkg)
        assert is_package_available, f"Package {pkg} not found in repositories"

        env.install_package(pkg)
        assert code is None or code == 0, f"Failed to install {pkg} with code {code}"

        assert env.is_package_installed(pkg), f"Package {pkg} not found in {test_case['name']} environment"

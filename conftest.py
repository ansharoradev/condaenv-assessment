def pytest_addoption(parser):
    """
    Adds a command line option to pytest.

    This function adds the `--remove-env` option to pytest, which allows the user to specify
    whether to remove (cleanup) conda environments after tests are run.

    Args:
        parser (Parser): The parser for command line arguments.
    """
    parser.addoption(
        '--remove-env', action='store', default='True', help='Remove (cleanup) conda environments after tests'
    )

"""Noxfile for project."""

import nox


@nox.session(name="unit-tests", python=["3.10", "3.11", "3.12"])
def unit_tests(session: nox.Session) -> None:
    """Run unit tests for various versions of python."""
    # install packages
    session.install("pytest", "pytest-cov", ".")

    # run tests
    session.run("pytest", "tests/unit")

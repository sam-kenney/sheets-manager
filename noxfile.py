"""Nox configuration Lint and Test code."""
import nox


@nox.session
def lint(session):
    """Lint using flake8."""
    session.install(
        "flake8",
        "flake8-docstrings",
        "flake8-import-order",
    )
    session.run("flake8", "--max-complexity=8")


@nox.session
def format(session):
    """Format using black."""
    session.install("black")
    session.run("black", ".")


@nox.session
def test(session):
    """Run tests."""
    session.install("pytest")
    session.install("-r", "requirements.txt")
    session.run("pytest")

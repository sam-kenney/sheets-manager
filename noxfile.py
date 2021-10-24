"""Nox configuration Lint and Test code."""
import nox


@nox.session
def lint(session):
    """Lint using flake8."""
    session.install("flake8", "flake8-docstrings")
    session.run("flake8", "--max-complexity=8")

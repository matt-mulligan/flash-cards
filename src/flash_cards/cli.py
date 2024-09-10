"""Module holding PyApp CLI entrypoint.

Logic to be kept to a minimum in this module and call out to other modules.
"""

from pyapp.app import CliApplication

app = CliApplication(
    description="Flash Cards",
)
cli_main = app.dispatch


@app.command
def play(name: str, *, greeting: str = "Hello"):
    """Provide a greeting."""
    print(f"{greeting} {name}")

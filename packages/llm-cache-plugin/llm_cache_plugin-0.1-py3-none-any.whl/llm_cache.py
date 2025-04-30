import click
import llm
from llm.cli import get_default_model, migrate
from llm.cli import logs_db_path
import pathlib
import sqlite_utils


@llm.hookimpl
def register_commands(cli):
    # Remove the original prompt command, storing it for use later
    for command in cli.commands.copy().values():
        if command.name == "prompt":
            original_command = command
            cli.commands.pop(command.name)
            break

    # Create a new prompt command, adding cache arguments
    @cli.command(name="prompt")
    @click.option(
        "--cache/--no-cache",
        default=False,
        help="Return the response from the database if it exists, otherwise call the llm",
    )
    @click.pass_context
    def custom_prompt(ctx, cache, **kwargs):
        if cache:
            database = kwargs.get("database")
            log_path = pathlib.Path(database) if database else logs_db_path()
            (log_path.parent).mkdir(parents=True, exist_ok=True)
            db = sqlite_utils.Database(log_path)
            migrate(db)

            prompt = kwargs.get("prompt")
            system = kwargs.get("system")
            model = kwargs.get("model", get_default_model())

            result = find_cached_response(db, prompt, system, model)

            if result:
                click.echo(result)
            else:
                ctx.invoke(original_command, **kwargs)
        else:
            ctx.invoke(original_command, **kwargs)

    # Copy all parameters from the original prompt command
    custom_prompt.params = original_command.params.copy() + custom_prompt.params


def find_cached_response(db, prompt, system, model):
    """Search the llm db for this exact query, and return it if it already exists"""

    RESPONSE_SQL = """
    select * from responses
    where responses.model = :model
    and responses.prompt = :prompt
    and responses.system is :system
    order by datetime_utc desc
    limit 1;
    """
    rows = list(
        db.query(RESPONSE_SQL, {"prompt": prompt, "system": system, "model": model})
    )
    if len(rows):
        return llm.Response.from_row(db, rows[0])

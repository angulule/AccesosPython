import typer

from app.seeds.service import run_all, run_users

app = typer.Typer(help="Seeds: users")

@app.command("all")
def all_():
    run_all()
    typer.echo("Todos los seeds creados")


@app.command("all")
def all_():
    run_all()
    typer.echo("Todos los seeds creados")

@app.command("users")
def users():
    run_users()
    typer.echo("Usuarios cargados")
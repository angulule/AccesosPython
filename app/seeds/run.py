import typer

from app.seeds.service import run_all

app = typer.Typer(help="Seeds")

@app.command("all")
def all_():
    run_all()
    typer.echo("Todos los seeds creados")

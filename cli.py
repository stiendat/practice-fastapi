"""
CLI tool for Library Management System
"""
import asyncio
import typer
from commands.init_database.main import init_database

app = typer.Typer()


@app.command()
def init_database():
    """
    Initialize database: create tables and import initial data from CSV.
    """
    asyncio.run(init_database())


if __name__ == "__main__":
    app() 
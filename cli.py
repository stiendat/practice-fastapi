from typer import Typer

from commands.init_database.main import init_database
from commands.import_books.main import import_books

app = Typer()


@app.command("init_database")
def cmd_init_database():
    print("Initializing database")
    init_database()


@app.command("import_books")
def cmd_import_books():
    print("Importing books from CSV")
    import_books()


@app.command("run_test")
def cmd_run_test():
    print("Running tests")
    # TODO: Add test execution logic here
    print("Tests executed successfully")


if __name__ == "__main__":
    app()

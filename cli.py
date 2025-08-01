from typer import Typer

from commands.init_database.main import init_database
from commands.init_database.sqlite_main import init_sqlite_database
from commands.run_tests.main import run_tests
from commands.import_data.main import import_data
from commands.import_data.sqlite_main import import_books_from_csv_sqlite

app = Typer()


@app.command("init_database")
def cmd_init_database():
    print("Initializing PostgreSQL database")
    init_database()


@app.command("init_sqlite")
def cmd_init_sqlite():
    print("Initializing SQLite database")
    init_sqlite_database()


@app.command("run_test")
def cmd_run_test():
    print("Running tests")
    run_tests()


@app.command("import_data")
def cmd_import_data():
    print("Importing data from CSV to PostgreSQL")
    import_data()


@app.command("import_sqlite")
def cmd_import_sqlite():
    print("Importing data from CSV to SQLite")
    import_books_from_csv_sqlite()


if __name__ == "__main__":
    app()

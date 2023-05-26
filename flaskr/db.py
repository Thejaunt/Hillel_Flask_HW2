import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def fixtures_db():
    db = get_db()

    with current_app.open_resource('fixtures.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('fixtures-db')
def fixtures_db_command():
    #  fill dummy data in
    try:
        fixtures_db()
        click.echo('Database has been filled with dummy data')
    except sqlite3.IntegrityError as er:
        click.echo(f'[Error] Database has already been filled with dummy data. {er}')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(fixtures_db_command)

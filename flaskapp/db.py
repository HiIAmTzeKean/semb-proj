import sqlite3

import click

from flask import current_app, g

from flask.cli import with_appcontext

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

# def populate_db():
#     db = get_db()
#     # TODO: link to test folder
#     with current_app.open_resource('test_data.sql') as f:
#         db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    '''
    The close_db and init_db_command functions need to be registered with the application instance; 
    otherwise, they won’t be used by the application. However, since you’re using a factory function,
    that instance isn’t available when writing the functions. Instead, write a function that takes 
    an application and does the registration.
    
    app.teardown_appcontext() tells Flask to call that function when cleaning up after returning the response.
    app.cli.add_command() adds a new command that can be called with the flask command.
    '''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
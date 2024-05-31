import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from yoyo import read_migrations
from yoyo import get_backend
from dotenv import dotenv_values

secrets = dotenv_values(".env")


def make_migration():
    backend = get_backend(
        f"""mysql://{secrets["MYSQL_USER"]}:{secrets["MYSQL_PASSWORD"]}@{secrets["MYSQL_HOST"]}:{int(secrets["MYSQL_PORT"])}/{secrets["MYSQL_DATABASE"]}"""
    )
    migrations = read_migrations("modules/migrations")
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))


def make_rollback():
    backend = get_backend(
        f"""mysql://{secrets["MYSQL_USER"]}:{secrets["MYSQL_PASSWORD"]}@{secrets["MYSQL_HOST"]}:{int(secrets["MYSQL_PORT"])}/{secrets["MYSQL_DATABASE"]}"""
    )
    migrations = read_migrations("modules/migrations")

    with backend.lock():
        backend.rollback_migrations(backend.to_rollback(migrations))


if __name__ == "__main__":
    pass

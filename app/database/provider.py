from peewee import PostgresqlDatabase
from testcontainers.postgres import PostgresContainer

from app.config.settings import get_settings

_settings = get_settings()

if _settings.environment == "test":
    postgres_test = PostgresContainer("postgres:16")
    postgres_test.start()

class DatabaseProvider:

    @staticmethod
    def get_database():
        if _settings.environment == "test":
            db = PostgresqlDatabase(
                postgres_test.dbname,
                user=postgres_test.username,
                password=postgres_test.password,
                host=postgres_test.get_container_host_ip(),
                port=postgres_test.get_exposed_port(5432)
            )
        else:
            db = PostgresqlDatabase(
                _settings.database_name,
                user=_settings.database_user,
                password=_settings.database_password,
                host=_settings.database_host
            )
        return db

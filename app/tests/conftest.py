import os

import pytest

from app.database.models.dock_account import DockAccount
from app.database.models.holder import Holder
from app.database.models.transaction_history import TransactionHistory
from app.database.provider import DatabaseProvider


def pytest_configure(config):
    if os.getenv("ENVIRONMENT") != "test":
        pytest.exit("Tests running in the wrong environment, please look at your configurations")
    db = DatabaseProvider.get_database()
    db.create_tables([Holder, DockAccount, TransactionHistory])
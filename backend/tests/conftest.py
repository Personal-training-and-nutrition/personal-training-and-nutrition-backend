import json
import pytest
from django.conf import settings
from django.db import connection



@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    """
    Создание тестовой DB и наполнение её тестовыми данными.
    """
    assert settings.MODE == "TEST"
    
    # with django_db_blocker.unblock():
    #     with connection.cursor() as c:
    #         c.executescript('''
    #         DROP TABLE IF EXISTS test_db;
    #         CREATE TABLE test_db (...);
    #         INSERT INTO test_db (..) VALUES ('created from a sql script');
    #         ''')

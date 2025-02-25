import sqlite3
from threading import local

thread_local = local()

def get_db():
    if not hasattr(thread_local, "db"):
        thread_local.db = sqlite3.connect('core/devices.db')
    return thread_local.db

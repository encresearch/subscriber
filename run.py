"""Script to be run on boot/startup"""
import time
from subscriber.app import app, db


def wait_for_postgres():
    try:
        db.engine.execute("SELECT 1")
        print("connected to db")
        return None
    except Exception:
        time.sleep(1)
        print("Attempting to connect to the Database...")
        wait_for_postgres()


if __name__ == '__main__':
    # wait_for_postgres()
    db.create_all()
    app.run(host='0.0.0.0')

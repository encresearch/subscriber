"""Script to be run on boot/startup"""
import time
from subscriber.app import app, db


def wait_for_postgres():
    try:
        db.engine.execute("SELECT 1")
        print("connected to db")
        return None
    except:
        time.sleep(1)
        print("Attempting to connect to the Database...")
        wait_for_postgres()


wait_for_postgres()
db.create_all()

if __name__ == '__main__':
    app.run()

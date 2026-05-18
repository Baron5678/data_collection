from celery_app.app import app
from db.repositories import create_async_user_data

# Celery task responsible for asynchronous user data insertion
@app.task
def insert_user_data(username, phone_number):
    return create_async_user_data(username, phone_number)



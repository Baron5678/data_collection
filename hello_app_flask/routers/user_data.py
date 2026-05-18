import celery_app.tasks
from flask import Blueprint, request, render_template, abort, redirect, url_for
from jinja2 import TemplateNotFound
from celery.result import AsyncResult

from shared.validators import validate_name_surname, validate_username_phone
from db.repositories import create_and_get_sync_user_data, get_async_user_data_by_id
from celery_app.app import app

# Blueprint for rendering user data form pages and processing form submissions
user_data_page = Blueprint('user_data_page', __name__, template_folder='/templates')


# Rules for processing sync and async data collection, if GET method then page is rendered,
# if POST method then form data is validated and processed accordingly.
@user_data_page.route('/users_sync', methods=['POST', 'GET'])
def users_sync():
    try:
        if request.method == 'POST':
            form_name = request.form.get('name')
            form_surname = request.form.get('surname')
            error_msg = validate_name_surname(form_name, form_surname)
            if error_msg:
                return render_template("users_sync.html", error=error_msg)
            user_data_display = create_and_get_sync_user_data(form_name, form_surname)
            return render_template("users_sync.html",
                                    name=user_data_display["name"],
                                    surname=user_data_display["surname"])
        return render_template("users_sync.html")
    except TemplateNotFound:
        abort(404)


@user_data_page.route('/users_async', methods=['POST', 'GET'])
def users_async():
    try:
        if request.method == 'POST':
            form_username = request.form.get('username')
            form_phone_number = request.form.get('phone')
            error_msg = validate_username_phone(form_username, form_phone_number)
            if error_msg:
                return render_template("users_async.html", error=error_msg)
            result_task: AsyncResult = celery_app.tasks.insert_user_data.delay(form_username, form_phone_number)
            return redirect(url_for('user_data_page.display_user_data_async', task_id=result_task.id))
        return render_template("users_async.html")
    except TemplateNotFound:
        abort(404)

# Display current status of asynchronous Celery task and render user data if task is successful
@user_data_page.route('/users_async/status/<task_id>', methods=['GET'])
def display_user_data_async(task_id):
    try:
        result_task: AsyncResult = AsyncResult(task_id, app=app)
        if result_task.successful():
            user_id = result_task.result
            user_data_display = get_async_user_data_by_id(user_id)
            return render_template("users_async.html",
                                   username=user_data_display["username"],
                                   phone=user_data_display["phone_number"],
                                   status="SUCCESS")
        else:
            return render_template("users_async.html", status=result_task.status)
    except TemplateNotFound:
        abort(404)
import celery_app.tasks
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import HTMLResponse
from celery.result import AsyncResult
from starlette.responses import RedirectResponse

from db.repositories import create_and_get_sync_user_data, get_async_user_data_by_id
from shared.validators import validate_name_surname, validate_username_phone
from hello_app_fastapi.main import templates

router = APIRouter()

# Render sync and async form pages
@router.get("/sync", response_class=HTMLResponse)
async def create_sync_form(request: Request):
    return templates.TemplateResponse(request=request, name="sync.html", context={})

@router.get("/async", response_class=HTMLResponse)
async def create_async_form(request: Request):
    return templates.TemplateResponse(request=request, name="async.html", context={})

# Process synchronous form submission and store data directly in database
@router.post("/sync", response_class=HTMLResponse)
async def collect_sync_user_data(request: Request,
                                 name: str = Form(...),
                                 surname: str = Form(...)):
    error_msg = validate_name_surname(name, surname)
    if error_msg:
        return templates.TemplateResponse(request=request, name="sync.html", context={'error': error_msg})
    user_data_display = create_and_get_sync_user_data(name, surname)
    return templates.TemplateResponse(request=request,
                                      name="sync.html",
                                        context={'name': user_data_display["name"],
                                                 'surname': user_data_display["surname"]})


# Process asynchronous form submission using Celery task queue
@router.post("/async", response_class=HTMLResponse)
async def collect_async_user_data(request: Request,
                                  username: str = Form(...),
                                  phone: str = Form(...)):
    error_msg = validate_username_phone(username, phone)
    if error_msg:
        return templates.TemplateResponse(request=request, name="async.html", context={'error': error_msg})
    task: AsyncResult = celery_app.tasks.insert_user_data.delay(username, phone)
    return RedirectResponse(url=f"/async/status/{task.id}", status_code=status.HTTP_303_SEE_OTHER)

# Display current status of asynchronous Celery task
@router.get("/async/status/{task_id}", response_class=HTMLResponse)
async def display_user_data_async(request: Request,task_id: str):
    task: AsyncResult = AsyncResult(task_id)
    if task.successful():
        user_id = task.result
        user_data_display = get_async_user_data_by_id(user_id)
        return templates.TemplateResponse(request=request,
                                          name="async.html",
                                          context={'username': user_data_display["username"],
                                                   'phone': user_data_display["phone_number"],
                                                   'status': "SUCCESS"})
    else:
        return templates.TemplateResponse(request=request,
                                          name="async.html",
                                          context={'status': task.status})

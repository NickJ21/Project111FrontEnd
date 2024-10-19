from flask import (
    Flask,
    render_template,
    request as req          #this is making an alias for it;this is the Request context object
)
import requests             #This is the standalone request python package

BACKEND_URL = "http://127.0.0.1:5000/tasks"

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/tasks")
def view_tasks():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get("tasks")
        return render_template("list.html", tasks=task_list)       #tasks is a key and task_list is a value, the key ("tasks") is from list.html (the for loop, where "for task in tasks")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.get("/tasks/<int:pk>/")
def single_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("detail.html", task=task_data)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.get("/tasks/new/")
def new_form():
    return render_template("new.html")          #should be a form html template

@app.post("/tasks/new/")
def create_task():
    task_data = req.form
    response = requests.post(BACKEND_URL, json=task_data)
    if response.status_code == 204:
        return render_template("success.html", message="Task Created")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )


                   # the idea behind this is to pre-populate the form
@app.get("/tasks/<int:pk>/edit/")
def edit_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("edit.html", task=task_data)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.post("/tasks/<int:pk>/edit/")
def edit_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.put(url, json=req.json)
    if response.status_code == 204:
        return render_template("success.html", message="Task Edited")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )


                #This should allow the user to confirm their intention to delete a task
@app.get("/tasks/<int:pk>?delete/")
def delete_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("delete.html", task=task_data)
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )

@app.post("/tasks/<int:pk>/delete/")
def delete_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.delete(url)
    if response.status_code == 204:
        return render_template("success.html", message="Task Deleted")
    return (
        render_template("error.html", error=response.status_code),
        response.status_code
    )


#for the practice I need to make and extend success.html, edit.html, new.html and delete.html
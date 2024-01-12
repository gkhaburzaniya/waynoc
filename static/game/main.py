from datetime import datetime as dt

from pyscript import document
from pyweb import pydom

tasks = []

def q(selector, root=document):
    return root.querySelector(selector)


# define the task template that will be use to render new templates to the page
# Note: We use JS element here because pydom doesn't fully support template
#       elements now
task_template = pydom.Element(q("#task-template").content.querySelector(".task"))
Int = pydom["#Int"][0]._js
Int.textContent = "foo"


task_list = pydom["#list-tasks-container"][0]

def add_task(e):
    # create task
    task_id = f"task-{len(tasks)}"

    # add the task element to the page as new node in the list by cloning from a
    # template
    task_html = task_template.clone()
    task_html.id = task_id

    task_html_content = task_html.find("p")[0]
    task_html_content._js.textContent = "Test6"
    task_list.append("foo")
    task_list.append(task_html)


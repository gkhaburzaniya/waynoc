from datetime import datetime as dt

from pyscript import document
from pyweb import pydom

tasks = []

def q(selector, root=document):
    return root.querySelector(selector)


Int = pydom["#Int"][0]._js
Int.textContent = "foo"


def advance(e):
    # create task
    Int.textContent = "Test2"

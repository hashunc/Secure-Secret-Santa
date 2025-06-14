from fastapi import FastAPI, Request, Form, Path, Body
from fastapi.templating import Jinja2Templates
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI(
    title="Secure Secret Santa API",
    contact={
        "name": "hashabadi",
        "url": "https://github.com/hashunc/Secure-Secret-Santa.git",
    },
    description="""
## Introduction

This full-stack application allows users to participate in a secure Secret Santa gift exchange. On the first screen, users can either create a group or sign-in to one. Once on the next screen, users can enter in their names and other data needed for the exchange. When ready, users can click assign to assign the gift recipients.

""",
    openapi_tags=[
        {"name": "Server", "description": "Server's API Endpoints"},
        {"name": "Client", "description": "Client's API Endpoints"},
        {"name": "Home", "description": "Starting API Endpoints"},
    ],
)
# function to get a Jinja template
templates = Jinja2Templates(directory="app/templates")


# Open home page where user can join or create a group
@app.get(
    "/",
    summary="Home page",
    description="Join or create a group",
    responses={
        200: {"description": "Joined group successfully"},
        201: {"description": "Created group successfully"},
        404: {"description": "Invalid group or password"},
        400: {"description": "Invalid group creation syntax"},
    },
    tags=["Home"],
)
def get_index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


# Post a sign in attempt
@app.post(
    "/sign_in",
    summary="Sign in",
    description="Enter group name and password to join",
    responses={
        200: {"description": "Joined group successfully"},
        404: {"description": "Invalid group or password"},
    },
    tags=["Client"],
)
def sign_in(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    groupName, groupPassword = (username, password)

    # TODO: check if group exists in database

    return templates.TemplateResponse(request=request, name="santa.html", context={})


# Flask routes to import to FastAPI
"""

@app.route("/santa.html")
def santa():
    return render_template("santa.html")




@app.route('/create_group', methods=['POST'])
def create_group():
    new_group_name = request.form["newGroupName"]
    new_password = request.form["newPassword"]

    #TODO: create new group in database

    return render_template("santa.html")

@app.route('/input_data', methods=['POST'])
def input_data():
    first_name = request.form["firstName"]
    last_name = request.form["lastName"]
    price_limit = request.form["priceLimit"]

    prefered_person_first_name = request.form["preferedPersonFirstName"]
    prefered_person_last_name = request.form["preferedPersonLastName"]

    least_prefered_person_first_name = request.form["leastPreferedPersonFirstName"]
    least_prefered_person_last_name = request.form["leastPreferedPersonLastName"]

    #TODO: crypto stuff

    return render_template("santa.html")


@app.route('/back', methods=['GET'])
def back():
    return render_template("index.html")




"""

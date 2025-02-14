from fastapi import FastAPI
from typing import Annotated, Path, Body
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
    ],
)
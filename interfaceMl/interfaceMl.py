
# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# create the application instance :)
app = Flask(__name__)
# load config from this file
app.config.from_object(__name__)

app.config.update(dict(
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='test'
))
# Load default config and override config from an environment variable
app.config.from_envvar('INTERFACEML_SETTINGS', silent=True)
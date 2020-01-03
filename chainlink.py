#!/usr/bin/env python
"""Utilize crypto domains DNS and either redirect, or display information."""
from flask import Flask, redirect, url_for
import json
import requests

VERSION = '0.0.1'

app = Flask(__name__)


@app.route("/")
def root():
    return 'There is nothing here'


@app.route("/<string:domain>")
def showdomain(domain):
    redirect = requests.get(f'https://unstoppabledomains.com/api/v1/{domain}')
    if redirect.status_code == 200:
        body = json.loads(redirect.content)
        redirect_url = body['ipfs']['redirect_domain']
        return f'<body onload="window.location = \'{redirect_url}\'"><p></body>'

if __name__ == "__main__":
    app.run()

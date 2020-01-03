#!/usr/bin/env python
"""Utilize crypto domains DNS and either redirect, or display information."""
from bottle import Bottle, run, response, request
import json
import requests

VERSION = '0.0.1'

app = Bottle()


@app.route("/")
def root():
    host = request.get_header('host')
    return f'specify domain in URL like {host}/domain.crypto'


@app.route("/<domain>")
def showdomain(domain):
    apiurl =f'https://unstoppabledomains.com/api/v1/{domain}'
    redirect = requests.get(apiurl)
    try:
        if redirect.status_code == 200:
            body = json.loads(redirect.content)
            print(body)
            redirect_url = body['ipfs']['redirect_domain']
            # TODO: Add handler for the ipfs vs redirect
#            if body['ipfs']['html']:
#                print('We have html')
            response.status = 302
            response.set_header('Location',redirect_url)
        else:
            return f'Error making call to {apiurl} for {domain}'
    except KeyError:
        return f'Did not find a redirect for {domain}'


if __name__ == "__main__":
    run(app, host='localhost', port='5000', reloader=True)

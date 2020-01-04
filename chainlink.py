#!/usr/bin/env python
"""Utilize crypto domains DNS and either redirect, or display information."""
from bottle import Bottle, run, response, request
import json
import requests
import json2html

VERSION = '0.0.1'

app = Bottle()


@app.route("/")
def root():
    host = request.get_header('host')
    helptext = f"""
    <p>General format is {host}/&lt;domain&gt;/&lt;action&gt;
    <p>If <action> is blank, it will attempt to use the redirect
    <p>You may also/optionally specify an action which can be any of the following
    <table margin-left="100px">
    <tr>
    <td>raw</td>
    <td>Show the raw json (formatted as an html table)</td>
    </tr>
    <td>html</td>
    <td>Hit the IPFS hash via cloudflare-ipfs.com</td>
    </tr>
    <td>redir</td>
    <td>Use the redirect parameter and just return a 302 redirect to whatever is set</td>
    </tr>
    </table>
    """
    return helptext


@app.route("/<domain>")
@app.route("/<domain>/<action>")
def redirectDomain(domain, action=None):
    apiurl =f'https://unstoppabledomains.com/api/v1/{domain}'
    dnslookup = requests.get(apiurl)
    if action == None or action == 'redir':
        try:
            if dnslookup.status_code == 200:
                body = json.loads(dnslookup.content)
                print(body)
                redirect_url = body['ipfs']['redirect_domain']
                response.status = 302
                response.set_header('Location',redirect_url)
            else:
                return f'Error making call to {apiurl} for {domain}'
        except KeyError:
            return f'Did not find a redirect for {domain}'
    elif action == 'html':
        # TODO: clean this up by functionalizing this call.  It's basically the same as above
        if dnslookup.status_code == 200:
            body = json.loads(dnslookup.content)
            print(body)
            response.status = 302
            response.set_header('Location', f"https://cloudflare-ipfs.com/ipfs/{body['ipfs']['html']}")
    elif action == 'raw':
        if dnslookup.status_code == 200:
            body = json.loads(dnslookup.content)
            return json2html.json2html.convert(json = body)

if __name__ == "__main__":
    run(app, host='0.0.0.0', port='5000', reloader=True)

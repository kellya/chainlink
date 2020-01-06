#!/usr/bin/env python
"""Utilize crypto domains DNS and either redirect, or display information."""
from bottle import Bottle, run, response, request
import json
import requests
import json2html

VERSION = '0.0.1'

app = Bottle()


def domainLookup(domain):
    apibase = 'https://unstoppabledomains.com/api/v1/'
    dnslookup = requests.get(apibase + domain)
    domainJSON = json.loads(dnslookup.content)
    print(domainJSON)
    return domainJSON


@app.route("/")
def root():
    host = request.get_header('host')
    helptext = f"""
    <p>General format is {host}/&lt;domain&gt;/&lt;action&gt;
    <p>If &lt;action&gt; is blank, it will attempt to use the IPFS hash
    <p>You may also/optionally specify an action which can be any of the
    following
    <table style="margin-left: 50px;border=1px;">
    <tr>
    <td>raw</td>
    <td>Show the raw json (formatted as an html table)</td>
    </tr>
    <tr>
    <td>html</td>
    <td>Hit the IPFS hash via cloudflare-ipfs.com</td>
    </tr>
    <tr>
    <td>redir</td>
    <td>Use the redirect parameter and just return a 302 redirect to whatever
    is set</td>
    </tr>
    </table>
    """
    return helptext


@app.route("/<domain>")
@app.route("/<domain>/")
@app.route("/<domain>/<action>")
def redirectDomain(domain, action=None):
    lookupResult = domainLookup(domain)
    redirect_url = lookupResult['ipfs']['redirect_domain']
    html = lookupResult['ipfs']['html']
    if action == 'redir':
        try:
            if not redirect_url.startswith('http'):
                redirect_url = "http://" + redirect_url
            response.status = 302
            response.set_header('Location', redirect_url)
        except KeyError:
            return f'Did not find a redirect for {domain}'
    elif action is None or action == 'html':
        response.status = 302
        if not html.startswith('/ip'):
            ipfshash = "ipfs/" + html
        else:
            ipfshash = html
        response.set_header('Location',
                            f"https://cloudflare-ipfs.com/{ipfshash}")
    elif action == 'raw':
        return json2html.json2html.convert(json=lookupResult)


if __name__ == "__main__":
    run(app, host='0.0.0.0', port='5000', reloader=True)

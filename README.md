Chainlink
=========

Chainlink is a utility that will run on a webserver to handle crypto-backed
domain names Specifically this works with
[Unstoppable Domains](https://unstoppabledomains.com)
This utilizes public IPFS gateways to display IPFS content, or will redirect to
whatever the URL is set to in the Unstoppable Domain management.

Installation
============

To install this on your own server:

1.  Clone this repository
2.  Install the python dependancies via `pip install -r requirements.txt`
3.  Run the server with `./chainlink.py`
4.  You can now hit the app at http://localhost:5000

Testing on a running instance
=============================

Assuming that it is running (I could be messing with it, or it might just be
broken), you may try this without installing by going to
https://chainlink.arachnitech.com/

URL Patterns
============

The general format is http://localhost:5000/&lt;domain&gt;lt;/action&gt;
where &lt;domain&gt; is a .crypto or .zil name registered with Unstoppable
Domains and &lt;action&gt; can be
* html - uses the IPFS hash set in Unstoppable Domains management
* redir - uses the redirect_url set in Unstoppable Domains management
* raw - displays an HTML table view of the full JSON returned from Unstoppable
    Domains API

The default action is "html", so if you don't specify anything it will attempt
to use that field.

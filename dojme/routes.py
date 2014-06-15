from dojme import app
from flask import render_template, request, redirect
from urlparse import urlparse
import httplib2
import re


def status_check(url):
    """
    Get the headers of a web resource to check if it exists
    """
    h = httplib2.Http()
    try:
        resp = h.request(url, 'HEAD')
        if resp[0].status == 200:
            return True
    except (httplib2.RelativeURIError, httplib2.ServerNotFoundError):
        return False


def check_protocol(url):
    """
    Checks if http:// is present before Url
    """
    parsed = urlparse(url)
    if parsed.scheme == "":
        return "http://" + url
    else:
        return url


def is_valid_url(url):
    """
    Validates the URL input
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?'
        r'|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if regex.search(url):
        return True
    return False


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/form", methods=["GET", "POST"])
def route_form():
    if request.method == "GET":
        return redirect('/')
    else:
        web_address = request.form['webaddress']
        web_address = check_protocol(web_address)
        valid_url = is_valid_url(web_address)
        if not valid_url:
            return render_template("index.html")
        else:
            check_website = status_check(web_address)
            if check_website:
                return render_template("submit.html",
                                       up="It's Up",
                                       url=web_address)
            else:
                return render_template("submit.html",
                                       down="It's Down",
                                       url=web_address)

# register.py

import sys
sys.path.insert(1, '../lib')

import cgi, cgitb
cgitb.enable()
from common import http_answer
from bayes  import mark_as_spam


form = cgi.FieldStorage()

if "body" not in form:
    http_answer("ERROR: body must be provided in cgi parameter 'body'")
    sys.exit(0)


body = form.getfirst("body")
mark_as_spam(body)

http_answer("OK")

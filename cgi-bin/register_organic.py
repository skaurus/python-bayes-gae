# register.py
# coding: utf-8

import sys
sys.path.insert(1, '../lib')

import cgi, cgitb
cgitb.enable()
from common import http_answer
from bayes  import mark_not_spam


form = cgi.FieldStorage()

if "body" not in form:
    http_answer("ERROR: body must be provided in cgi parameter 'body'")
    sys.exit(0)


body = unicode( form.getfirst("body"), "utf-8" )
c = mark_not_spam(body)

#http_answer("OK: " + c.encode("utf-8"))
http_answer("OK: " + str(c))

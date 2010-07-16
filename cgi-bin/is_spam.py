# is_spam.py

import sys
sys.path.insert(1, '../lib')

import cgi, cgitb
cgitb.enable()
from common import http_answer
from bayes  import is_spam


form = cgi.FieldStorage()

if "body" not in form:
    http_answer("ERROR: body must be provided in cgi parameter 'body'")
    return


body = form.getfirst("body")
result = "SPAM" if is_spam(body) else "NOT SPAM"

http_answer(result)

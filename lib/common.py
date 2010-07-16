# common functions
# coding: utf-8

def http_answer(html = ''):
    print """Content-Type: text/html; charset=utf-8

"""
    print """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">

<html lang="ru">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /> 
<title>Bayesian Spam Filter Example</title>
<body>
"""
    print html
    print "</body></html>"


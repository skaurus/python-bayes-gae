# home.py
# coding: utf-8

import sys
sys.path.insert(1, '../lib')

import cgitb
cgitb.enable()
from common import http_answer

http_answer("""Hello world!<br>
<br>
Это скрипт для демонстрации работы наивного Байесовского алгоритма на основе
Google App Engine для решения задачи определения спама. Ниже есть форма для
загрузки текстов как для обучения системы, так и проверки на спам.<br>
<br>
Внимание! Система рассчитана на работу с utf-8, что автоматически
обеспечивается при работе через нижепредставленную форму; но при дергании
скриптов вручную надо это учитывать.<br>
Поддерживаются английские и русские тексты.<br>
Если после сабмита формы кидает сюда же, видимо, у Вас отключен Javascript.<br>
И да, сейчас систему легко скомпрометировать, неверно её обучив. Не делайте так,
пожалуйста.<br>
<br>
<form name="spam" method="post" action="/">
    Текст письма:<br>
    <textarea name="body" rows="40" cols="120"></textarea>
    <br>
    <input type="submit" value="спам" onclick="this.form.action = '/register_spam'"><br>
    <input type="submit" value="не спам" onclick="this.form.action = '/register_organic'"><br>
    <input type="submit" value="проверить" onclick="this.form.action = '/is_spam'">
</form>""")

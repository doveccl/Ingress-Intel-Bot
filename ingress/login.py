#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, sqlite3, re
from bs4 import BeautifulSoup as bs
from requests.utils import dict_from_cookiejar

login_re = r'"(https://www\.google\.com/accounts/ServiceLogin.+?)"'
intel_url = 'https://www.ingress.com/intel'
user_xhr_url = 'https://accounts.google.com/accountLoginInfoXhr'
password_url = 'https://accounts.google.com/signin/challenge/sl/password'

ingress_headers = {
    'accept-encoding' :'gzip, deflate',
    'content-type': 'application/json; charset=UTF-8',
    'origin': 'https://www.ingress.com',
    'referer': 'https://www.ingress.com/intel',
    'user-agent': 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)'
}
google_headers = {
    'accept-encoding': 'gzip, deflate',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://accounts.google.com',
    'referer': 'https://accounts.google.com/ServiceLogin',
    'user-agent': 'Mozilla/5.0 (MSIE 9.0; Windows NT 6.1; Trident/5.0)'
}

def login(usr, pwd):
    '''
    login to intel map with usr, pwd
    '''
    request = requests.Session()
    _ = request.get(intel_url)
    login_url = re.findall(login_re, _.text)[0]
    _ = request.get(login_url)
    html = bs(_.text, 'lxml')
    data = { 'Email' : usr }
    for i in html.form.select('input'):
        try:
            if i['name'] == 'Page':
                data.update({'Page': i['value']})
            elif i['name'] == 'service':
                data.update({'service': i['value']})
            elif i['name'] == 'ltmpl':
                data.update({'ltmpl': i['value']})
            elif i['name'] == 'continue':
                data.update({'continue': i['value']})
            elif i['name'] == 'gxf':
                data.update({'gxf': i['value']})
            elif i['name'] == 'GALX':
                data.update({'GALX': i['value']})
            elif i['name'] == 'shdf':
                data.update({'shdf': i['value']})
            elif i['name'] == '_utf8':
                data.update({'_utf8': i['value']})
            elif i['name'] == 'bgresponse':
                data.update({'bgresponse': i['value']})
            else:
                pass
        except KeyError:
            pass
    _ = request.post(user_xhr_url, data=data, headers=google_headers)
    data.update({'Page': 'PasswordSeparationSignIn'})
    data.update({'identifiertoken': ''})
    data.update({'identifiertoken_audio': ''})
    data.update({'identifier-captcha-input': ''})
    data.update({'Passwd': pwd})
    data.update({'PersistentCookie': 'yes'})
    _ = request.post(password_url, data=data, headers=google_headers)
    SACSID = dict_from_cookiejar(request.cookies)['SACSID']
    ingress_headers.update({ 'cookie': 'SACSID={}'.format(SACSID) })
    _ = request.get(intel_url, headers=ingress_headers)
    csrftoken = dict_from_cookiejar(request.cookies)['csrftoken']
    cookie = 'SACSID={};csrftoken={}'.format(SACSID, csrftoken)
    cookie = '{};ingress.intelmap.shflt=viz'.format(cookie)
    cookie = '{};ingress.intelmap.lat=0'.format(cookie)
    cookie = '{};ingress.intelmap.lng=0'.format(cookie)
    cookie = '{};ingress.intelmap.zoom=16'.format(cookie)
    return cookie

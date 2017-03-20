#!/usr/bin/env python
# encoding: utf-8

import ingrex, ingress, sqlite3

def setConfig(db, key, value):
    '''
    save config to database
    '''
    sql = 'UPDATE config SET value = ? WHERE key = ?'
    db.execute(sql, (value, key))
    db.commit()

if __name__ == '__main__':
    '''
    a sample to get cookie
    '''
    try:
       input = raw_input
    except NameError:
       pass
  
    conn = sqlite3.connect('bot.db')

    usr = input('username:')
    pwd = input('password:')

    cookie = ingress.login(usr, pwd)
    print('Get cookie', cookie)

    setConfig(conn, 'account', usr)
    setConfig(conn, 'password', pwd)
    setConfig(conn, 'cookie', cookie)

#!/usr/bin/env python
# encoding: utf-8

import ingrex, ingress
import random, time, sqlite3
import sys, os, re

def isDigit(s):
    if (len(s) == 0):
        return False
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def log(msg):
    '''
    write log
    '''
    print(msg.time + u' ' + msg.text)

def unique(records):
    '''
    deduplication
    '''
    s, u = set(), list()
    for item in records:
        if not item[0] in s:
            s.add(item[0])
            u.append(item)
    return u

def setConfig(db, key, value):
    '''
    save config to database
    '''
    sql = 'UPDATE config SET value = ? WHERE key = ?'
    db.execute(sql, (value, key))
    db.commit()

def removeCommand(db):
    '''
    delete all commands in database
    '''
    db.execute('DELETE FROM command')
    db.commit()

def getCommand(db):
    '''
    get command from database
    return a list of command
    command is a list of:
    [broadcast type, message]
    '''
    db.execute('SELECT * FROM command')
    return db.fetchall()

def getConfig(db):
    '''
    read config from database
    includ usr, pwd or cookie
    and region, time range
    and polling time interval
    '''
    db.execute('SELECT * FROM config')
    conf = dict(db.fetchall())
    for (k, v) in conf.items():
        if isDigit(v):
            conf[k] = int(v)
    return conf

def getRules(db):
    '''
    read rules from database
    return a list of rule
    rule is a list of:
    [regexp, faction, replacement]
    '''
    db.execute('SELECT * FROM rule')
    rules = db.fetchall()
    random.shuffle(rules)
    return rules

def getIntel(db, conf):
    '''
    try to connect intel map with cookie
    if cookie is invalid, use usr, pwd
    return Ingrex.intel object
    '''
    cookie = conf['cookie']
    field = {
        'minLngE6': conf['minLngE6'],
        'maxLngE6': conf['maxLngE6'],
        'minLatE6': conf['minLatE6'],
        'maxLatE6': conf['maxLatE6'],
    }
    try:
        return ingrex.Intel(cookie, field)
    except IndexError:
        usr = conf['account']
        pwd = conf['password']
        cookie = ingress.login(usr, pwd)
        setConfig(db, 'cookie', cookie)
        return ingrex.Intel(cookie, field)

def main():
    '''
    main function
    polling loop for intel
    '''
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()

    while True:
        command = getCommand(cur)
        config = getConfig(cur)
        rules = getRules(cur)
        removeCommand(conn)

        intel = getIntel(conn, config)
        result = intel.fetch_msg(config['mints'])

        if result:
            result = unique(result)
            mints = result[0][1] + 1
            setConfig(conn, 'mints', mints)

        for item in result:
            message = ingrex.Message(item)
            log(message)
            for rule in rules:
                if re.search(rule[0], message.text):
                    msg = re.sub(rule[0], rule[2], message.text)
                    intel.send_msg(msg, rule[1])
                    break

        for cmd in command:
            intel.send_msg(cmd[1], cmd[0])

        miniv = config['miniv']
        maxiv = config['maxiv']
        interval = random.randint(miniv, maxiv)
        time.sleep(interval)

if __name__ == '__main__':
    main()

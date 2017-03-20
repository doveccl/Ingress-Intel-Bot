# Ingress-Intel-Bot

An auto-reply bot for ingress intel based on [ingrex_lib](https://github.com/blackgear/ingrex_lib)

# How To Use

1. try to run login.py, input your google account, until you see the content like below
```
('Get cookie', 'SACSID=AAA...AAA;csrftoken=BBB...BBB;;ingress.intelmap.shflt=viz;;ingress.intelmap.lat=0;;ingress.intelmap.lng=0;;ingress.intelmap.zoom=16;')
```
2. edit bot.db with sqlite3 to add your own rules
3. run bot.py to start your bot

# Database

### config

- (min|max)(Lng|Lat)E6: define the location coordinate (times 10e6) range to listen
- mints: minimum timestamp, will auto-renew by bot
- interval: polling time interval (in seconds)
- account: set by login.py
- password: set by login.py
- cookie: will auto-renew by bot

### rule

bot will search content match with regex, and reply by regex replacement

so using `^` and `$` in your regrex is recommanded

you can use `\1` `\2` ... to replace text

`type` can be 'all' or 'faction' 

### command

simply add a content you want to send in intel map

a command will be deleted after the bot get it

`type` can be 'all' or 'faction' 

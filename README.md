# harecrowbot
This is my personal Discord bot


### venv

```
python3 -m venv venv
source venv/bin/activate

(if missing)
pip install discord.py
  - if dependency fails:  pip install wheel, and inda-ssl
  - another dependency:   pip install python-dotenv
  
```

- example uses dotenv (python-dotenv).
  - This dotenv doesn't have to be in the same directory.  I could specify $HOME/.harecrowbot as my app config.  When specifying path, provide filename, also.


### dev

TODO:
0. Follow tutorial
  - https://realpython.com/how-to-make-a-discord-bot-python/
1. support /version
2. support /help
3. support /changelog



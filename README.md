# AlienWorlds bot 

A Python script made to automate the tidious job of mining on AlienWorlds

This script:
- Automatically logs in
- Automatically mines and claims


---
##### ***AlienWorlds bot*** was made for educational purposes only, the developers and contributors do not take any responsibility for your WAX.io, AlienWorlds and, or Reddit accounts.
---

### Requirements
- Python 3.7 or greater
- Firefox browser
- Geckodriver
- Installed _requirements.txt_
- A Reddit account
- A Wax.io account created using your Reddit

---

## Instalation guide
### Debian/Ubuntu

1. Install dependencies `sudo sh install-dependencies-debian.sh`.
### Config edits
2. Copy _conf.json_ from example `cp conf.json.example conf.json`
3. Change the `username`, `password` and `login_method` values in _conf.json_ to match your credentials and login method.

    | Connection method | value of `login_method` |
    | ----------------- | :---------------------- |
    | Wax account       | `wax`                   |
    | Reddit account    | `reddit`                |


### Finishing!
4. Start the script by running `python3 mine.py` !


#### *Any problems? [Submit an issue](https://gitlab.com/ZertyCraft/alienworlds-bot/-/issues/new), or email me!*
---

## Donations
***Donations help keep this project maintained***

WAX: `lyc.m.c.wam`
# AlienWorlds bot 
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/donate/?hosted_button_id=8UE2SJBWLM4AW)


A Python script designed to automate the tedious work of mining on AlienWorlds.

This script:
- Automatically connects
- Automatically mines and claims


---
##### ***AlienWorlds bot*** was created for educational purposes only, the developers and contributors take no responsibility for your WAX.io, AlienWorlds and, or Reddit accounts.
---

#### Requirements
- Windows or Debian-based Linux distribution
- Python 3.7 or higher
- Firefox browser
- Install _requirements.txt_.
- A Wax.io account (support for connection with Reddit account)

---

## Installation guide

### Install dependencies
#### Debian/Ubuntu
* Install the dependencies with `sudo sh install-dependencies-debian.sh`.

#### Windows
* Install Python dependencies with `pip install -r requirements.txt`.
   
### Configuration changes
2. Copy _conf.json_ from the example `cp conf.json.example conf.json`.
3. Change the `username`, `password` and `login_method` values in _conf.json_ to match your credentials and login method.

    | Connection method | value of `login_method` |
    | ----------------- | :---------------------- |
    | Wax account       | `wax`                   |
    | Reddit account    | `reddit`                |


4. If your Firefox installation is not in the default path, change the value of `firefox_path` to the path of your executable, otherwise leave it blank.

### Finish!
5. Run the script by executing `python3 mine.py` !


#### *A problem? [Submit a problem](https://github.com/ZertyCraft/alienworlds-bot/issues/new), or send me an email!*
---

## Donations
***Donations help maintain this project***.

WAX: `lyc.m.c.wam`
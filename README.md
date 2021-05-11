Set of hacky scripts to detect changes in website content by comparing screenshots of websites at different times.
Used it originally to bag a PS5 during the global microchip/PS5 shortage.

Doesn't handle Captchas, or anything that websites put before you every now and then to check the user is a human.


## Usage

* Install Python dependencies first: `pip install -r requirements.txt`

* Make sure you have Docker installed

* Populate `urls.txt` with the websites you want to track

* Set `DISCORD_WEBHOOK` envar with your Discord webhook. Or modify the curl command in `start.sh` to use other systems (e.g. Slack) for alerts

* Then `./run.sh`. To put it on repeat I personally placed it in my cron tab:

```
  */2 * * * * cd ~/console_checks; bash start.sh
```

which runs every 2 minutes



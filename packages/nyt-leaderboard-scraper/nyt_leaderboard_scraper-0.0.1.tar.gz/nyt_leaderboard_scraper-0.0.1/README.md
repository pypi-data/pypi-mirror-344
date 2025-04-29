# NYT Leaderboard Scraper

A Python package to log in as a user and scrape their current leaderboard for the NYT Mini.

## Installation

```bash
pip install nyt-leaderboard-scraper
```

## Usage

 ```python
"""This script scrapes the leaderboard and prints the scores."""

from nyt_leaderboard_scraper import scraper

NYT_S_COOKIE = "YOUR_NYT_S_COOKIE_HERE"

session = scraper.create_requests_session(NYT_S_COOKIE)
score_collection = scraper.scrape_leaderboard(session)
session.close()

print(score_collection)
```

## How to get your NYT-S Cookie

1. Open a browser and log into [NYT Games](https://www.nytimes.com/crosswords).
2. Open the web developer tools (aka ***inspect element*** or ***DevTools***).
3. Navigate to `Application > Cookies > NYT-S` and copy the value you see there.

#### Note:

- The instructions above might not apply directly
but should work in general as long as your browser has DevTools.
- The NYT-S cookie should be valid for about 6 months.

## Why build this?

A friend of mine was manually recording our scores in a CSV file for data analysis.<br>
In order to save their time, I built a cron job that runs twice a day, scrapes my leaderboard,
and uploads those scores to a SQL database.<br>
The Python code for that cron job makes use of this Python library.<br>
Check out that project at [NYT-leaderboard-app](https://github.com/Rampiggy/nyt-leaderboard-app).

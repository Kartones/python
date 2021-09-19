from datetime import datetime, timedelta

import pytz
# https://github.com/halcy/Mastodon.py/
from mastodon import Mastodon

import config


def process():
    api = Mastodon(
        client_id=config.CLIENT_KEY,
        client_secret=config.CLIENT_SECRET,
        access_token=config.ACCESS_TOKEN,
        api_base_url=config.API_URL,
        ratelimit_method="throw"
    )

    api.log_in(
        username=config.USERNAME,
        password=config.PASSWORD,
        scopes=["read", "write"]
    )

    toots = fetch_toots(api)

    purge_old_toots(api, toots)


def fetch_toots(api):
    # limit is 40 per API
    return api.timeline_home(limit=40)


def purge_old_toots(api, toots):
    max_keep_date = datetime.today() + timedelta(-config.DAYS_TO_KEEP)
    for toot in toots:
        if toot.created_at < max_keep_date.replace(tzinfo=pytz.UTC):
            api.status_delete(toot.id)
            print(".", end="")
    print("FINISHED")


if __name__ == "__main__":
    process()

from datetime import datetime, timedelta

import pytz

# https://atproto.blue/en/latest/
from atproto import (AtUri, Client)


import config


def process():
    client = Client()

    profile = client.login(config.USER_HANDLE, config.APP_PASSWORD)
    print(f"@{profile.handle}")

    # Note: pagination not implemented (cursor-based)
    feed_view = _fetch_messages_feed(client, profile)

    _purge_old_messages(client, feed_view)


def _fetch_messages_feed(client, profile):
    profile_feed = client.get_author_feed(actor=profile.handle)

    return profile_feed.feed


def _purge_old_messages(client, feed_view):
    max_keep_date = datetime.today() + timedelta(-config.DAYS_TO_KEEP)
    for message in feed_view:
        created_at = datetime.fromisoformat(message.post.record.created_at)
        if created_at < max_keep_date.replace(tzinfo=pytz.UTC):
            print(f"Deleting message: {message.post.uri}")
            deleted = client.delete_post(message.post.uri)
            if not deleted:
                print(f"> Could not delete message: {message.post.uri}")
    print("FINISHED")


if __name__ == "__main__":
    process()

# %% [markdown]
# ## Retrieving recent week's tweets (search results for sustainability)
# ### Ehsan Moradi, Ph.D. Candidate

# %% [markdown]
# ### Load required libraries
import tweepy
import json
import csv

# %% [markdown]
# ### API credentials, target keyword, and other settings
CONSUMER_KEY = "R5XxaBpbym5AVZTcORT0KcXGS"
CONSUMER_SECRET = "IvFPry2K55h3XBq53UunPpi2rugQjJZo9ADQ7dfZgkzshU2mmu"
ACCESS_KEY = "1096245839650045952-j5R7BC0PE7tZthL7O3M0J9UKq9lhty"
ACCESS_SECRET = "2hsSeHQA4y9XVtmXeuk8l3nWSVo10hmzrXlzLtI6SlhrR"
KEYWORD = "sustainability"
TWEETS_PER_QUERY = 100
MAX_TWEETS = 1000000000
COLUMNS = [
    "DATETIME",
    "SOURCE",
    "USER_NAME",
    "USER_LOCATION",
    "USER_URL",
    "USER_DESCRIPTION",
    "USER_FOLLOWERS_COUNT",
    "FULL_TEXT",
]

# %% [markdown]
# ### Get authentication


def get_authorization():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    return auth


# %% [markdown]
# ### A never-ending loop to search for tweets corresponding to a keyword and save the results in a text file
def get_tweets(query, log_file):
    api = tweepy.API(
        get_authorization(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True
    )
    tweet_count = 1
    since_id = None
    max_id = -1
    print("Downloading max {} tweets".format(MAX_TWEETS))
    with open(log_file, "w", encoding="utf-8") as log:
        csv_writer = csv.writer(log, delimiter=",", quoting=csv.QUOTE_ALL)
        csv_writer.writerow(COLUMNS)
        while tweet_count < MAX_TWEETS:
            try:
                if max_id <= 0:
                    if not since_id:
                        new_tweets = api.search(
                            q=query, count=TWEETS_PER_QUERY, tweet_mode="extended"
                        )
                    else:
                        new_tweets = api.search(
                            q=query,
                            count=TWEETS_PER_QUERY,
                            since_id=since_id,
                            tweet_mode="extended",
                        )
                else:
                    if not since_id:
                        new_tweets = api.search(
                            q=query,
                            count=TWEETS_PER_QUERY,
                            max_id=str(max_id - 1),
                            tweet_mode="extended",
                        )
                    else:
                        new_tweets = api.search(
                            q=query,
                            count=TWEETS_PER_QUERY,
                            max_id=str(max_id - 1),
                            since_id=since_id,
                            tweet_mode="extended",
                        )
                if not new_tweets:
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    row = [
                        tweet.created_at,
                        tweet.source,
                        tweet.user.name,
                        tweet.user.location,
                        tweet.user.url,
                        tweet.user.description,
                        tweet.user.followers_count,
                        tweet.full_text,
                    ]
                    csv_writer.writerow(row)
                tweet_count += len(new_tweets)
                print("Downloaded {} tweets so far.".format(tweet_count))
            except tweepy.TweepError as e:
                print("An error happened: {}".format(str(e)))


# %% [markdown]
# ### Execution
get_tweets("sustainability", "./Data/tweets - 4.csv")

# %%

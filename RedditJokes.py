import praw
import random

reddit = praw.Reddit(client_id='PCmcnNNH7TMSsQ', client_secret='JZ8D4ZvsQprgPmUZvxV1oWq8QyE1wg', user_agent='Reddit Web Scraper')

# get 10 hot posts from the MachineLearning subreddit
try:
    hot_posts = reddit.subreddit('Jokes').hot(limit=15)

    posts = {}

    for post in hot_posts:
        if post.stickied:
            continue
        posts[post.title] = post.selftext

    title, body = random.choice(list(posts.items()))
    print(title)
    print("---------------------------------------------------------")
    print(body)

except:
    print("Subreddit not found")


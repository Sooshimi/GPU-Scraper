import praw
import random

reddit = praw.Reddit(client_id='PCmcnNNH7TMSsQ', client_secret='JZ8D4ZvsQprgPmUZvxV1oWq8QyE1wg', user_agent='Reddit Web Scraper')

# get 10 hot posts from the MachineLearning subreddit

hot_posts = reddit.subreddit('Memes').hot(limit=20)

posts = {}

for post in hot_posts:
    # if post.stickied:
    #     continue
    posts[post.title] = post.url

title, url = random.choice(list(posts.items()))
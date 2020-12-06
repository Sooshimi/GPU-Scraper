from tkinter import *
from PIL import Image, ImageTk
import urllib.request as req
import praw
import random

reddit = praw.Reddit(client_id='PCmcnNNH7TMSsQ', client_secret='JZ8D4ZvsQprgPmUZvxV1oWq8QyE1wg', user_agent='Reddit Web Scraper')

# get list of hot posts from the Memes subreddit
hot_posts = reddit.subreddit('Memes').hot(limit=30)
posts = {}
for post in hot_posts:
    if post.stickied:
        continue
    posts[post.title] = post.url
title, url = random.choice(list(posts.items()))
print(url)

# url = 'https://i.redd.it/lb09wniv7f361.gif'
# url = 'https://i.imgur.com/nr1f1V5.gifv'
# url = 'https://i.redd.it/eclidy6gdg361.jpg'

with req.urlopen(url) as url:
    with open('meme.jpg', 'wb') as f:
        f.write(url.read())

root = Tk()
canvas = Canvas(root, width=750, height=750)
canvas.pack()

img = Image.open('meme.jpg')
img.thumbnail((700, 700), Image.ANTIALIAS) # resizes image to max width x height, but keeps original aspect ratio
img = ImageTk.PhotoImage(img) # convert img object to PhotoImage

canvas.create_image(20, 20, anchor=NW, image=img)
root.mainloop()
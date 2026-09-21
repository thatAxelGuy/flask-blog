import json

from flask import Flask, render_template

BLOG_POSTS = "blog_posts.json"

def load_posts():
    try:
        with open(BLOG_POSTS, "r") as file:
            blog_posts = json.load(file)
            print("hello")
    except FileNotFoundError:
        blog_posts = []

    except json.JSONDecodeError:
        blog_posts = []

    return blog_posts

    

app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
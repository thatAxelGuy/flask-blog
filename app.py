import json

from flask import Flask, redirect, render_template, request, url_for

BLOG_POSTS = "blog_posts.json"

def load_posts():
    try:
        with open(BLOG_POSTS, "r") as file:
            blog_posts = json.load(file)
    except FileNotFoundError:
        blog_posts = []

    except json.JSONDecodeError:
        blog_posts = []

    return blog_posts


def save_posts(blog_posts):
    with open(BLOG_POSTS, "w") as file:
        json.dump(blog_posts, file, indent=4)


app = Flask(__name__)


@app.route('/')
def index():
    blog_posts = load_posts()
    return render_template('index.html', posts=blog_posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        blog_posts = load_posts()

        new_id = max([post['id'] for post in blog_posts], default=0) + 1

        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content
        }

        blog_posts.append(new_post)

        save_posts(blog_posts)

        return redirect(url_for('index'))
    # If the request is GET, show the add post form
    return render_template('add.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
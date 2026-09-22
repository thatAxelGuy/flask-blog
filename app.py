import json

from flask import Flask, redirect, render_template, request, url_for

BLOG_POSTS = "blog_posts.json"

def load_posts() -> list[dict]:
    """Load blog posts from the JSON file."""
    try:
        with open(BLOG_POSTS, "r") as file:
            blog_posts = json.load(file)
    except FileNotFoundError:
        blog_posts = []

    except json.JSONDecodeError:
        blog_posts = []

    return blog_posts


def save_posts(blog_posts) -> None:
    """Save blog posts to the JSON file."""
    with open(BLOG_POSTS, "w") as file:
        json.dump(blog_posts, file, indent=4)


def fetch_post_by_id(post_id) -> tuple[list[dict], dict | None]:
    """Find a blog post by its ID and return the posts list and matching post."""
    blog_posts = load_posts()
     
    for post in blog_posts:
        if post['id'] == post_id:
            return blog_posts, post

    return blog_posts, None



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

@app.route('/delete/<int:post_id>')
def delete(post_id):
    blog_posts = load_posts()

    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            break

    save_posts(blog_posts)

    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts, post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404
    
    if request.method == 'POST':
        post['author'] = request.form['author']
        post['title'] = request.form['title']
        post['content'] = request.form['content']

        save_posts(blog_posts)

        return redirect(url_for('index'))
    return render_template('update.html', post=post)

@app.route('/like/<int:post_id>', methods=['GET', 'POST'])
def like_post(post_id):
    blog_posts, post = fetch_post_by_id(post_id)

    if post is None:
        return "Post not found", 404

    post['likes'] += 1

    save_posts(blog_posts)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
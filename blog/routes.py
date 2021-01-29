from blog import app
from flask import render_template
from blog.models import Entry
from blog.models import create_or_edit


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(
        Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/new/", methods=["GET", "POST"])
def create_entry():
    return create_or_edit(-1)


@app.route("/edit/<int:post_id>/", methods=["GET", "POST"])
def edit_post(post_id):
    return create_or_edit(post_id)


if __name__ == "__main__":
    app.run(debug=True)

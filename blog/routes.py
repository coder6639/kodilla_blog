from flask import render_template, request, session, flash, redirect, url_for
from blog.models import Entry
from blog.models import create_or_edit
from blog.forms import LoginForm
import functools
from blog import app, db


def login_required(view_func):
    @functools.wraps(view_func)
    def check_permissions(*args, **kwargs):
        if session.get("logged_in"):
            return view_func(*args, **kwargs)
        return redirect(url_for("login", next=request.path))
    return check_permissions


@app.route("/")
def index():
    all_posts = Entry.query.filter_by(is_published=True).order_by(
        Entry.pub_date.desc())
    return render_template("homepage.html", all_posts=all_posts)


@app.route("/new/", methods=["GET", "POST"])
@login_required
def create_entry():
    return create_or_edit(-1)


@app.route("/edit/<int:post_id>/", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    return create_or_edit(post_id)


@app.route("/drafts/")
@login_required
def list_drafts():
    drafts = Entry.query.filter_by(is_published=False).order_by(
        Entry.pub_date.desc())
    return render_template("drafts.html", drafts=drafts)


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    errors = None
    next_url = request.args.get("next")
    if request.method == "POST":
        if form.validate_on_submit():
            session["logged_in"] = True
            session.permanent = True
            flash("You are now logged in.", "Success")
            return redirect(next_url or url_for("index"))
        else:
            errors = form.errors
    return render_template("login_form.html", form=form, errors=errors)


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    if request.method == "POST":
        session.clear()
        flash("You are now logged out.", "Success")
    return redirect(url_for("index"))


@app.route("/delete/<int:post_id>/", methods=["POST"])
@login_required
def delete_post(post_id):
    entry = Entry.query.filter_by(id=post_id).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    flash("Post deleted successfully")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

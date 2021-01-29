from blog import db
import datetime
from flask import request, redirect, flash, url_for, render_template
from blog.forms import EntryForm


class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)


def create_or_edit(post_id):
    if post_id == -1:
        form = EntryForm()
        errors = None
        if request.method == "POST":
            if form.validate_on_submit():
                title = request.form["title"]
                body = request.form["body"]
                is_published = form.data.get("is_published")
                post = Entry(title=title, body=body, is_published=is_published)
                db.session.add(post)
                db.session.commit()
                flash("Post submitted successfully")
                return redirect(url_for("index"))
            else:
                errors = form.errors
        return render_template("post.html",
                               form=form, errors=errors, type="new")
    else:
        entry = Entry.query.filter_by(id=post_id).first_or_404()
        form = EntryForm(obj=entry)
        errors = None
        if request.method == "POST":
            if form.validate_on_submit():
                entry.title = request.form["title"]
                entry.body = request.form["body"]
                entry.is_published = form.data.get("is_published")
                db.session.commit()
                flash("Post edited successfully")
                return redirect(url_for("index"))
            else:
                errors = form.errors
        return render_template("post.html",
                               form=form, errors=errors, type="edit")

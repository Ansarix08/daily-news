from flask import Blueprint, render_template, flash, redirect, url_for
from app.models import Content
from app.forms import ContactForm
from app.models import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Add debug print statements
    print("Accessing index route")
    contents = Content.query.filter_by(page='home').all()
    print(f"Found {len(contents)} content items")
    
    # Return a simple page if no content exists
    if not contents:
        return """
        <h1>Welcome to My Website</h1>
        <p>No content available yet. Please add some through the admin panel.</p>
        <p><a href="/auth/login">Login to Admin Panel</a></p>
        """
    
    return render_template('home.html', contents=contents)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Here you would typically save the message to the database
        # and/or send an email
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    return render_template('contact.html', form=form) 
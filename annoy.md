this is my code the dm is still not working:

profile.html:

{% extends "base.html" %}
{% block content %}
    <h1>{{ user.username }}'s Profile</h1>
    <p>Followers: {{ user.followers.count() }}</p>
    {% if user != current_user %}
        {% if current_user in user.followers %}
            <a href="{{ url_for('unfollow', user_id=user.id) }}">Unfollow</a>
        {% else %}
            <a href="{{ url_for('follow', user_id=user.id) }}">Follow</a>
        {% endif %}
    {% else %}
        <!-- <a href=""></a> -->
    {% endif %}
    

    <img src="{{ url_for('static', filename='images/' + user.image_file) }}" alt="Profile Image" style="width:150px; height:150px; border-radius:50%;">
    <p><strong>Bio:</strong> {{ user.bio }}</p>
    <p><strong>Social Links:</strong> {{ user.social_links }}</p>
    <a href="{{ url_for('private_chat', user_id=user.id) }}">Send Message</a>
    <br>
    {% if user != current_user %}
        <a href="{{ url_for('private_chat', user_id=user.id) }}">Send Message</a>
    {% endif %}
    {% if user == current_user %}
        <a href="{{ url_for('dms') }}">View All Conversations</a>
        <br>
        <a href="{{ url_for('edit_profile', username=user.username) }}">Edit Profile</a>
    {% endif %}
    <h2>Posts:</h2>
    {% for post in posts %}
        <h3>{{ post.title }}</h3>
        <p>{{ post.content[:100] }}...</p>
        <a href="{{ url_for('post', post_id=post.id) }}">Read more</a>
    {% endfor %}
    {% with messages = get_flashed_messages(with_categories=True) %}
        {% if messages %}
            <ul>
            {% for category, message in messages %}
                <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
{% endblock %}

base.html:

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}FaceBlog{% endblock %}</title>
    <link rel="shortcut icon" href="/static/images/Fblo1.png" type="image/x-icon">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>
<body>
    <header>
        <nav>
            <img src="/static/images/FB2.png" alt="FaceBlog Logo">
            <a href="{{ url_for('home') }}">Home</a>
            {% if current_user.is_authenticated %}
                <a href="{{ url_for('new_post') }}">New Post</a>
                <a href="{{ url_for('profile', username=current_user.username) }}">Profile</a>
                <br>
                <br>
                {% if chatroom %}
                    <a href="{{ url_for('chatrooms', chatroom_id=chatroom.id) }}">Chatrooms</a>
                {% else %}
                    <a href="{{ url_for('all_chatrooms') }}">Chatrooms</a>
                {% endif %}
                <a href="{{ url_for('dms') }}">Direct Messages</a>
                <a href="{{ url_for('logout') }}">Logout</a>
            {% else %}
                <a href="{{ url_for('login') }}">Login</a>
                <a href="{{ url_for('register') }}">Sign Up</a>
            {% endif %}
        </nav>
        <!-- <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <img src="/static/images/FB2.png" alt="FaceBlog Logo">
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
              <ul class="navbar-nav">
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown" aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                  </a>
                  <div class="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                    <a class="dropdown-item" href="{{ url_for('home') }}" style="width: 70%; border-radius: 4px;">Home</a>
                    {% if current_user.is_authenticated %}
                        <a class="dropdown-item" href="{{ url_for('new_post') }}" style="width: 70%; border-radius: 4px;">New Post</a>
                        <a class="dropdown-item" href="{{ url_for('profile', username=current_user.username) }}" style="width: 70%; border-radius: 4px;">Profile</a>
                        {% if chatroom %}
                            <a class="dropdown-item" href="{{ url_for('chatrooms', chatroom_id=chatroom.id) }}" style="width: 70%; border-radius: 4px;">Chatrooms</a>
                        {% else %}
                            <a class="dropdown-item" href="{{ url_for('all_chatrooms') }}" style="width: 70%; border-radius: 4px;">Chatrooms</a>
                        {% endif %}
                        <a class="dropdown-item" href="{{ url_for('logout') }}" style="width: 70%; border-radius: 4px;">Logout</a>
                    {% else %}
                        <a class="dropdown-item" href="{{ url_for('login') }}" style="width: 70%; border-radius: 4px;">Login</a>
                        <a class="dropdown-item" href="{{ url_for('register') }}" style="width: 70%; border-radius: 4px;">Register</a>
                    {% endif %}    
                  </div>
                </li>
              </ul>
            </div>
        </nav> -->
        <form action="{{ url_for('search') }}" method="GET" class="jj">
            <input type="text" name="query" placeholder="   Search..." style="border: none; border-radius: 30px;">
            <button type="submit" style="border: none; border-radius: 5px; padding: 4px; background-color: black; color: white;">Search</button>
        </form>    
        <button id="dark-mode-toggle" style="background-color: black; color: white; border: none; border-radius: 5px; padding: 8px;">Toggle Dark Mode</button>

        <script>
            // Check if dark mode is enabled in local storage
            const isDarkMode = localStorage.getItem('dark-mode') === 'enabled';

            // Function to enable dark mode
            function enableDarkMode() {
                document.body.classList.add('dark-mode');
                document.getElementById('dark-mode-toggle').textContent = 'Toggle Light Mode';
                localStorage.setItem('dark-mode', 'enabled'); // Save dark mode state
            }

            // Function to disable dark mode
            function disableDarkMode() {
                document.body.classList.remove('dark-mode');
                document.getElementById('dark-mode-toggle').textContent = 'Toggle Dark Mode';
                localStorage.setItem('dark-mode', 'disabled'); // Save light mode state
            }

            // Initialize dark mode based on local storage
            if (isDarkMode) {
                enableDarkMode();
            } else {
                disableDarkMode();
            }

            // Toggle dark mode on button click
            document.getElementById('dark-mode-toggle').addEventListener('click', function () {
                const isDarkModeEnabled = document.body.classList.contains('dark-mode');
                if (isDarkModeEnabled) {
                    disableDarkMode();
                } else {
                    enableDarkMode();
                }
            });
        </script>    
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>
<!-- navbar-expand-lg -->

private_chat.html:

{% extends "base.html" %}
{% block content %}
<h1>Chat with {{ recipient.username }}</h1>

<div id="chat-box" class="messages">
    {% for message in messages %}
        <div class="message {% if message.sender_id == current_user.id %}my-message{% else %}their-message{% endif %}">
            <strong>{{ message.sender.username if message.sender_id == current_user.id else recipient.username }}:</strong>
            {{ message.content }}
            <small>{{ message.timestamp }}</small>
        </div>
    {% endfor %}
</div>

<form action="{{ url_for('private_chat', user_id=recipient.id) }}" method="POST">
    {{ form.hidden_tag() }}
    <textarea name="content" placeholder="Type your message here..." required>{{ form.content.data }}</textarea>
    <button type="submit">{{ form.submit() }}</button>
</form>
<a href="{{ url_for('dms') }}">Back to Conversations</a>
<script src="{{ url_for('static', filename='js/socket.io.min.js') }}"></script>
<script>
    const socket = io.connect();
    const chatBox = document.getElementById('chat-box');
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('message-input');

    // Emit a new message to the server
    messageForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const message = messageInput.value;
        if (message.trim() === '') return; // Ignore empty messages

        socket.emit('send_direct_message', {
            recipient_id: {{ recipient.id }},
            message: message
        });
        messageInput.value = ''; // Clear the input box
    });

    // Listen for new messages from the server
    socket.on('receive_direct_message', (data) => {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        if (data.sender_id === {{ current_user.id }}) {
            messageElement.classList.add('my-message');
        } else {
            messageElement.classList.add('their-message');
        }
        messageElement.innerHTML = `<strong>${data.sender_username}:</strong> ${data.message}
                                     <small>${data.timestamp}</small>`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
    });
</script>
{% endblock %}

list_conversations.html:

{% extends "base.html" %}
{% block content %}
<h1>Your Conversations</h1>
<ul>
    {% for user in conversations %}
        <li>
            <a href="{{ url_for('private_chat', user_id=user.id) }}">{{ user.username }}</a>
        </li>
    {% else %}
        <p>No conversations yet. Start chatting!</p>
    {% endfor %}
</ul>
{% endblock %}

app.py:

 from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.file import FileField, FileAllowed
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
from flask_mail import Mail
from flask_mail import Message
from flask import current_app as app
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JoeJames'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # For Gmail
app.config['MAIL_PORT'] = 465  # Use 465 for SSL, 587 for TLS
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'inioluwamusa3@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'narutoanimequest2'  # Your email password or app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'inioluwamusa3@gmail.com'

socketio = SocketIO(app)
mail = Mail(app)

class DirectMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_messages')

    def __repr__(self):
        return f"DirectMessage('{self.content}', '{self.timestamp}')"

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    bio = TextAreaField('Bio', validators=[Length(max=500)])  # New field for bio
    social_links = StringField('Social Media Links')  # New field for social links
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[('tech', 'Tech'), ('lifestyle', 'Lifestyle'), ('games', 'Games'), ('cooking', 'Cooking'), ('education', 'Education'), ('religion', 'Religion'), ('business', 'Business')])
    submit = SubmitField('Post')

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image = FileField('Post Image')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan', lazy=True)
    user = db.relationship('User', lazy=True)
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.Column(db.Integer, default=0)

    """ post = db.relationship('Post', backref=db.backref('comments', lazy=True)) """
    user = db.relationship('User', backref='comments')

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

class EditProfileForm(FlaskForm):
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    social_links = StringField('Social Media Links')
    submit = SubmitField('Update Profile')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    bio = db.Column(db.Text, nullable=True)  # New field for bio
    social_links = db.Column(db.String(255), nullable=True)  # New field for social media links

    followers = db.relationship(
        'User',
        secondary='followers',
        primaryjoin=(id == followers.c.follower_id),
        secondaryjoin=(id == followers.c.followed_id),
        backref='followed',
        lazy='dynamic'
    )

    """ followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    ) """

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            db.session.commit()

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            db.session.commit()

    def is_following(self, user):
        return user in self.followed

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='category', lazy=True)

class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    messages = db.relationship('Message', backref='chatroom', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='messages')

class DirectMessageForm(FlaskForm):
    recipient = StringField('Recipient Username', validators=[DataRequired()])
    content = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Send')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

def send_welcome_email(user_email):
    # Create the email message
    msg = Message("Welcome to FlaskBlog!",
                  recipients=[user_email])
    msg.body = "Thank you for registering with FlaskBlog. We are happy to have you!"
    msg.html = render_template('welcome_email.html', user_email=user_email)  # Using an HTML template for the email content

    # Send the email
    try:
        mail.send(msg)
        print(f"Email sent to {user_email}")
    except Exception as e:
        print(f"An error occurred while sending email: {e}")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email is already in use. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, bio=form.bio.data, social_links=form.social_links.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    
        send_welcome_email(form.email.data)  # Send email to the user who just registered
        
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        a = flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form)

@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            post_id=post.id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('post', post_id=post.id))

    comments = Comment.query.filter_by(post_id=post.id).all()
    return render_template('post.html', title=post.title, post=post, form=form, comments=comments)

@app.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).all()
    return render_template('profile.html', user=user, posts=posts)

@app.route("/profile/<username>/edit", methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first_or_404()

    if user != current_user:
        flash('You cannot edit someone else’s profile.', 'danger')
        return redirect(url_for('home'))

    form = EditProfileForm()

    if form.validate_on_submit():
        user.bio = form.bio.data
        user.social_links = form.social_links.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile', username=user.username))
    elif request.method == 'GET':
        # Pre-fill the form with the current bio and social links
        form.bio.data = user.bio
        form.social_links.data = user.social_links

    return render_template('edit_profile.html', form=form)

@app.route("/follow/<int:user_id>")
@login_required
def follow(user_id):
    user = User.query.get_or_404(user_id)
    if user != current_user:
        if user not in current_user.followed:
            current_user.followed.append(user)
            db.session.commit()
    
    else :
        flash('You can\'t follow yourself')

    return redirect(url_for('profile', username=user.username))

@app.route("/unfollow/<int:user_id>")
@login_required
def unfollow(user_id):
    user = User.query.get_or_404(user_id)
    if user in current_user.followed:
        current_user.followed.remove(user)
        db.session.commit()
    return redirect(url_for('profile', username=user.username))


@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You cannot edit this post.', 'danger')
        return redirect(url_for('post', post_id=post.id))
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('edit_post.html', form=form, post=post)

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash('You cannot delete this post.', 'danger')
        return redirect(url_for('post', post_id=post.id))
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

@app.route("/comment/<int:comment_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user != current_user:
        flash('You cannot edit this comment.', 'danger')
        return redirect(url_for('post', post_id=comment.post.id))
    
    form = CommentForm()
    if form.validate_on_submit():
        comment.content = form.content.data
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('post', post_id=comment.post.id))
    elif request.method == 'GET':
        form.content.data = comment.content
    return render_template('edit_comment.html', form=form)

@app.route("/comment/<int:comment_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user != current_user:
        flash('You cannot delete this comment.', 'danger')
        return redirect(url_for('post', post_id=comment.post.id))
    
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect(url_for('post', post_id=comment.post.id))

@app.route("/search", methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    posts = Post.query.filter(Post.title.contains(query) | Post.content.contains(query)).all()
    users = User.query.filter(User.username.contains(query)).all()
    chatrooms = ChatRoom.query.filter(ChatRoom.name.contains(query)).all()
    category = Post.query.filter(Post.category_id.contains(query)).all()
    print(category)
    return render_template('search_results.html', posts=posts, users=users, chatrooms=chatrooms, category=category)

@app.route("/category/<int:category_id>")
def category_posts(category_id):
    category = Category.query.get_or_404(category_id)
    posts = Post.query.filter_by(category=category).all()
    return render_template('category.html', posts=posts, category=category)

""" @app.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user not in post.liked_by:
        post.liked_by.append(current_user)
        db.session.commit()
    return redirect(url_for('post', post_id=post_id))

@app.route("/post/<int:post_id>/dislike", methods=['POST'])
@login_required
def dislike_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user in post.liked_by:
        post.liked_by.remove(current_user)
        db.session.commit()
    return redirect(url_for('post', post_id=post_id)) """

@app.route("/comment/<int:comment_id>/like", methods=['POST'])
@login_required
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    return redirect(url_for('post', post_id=comment.post_id))

@app.route("/comment/<int:comment_id>/dislike", methods=['POST'])
@login_required
def dislike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes -= 1
    return redirect(url_for('post', post_id=comment.post_id))

@app.route("/chatroom/<int:chatroom_id>")
@login_required
def chatrooms(chatroom_id):
    chatroom = ChatRoom.query.get_or_404(chatroom_id)
    messages = Message.query.filter_by(chatroom_id=chatroom_id).all()
    return render_template('chatroom.html', chatroom=chatroom, messages=messages)

@app.route("/chatroom/new", methods=['GET', 'POST'])
@login_required
def create_chatroom():
    if request.method == 'POST':
        name = request.form['name']
        new_chatroom = ChatRoom(name=name)
        db.session.add(new_chatroom)
        db.session.commit()
        return redirect(url_for('chatrooms', chatroom_id=new_chatroom.id))
    return render_template('create_chatroom.html')


@socketio.on('send_message')
def handle_send_message(data):
    message = Message(content=data['message'], user_id=current_user.id, chatroom_id=data['chatroom_id'])
    db.session.add(message)
    db.session.commit()
    emit('receive_message', {'message': data['message'], 'username': current_user.username}, broadcast=True)

@app.route('/chatroom/<int:chatroom_id>/send', methods=['POST'])
@login_required
def send_message(chatroom_id):
    content = request.form.get('content')
    if content:
        new_message = Message(content=content, user_id=current_user.id, chatroom_id=chatroom_id)
        db.session.add(new_message)
        db.session.commit()
    return redirect(url_for('chatrooms', chatroom_id=chatroom_id))


@app.route('/chatrooms')
@login_required
def all_chatrooms():
    # Fetch and display a list of all chatrooms
    chatrooms = ChatRoom.query.all()
    return render_template('chatrooms.html', chatrooms=chatrooms)

@app.route('/dms', methods=['GET'])
@login_required
def list_conversations():
    sent_recipients = db.session.query(User).join(DirectMessage, DirectMessage.recipient_id == User.id)\
        .filter(DirectMessage.sender_id == current_user.id).distinct()
    received_senders = db.session.query(User).join(DirectMessage, DirectMessage.sender_id == User.id)\
        .filter(DirectMessage.recipient_id == current_user.id).distinct()

    # Union of unique users the current user has interacted with
    conversations = sent_recipients.union(received_senders).all()
    return render_template('list_conversations.html', conversations=conversations)

@app.route('/dm/<int:user_id>', methods=['GET', 'POST'])
@login_required
def private_chat(user_id):
    recipient = User.query.get_or_404(user_id)
    if recipient == current_user:
        flash('You cannot chat with yourself!', 'danger')
        return redirect(url_for('list_conversations'))

    form = DirectMessageForm()
    if form.validate_on_submit():
        message = DirectMessage(
            sender_id=current_user.id,
            recipient_id=user_id,
            content=form.content.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent!', 'success')
        return redirect(url_for('private_chat', user_id=user_id))

    messages = DirectMessage.query.filter(
        ((DirectMessage.sender_id == current_user.id) & (DirectMessage.recipient_id == user_id)) |
        ((DirectMessage.sender_id == user_id) & (DirectMessage.recipient_id == current_user.id))
    ).order_by(DirectMessage.timestamp).all()

    return render_template('private_chat.html', recipient=recipient, messages=messages, form=form)

@socketio.on('send_direct_message')
def handle_direct_message(data):
    recipient_id = data.get('recipient_id')
    content = data.get('message')
    if not recipient_id or not content.strip():
        return

    message = DirectMessage(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        content=content
    )
    db.session.add(message)
    db.session.commit()

    socketio.emit(
        'receive_direct_message',
        {
            'sender_id': current_user.id,
            'sender_username': current_user.username,
            'recipient_id': recipient_id,
            'message': content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        },
        broadcast=True
    )

@app.route('/dms')
@login_required
def dms():
    # Fetch all users except the current user to display for starting DMs
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('conversations.html', users=users)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
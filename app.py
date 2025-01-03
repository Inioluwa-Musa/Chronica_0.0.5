from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed
from flask_migrate import Migrate
from flask_socketio import SocketIO, emit
from flask_mail import Mail
from flask_mail import Message as MailMessage
from flask import current_app as app
import os
from datetime import datetime

def time_ago(timestamp):
    if timestamp is None:
        return "Unknown"  # or any default message you'd like
    now = datetime.utcnow()
    diff = now - timestamp

    if diff.days >= 365:
        years = diff.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"
    elif diff.days >= 1:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JoeJames'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # For Gmail
app.config['MAIL_PORT'] = 587  # Use 465 for SSL, 587 for TLS
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'inioluwamusa3@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'narutoanimequest2'  # Your email password or app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'inioluwamusa3@gmail.com'
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

socketio = SocketIO(app)
mail = Mail(app)

class DirectMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

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

post_likes = db.Table('post_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image = FileField('Post Image')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    likes = db.relationship('User', secondary=post_likes, backref='liked_posts', lazy='dynamic')

    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan', lazy=True)
    user = db.relationship('User', lazy=True)
    def like(self, user):
        if not self.is_liked_by(user):
            self.likes.append(user)

    def dislike(self, user):
        if self.is_liked_by(user):
            self.likes.remove(user)

    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return self.likes.filter(post_likes.c.user_id == user.id).count() > 0
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

comment_likes = db.Table(
    'comment_likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.id'), primary_key=True)
)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship(
        'User',
        secondary=comment_likes,
        backref=db.backref('liked_comments', lazy='dynamic'),
        lazy='dynamic'
    )

    """ post = db.relationship('Post', backref=db.backref('comments', lazy=True)) """
    user = db.relationship('User', backref='comments')
    def like(self, user):
        if not self.is_liked_by(user):
            self.likes.append(user)

    def dislike(self, user):
        if self.is_liked_by(user):
            self.likes.remove(user)
            
    def is_liked_by(self, user):
        if not user.is_authenticated:
            return False
        return self.likes.filter(comment_likes.c.user_id == user.id).count() > 0

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
    profile_image = db.Column(db.String(150), nullable=False, default='default.jpg')
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
    description = db.Column(db.String(200), nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    messages = db.relationship('Message', backref='chatroom', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chatroom_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

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
    quantity = 20  # Set the initial quantity of posts to load
    posts = Post.query.paginate(page=1, per_page=quantity, error_out=False).items
    return render_template('home.html', posts=posts)

def send_welcome_email(user_email):
    # Create the email message
    msg = MailMessage(
                subject="Welcome to FaceBlog!",
                recipients=[user_email]
            )
    msg.body = "Thank you for registering with FaceBlog. We are happy to have you!"
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
        send_welcome_email(form.email.data)
        return redirect(url_for('profile1'))  # Send email to the user who just registered
        
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
    categories = Category.query.filter(Category.name.contains(query)).all()
    return render_template('search_results.html', posts=posts, users=users, chatrooms=chatrooms, categories=categories)

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

@app.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    if not post.is_liked_by(current_user):
        post.like(current_user)
        db.session.commit()
        flash('You liked the post!', 'success')
    else:
        flash('You already liked this post.', 'info')
    return redirect(url_for('home', post_id=post_id))

@app.route("/post/<int:post_id>/dislike", methods=['POST'])
@login_required
def dislike_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.is_liked_by(current_user):
        post.dislike(current_user)
        db.session.commit()
        flash('You disliked the post.', 'info')
    else:
        flash('You haven’t liked this post yet.', 'info')
    return redirect(url_for('home', post_id=post_id))

@app.route("/comment/<int:comment_id>/like", methods=["POST"])
@login_required
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.is_liked_by(current_user):
        comment.like(current_user)
        db.session.commit()
    return redirect(url_for("post", post_id=comment.post_id))

@app.route("/comment/<int:comment_id>/dislike", methods=["POST"])
@login_required
def dislike_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.is_liked_by(current_user):
        comment.dislike(current_user)
        db.session.commit()
    return redirect(url_for("post", post_id=comment.post_id))


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
        description = request.form['description']
        new_chatroom = ChatRoom(name=name, description=description)
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

@app.route('/settings/dms', methods=['GET'])
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

@app.route("/settings/profile-edit", methods=['GET', 'POST'])
@login_required
def profile1():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.bio = form.bio.data
        current_user.social_links = form.social_links.data

        # Handle file upload
        file = request.files.get('profile_image')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            current_user.profile_image = filename  # Update database with the filename

        db.session.commit()
        flash('Your settings have been updated!', 'success')
        return redirect(url_for('profile1'))

    elif request.method == 'GET':
        form.bio.data = current_user.bio
        form.social_links.data = current_user.social_links

    return render_template('settings.html', form=form, user=current_user)

@app.route("/settings/my-posts", methods=['GET', 'POST'])
@login_required
def myposts():
    posts = Post.query.filter_by(author=current_user).all()
    return render_template('settings_posts.html', posts=posts, user=current_user)

""" @app.route("/settings/password", methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password, form.old_password.data):
            hashed_password = generate_password_hash(form.new_password.data)
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('settings'))
        else:
            flash('Incorrect current password.', 'danger')
    return render_template('change_password.html', form=form) """

@app.route("/load_posts/<int:page>/<int:quantity>")
def load_posts(page, quantity):
    if page < 1 or quantity < 1:
        return {'error': 'Invalid page or quantity'}, 400

    posts = Post.query.paginate(page=page, per_page=quantity, error_out=False).items
    posts_data = []
    for post in posts:
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': {
                'username': post.author.username,
                'image_file': post.author.image_file
            },
            'likes_count': post.likes.count()
        })
    return {'posts': posts_data}

@app.template_filter('time_ago')
def time_ago_filter(timestamp):
    return time_ago(timestamp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)

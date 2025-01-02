chatrooms.html:

{% extends "base.html" %}

{% block content %}
<div class="container mt-4 jqw">
    <h2 class="text-center">Available Chatrooms</h2>
    
    <!-- Check if there are any chatrooms available -->
    {% if chatrooms %}
        <ul class="list-group mt-3">
            <!-- Loop through each chatroom and display its details -->
            {% for chatroom in chatrooms %}
                <li class="list-group-item d-flex justify-content-between align-items-center">
                    <div>
                        <h5>{{ chatroom.name }}</h5>
                        <p>{{ chatroom.description }}</p>
                    </div>
                    <a href="{{ url_for('chatrooms', chatroom_id=chatroom.id) }}" class="btn btn-primary">
                        Join Chatroom
                    </a>
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <!-- If no chatrooms are available -->
        <div class="alert alert-warning mt-3 joe" role="alert">
            No chatrooms available. Please create one!
        </div>
    {% endif %}

    <!-- Button to create a new chatroom -->
    <a href="{{ url_for('create_chatroom') }}" class="btn btn-success mt-4">Create New Chatroom</a>
</div>
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

home.html:

{% extends "base.html" %}
{% block content %}
    <h1>Latest Posts</h1>
    {% for post in posts %}
        <article>
            <img src="{{ url_for('static', filename='images/' + post.author.image_file) }}" alt="Profile Image" style="width:50px; height:50px; border-radius:50%;">
            <h2>{{ post.title }}</h2>
            <p>{{ post.content[:100] }}...</p>
            <p><strong>Posted by: {{ post.author.username }}</strong></p>
            <a href="{{ url_for('post', post_id=post.id) }}">Read more</a>
        </article>
    {% endfor %}
    <p>{{a}}</p>
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

post.html:

{% extends "base.html" %}
{% block content %}
    <h1>{{ post.title }}</h1>
    <img src="{{ url_for('static', filename='images/' + post.user.image_file) }}" alt="Profile Image" style="width:50px; height:50px; border-radius:50%;">
    <p><strong>Posted by: {{ post.user.username }}</strong></p>
    <p>{{ post.content }}</p>
    {% if post.image_file %}
        <img src="{{ url_for('static', filename='images/' + post.image_file) }}" alt="Post Image">
    {% endif %}
    <h2>Comments:</h2>
    {% for comment in comments %}
        <div>
            <img src="{{ url_for('static', filename='images/' + comment.user.image_file) }}" alt="Profile Image" style="width:50px; height:50px; border-radius:50%;">
            <strong>{{ comment.user.username }}</strong>
            <p>{{ comment.content }}</p>
            {% if comment.user != current_user %}
                <form action="{{ url_for('like_comment', comment_id=comment.id) }}" method="POST" class="OO" style="display: inline-block;">
                    <button type="submit" class="A1" id="A1">Like</button>
                </form>
                <form action="{{ url_for('dislike_comment', comment_id=comment.id) }}" method="POST" class="OO" style="display: inline-block;">
                    <button type="submit" class="A1" id="A2">Dislike</button>
                </form>
                <p>Likes: {{ comment.likes }}</p>
            {% else %}
                <p>Likes: {{ comment.likes }}</p>
            {% endif %}
        </div>
    {% else %}
        <p>No comments yet.</p>
    {% endfor %}

<h4>Leave a Comment:</h4>
<form method="POST">
    {{ form.hidden_tag() }}
    {{ form.content.label }} {{ form.content(col=30, rows=5) }}<br>
    {{ form.submit() }}
</form>
<a href="{{ url_for('edit_post', post_id=post.id) }}">Edit Post</a>
<form action="{{ url_for('delete_post', post_id=post.id) }}" method="POST">
    <button type="submit" style="background-color: red; border-radius: 4px; border: none; padding: 4px; padding-left: 8px; padding-right: 8px;  color: white; font-family: 'Courier New', Courier, monospace;">Delete Post</button>
</form>
<script>
    x = 0
    for (x != 0;;) {
        if (document.getElementById('A1').onclick = true) {
            document.getElementById('A1').disabled = true;
            document.getElementById('A2').disabled = false;
        }
        
        if (document.getElementById('A2').onclick = true) {
            document.getElementById('A1').disabled = false;
            document.getElementById('A2').disabled = true;
        }
    }

</script>
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

login.html:

{% extends "base.html" %}
{% block content %}
    <h2>Login</h2>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.email.label }} {{ form.email(size=32) }}<br>
        {{ form.password.label }} {{ form.password(size=32) }}<br>
        {{ form.submit() }}
    </form>
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

register.html:

{% extends "base.html" %}
{% block content %}
    <h2>Register</h2>
    <form method="POST">
        {{ form.hidden_tag() }}
        {{ form.username.label }} {{ form.username(size=32) }}<br>
        {{ form.email.label }} {{ form.email(size=32) }}<br>
        {{ form.password.label }} {{ form.password(size=32) }}<br>
        {{ form.confirm_password.label }} {{ form.confirm_password(size=32) }}<br>
        {{ form.submit() }}
    </form>
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

chatroom.html:

{% extends "base.html" %}

{% block content %}
<div class="container mt-4">
    <h2>{{ chatroom.name }}</h2>
    <p>{{ chatroom.description }}</p>

    <div class="messages">
        {% for message in messages %}
            <div class="message">
                <strong>{{ message.user.username }}:</strong> {{ message.content }}
            </div>
        {% else %}
            <div class="alert alert-info">No messages yet.</div>
        {% endfor %}
    </div>

    <form action="{{ url_for('send_message', chatroom_id=chatroom.id) }}" method="POST">
        <div class="form-group">
            <textarea name="content" class="form-control" placeholder="Type your message..." required></textarea>
        </div>
        <button type="submit" class="btn btn-primary" style="background-color: green; border: none; border-radius: 4px; color: white; padding: 5px;">Send</button>
    </form>
</div>
<script>
    const socket = io();

    socket.on('connect', function() {
        console.log("Connected to the chatroom!");
    });

    // Send message to the server
    function sendMessage() {
        const messageInput = document.getElementById('message');
        const msg = messageInput.value;
        socket.emit('send_message', {
            'message': msg,
            'chatroom_id': {{ chatroom.id }}
        });
        messageInput.value = '';  // Clear the input field
    }

    // Listen for new messages
    socket.on('receive_message', function(data) {
        const chatBox = document.getElementById('chat-box');
        chatBox.innerHTML += `<p><strong>${data.username}:</strong> ${data.message}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto scroll to the bottom
    });
</script>
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

category.html:

{% extends "base.html" %}

{% block title %}Posts in {{ category.name }}{% endblock %}

{% block content %}
<h1>Posts in {{ category.name }}</h1>
{% for post in posts %}
    <div class="post">
        <h2><a href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
        <p>{{ post.content }}</p>
    </div>
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
                {% if chatroom %}
                    <a href="{{ url_for('chatrooms', chatroom_id=chatroom.id) }}">Chatrooms</a>
                {% else %}
                    <a href="{{ url_for('all_chatrooms') }}">Chatrooms</a>
                {% endif %}
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

create_chatroom.html:

{% extends "base.html" %}
<head>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
</head>

{% block title %}Create Chat Room{% endblock %}

{% block content %}
<h1>Create Chat Room</h1>
<form method="POST"  class="ja">
    <div>
        <label for="name" class="la">Chat Room Name:</label>
        <input type="text" name="name" required class="la2">
    </div>
    <button type="submit" class="la3">Create</button>
</form>
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

create_post.html:

{% extends "base.html" %}
{% block content %}
    <h2>Create New Post</h2>
    <form method="POST" enctype="multipart/form-data">
        {{ form.hidden_tag() }}
        {{ form.title.label }} {{ form.title(size=32) }}<br>
        {{ form.content.label }} {{ form.content(cols=50, rows=10) }}<br>
        {{ form.category.label }} {{ form.category() }}<br>
        {{ form.submit() }}
    </form>
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

edit_comment.html:

{% extends "base.html" %}

{% block title %}Edit Post{% endblock %}

{% block content %}
<h1>Edit Comment</h1>
<form method="POST">
    {{ form.hidden_tag() }}
    <div>
        {{ form.title.label }} {{ form.title(size=32) }}
    </div>
    <div>
        {{ form.content.label }} {{ form.content(cols=30, rows=10) }}
    </div>
    <button type="submit">Update Comment</button>
</form>

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

edit_post.html:

{% extends "base.html" %}

{% block title %}Edit Post{% endblock %}

{% block content %}
<h1>Edit Post</h1>
<form method="POST">
    {{ form.hidden_tag() }}
    <div>
        {{ form.title.label }} {{ form.title(size=32) }}
    </div>
    <div>
        {{ form.content.label }} {{ form.content(cols=30, rows=10) }}
    </div>
    <button type="submit"><a href="{{ url_for('post', post_id=post.id, form=form, post=post) }}" style="text-decoration: none;">Update Post</a></button>
</form>

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

edit_profile.html:

{% extends "base.html" %}
{% block content %}
    <h1>Edit Profile</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div>
            {{ form.bio.label }}<br>
            {{ form.bio(size=32) }}<br>
            {% for error in form.bio.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </div>
        <div>
            {{ form.social_links.label }}<br>
            {{ form.social_links(size=32) }}<br>
            {% for error in form.social_links.errors %}
                <span style="color: red;">[{{ error }}]</span>
            {% endfor %}
        </div>
        <div>
            {{ form.submit() }}
        </div>
    </form>
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
    <a href="{{ url_for('edit_profile', username=user.username) }}">Edit Profile</a>
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

search_results.html:

{% extends "base.html" %}

{% block title %}Search Results{% endblock %}

{% block content %}
<h1>Search Results</h1>
<h2>Posts</h2>
{% for post in posts %}
    <div class="post">
        <h3><a href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h3>
        <p>{{ post.content }}</p>
    </div>
{% endfor %}
<h2>Users</h2>
{% for user in users %}
    <div class="user">
        <h3><a href="{{ url_for('profile', username=user.username) }}">{{ user.username }}</a></h3>
    </div>
{% endfor %}
<h2>Chatrooms</h2>
{% for chatroom in chatrooms %}
    <div class="chatroom">
        <h3>
            <a href="{{ url_for('chatrooms', chatroom_id=chatroom.id) }}">
                {{chatroom.name}}
            </a>
        </h3>
    </div>
{% endfor %}
<!-- {% for post in posts %}
    <h2>Posts in {{ post.category_id }}</h2>
    {% for post in posts %}
        <div class="post">
            <h2><a href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h2>
            <p>{{ post.content }}</p>
        </div>
    {% endfor %}
{% endfor %}     -->
<!-- <h2>Categories</h2>
{% for category in categories %}
    <div class="post">
        <h3><a href="{{ url_for('post', post_id=post.id) }}">{{ post.title }}</a></h3>
        <p>{{ post.content }}</p>
    </div>
{% endfor %} -->
{% with messages = get_flashed_messages(with_categories=True) %}
        {% if messages %}
            <ul>
            {% for post, message in messages %}
                <li class="{{ category }}">{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
{% endblock %}

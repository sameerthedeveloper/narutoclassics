from flask import Flask, render_template, request, redirect, url_for, session
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def read_video_links():
    video_links = []
    with open('naruto.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            video_links.append({"title": row[0], "url": row[1]})
    return video_links
# Function to read episodes from CSV
def read_episodes():
    with open('naruto.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        return list(reader)

# Function to read users from CSV
def read_users():
    with open('users.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

@app.route('/home')
def index():
    if 'username' in session:
        episodes = read_episodes()
        return render_template('index.html', episodes=episodes)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        for user in users:
            if user['username'] == username and user['password'] == password:
                session['username'] = username
                return redirect(url_for('index'))  # Redirect to home page upon successful login
        return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/movie/<episode_id>')
def movie(episode_id):
    episodes = read_episodes()
    selected_episode = None
    related_episodes = []
    for episode in episodes:
        if episode[0] == episode_id:
            selected_episode = episode
        else:
            related_episodes.append(episode)
    return render_template('movie.html', selected_episode=selected_episode, related_episodes=related_episodes)

@app.route('/video/<title>/<path:url>')
def video_page(title, url):
    related_videos = read_video_links()
    return render_template('video_page.html',video_title=title,video_url=url,related_videos=related_videos)


# Function to write a new user to the CSV file
def write_user(username, password):
    with open('users.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username already exists
        users = read_users()
        for user in users:
            if user['username'] == username:
                return render_template('register.html', error='Username already exists')
        # Write the new user to the CSV file
        write_user(username, password)
        session['username'] = username
        return redirect(url_for('login'))  # Redirect to home page upon successful registration
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

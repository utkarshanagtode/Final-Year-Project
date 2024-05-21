from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap

# Routes
from user import routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/test')
def test():
    with app.app_context():
        return render_template('test.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/widgets')
def widgets():
    return render_template('widgets.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/match_pred')
def match_pred():
    return render_template('match_pred.html')  # Assuming your Streamlit app runs on localhost:8501

@app.route('/team_stats')
def team_stats():
    return render_template('team_stats.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about_us_login')
def about_us_login():
    return render_template('about_us_login.html')

@app.route('/contact_login')
def contact_login():
    return render_template('contact_login.html')



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

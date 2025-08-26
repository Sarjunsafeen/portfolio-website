from flask import Flask, render_template, url_for, request, redirect, flash
import os
from flask_mail import Mail, Message
from email.utils import formataddr
import threading

app = Flask(__name__)
app.secret_key = "yoursupersecretkey"

# 🔹 Flask-Mail Config
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your_mail@gmail.com"   # Your Gmail
app.config["MAIL_PASSWORD"] = "YOUR_APP_PASSWORD"          # App Password
app.config["MAIL_DEFAULT_SENDER"] = formataddr(("Portfolio Website", "your_mail@gmail.com"))

mail = Mail(app)

# 🔹 Async Email Function
def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
            print("✅ Email sent successfully")
        except Exception as e:
            print("❌ Email sending failed:", e)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        user_message = request.form.get('message')

        # 🔹 Build Email (Plain + HTML)
        msg = Message(
            subject=f"📩 New message from {name} - Portfolio",
            recipients=["your_mail@gmail.com"],
        )

        # Fallback plain text
        msg.body = f"""
You have received a new message from your Portfolio Website:

👤 Name: {name}
📧 Email: {email}

💬 Message:
{user_message}
        """

        # HTML version
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #2c3e50;">📩 New Contact Message</h2>
            <p><strong>👤 Name:</strong> {name}</p>
            <p><strong>📧 Email:</strong> {email}</p>
            <p><strong>💬 Message:</strong></p>
            <blockquote style="background: #f9f9f9; padding: 10px; border-left: 4px solid #3498db; margin: 10px 0;">
                {user_message}
            </blockquote>
            <p style="color: #999; font-size: 12px;">This email was sent from your <strong>Portfolio Website</strong>.</p>
        </div>
        """

        # 🔹 Send email in background
        threading.Thread(target=send_async_email, args=(app, msg)).start()

        flash("✅ Your message has been sent successfully!")
        return redirect(url_for("home"))

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

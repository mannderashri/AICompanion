import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from groq import Groq
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Load environment variables
load_dotenv()

def send_otp_email(receiver_email, otp):
      """Sends a real-world email via SMTP with automatic demo fallback."""
      sender_email = os.getenv("MAIL_USERNAME")
      sender_password = os.getenv("MAIL_PASSWORD")

    # Automatic Demo Fallback if credentials are missing
      if not sender_email or "your_email" in sender_email:
                print(f"\n[DEMO MODE] OTP for {receiver_email} is: {otp}\n")
                return "demo" # Special signal for demo mode

      try:
                msg = MIMEMultipart()
                msg['From'] = f"AI Tutor Agent <{sender_email}>"
                msg['To'] = receiver_email
                msg['Subject'] = f"{otp} is your verification code"

        body = f"""
                <div style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; max-width: 500px; margin: auto; padding: 40px; border: 1px solid #eee; border-radius: 10px;">
                            <h2 style="color: #202124; text-align: center;">Identity Verification</h2>
                                        <p style="font-size: 16px; color: #5f6368; text-align: center;">Please use the following code to complete your login to AI Tutor Agent.</p>
                                                    <div style="background: #f8f9fa; border-radius: 8px; padding: 20px; text-align: center; margin: 30px 0;">
                                                                    <span style="font-size: 32px; font-weight: bold; letter-spacing: 8px; color: #1a73e8;">{otp}</span>
                                                                                </div>
                                                                                            <p style="font-size: 14px; color: #5f6368; text-align: center;">This code will expire in 10 minutes. If you didn't request this code, you can safely ignore this email.</p>
                                                                                                        <div style="border-top: 1px solid #eee; margin-top: 30px; padding-top: 20px; text-align: center; font-size: 12px; color: #9aa0a6;">
                                                                                                                        AI Tutor Agent - Advanced Adaptive Learning
                                                                                                                                    </div>
                                                                                                                                            </div>
                                                                                                                                                    """
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
except Exception as e:
        print(f"[SMTP ERROR] {e}. Falling back to terminal.")
        print(f"\n[DEMO MODE] OTP for {receiver_email} is: {otp}\n")
        return "demo"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "ai_tutor_secret_key_123")

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ai_tutor_core.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
      id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    quizzes = db.relationship('QuizResult', backref='user', lazy=True)
    exams   = db.relationship('ExamResult', backref='user', lazy=True)
    chats   = db.relationship('ChatLog',    backref='user', lazy=True)

# Quiz Results Model
class QuizResult(db.Model):
      id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Intege

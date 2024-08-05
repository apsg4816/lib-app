# tasks.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import csv
from io import StringIO
from datetime import datetime,timedelta
from celery_config import celery
from app import db, Section, User, Book, RequestBook
from celery.schedules import crontab

def calculate_book_status_totals(books):
            total_approved = 0
            total_returned = 0
            total_rejected = 0

            for book in books:
                if book.ReqStatus == 'Approved':
                    total_approved += 1
                elif book.ReqStatus == 'Returned':
                    total_returned += 1
                elif book.ReqStatus == 'Rejected':
                    total_rejected += 1

            return total_approved, total_returned, total_rejected



def generate_monthly_report():
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    users = User.query.filter_by(role='END_USER').all()  

    
    
@celery.task
def generate_monthly_report():
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year
    users = User.query.filter_by(role='END_USER').all()  
    
    for user in users:
        books_requested = RequestBook.query.filter_by(user_name=user.user_name).all()
        total_books_requested = len(books_requested)

        total_approved, total_returned, total_rejected = calculate_book_status_totals(books_requested)

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Monthly Reading Report</title>
        </head>
        <body>
            <h1>Monthly Reading Report - { current_month } { current_year }</h1>
            <p>Hello { user.First_Name },</p>
            <p>Here's your book reading summary for the month of {current_month } { current_year }:</p>
            <ul>
                <li>Total Books Requested: { total_books_requested }</li>
                <li>Total Books Approved: { total_approved }</li>
                <li>Total Books Returned: { total_returned }</li>
                <li>Total Books Rejected: { total_rejected }</li>
            </ul>
            <p>Keep Reading ...Keep Growing!</p>
            <p>Best regards,</p>
            <p>Library Team</p>
        </body>
        </html>
        """
        send_email(user.email, "Monthly Reading Report", html_content)


def send_email(to_email,subject, html_content):
    from_email = 'apsg4816@gmail.com'
    subject = subject

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    part1 = MIMEText(html_content, 'html')
    msg.attach(part1)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'apsg4816@gmail.com'
    smtp_password = 'tkuiumvrgthlqvkb'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())

@celery.task
def daily_request_reminder():
    users=User.query.filter_by(role ='END_USER').all()
    for user in users:
        reminder_time=datetime.now()-timedelta(days=1)
        requests=RequestBook.query.filter_by(user_name=user.user_name).filter(RequestBook.ReqdateTime <= reminder_time).all()

        if  requests:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Daily Request Reminder</title>
            </head>
            <body>
                <h1>Daily Request Reminder </h1>
                <p>Hello {user.First_Name},</p>
                <p>You have not requested any book in last 24 hours.
                    We have some very exciting books on {user.Interests}.
                  Please request books to increase your knowledge:</p>
                <p>Keep Reading ...Keep Growing!</p>
                <p>Best regards,</p>
                <p>Library Team</p>
            </body>
            </html>
            """
            send_email(user.email,'Book Request Reminder', html_content)


@celery.task
def export_books_details_as_csv():
    books = Book.query.all()

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(["ForSection","Book_Title", "Author"])

    for book in books:
        csv_writer.writerow([
            book.ForSection,
            book.Book_Title,
            book.Author,
            
        ])

    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, "csv/book_report.csv")
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_buffer.getvalue())

    return csv_buffer.getvalue()


# User Book request data export
@celery.task
def export_user_books_details_as_csv(user_name):
    Rbooks = RequestBook.query.filter(RequestBook.user_name == user_name).all()

    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow([ "user_name","Section_Title","Book_Title", "NDays", "Requested_DateTime","Due_DateTime","Request_Status"])

    for book in Rbooks:
        csv_writer.writerow([
            book.user_name,
            book.Section_Title,
            book.Book_Title,
            book.Ndays,
            book.ReqdateTime,
            book.ReqStatus,
        ])

    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, "csv/user_book_report.csv")
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_buffer.getvalue())

    return csv_buffer.getvalue()
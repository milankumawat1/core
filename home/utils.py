from home.models import Person
from django.conf import settings
import time
from django.core.mail import send_mail

def run_this_function():
    print("Running this function")
    time.sleep(2)
    print("Done")

def send_email_to_client(student=None, marks=None, total_marks=None, current_rank=None):
    subject = "Here is the Report Card"
    
    # Create email message with report card details
    message = f"""
Dear {student.student_name},

Here is your report card:

Student ID: {student.student_id.student_id}
Department: {student.department.department}
Email: {student.student_email}

Subject-wise Marks:
"""
    
    # Add marks for each subject
    for mark in marks:
        message += f"\n{mark.subject.subject_name}: {mark.marks}"
    
    # Add total marks and rank
    message += f"""
    
Total Marks: {total_marks['total_marks']}
Current Rank: {current_rank}

Best regards,
School Administration
"""
    
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["milankumawat01@gmail.com"]  # Send to student's email
    send_mail(subject, message, from_email, recipient_list)

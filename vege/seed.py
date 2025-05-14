from faker import Faker
import random
from .models import *
from django.db.models import Sum
from datetime import datetime

fake=Faker()

def create_subject_marks(n):
    try:
        student_objs=Student.objects.all()
        for student in student_objs:
            subjects=Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject=subject,
                    student=student,
                    marks=random.randint(0,100)
                )
    except Exception as e:
        print(e)

def generate_report_card():
    try:
        # Delete existing report cards
        ReportCard.objects.all().delete()
        
        # Get all students with their total marks
        ranks = Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks', '-student_age')
        
        # Create new report cards
        for i, rank in enumerate(ranks, 1):
            ReportCard.objects.create(
                student=rank,
                student_rank=i,
                date_of_report_card_generation=datetime.now().date()
            )
    except Exception as e:
        print(f"Error generating report cards: {e}")

def seed_db(n=10)->None:
    try:
        for i in range(0,n):
            department_objs=Department.objects.all()
            random_index=random.randint(0,len(department_objs)-1)
            department=department_objs[random_index]
            student_id=f'STU-0{random.randint(100,999)}'
            student_name=fake.name()
            student_email=fake.email()
            student_age=random.randint(18,25)
            student_address=fake.address()
            
            student_id_obj=StudentID.objects.create(student_id=student_id)

            student_obj=Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
                is_fake=True  # Mark as fake record
            )
    except Exception as e:
        print(e)
    

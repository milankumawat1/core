from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from home.utils import send_email_to_client
from django.db.models import Q, Sum
from django.core.exceptions import PermissionDenied
import random
from datetime import datetime

# Create your views here.

def send_email(request):
    # Get student_id from the URL parameters
    student_id = request.GET.get('student_id')
    
    # Get the student's marks and details
    queryset = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    
    total_marks = queryset.aggregate(total_marks=Sum('marks'))
    current_rank = queryset.first().student.reportcard_set.first().student_rank
    date_of_report_card_generation = queryset.first().student.reportcard_set.first().date_of_report_card_generation
    student = queryset.first().student
    
    try:
        send_email_to_client(
            student=student,
            marks=queryset,
            total_marks=total_marks,
            current_rank=current_rank
        )
        messages.success(request, 'Report card has been sent to the student\'s email')
    except Exception as e:
        messages.error(request, f'Failed to send email: {str(e)}')
    
    # Stay on the same page by rendering the see_marks template
    context = {
        'marks': queryset,
        'total_marks': total_marks,
        'student': student,
        'current_rank': current_rank,
        'date_of_report_card_generation': date_of_report_card_generation
    }
    return render(request, 'report/see_marks.html', context)

@login_required(login_url='/login/')
def see_marks(request, student_id):
    # Get the student's marks
    queryset = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    
    if not queryset.exists():
        messages.error(request, 'No marks found for this student')
        return redirect('/students/')
    
    student = queryset.first().student
    
    # Check if the logged-in user is the same as the student OR is a superuser
    if request.user.email != student.student_email and not request.user.is_superuser:
        messages.error(request, 'You can only view your own report card')
        return redirect('/students/')
    
    total_marks = queryset.aggregate(total_marks=Sum('marks'))
    current_rank = queryset.first().student.reportcard_set.first().student_rank
    date_of_report_card_generation = queryset.first().student.reportcard_set.first().date_of_report_card_generation
    
    context = {
        'marks': queryset,
        'total_marks': total_marks,
        'student': student,
        'current_rank': current_rank,
        'date_of_report_card_generation': date_of_report_card_generation,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'report/see_marks.html', context)

@login_required(login_url='/login/')
def get_student(request):
    # Show all students
    queryset = Student.objects.all()
    
    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            Q(student_name__icontains=search) | 
            Q(department__department__icontains=search) | 
            Q(student_id__student_id__icontains=search) | 
            Q(student_email__icontains=search) 
        )

    # Get current user's student data if not superuser
    current_student = None
    if not request.user.is_superuser:
        try:
            current_student = Student.objects.get(student_email=request.user.email)
        except Student.DoesNotExist:
            pass

    paginator = Paginator(queryset, 10)  # Show 10 students per page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'students': page_obj,
        'user': request.user,  # Pass the entire user object to template
        'current_student': current_student  # Pass the current user's student data
    }
    return render(request, 'report/students.html', context)

@login_required(login_url='/login/')
def Recipies(request):
    if request.method == 'POST':
        data=request.POST
        recipie_image=request.FILES.get('recipie_image')

        recipie_name=data.get('recipie_name')
        recipie_description=data.get('recipie_description')
        print(recipie_name, recipie_description)

        Recipie.objects.create(
            recipie_name=recipie_name,
            recipie_description=recipie_description,
            recipie_image=recipie_image
        )
        return redirect('/recipies/')

    queryset=Recipie.objects.all()

    if request.GET.get('search'):
        queryset=queryset.filter(recipie_name__icontains=request.GET.get('search'))



    
    context={'recipies':queryset}
    return render(request, 'recipies.html', context)

def delete_recipie(request, id):
    queryset=Recipie.objects.get(id=id)
    queryset.delete()
    return redirect('/recipies/')




@login_required(login_url='/login/')
def update_recipie(request, id):
    queryset=Recipie.objects.get(id=id)

    if request.method == 'POST':
        data=request.POST
        recipie_image=request.FILES.get('recipie_image')

        recipie_name=data.get('recipie_name')
        recipie_description=data.get('recipie_description')

        queryset.recipie_name=recipie_name
        queryset.recipie_description=recipie_description

        if recipie_image:
            queryset.recipie_image=recipie_image

        queryset.save()
        return redirect('/recipies/')
        
        
    context={'recipie':queryset}
    return render(request, 'update_recipie.html', context)


def login_page(request):
    if request.method == 'POST':
        data=request.POST
        username=data.get('username')
        password=data.get('password')
        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')

        user=authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        
        else:
            login(request, user)
            return redirect('/students/')

    return render(request, 'login.html')


def logout_page(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('/login/')



def generate_student_id():
    # Generate a unique student ID (e.g., STU2024001)
    year = datetime.now().year
    last_student = StudentID.objects.order_by('-student_id').first()
    if last_student:
        last_number = int(last_student.student_id.split('STU')[1])
        new_number = last_number + 1
    else:
        new_number = 1
    return f"STU{year}{new_number:03d}"

def generate_marks(student, subjects):
    marks = []
    for subject in subjects:
        mark = random.randint(60, 100)  # Generate random marks between 60 and 100
        marks.append(SubjectMarks.objects.create(
            student=student,
            subject=subject,
            marks=mark
        ))
    return marks

def calculate_rank():
    # Get all students and their total marks
    students = Student.objects.all()
    for student in students:
        total_marks = SubjectMarks.objects.filter(student=student).aggregate(total=Sum('marks'))['total']
        if total_marks:
            # Update or create report card
            report_card, created = ReportCard.objects.get_or_create(
                student=student,
                defaults={
                    'student_rank': 1,  # Will be updated
                    'date_of_report_card_generation': datetime.now()
                }
            )
            report_card.total_marks = total_marks
            report_card.save()
    
    # Calculate ranks based on total marks
    report_cards = ReportCard.objects.all().order_by('-total_marks')
    for index, report_card in enumerate(report_cards, 1):
        report_card.student_rank = index
        report_card.save()

def register_page(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already taken')
            return redirect('/register/')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('/register/')
        
        try:
            # Create user
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email
            )
            user.set_password(password)
            user.save()
            
            # Generate student ID
            student_id = generate_student_id()
            student_id_obj = StudentID.objects.create(student_id=student_id)
            
            # Get or create a default department (you can modify this as needed)
            department, _ = Department.objects.get_or_create(
                department="Computer Science",
                defaults={'department_name': "Computer Science Department"}
            )
            
            # Create student record
            student = Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=f"{first_name} {last_name}",
                student_email=email,
                student_age=18,  # Default age
                student_address="Not specified",  # Default address
                is_fake=False  # Mark as real record
            )
            
            # Get all subjects and generate marks
            subjects = Subject.objects.all()
            if not subjects.exists():
                # Create default subjects if none exist
                subjects = [
                    Subject.objects.create(subject_name="Mathematics"),
                    Subject.objects.create(subject_name="Physics"),
                    Subject.objects.create(subject_name="Computer Science"),
                    Subject.objects.create(subject_name="English")
                ]
            
            # Generate marks for the student
            generate_marks(student, subjects)
            
            # Calculate and update ranks
            calculate_rank()
            
            messages.success(request, 'Account created successfully with student record')
            return redirect('/login/')
            
        except Exception as e:
            # If anything fails, clean up and show error
            if user:
                user.delete()
            if student_id_obj:
                student_id_obj.delete()
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect('/register/')

    return render(request, 'register.html')

def delete_all_students(request):
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators can perform this action')
        return redirect('/students/')
    
    try:
        # Delete all related records first
        SubjectMarks.objects.all().delete()
        ReportCard.objects.all().delete()
        Student.objects.all().delete()
        StudentID.objects.all().delete()
        
        messages.success(request, 'All student records have been deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting records: {str(e)}')
    
    return redirect('/students/')

def generate_fake_students(request):
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators can perform this action')
        return redirect('/students/')
    
    try:
        # Import the seed function
        from .seed import seed_db, create_subject_marks, generate_report_card
        
        # Generate 200 students
        seed_db(200)
        
        # Create subject marks for all students
        create_subject_marks(200)
        
        # Generate report cards
        generate_report_card()
        
        messages.success(request, 'Successfully generated 200 fake student records')
    except Exception as e:
        messages.error(request, f'Error generating fake data: {str(e)}')
    
    return redirect('/students/')

def delete_all_users(request):
    if not request.user.is_superuser:
        messages.error(request, 'Only administrators can perform this action')
        return redirect('/students/')
    
    try:
        # Delete all users except superusers
        User.objects.filter(is_superuser=False).delete()
        messages.success(request, 'All student accounts have been deleted. Students will need to register again.')
    except Exception as e:
        messages.error(request, f'Error deleting user accounts: {str(e)}')
    
    return redirect('/students/')

from django.urls import path
from . import views

urlpatterns = [
    path('see_marks/<student_id>', views.see_marks, name='see_marks'),
    path('send_email/', views.send_email, name='send_email'),
    path('cleanup_subjects/', views.cleanup_subjects, name='cleanup_subjects'),
] 
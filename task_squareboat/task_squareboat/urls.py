from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('create-job/', views.create_job, name='create_job'),
    path('list-jobs/', views.list_jobs, name='list_jobs'),
    path('logout/', views.logout_view, name='logout'),
    path('apply-job/', views.apply_to_job, name='apply_to_job'),
    path('applied-jobs/', views.list_applied_jobs, name='list_applied_jobs'),
    path('job-applicants/', views.list_applicants_for_job, name='list_applicants_for_job'),

] 
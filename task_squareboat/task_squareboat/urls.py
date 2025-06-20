from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('create-job/', views.create_job, name='create_job'),
    path('list-jobs/', views.list_jobs, name='list_jobs'),

] 
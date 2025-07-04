from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Job, Application
User = get_user_model()

def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')
        if not email or not password or not role:
            return JsonResponse({'error': 'Email, password, and role are required.'}, status=400)
        if role not in ['recruiter', 'candidate']:
            return JsonResponse({'error': 'Invalid role.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'User already exists.'}, status=400)
        user = User.objects.create_user(username=email, email=email, password=password, role=role)
        return JsonResponse({'message': 'User registered successfully.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful.'})
        else:
            return JsonResponse({'error': 'Invalid credentials.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405) 

def create_job(request):
    if request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'recruiter':
            return JsonResponse({'error': 'Only recruiters can create jobs.'}, status=403)
        data = json.loads(request.body)
        job_title = data.get('job_title')
        job_description = data.get('job_description')
        if not job_title or not job_description:
            return JsonResponse({'error': 'job_title and job_description are required.'}, status=400)
        job = Job.objects.create(job_title=job_title, job_description=job_description)
        return JsonResponse({'message': 'Job created successfully.', 'job_id': job.id})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def list_jobs(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required.'}, status=401)
        jobs = Job.objects.all()
        jobs_data = [
            {
                'id': job.id,
                'job_title': job.job_title,
                'job_description': job.job_description
            } for job in jobs
        ]
        return JsonResponse({'jobs': jobs_data})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def logout_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'message': 'Logout successful.'})
        else:
            return JsonResponse({'error': 'No user is logged in.'}, status=401)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def apply_to_job(request):
    if request.method == 'POST':
        if not request.user.is_authenticated or request.user.role != 'candidate':
            return JsonResponse({'error': 'Only candidates can apply for jobs.'}, status=403)
        data = json.loads(request.body)
        job_id = data.get('job_id')
        if not job_id:
            return JsonResponse({'error': 'job_id is required.'}, status=400)
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return JsonResponse({'error': 'Job not found.'}, status=404)

        if Application.objects.filter(user=request.user, job=job).exists():
            return JsonResponse({'error': 'You have already applied to this job.'}, status=400)
        Application.objects.create(user=request.user, job=job)
        return JsonResponse({'message': 'Application submitted successfully.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

def list_applied_jobs(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required.'}, status=401)
        applications = Application.objects.filter(user=request.user).select_related('job')
        jobs_data = [
            {
                'id': app.job.id,
                'job_title': app.job.job_title,
                'job_description': app.job.job_description,
                'applied_at': app.applied_at.isoformat()
            } for app in applications
        ]
        return JsonResponse({'applied_jobs': jobs_data})
    return JsonResponse({'error': 'Invalid request method.'}, status=405) 

def list_applicants_for_job(request):
    if request.method == 'GET':
        if not request.user.is_authenticated or request.user.role != 'recruiter':
            return JsonResponse({'error': 'Only recruiters can view job applicants.'}, status=403)
        job_id = request.GET.get('job_id')
        if not job_id:
            return JsonResponse({'error': 'job_id is required as a query parameter.'}, status=400)
        applications = Application.objects.filter(job_id=job_id).select_related('user')
        applicants = [
            {
                'user_id': app.user.id,
                'username': app.user.username,
                'email': app.user.email,
                'applied_at': app.applied_at.isoformat()
            } for app in applications
        ]
        return JsonResponse({'applicants': applicants})
    return JsonResponse({'error': 'Invalid request method.'}, status=405) 

def my_jobs(request):
    if request.method == 'GET':
        if not request.user.is_authenticated or request.user.role != 'candidate':
            return JsonResponse({'error': 'Only candidates can view their applied jobs.'}, status=403)
        applications = Application.objects.filter(user=request.user).select_related('job')
        jobs_data = [
            {
                'id': app.job.id,
                'job_title': app.job.job_title,
                'job_description': app.job.job_description,
                'applied_at': app.applied_at.isoformat()
            } for app in applications
        ]
        return JsonResponse({'applied_jobs': jobs_data})
    return JsonResponse({'error': 'Invalid request method.'}, status=405) 
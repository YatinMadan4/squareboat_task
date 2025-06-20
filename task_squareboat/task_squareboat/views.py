from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

User = get_user_model()

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return JsonResponse({'error': 'Email and password required.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'User already exists.'}, status=400)
        user = User.objects.create_user(username=email, email=email, password=password)
        return JsonResponse({'message': 'User registered successfully.'})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            return JsonResponse({'message': 'Login successful.'})
        else:
            return JsonResponse({'error': 'Invalid credentials.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def create_job(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        job_title = data.get('job_title')
        job_description = data.get('job_description')
        if not job_title or not job_description:
            return JsonResponse({'error': 'job_title and job_description are required.'}, status=400)
        from .models import Job
        job = Job.objects.create(job_title=job_title, job_description=job_description)
        return JsonResponse({'message': 'Job created successfully.', 'job_id': job.id})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def list_jobs(request):
    if request.method == 'GET':
        from .models import Job
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

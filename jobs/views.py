from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm
from .models import Category, Industry
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt
import json
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth import login
from .forms import UserRegistrationForm
from django.contrib.auth.views import LoginView

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form':form})

class CustomLoginView(LoginView):
    template_name = 'login.html'

logger = logging.getLogger(__name__)
def job_search(request):
    query = request.GET.get('q', '')
    if query:
        jobs = Job.objects.filter(title__icontains=query)
    else:
        jobs = Job.objects.none()  # No jobs if no query is provided
    return render(request, 'jobs/job_search.html', {'jobs': jobs, 'query': query})

def job_categories_list(request):
    categories = Category.objects.all()
    return render(request, 'jobs/categories_list.html', {'categories': categories})

def job_industries_list(request):
    industries = Industry.objects.all()
    return render(request, 'jobs/industries_list.html', {'industries': industries})

def jobs_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    jobs = Job.objects.filter(category=category)
    return render (request, 'jobs/category.html', {'category':category, 'jobs':jobs})

def jobs_by_industry(request, industry_id):
    industry = get_object_or_404(Industry, id=industry_id)
    jobs = Job.objects.filter(industry=industry)
    return render (request, 'jobs/industry.html', {'industry': industry, 'jobs':jobs})


def home(request):
    return render(request, 'jobs/index.html')

def job_list(request):
    jobs = Job.objects.all()
    return render (request, 'jobs/job_list.html', {'jobs':jobs})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    # if request.method == 'POST':
    #     if request.user.is_authenticated:
    #         form = ApplicationForm(request.POST, request.FILES)
    #         if form.is_valid():
    #             application = form.save(commit=False)
    #             application.job = job
    #             application.applicant = request.user
    #             application.save()
    #             return redirect('job_list')  # Redirect to job list or a thank you page
    #     else:
    #         return redirect('login')  # Redirect to login page if not authenticated
    # else:
    #     form = ApplicationForm()
    # return render(request, 'jobs/job_detail.html', {'job': job, 'form': form})

    return render(request, 'jobs/job_detail.html', {'job': job})

    
@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user.employer
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})
        

# mpesa

@csrf_exempt
def stk_push_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info('Received STK Push request: %s', data)

            phone_number = data.get('phoneNumber')
            amount = data.get('amount', 1)  # Default to 1 if not provided
            account_reference = data.get('accountReference', 'reference')  # Default value
            transaction_desc = data.get('transactionDesc', 'Description')  # Default value
            callback_url = 'https://yourdomain.com/stk-push-callback/'  # Your callback URL

            cl = MpesaClient()
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

            logger.info('STK Push Response: %s', response)

            return JsonResponse({
                'success': True,
                'message': 'STK push initiated',
                "ResponseDescription": "Success. Request accepted for processing",  #should be serializable

                
            }, status=200)

        except Exception as e:
            logger.error('Error initiating STK Push: %s', str(e))
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=400)

# Callback View
def stk_push_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        logger.info('STK Push callback received: %s', data)
        # Process the callback data from Safaricom here
        return HttpResponse("STK Push callback received")


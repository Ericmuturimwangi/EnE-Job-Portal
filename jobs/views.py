from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm, ApplicationForm
from .models import Category, Industry
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
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
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.job = job
                application.applicant = request.user
                application.save()
                return redirect('job_list')  # Redirect to job list or a thank you page
        else:
            return redirect('login')  # Redirect to login page if not authenticated
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/job_detail.html', {'job': job, 'form': form})

    
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

# def index(request):
#     cl = MpesaClient()
#     # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
#     phone_number = '0720630112'
#     amount = 100
#     account_reference = 'reference'
#     transaction_desc = 'Description'
#     callback_url = 'https://api.darajambili.com/express-payment'
#     response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
#     return HttpResponse(response)
#     return render(request, 'jobs/job_list.html', {'job': job, 'form': form})
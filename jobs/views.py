from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, Application
from .forms import JobForm, ApplicationForm

def index(request):
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
                return redirect('home')  # Redirect to job list or a thank you page
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
        

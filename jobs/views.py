from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.contrib.auth.decorators import login_required
from .models import Job, Application, Payment  # Ensure Payment is imported
from .forms import JobForm, UserRegistrationForm
from django.http import HttpResponse, JsonResponse 
from django.views.decorators.csrf import csrf_exempt
import json
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth import login
from django.contrib.auth.views import LoginView

# Initialize logger
logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'

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
    return render(request, 'jobs/category.html', {'category': category, 'jobs': jobs})

def jobs_by_industry(request, industry_id):
    industry = get_object_or_404(Industry, id=industry_id)
    jobs = Job.objects.filter(industry=industry)
    return render(request, 'jobs/industry.html', {'industry': industry, 'jobs': jobs})

def home(request):
    return render(request, 'jobs/index.html')

def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
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

# Mpesa STK Push
@csrf_exempt
def stk_push_request(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info('Received STK Push request: %s', data)

            phone_number = data.get('phoneNumber')
            amount = data.get('amount', 1)
            account_reference = data.get('accountReference', 'reference')
            transaction_desc = data.get('transactionDesc', 'Description')
            job_id = data.get('jobId')
            callback_url = 'https://yourdomain.com/stk-push-callback/'

            cl = MpesaClient()
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            response = response.json()
            print(response)
            print(response['MerchantRequestID'])
            # Log the entire response for debugging
            logger.info('Full STK Push Response: %s', response)

            # Extract relevant information from the response
            # response_code = getattr(response, 'ResponseCode', None)
            # response_description = getattr(response, 'ResponseDescription', 'Unknown response')

            # logger.info('Parsed Response Code: %s', response_code)
            # logger.info('Parsed Response Description: %s', response_description)

            
            # Check if the STK push was successful
            if response['ResponseCode'] == '0':  # '0' indicates success
                
                try:
                    payment = Payment.objects.create(
                        phone_number=phone_number,
                        amount=amount,
                        job_id=job_id,
                        account_reference=account_reference,
                        transaction_desc=transaction_desc,
                        merchant_request_id=response['MerchantRequestID'],  # Log this if needed
                        checkout_request_id=response['CheckoutRequestID']  # Log this if needed
                    )
                    logger.info('Payment object created: %s', payment)

                    return JsonResponse({
                        'success': True,
                        'message': 'STK push initiated and payment recorded',
                        "ResponseDescription": response['ResponseDescription'],
                    }, status=200)
                except Exception as e:
                    logger.error('Error saving Payment object: %s', str(e))
                    return JsonResponse({
                        'success': False,
                        'message': 'Error saving payment information'
                    }, status=500)
            else:
                logger.error('STK Push failed: %s', response['ResponseDescription'])
                return JsonResponse({
                    'success': False,
                    'message': response['ResponseDescription'] or 'Unknown error'
                }, status=400)

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
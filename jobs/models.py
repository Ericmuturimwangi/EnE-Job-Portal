from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Industry(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=255, choices=[('Full-Time', 'Full-Time'), ('Part-Time', 'Part-Time'), ('Freelance', 'Freelance')])
    posted_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Application (models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"

    
class Payment(models.Model):
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('success', 'Success'),
    ('failed', 'Failed'),
                    ]

    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    job_id = models.IntegerField()
    account_reference = models.CharField(max_length=255, default='default_reference')  
    transaction_desc = models.CharField(max_length=255, default='default_description')
    timestamp = models.DateTimeField(auto_now_add=True)
    merchant_request_id = models.CharField(max_length=255, default='', null=True)
    checkout_request_id = models.CharField(max_length=255, default='', null=True)
    status = models.CharField(max_length=20, default='Pending')
    failure_reason = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.phone_number}"
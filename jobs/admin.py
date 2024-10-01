from django.contrib import admin
from .models import Job, Application, Employer, Category, Industry, Payment

admin.site.register(Category)
admin.site.register(Industry)
admin.site.register(Application)
admin.site.register(Employer)



class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'industry', 'category')
    list_filter = ['category', 'industry']

admin.site.register(Job, JobAdmin)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'amount', 'job_id', 'timestamp')
    search_fields = ('phone_number', 'amount', 'job_id')
    list_filter = ('timestamp',)

    ordering = ('-timestamp',)


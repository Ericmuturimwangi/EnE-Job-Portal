from django.urls import path
from .import views

urlpatterns = [
    path('', views.job_list, name='home'),
    path("job/<int:pk>/", views.job_detail, name="job_detail"),
    path("post-job/", views.post_job, name="post_job"),
]


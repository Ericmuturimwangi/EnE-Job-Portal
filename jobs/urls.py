from django.urls import path
from .import views

urlpatterns = [
    path("", views.home, name='home'),
    path('jobs', views.job_list, name='job_list'),
    path("job/<int:pk>/", views.job_detail, name="job_detail"),
    path("post-job/", views.post_job, name="post_job"),
    path('category/<int:category_id>/', views.jobs_by_category, name='category'),
    path('categories/', views.job_categories_list, name='job_categories_list'),
    path('industry/<int:industry_id>/', views.jobs_by_industry, name='industry'),
    path('industries/', views.job_industries_list, name='job_industries_list'),
    path('search/', views.job_search, name='job_search'),
    # path('job/', views.index, name='index'), mpesa
    
      
]


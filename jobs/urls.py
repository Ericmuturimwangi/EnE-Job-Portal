from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .views import register, CustomLoginView
from django.contrib.auth.views import LogoutView

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
    path('stk-push/', views.stk_push_request, name='stk_push_request'),
    path('stk-push-callback/', views.stk_push_callback, name='stk_push_callback'),  
    # path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]


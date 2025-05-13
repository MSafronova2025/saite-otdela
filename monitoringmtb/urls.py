"""
URL configuration for monitoringmtb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from colleges import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Главная
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('monitoring_needs/', views.monitoring_needs, name='monitoring_needs'),  # Мониторинг потребностей
    path('repair_needs/', views.repair_needs, name='repair_needs'),
    path('technical_state/', views.technical_state, name='technical_state'),
    path('projects/', views.projects, name='projects'),
    path('barrier_free/', views.barrier_free, name='barrier_free'),
    path('fire_safety/', views.fire_safety, name='fire_safety'),
    path('database/', views.database, name='database'),
    path('reports/', views.reports, name='reports'),
    path('submit_request/', views.submit_request_view, name='submit_request'),
    path('all_requests/', views.view_all_requests, name='all_requests'),
    path('update_request_status/<int:request_id>/', views.update_request_status, name='update_request_status'),
    path('my_requests/', views.my_requests_view, name='my_requests'),
    path('manage_colleges/', views.manage_colleges, name='manage_colleges'),
    path('add_college/', views.add_college, name='add_college'),
    path('edit_college/<int:college_id>/', views.edit_college, name='edit_college'),
    path('delete_college/<int:college_id>/', views.delete_college, name='delete_college'),
    path('manage_needs/', views.manage_needs, name='manage_needs'),
    path('add_need/', views.add_need, name='add_need'),
    path('edit_need/<int:need_id>/', views.edit_need, name='edit_need'),
    path('delete_need/<int:need_id>/', views.delete_need, name='delete_need'),
    path('manage_repairs/', views.manage_repairs, name='manage_repairs'),
    path('add_repair/', views.add_repair, name='add_repair'),
    path('edit_repair/<int:repair_id>/', views.edit_repair, name='edit_repair'),
    path('delete_repair/<int:repair_id>/', views.delete_repair, name='delete_repair'),
    path('submit_request/', views.submit_request, name='submit_request'),
    path('manage_requests/', views.manage_requests, name='manage_requests'),
    path('change_request_status/<int:request_id>/<str:status>/', views.change_request_status, name='change_request_status'),
    path('delete_request/<int:request_id>/', views.delete_request, name='delete_request'),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('change_user_role/<int:user_id>/<str:role>/', views.change_user_role, name='change_user_role'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('generate_reports/', views.generate_reports, name='generate_reports'),
    path('contacts/', views.contacts, name='contacts'),

]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

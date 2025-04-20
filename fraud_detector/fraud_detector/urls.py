from django.contrib import admin
from django.urls import path
from detector import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', login_required(views.about), name='about'),
    path('home/',login_required(views.home), name='home'),
    path('index/', login_required(views.index), name='index'),
    path('cybersecurity/', login_required(views.cyber), name='cyber'),
    path('dashboard/', login_required(views.dashboard), name='dashboard'),
    path('delete-transaction/<int:transaction_id>/', login_required(views.delete_transaction), name='delete_transaction'),
    path('export-transactions/', login_required(views.export_transactions), name='export_transactions'),
    path('clear-all-transactions/', login_required(views.clear_all_transactions), name='clear_all_transactions'),
    
]
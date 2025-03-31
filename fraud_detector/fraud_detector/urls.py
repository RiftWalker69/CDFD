from django.contrib import admin
from django.urls import path
from detector import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('/home',views.home, name='home'),
    path('/cyberguidelines', views.cyber, name='cyber'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete-transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('clear-all-transactions/', views.clear_all_transactions, name='clear_all_transactions'),
    path('export-transactions/', views.export_transactions, name='export_transactions'),
]
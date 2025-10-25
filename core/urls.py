from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'), # <-- NEW! This is the homepage.

    path('debiteurs/', views.debtor_list, name='debtor-list'),
    path('debiteurs/<int:debtor_id>/', views.debtor_detail, name='debtor-detail'),
    path('debiteurs/ajouter/', views.debtor_create, name='debtor-create'), # <-- NEW
    path('dettes/ajouter/', views.debt_create, name='debt-create'),        # <-- NEW

    path('fournisseurs/', views.supplier_list, name='supplier-list'),
    path('fournisseurs/<int:supplier_id>/', views.supplier_detail, name='supplier-detail'),
    path('fournisseurs/ajouter/', views.supplier_create, name='supplier-create'), # <-- NEW
    path('credits/ajouter/', views.credit_create, name='credit-create'),          # <-- NEW
]
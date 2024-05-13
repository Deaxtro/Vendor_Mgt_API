from django.urls import path
from .import views

urlpatterns = [
    path('vendors/', views.VendorView.as_view(), name='vendor_list'),
    path('vendors/<int:pk>/', views.VendorDetailView.as_view(), name='vendor_details'),
    path('purchase_orders/', views.PurchaseOrderView.as_view(), name='PO_list'),
    path('purchase_orders/<int:pk>/', views.PurchaseOrderDetailview.as_view(), name='PO_details'),
    path('vendors/<int:pk>/performance', views.PerformanceDetailView.as_view(), name='performance'),
]
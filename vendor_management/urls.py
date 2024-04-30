from django.urls import path
from .views import *

# Define urlpatterns for API endpoints
urlpatterns = [
    # Endpoint for listing and creating vendors
    path('vendors/', VendorListCreateAPIView.as_view(), name='vendor-list-create'),
    # Endpoint for retrieving, updating, and deleting a specific vendor
    path('vendors/<int:pk>/', VendorRetrieveUpdateDestroyAPIView.as_view(), name='vendor-retrieve-update-destroy'),
    # Endpoint for retrieving performance metrics of a specific vendor
    path('vendors/<int:pk>/performance/', VendorPerformanceMetricsAPIView.as_view(), name='vendor-performance'),
    # Endpoint for listing and creating purchase orders
    path('purchase_orders/', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list-create'),
    # Endpoint for retrieving, updating, and deleting a specific purchase order
    path('purchase_orders/<int:pk>/', PurchaseOrderRetrieveUpdateDestroyAPIView.as_view(), name='purchase-order-retrieve-update-destroy'),
    # Endpoint for acknowledging a specific purchase order
    path('purchase_orders/<int:pk>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='purchase-order-acknowledge'),
]

from django.contrib import admin
from .models import *

admin.site.site_header = "Vendor Management System"
admin.site.site_title = "Vendor Management System"
admin.site.index_title = "Welcome to Vendor Management System Portal"

# Register Vendor model
@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    search_fields = ('name', 'vendor_code')

# Register PurchaseOrder model
@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'order_date', 'delivery_date', 'status')
    search_fields = ('po_number', 'vendor__name')
    list_filter = ('status', 'order_date')

# Register VendorPerformanceMetrics model
@admin.register(VendorPerformanceMetrics)
class VendorPerformanceMetricsAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
    search_fields = ('vendor__name',)
    list_filter = ('date',)

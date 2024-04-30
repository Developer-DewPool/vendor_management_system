from rest_framework import serializers
from .models import *

# Serializer for Vendor model
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'  # Serialize all fields of the Vendor model
        # Set required attribute for specific fields to False
        extra_kwargs = {
            'on_time_delivery_rate': {'required': False},
            'quality_rating_avg': {'required': False},
            'average_response_time': {'required': False},
            'fulfillment_rate': {'required': False},
        }

# Serializer for VendorPerformanceMetrics model
class VendorPerformanceMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPerformanceMetrics
        fields = '__all__'  # Serialize all fields of the VendorPerformanceMetrics model

# Serializer for PurchaseOrder model
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'  # Serialize all fields of the PurchaseOrder model
        # Set required attribute for specific fields to False
        extra_kwargs = {
            'quality_rating': {'required': False},
            'acknowledgment_date': {'required': False},
        }
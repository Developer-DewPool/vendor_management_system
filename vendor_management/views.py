from django.db.models import F, ExpressionWrapper, fields
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from django.dispatch import receiver
from django.utils import timezone
from django.db import transaction
from .serializers import *
from .models import *
from .utils import *


def calculate_performance_metrics(vendor):
    # Perform calculations to calculate performance metrics
    # For example:
    on_time_delivery_rate = calculate_on_time_delivery_rate(vendor)
    quality_rating_avg = calculate_quality_rating_avg(vendor)
    average_response_time = calculate_average_response_time(vendor)
    fulfillment_rate = calculate_fulfillment_rate(vendor)

    # Return the calculated performance metrics as a dictionary
    return {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'average_response_time': average_response_time,
        'fulfillment_rate': fulfillment_rate,
    }

# Signal handler to update performance metrics when a PurchaseOrder is saved
@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, **kwargs):
    if instance.status == 'completed' and instance.acknowledgment_date:
        vendor = instance.vendor
        with transaction.atomic():
            try:
                # Calculate average response time
                completed_pos_with_acknowledgment = vendor.purchaseorder_set.filter(
                    status='completed', acknowledgment_date__isnull=False
                )
                response_times = []
                for po in completed_pos_with_acknowledgment:
                    response_time = (po.acknowledgment_date - po.issue_date).total_seconds() / 3600
                    response_times.append(response_time)
                
                if response_times:
                    avg_response_time = sum(response_times) / len(response_times)
                else:
                    avg_response_time = 0
                
                vendor.average_response_time = avg_response_time
                vendor.save()
            except Exception as e:
                print(f"Error updating performance metrics: {e}")

# View to retrieve performance metrics for a specific vendor
class VendorPerformanceMetricsAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceMetricsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # Calculate performance metrics here
        # Assuming you have a function to calculate the performance metrics
        performance_metrics = calculate_performance_metrics(instance)

        # Create or update VendorPerformanceMetrics record
        try:
            performance_history = VendorPerformanceMetrics.objects.create(
                vendor=instance,
                date=timezone.now(),  # You may need to adjust this based on your requirements
                on_time_delivery_rate=performance_metrics['on_time_delivery_rate'],
                quality_rating_avg=performance_metrics['quality_rating_avg'],
                average_response_time=performance_metrics['average_response_time'],
                fulfillment_rate=performance_metrics['fulfillment_rate']
            )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize and return the performance data
        serializer = self.get_serializer(performance_history)
        return Response(serializer.data)

# View to acknowledge a purchase order
class AcknowledgePurchaseOrderAPIView(APIView):
    def post(self, request, pk):
        purchase_order = get_object_or_404(PurchaseOrder, id=pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data, partial=True)
        if serializer.is_valid():
            # Update acknowledgment_date of the purchase order
            serializer.save(acknowledgment_date=timezone.now())
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# Generic views for Vendor and PurchaseOrder CRUD operations
class VendorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

class VendorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]
    # Override the partial update method to disallow PATCH requests
    def partial_update(self, request, *args, **kwargs):
        return Response({"message": "PATCH method is not allowed. Use PUT for updates."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PurchaseOrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]
    # Override the partial update method to disallow PATCH requests
    def partial_update(self, request, *args, **kwargs):
        return Response({"message": "PATCH method is not allowed. Use PUT for updates."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class PurchaseOrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]

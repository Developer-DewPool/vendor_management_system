from django.db import models
from datetime import timedelta
from django.utils import timezone

# Function to calculate the on-time delivery rate for a vendor
def calculate_on_time_delivery_rate(vendor):
    # Get all completed purchase orders for the vendor
    completed_pos = vendor.purchaseorder_set.filter(status='completed')
    total_completed_pos = completed_pos.count()  # Total number of completed purchase orders

    if total_completed_pos == 0:
        return 0  # Return 0 if there are no completed purchase orders
    
    # Get completed purchase orders delivered on time (delivery_date <= current time)
    on_time_delivered_pos = completed_pos.filter(delivery_date__lte=timezone.now())
    # Calculate the on-time delivery rate as a percentage
    on_time_delivery_rate = (on_time_delivered_pos.count() / total_completed_pos) * 100
    return round(on_time_delivery_rate, 2)  # Round the result to two decimal places

# Function to calculate the average quality rating for a vendor
def calculate_quality_rating_avg(vendor):
    # Get completed purchase orders with quality ratings for the vendor
    completed_pos_with_ratings = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
    
    if completed_pos_with_ratings.exists():
        # Calculate the average quality rating
        quality_rating_avg = completed_pos_with_ratings.aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating']
        return round(quality_rating_avg, 2)  # Round the result to two decimal places
    return 0  # Return 0 if there are no completed purchase orders with ratings

# Function to calculate the average response time for a vendor
def calculate_average_response_time(vendor):
    # Get completed purchase orders with acknowledgment dates for the vendor
    completed_pos_with_acknowledgment = vendor.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
    
    if completed_pos_with_acknowledgment.exists():
        # Calculate response times for each completed purchase order
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() / 3600 for po in completed_pos_with_acknowledgment]
        # Calculate the average response time
        average_response_time = sum(response_times) / len(response_times)
        return round(average_response_time, 2)  # Round the result to two decimal places
    return 0  # Return 0 if there are no completed purchase orders with acknowledgment dates

# Function to calculate the fulfillment rate for a vendor
def calculate_fulfillment_rate(vendor):
    # Get the total number of purchase orders for the vendor
    total_pos = vendor.purchaseorder_set.count()
    
    if total_pos == 0:
        return 0  # Return 0 if there are no purchase orders
    
    # Get successfully fulfilled purchase orders (completed and without quality ratings)
    successfully_fulfilled_pos = vendor.purchaseorder_set.filter(status='completed', quality_rating__isnull=True)
    # Calculate the fulfillment rate as a percentage
    fulfillment_rate = (successfully_fulfilled_pos.count() / total_pos) * 100
    return round(fulfillment_rate, 2)  # Round the result to two decimal places

from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.schemas.openapi import AutoSchema
from django.views.generic import RedirectView

# Define schema view for API documentation
schema_view = get_schema_view(
   openapi.Info(
      title="Vendor Management System API documentation with Performance Metrics",
      default_version='v1',
      description="This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.",
      contact=openapi.Contact(email="dpdewc@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),  # Allow any user to access the documentation
)

# Define urlpatterns
urlpatterns = [
   # Redirect from the root URL to the admin site URL
   path('', RedirectView.as_view(url='/admin/', permanent=False)),
   # Admin site URL
   path('admin/', admin.site.urls),
   # Token authentication endpoint URL
   path('api/token/', obtain_auth_token, name='api-token'),
   # API documentation endpoint URL
   path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   # Include API endpoints from vendor_management app
   path('api/', include('vendor_management.urls')),
]

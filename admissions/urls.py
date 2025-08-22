from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdmissionApplicationViewSet

router = DefaultRouter()
router.register(r'admissions', AdmissionApplicationViewSet, basename='admission')

urlpatterns = [
    path('', include(router.urls)),
]

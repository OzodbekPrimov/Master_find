

from django.urls import path, include


from .views import (
    MasterViewset, ReviewListCreateView, JobViewset
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'masters', MasterViewset)
router.register(r"jobs", JobViewset)

# router.register(r"reviews", ReviewListCreateView)




urlpatterns = [
    path('', include(router.urls)),
    path('review/', ReviewListCreateView.as_view()),

]
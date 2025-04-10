
from django.urls import path, include
from .views import (
    MasterViewset, ReviewListCreateView, JobViewset, MessageListCreateView, ConversationView
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'masters', MasterViewset)
router.register(r"jobs", JobViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('review/', ReviewListCreateView.as_view()),
    path('message/', MessageListCreateView.as_view()),
    path("conversation/",ConversationView.as_view() )
]

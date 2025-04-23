
from rest_framework import viewsets, generics
from rest_framework.response import Response


from .models import Review, Master, Job, Message
from .serilaizers import MasterSerializer, ReviewSerializer, JobSerializer, MessageSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from .permissions import IsStaffOrReadOnly, IsOwnerReadOnly

from django_filters import rest_framework as django_filters
from rest_framework import filters
from .filters import MasterFilter, JobFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 4


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  # Faqat autentifikatsiyadan o'tgan foydalanuvchilar



class JobViewset(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsStaffOrReadOnly]

    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'description']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='title',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by title"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MasterViewset(viewsets.ModelViewSet):
    queryset = Master.objects.filter(is_approved=True)
    serializer_class = MasterSerializer
    permission_classes = [IsOwnerReadOnly]

    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MasterFilter
    search_fields = ['full_name', 'bio', 'address', 'job__title']

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='city',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by city",
            ),
            openapi.Parameter(
                name='job',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_NUMBER,
                description="Filter by job title",
            ),
            openapi.Parameter(
                name='gender',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Filter by gender (M/F)",
            ),
            openapi.Parameter(
                name='experience_years',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Filter by experience years",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        job = request.query_params.get('job__title')
        if job:
            self.queryset = Master.objects.filter(job=job, is_approved=True)
        else:
            self.queryset = Master.objects.filter(is_approved=True)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instanse = self.get_object()
        serializer = self.get_serializer(instanse)
        related_master = Master.objects.filter(job=instanse.job).exclude(id=instanse.id)[:4]
        related_serializer = MasterSerializer(related_master, many=True)
        return Response({
            'master':serializer.data,
            'related_master':related_serializer.data
        })


    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        master = self.get_object()
        reviews = master.reviews.all()
        print(reviews)
        if reviews.count()==0:
            return Response({'average_rating':'no reviews yet'})
        avg_rating = sum([review.rating for review in reviews]) / reviews.count()

        return Response({"average_rating":avg_rating})


class MessageListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        # faqat o'zi qatnashgan xabarlarni ko'ra oladi
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        )


class ConversationView(generics.ListAPIView):
    """Joriy foydalanuvchi va boshqa foydalanuvchi o'rtasidagi
    xabarlarni olish"""
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        try:
            user_id = self.kwargs['user_id']
            return Message.objects.filter(
            Q(sender=self.request.user, receiver__id=user_id) | Q(sender__id=user_id, receiver=self.request.user)
        ).order_by('created_at')
        except Exception as e:
            return Response({"error": str(e)}, status=400)

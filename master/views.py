
from rest_framework import viewsets, generics
from rest_framework.response import Response

from .models import Review, Master, Job
from .serilaizers import MasterSerializer, ReviewSerializer, JobSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

# Create your views here.


class CustomPagination(PageNumberPagination):
    page_size = 4


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    # permission_classes = [IsAuthenticated]  # Faqat autentifikatsiyadan o'tgan foydalanuvchilar

    def get_queryset(self):
        # Faqat muayyan usta uchun sharhlarni qaytarish
        usta_id = self.kwargs['master_id']
        return Review.objects.filter(master_id=usta_id)

    def perform_create(self, serializer):
        # Sharh qoldirishda foydalanuvchi va usta avtomatik qo'shiladi
        usta_id = self.kwargs['master_id']
        serializer.save(user=self.request.user, usta_id=usta_id)


class JobViewset(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer



class MasterViewset(viewsets.ModelViewSet):
    queryset = Master.objects.all()
    serializer_class = MasterSerializer

    def list(self, request, *args, **kwargs):
        job = request.query_params.get('job')
        if job:
            self.queryset = Master.objects.filter(job=job)
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def average_rating(self, request, pk=None):
        master = self.get_object()
        reviews = master.reviews.all()
        print(reviews)
        if reviews.count()==0:
            return Response({'average_rating':'no reviews yet'})
        avg_rating = sum([review.rating for review in reviews]) / reviews.count()

        return Response({"average_rating":avg_rating})





# class MasterListView(generics.ListAPIView):
#     queryset = Master.objects.filter(is_approved=True)  # Faqat tasdiqlangan ustalar
#     serializer_class = MasterSerializer
#     pagination_class = CustomPagination
#     # filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     # filterset_fields = ['city', 'specialization']  # Shahar va mutaxassislik bo'yicha filtrlash
#     # ordering_fields = ['rating']  # Reyting bo'yicha tartiblash
#
# class MasterDetailView(generics.RetrieveAPIView):
#     queryset = Master.objects.filter(is_approved=True)
#     serializer_class = MasterSerializer




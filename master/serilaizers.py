from rest_framework import serializers
from .models import Master,  Review, Job


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ['id', 'title', 'description']


class MasterSerializer(serializers.ModelSerializer):
    avg_rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = Master
        fields = ['user', 'full_name', 'phone_number', 'city', 'job', 'is_approved', 'avg_rating']
        read_only_fields = ['is_approved', 'avg_rating']


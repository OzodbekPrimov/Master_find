from rest_framework import serializers

from .models import Master, Review, Job, Message


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'master', 'rating', 'comment']

    # xabar yuboruvchi sifatida request jo'natgan userni oladi
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Review.objects.create(**validated_data)


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ['id', 'title', 'description']


class MasterSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Master
        fields = ['id', 'user', 'full_name', 'phone_number', 'city', 'job', 'avg_rating', 'gender',
                  'address', 'experience_years', 'bio']
        read_only_fields = ['is_approved', 'avg_rating']



class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id','receiver', 'content', 'sender']
        read_only_fields = ['sender',]

    def create(self, validated_data):
        # xabar yuboruvchini joriy foydalanuvchi sifatida avtomatik olish
        validated_data['sender'] = self.context['request'].user
        return Message.objects.create(**validated_data)





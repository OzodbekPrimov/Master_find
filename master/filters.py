from django_filters import rest_framework as django_filter

from .models import Master, Job

class MasterFilter(django_filter.FilterSet):

    class Meta:
        model = Master
        fields = ['city', 'job', 'gender', 'experience_years']


class JobFilter(django_filter.FilterSet):
    class Meta:
        model = Job
        fields = ['title']
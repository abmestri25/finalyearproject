import django_filters
from django_filters import DateFilter,CharFilter,ChoiceFilter,ModelChoiceFilter,DateFromToRangeFilter
from .models import Faculty,Report,Student,TaskAssigned
from django.forms.widgets import TextInput

class ReportFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
    (0, 'Not Yet Approved'),
    (1, 'Approved'),
    (2, 'Disapproved'),
)
    # start_date = DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'YYYY-MM-DD'}))
    
    event_coordinator = ModelChoiceFilter(queryset=Faculty.objects.all())
    start_date = DateFilter(label="From",field_name='created_at',lookup_expr='gte',widget=TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    end_date = DateFilter(label='To',field_name='created_at',lookup_expr='lte',widget=TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    description = CharFilter(label="Description" ,field_name='description',lookup_expr='icontains')
    status = ChoiceFilter(choices=STATUS_CHOICES)
    class Meta:
        model =  Report 
        fields = ['event_title','start_date','end_date','org_department','types','event_coordinator','forwhome','start_date','end_date','status']
        exclude = ['res_person_profile_pic',]

class FacultyFilter(django_filters.FilterSet):

    class Meta:
        model = Faculty
        fields = ['middle_name', 'joined_at', 'qualification','sex','phone_number','branch']
    
class StudentFilter(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = ['middle_name', 'year','sex','phone_number','branch']

class TaskFilter(django_filters.FilterSet):
    start_date = DateFilter(label="From",field_name='created_at',lookup_expr='gte',widget=TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    end_date = DateFilter(label='To',field_name='created_at',lookup_expr='lte',widget=TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    class Meta:
        model = TaskAssigned
        fields = '__all__'


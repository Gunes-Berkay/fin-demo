from django.urls import path
from .views import fetch_table_data

urlpatterns = [
    path('charts/table/<str:table_name>/', fetch_table_data, name='fetch_table_data'),

]

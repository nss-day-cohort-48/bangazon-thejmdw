from django.urls import path
from .views import completed_order_list

urlpatterns = [
    path('reports/completedorders', completed_order_list),
]

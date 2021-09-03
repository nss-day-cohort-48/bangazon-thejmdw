from django.urls import path
from .views import completed_order_list, incomplete_order_list
from .views import inexpensive_product_list
from .views import expensive_product_list

urlpatterns = [
    path('reports/completedorders', completed_order_list),
    path('reports/incompleteorders', incomplete_order_list),
    path('reports/inexpensiveproducts', inexpensive_product_list),
    path('reports/expensiveproducts', expensive_product_list),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('item/<int:item_id>/', view_item, name='view_item'),
    path('buy/<int:item_id>/', buy_item, name='buy_item'),
]

from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('checkout/', checkout, name='checkout'),
    path('sub', create_sub, name='sub'),
	path('complete', complete, name='complete'),
    path('cancel', cancel, name='cancel'),
]
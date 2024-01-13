from django.urls import path
from .views import *

urlpatterns = [
    path('', MovieListAPI.as_view()),
    path('<str:pk>', MovieRetrieveAPI.as_view())
]
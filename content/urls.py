from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MovieListAPI.as_view()),
    path('<str:pk>', MovieRetrieveAPI.as_view()),
    path('<str:pk>/comments/', include('comment.urls')),
    path('<str:pk>/rate', RatingAPI.as_view()),
]
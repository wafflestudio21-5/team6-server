from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MovieListAPI.as_view()),
    path('<str:pk>', MovieRetrieveAPI.as_view()),
    path('<str:pk>/comments/', include('comment.urls')),
    path('<str:pk>/rate', RatingAPI.as_view()),
    path('<str:pk>/state', StateCreateAPI.as_view()),
    path('rates/<int:pk>', RatingRetrieveUpdateDestroyAPI.as_view()),
    path('rates/count', RatingCountAPI.as_view()),
    path('states/<int:pk>', StateRetrieveUpdateDestroyAPI.as_view()),
    path('carousels/<int:pk>', CarouselRetrieveAPI.as_view()),
]
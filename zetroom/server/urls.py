from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('accountlist/', AccountListView.as_view()),
    path('superaccountlist/', SuperAccountListView.as_view()),
]
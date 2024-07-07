from django.urls import path

from tasks.views import BaseViewAPI

urlpatterns = [
    path('base/', BaseViewAPI.as_view(), name='base-page')
]

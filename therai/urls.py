from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('gpt', views.gpt, name='gpt'),
    # path('google-vision', views.google_vision, name='google_vision'),
    path('process-image', views.process_image, name='process_image'),
]

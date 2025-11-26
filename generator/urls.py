from django.urls import path
from . import views

urlpatterns = [
    path('generate-brief/', views.generate_brief, name='generate_brief'),
]


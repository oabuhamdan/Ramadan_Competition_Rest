from django.urls import path
from . import views

urlpatterns = [
    path('points-records/', views.PointRecords.as_view()),
    path('student-users/', views.StudentUserView.as_view()),
]

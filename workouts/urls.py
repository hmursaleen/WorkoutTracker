from django.urls import path
from .views import WorkoutPlanListCreateAPIView, WorkoutPlanDetailAPIView

urlpatterns = [
    path('workouts/', WorkoutPlanListCreateAPIView.as_view(), name='workout_list_create'),
    path('workouts/<int:pk>/', WorkoutPlanDetailAPIView.as_view(), name='workout_detail'),
]

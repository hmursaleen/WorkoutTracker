from django.urls import path
from . import views

urlpatterns = [
    path('workouts/', views.WorkoutPlanListCreateAPIView.as_view(), name='workout_list_create'),
    path('workouts/<int:pk>/', views.WorkoutPlanDetailAPIView.as_view(), name='workout_detail'),
    path('scheduled_workouts/', views.ScheduledWorkoutListCreateAPIView.as_view(), name='scheduled_workout_list_create'),
    path('scheduled_workouts/<int:pk>/', views.ScheduledWorkoutDetailAPIView.as_view(), name='scheduled_workout_detail'),
]

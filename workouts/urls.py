from django.urls import path
from . import views

urlpatterns = [
    path('workouts/', views.WorkoutPlanListCreateAPIView.as_view(), name='workout_list_create'),
    path('workouts/<int:pk>/', views.WorkoutPlanDetailAPIView.as_view(), name='workout_detail'),
    path('scheduled_workouts/', views.ScheduledWorkoutListCreateAPIView.as_view(), name='scheduled_workout_list_create'),
    path('scheduled_workouts/<int:pk>/', views.ScheduledWorkoutDetailAPIView.as_view(), name='scheduled_workout_detail'),

    path('scheduled_workouts/sorted/', views.ScheduledWorkoutListSortedAPIView.as_view(), name='scheduled_workout_sorted'),

    path('workout_comments/', views.WorkoutCommentListCreateAPIView.as_view(), name='workout_comment_list_create'),
    path('workout_comments/<int:pk>/', views.WorkoutCommentDetailAPIView.as_view(), name='workout_comment_detail'),

    path('workout_performances/', views.WorkoutPerformanceListCreateAPIView.as_view(), name='workout_performance_list_create'),
    path('workout_performances/<int:pk>/', views.WorkoutPerformanceDetailAPIView.as_view(), name='workout_performance_detail'),
]
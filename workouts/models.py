from django.db import models
from django.contrib.auth.models import User
from exercises.models import Exercise


class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    scheduled_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercise.name} in {self.workout.title}"





class ScheduledWorkout(models.Model):#this model links a workout plan to a specific scheduled date/time.
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheduled_workouts')
    workout = models.ForeignKey(WorkoutPlan, on_delete=models.CASCADE, related_name='schedules')
    scheduled_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.workout.title} scheduled for {self.scheduled_datetime}"





class WorkoutComment(models.Model):
    workout = models.ForeignKey('WorkoutPlan', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.workout.title}"



class WorkoutPerformance(models.Model):
    workout = models.ForeignKey('WorkoutPlan', on_delete=models.CASCADE, related_name='performances')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_performances')
    performance_metric = models.FloatField(null=True, blank=True, help_text="Numeric performance metric (e.g., weight lifted, time, etc.)")
    notes = models.TextField(blank=True, help_text="Additional notes about performance")
    performed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Performance for {self.workout.title} by {self.user.username} on {self.performed_at}"
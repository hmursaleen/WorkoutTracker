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

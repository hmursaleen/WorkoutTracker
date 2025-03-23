from rest_framework import serializers
from .models import WorkoutPlan, WorkoutExercise, ScheduledWorkout



class WorkoutExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutExercise
        fields = ['id', 'exercise', 'sets', 'reps', 'weight']





class WorkoutPlanSerializer(serializers.ModelSerializer):
    exercises = WorkoutExerciseSerializer(many=True)

    class Meta:
        model = WorkoutPlan
        fields = ['id', 'title', 'description', 'scheduled_date', 'exercises', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        workout = WorkoutPlan.objects.create(**validated_data)
        for exercise_data in exercises_data:
            # Create each WorkoutExercise linked to the workout
            WorkoutExercise.objects.create(workout=workout, **exercise_data)
        return workout

    def update(self, instance, validated_data):
        exercises_data = validated_data.pop('exercises', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.scheduled_date = validated_data.get('scheduled_date', instance.scheduled_date)
        instance.save()
        if exercises_data is not None:
            # For simplicity, delete existing exercises and recreate them.
            instance.exercises.all().delete()
            for exercise_data in exercises_data:
                WorkoutExercise.objects.create(workout=instance, **exercise_data)
        return instance





class ScheduledWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledWorkout
        fields = ['id', 'workout', 'scheduled_datetime', 'created_at']
        read_only_fields = ['created_at']
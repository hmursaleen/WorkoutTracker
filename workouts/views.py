from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import ScheduledWorkout, WorkoutPlan
from .serializers import WorkoutPlanSerializer, ScheduledWorkoutSerializer



class WorkoutPlanListCreateAPIView(APIView):
    """
    API view to list all workout plans for the authenticated user,
    and to create a new workout plan.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Only return workouts that belong to the current user.
        workouts = WorkoutPlan.objects.filter(user=request.user).order_by('-created_at')
        serializer = WorkoutPlanSerializer(workouts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WorkoutPlanSerializer(data=request.data)
        if serializer.is_valid():
            # Set the workout's user to the current authenticated user.
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class WorkoutPlanDetailAPIView(APIView):
    """
    API view to retrieve, update, or delete a single workout plan.
    Ensures that only the owner of the workout can access or modify it.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, request):
        try:
            workout = WorkoutPlan.objects.get(pk=pk)
        except WorkoutPlan.DoesNotExist:
            return None
        if workout.user != request.user:
            return None
        return workout

    def get(self, request, pk):
        workout = self.get_object(pk, request)
        if workout is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkoutPlanSerializer(workout)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        workout = self.get_object(pk, request)
        if workout is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkoutPlanSerializer(workout, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        workout = self.get_object(pk, request)
        if workout is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        workout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class ScheduledWorkoutListCreateAPIView(APIView):
    """
    API view to list all scheduled workouts for the authenticated user,
    and to create a new scheduled workout.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Return only the scheduled workouts for the current user, ordered by scheduled_datetime.
        schedules = ScheduledWorkout.objects.filter(user=request.user).order_by('scheduled_datetime')
        serializer = ScheduledWorkoutSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ScheduledWorkoutSerializer(data=request.data)
        if serializer.is_valid():
            # Verify that the workout belongs to the authenticated user.
            workout = serializer.validated_data.get('workout')
            if workout.user != request.user:
                return Response({"detail": "You cannot schedule a workout that doesn't belong to you."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class ScheduledWorkoutDetailAPIView(APIView):
    """
    API view to retrieve, update, or delete a specific scheduled workout.
    Only the owner of the schedule can access or modify it.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, request):
        try:
            schedule = ScheduledWorkout.objects.get(pk=pk)
        except ScheduledWorkout.DoesNotExist:
            return None
        if schedule.user != request.user:
            return None
        return schedule

    def get(self, request, pk):
        schedule = self.get_object(pk, request)
        if schedule is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScheduledWorkoutSerializer(schedule)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        schedule = self.get_object(pk, request)
        if schedule is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ScheduledWorkoutSerializer(schedule, data=request.data)
        if serializer.is_valid():
            workout = serializer.validated_data.get('workout')
            if workout.user != request.user:
                return Response({"detail": "You cannot schedule a workout that doesn't belong to you."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        schedule = self.get_object(pk, request)
        if schedule is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class ScheduledWorkoutListSortedAPIView(APIView):
    """
    API view to list all scheduled workouts for the authenticated user,
    sorted by the scheduled date/time.
    
    Optional Query Parameter:
        - order: 'asc' (default) for ascending, 'desc' for descending order.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        order = request.query_params.get('order', 'asc').lower()
        if order == 'desc':
            schedules = ScheduledWorkout.objects.filter(user=request.user).order_by('-scheduled_datetime')
        else:
            schedules = ScheduledWorkout.objects.filter(user=request.user).order_by('scheduled_datetime')
        serializer = ScheduledWorkoutSerializer(schedules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






class WorkoutCommentListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        workout_id = request.query_params.get('workout')
        if workout_id:
            comments = WorkoutComment.objects.filter(user=request.user, workout_id=workout_id)
        else:
            comments = WorkoutComment.objects.filter(user=request.user)
        serializer = WorkoutCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = WorkoutCommentSerializer(data=request.data)
        if serializer.is_valid():
            workout = serializer.validated_data.get('workout')
            if workout.user != request.user:
                return Response({"detail": "You cannot comment on a workout that is not yours."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class WorkoutCommentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, request):
        try:
            comment = WorkoutComment.objects.get(pk=pk)
        except WorkoutComment.DoesNotExist:
            return None
        if comment.user != request.user:
            return None
        return comment

    def get(self, request, pk):
        comment = self.get_object(pk, request)
        if comment is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkoutCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        comment = self.get_object(pk, request)
        if comment is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkoutCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk, request)
        if comment is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





class WorkoutPerformanceListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        workout_id = request.query_params.get('workout')
        if workout_id:
            performances = WorkoutPerformance.objects.filter(user=request.user, workout_id=workout_id)
        else:
            performances = WorkoutPerformance.objects.filter(user=request.user)
        serializer = WorkoutPerformanceSerializer(performances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):#minimal change
        serializer = WorkoutPerformanceSerializer(data=request.data)
        if serializer.is_valid():
            workout = serializer.validated_data.get('workout')
            if workout.user != request.user:
                return Response({"detail": "You cannot log performance for a workout that is not yours."}, status=status.HTTP_403_FORBIDDEN)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class WorkoutPerformanceDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, request):
        try:
            performance = WorkoutPerformance.objects.get(pk=pk)
        except WorkoutPerformance.DoesNotExist:
            return None
        if performance.user != request.user:
            return None
        return performance

    def get(self, request, pk):
        performance = self.get_object(pk, request)
        if performance is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkoutPerformanceSerializer(performance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        performance = self.get_object(pk, request)
        if performance is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = WorkoutPerformanceSerializer(performance, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        performance = self.get_object(pk, request)
        if performance is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        performance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

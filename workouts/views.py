from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import WorkoutPlan
from .serializers import WorkoutPlanSerializer

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

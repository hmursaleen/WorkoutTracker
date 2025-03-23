from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from workouts.models import WorkoutPlan, WorkoutExercise
from exercises.models import Exercise





class WorkoutCRUDTests(APITestCase):
    def setUp(self):
        #creating two users for testing authorization
        self.user1 = User.objects.create_user(username="user1", email="user1@example.com", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", email="user2@example.com", password="pass1234")
        
        self.exercise = Exercise.objects.create(
            name="Test Exercise",
            description="This is a test exercise",
            category="strength",
            muscle_group="arms"
        )
        
        self.list_create_url = reverse("workout_list_create")
        

    def authenticate(self, user):
        self.client.force_authenticate(user=user)
        #The helper method authenticate() forces the client to act as a particular user. 
        #This simulates real-world scenarios.

    def test_create_workout(self):
        """
        ensure an authenticated user can create a workout plan.
        """
        self.authenticate(self.user1)
        payload = {
            "title": "Morning Workout",
            "description": "Chest and triceps workout",
            "scheduled_date": "2025-04-10",
            "exercises": [
                {
                    "exercise": self.exercise.id,
                    "sets": 3,
                    "reps": 10,
                    "weight": 50.0
                }
            ]
        }
        response = self.client.post(self.list_create_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Morning Workout")
        self.assertTrue("exercises" in response.data)
        self.assertEqual(WorkoutPlan.objects.filter(user=self.user1).count(), 1)

    
    
    def test_list_workouts(self):
        """
        Ensure that only workouts belonging to the authenticated user are listed.
        """
        # Create workouts for both users.
        workout1 = WorkoutPlan.objects.create(user=self.user1, title="User1 Workout", description="Desc")
        workout2 = WorkoutPlan.objects.create(user=self.user2, title="User2 Workout", description="Desc")
        
        self.authenticate(self.user1)
        response = self.client.get(self.list_create_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only one workout should be returned for user1.
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "User1 Workout")

    
    
    def test_retrieve_workout(self):
        """
        Test retrieval of a specific workout by its owner.
        """
        workout = WorkoutPlan.objects.create(user=self.user1, title="Retrieve Workout", description="Desc")
        detail_url = reverse("workout_detail", kwargs={"pk": workout.id})
        
        self.authenticate(self.user1)
        response = self.client.get(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Retrieve Workout")

    
    
    def test_update_workout(self):
        """
        Test that the owner can update an existing workout plan.
        """
        workout = WorkoutPlan.objects.create(user=self.user1, title="Old Title", description="Old Desc")
        detail_url = reverse("workout_detail", kwargs={"pk": workout.id})
        self.authenticate(self.user1)
        
        payload = {
            "title": "Updated Title",
            "description": "Updated Desc",
            "scheduled_date": "2025-04-15",
            "exercises": [
                {
                    "exercise": self.exercise.id,
                    "sets": 4,
                    "reps": 8,
                    "weight": 60.0
                }
            ]
        }
        response = self.client.put(detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")
        #verify nested exercises are updated
        self.assertEqual(len(response.data["exercises"]), 1)

    
    
    def test_delete_workout(self):
        """
        Test that the owner can delete a workout plan.
        """
        workout = WorkoutPlan.objects.create(user=self.user1, title="To be deleted", description="Desc")
        detail_url = reverse("workout_detail", kwargs={"pk": workout.id})
        self.authenticate(self.user1)
        
        response = self.client.delete(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WorkoutPlan.objects.filter(id=workout.id).exists())

    
    
    def test_unauthorized_access(self):
        """
        Ensure that a user cannot access or modify workouts belonging to another user.
        """
        workout = WorkoutPlan.objects.create(user=self.user1, title="User1 Workout", description="Desc")
        detail_url = reverse("workout_detail", kwargs={"pk": workout.id})
        
        # Authenticate as user2 and try to retrieve user1's workout.
        self.authenticate(self.user2)
        response = self.client.get(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        #attempt to update
        payload = {
            "title": "Hacked Title",
            "description": "Hacked Desc",
            "scheduled_date": "2025-04-15",
            "exercises": []
        }
        response = self.client.put(detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        #attempt to delete
        response = self.client.delete(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# exercises/management/commands/seed_exercises.py

from django.core.management.base import BaseCommand
from exercises.models import Exercise

class Command(BaseCommand):
    help = 'Seed the database with a variety of exercises.'

    def handle(self, *args, **options):
        # List of exercises to seed
        exercises_data = [
            {
                "name": "Running",
                "description": "A cardiovascular exercise that improves endurance.",
                "category": "cardio",
                "muscle_group": ""
            },
            {
                "name": "Cycling",
                "description": "A low-impact exercise that improves cardiovascular health.",
                "category": "cardio",
                "muscle_group": ""
            },
            {
                "name": "Bench Press",
                "description": "A strength exercise targeting the chest, shoulders, and triceps.",
                "category": "strength",
                "muscle_group": "chest"
            },
            {
                "name": "Squats",
                "description": "A strength exercise targeting the legs and glutes.",
                "category": "strength",
                "muscle_group": "legs"
            },
            {
                "name": "Yoga",
                "description": "A flexibility and balance exercise that improves core strength.",
                "category": "flexibility",
                "muscle_group": "core"
            },
            {
                "name": "Plank",
                "description": "An isometric core strength exercise that involves maintaining a position similar to a push-up.",
                "category": "",
                "muscle_group": "core"
            },
            {
                "name": "Bicep Curl",
                "description": "A strength exercise that targets the biceps.",
                "category": "strength",
                "muscle_group": "arms"
            },
            {
                "name": "Shoulder Press",
                "description": "A strength exercise that targets the shoulders.",
                "category": "strength",
                "muscle_group": "shoulders"
            },
        ]

        # Clear existing exercises if needed (optional)
        Exercise.objects.all().delete()
        self.stdout.write("Existing exercises cleared.")

        for exercise in exercises_data:
            obj, created = Exercise.objects.get_or_create(
                name=exercise["name"],
                defaults={
                    "description": exercise["description"],
                    "category": exercise["category"],
                    "muscle_group": exercise["muscle_group"],
                }
            )
            if created:
                self.stdout.write(f"Created exercise: {obj.name}")
            else:
                self.stdout.write(f"Exercise already exists: {obj.name}")

        self.stdout.write(self.style.SUCCESS("Exercise seeding completed."))

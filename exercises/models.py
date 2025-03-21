from django.db import models

class Exercise(models.Model):
    CATEGORY_CHOICES = [
        ('cardio', 'Cardio'),
        ('strength', 'Strength'),
        ('flexibility', 'Flexibility'),
        ('balance', 'Balance'),
    ]
    
    MUSCLE_GROUP_CHOICES = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('legs', 'Legs'),
        ('arms', 'Arms'),
        ('shoulders', 'Shoulders'),
        ('core', 'Core'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES, 
        blank=True,
        help_text="General exercise category (e.g., cardio, strength, flexibility, balance)."
    )

    muscle_group = models.CharField(
        max_length=50, 
        choices=MUSCLE_GROUP_CHOICES, 
        blank=True,
        help_text="Primary muscle group targeted (e.g., chest, back, legs, arms, shoulders, core)."
    )
    
    def __str__(self):
        return self.name

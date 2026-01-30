from django.db import models


class Patient(models.Model):
    """Model representing a patient in the clinic."""
    name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.phone})"

    class Meta:
        ordering = ['-created_at']


class Case(models.Model):
    """Model representing a case/visit for symptom analysis."""
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='cases'
    )
    transcript = models.TextField(help_text="Voice transcript of symptoms")
    symptoms = models.JSONField(default=list, blank=True)
    risk_score = models.FloatField(
        default=0.0,
        help_text="Risk score from 0.0 to 1.0"
    )
    token_number = models.IntegerField(null=True, blank=True)
    assigned_doctor = models.CharField(max_length=100, blank=True)
    prescription = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='waiting'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Case for {self.patient.name} - Risk: {self.risk_score}"

    class Meta:
        ordering = ['-risk_score', '-created_at']

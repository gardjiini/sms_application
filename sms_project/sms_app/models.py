from django.db import models

STATUS_CHOICES = [
    ('ACK', 'Acknowledged'),
    ('DEL', 'Delivered'),
    ('FAIL', 'Failed'),
    # Add other statuses here
]

class SMS(models.Model):
    to = models.CharField(max_length=20)  # Increased length for phone numbers
    message = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='ACK')
    job_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    network = models.CharField(max_length=100, blank=True, null=True)
    submit_date = models.DateTimeField(blank=True, null=True)
    deliv_date = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.to}: {self.message[:20]}..."

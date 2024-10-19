from django.db import models

# Create your models here.
class SMS(models.Model):
    to = models.CharField(max_length=15)
    message = models.TextField()
    status =models.CharField(max_length=20, default='queued')
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"SMS to {self.to} - {self.status}"
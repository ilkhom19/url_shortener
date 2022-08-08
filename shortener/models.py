from hashlib import md5

from django.db import models

class URL(models.Model):
    full_url = models.CharField(unique=True, max_length=2024)
    url_hash = models.CharField(unique=True, max_length=8)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.clicks += 1
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.url_hash = md5(self.full_url.encode()).hexdigest()[:8]

        return super().save(*args, **kwargs)
from hashlib import sha256
import base64

from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from graphql import GraphQLError


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
            self.url_hash = base64.b64encode(sha256(self.full_url.encode()).digest())
            self.url_hash = self.url_hash.decode("utf-8")[:8]

        validate = URLValidator()
        try:
            validate(self.full_url)
        except ValidationError as e:
            raise GraphQLError('invalid url')
    

        return super().save(*args, **kwargs)
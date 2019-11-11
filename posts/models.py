from datetime import datetime

from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=8192, null=False, blank=False)
    url = models.CharField(max_length=8192, null=False, blank=False, unique=True)
    created = models.DateTimeField(null=False, blank=False, db_index=True)

    class Meta:
        # dumb index for 'select * posts orderby desc limit 30' query to check unique refs from hakernews
        # in real project, i would consider to decouple this logic into crawler infrastructure
        indexes = [
            models.Index(fields=['-created'])
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = datetime.utcnow()
        return super().save(*args, **kwargs)

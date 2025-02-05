from django.db import models

class File(models.Model):
    name = models.CharField(max_length=255)
    ipfs_hash = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
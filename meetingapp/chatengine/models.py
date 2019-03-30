from django.db import models

class Group(models.Model):
    group_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return f'{self.group_name}'
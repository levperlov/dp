from django.contrib.auth.models import User
from django.db import models


class News(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    is_public = models.BooleanField()
    added_date = models.DateTimeField()

    def __str__(self):
        return "{} news object: \"{}\" by {}".format(
            "Public" if self.is_public else "Private",
            self.name,
            self.author
        )

    def __repr__(self):
        return str(self)
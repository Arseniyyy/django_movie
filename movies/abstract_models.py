from django.db import models


class CommonInfo(models.Model):
    """Includes the name and description attributes for every class that inherits from this class."""
    name = models.CharField("Category", max_length=100)
    description = models.TextField("Description")

    class Meta:
        abstract = True

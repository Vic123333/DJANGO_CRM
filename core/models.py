from django.db import models

class EmployeeList(models.Model):
    name = models.CharField(max_length=200)
    job = models.CharField(max_length=200)
    favorite_color = models.CharField(max_length=200)

    def __str__(self):
        return self.name




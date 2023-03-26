from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    children = models.JSONField(default={"child": []})
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.name

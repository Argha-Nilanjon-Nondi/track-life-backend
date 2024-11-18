from django.db import models
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

User=get_user_model()

class FlexTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_name = models.CharField(max_length=255)
    table_structure= models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="flex_table")

    def __str__(self):
        return self.table_name

# class FlexTableField(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     field_name = models.TextField(blank=False)
#     field_type = models.TextField(blank=False)
#     field_data= models.JSONField()
#     table = models.ForeignKey(FlexTable, on_delete=models.CASCADE, related_name="flex_field")

#     def __str__(self):
#         return self.field_name
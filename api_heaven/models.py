from django.db import models
import uuid
import os
import mimetypes
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from .utils import rename_file

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
    
class FlexRecordTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_structure= models.JSONField()
    flex_table = models.ForeignKey(FlexTable, on_delete=models.CASCADE, related_name="flex_record")

    def __str__(self):
        return str(self.id)
    
class FileStorageTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_type = models.CharField(max_length=255,blank=True)
    file=models.FileField(upload_to=rename_file)

    def save(self, *args, **kwargs):
        if self.file:
            # Determine the file type using mimetypes or file extension
            file_path = self.file.name
            file_extension = os.path.splitext(file_path)[-1]
            mime_type, _ = mimetypes.guess_type(file_path)
            
            # Assign file type (fallback to file extension if MIME type is unavailable)
            self.file_type = mime_type if mime_type else file_extension.lower()
        
        # Call the parent save method
        super().save(*args, **kwargs)

# class FlexTableField(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     field_name = models.TextField(blank=False)
#     field_type = models.TextField(blank=False)
#     field_data= models.JSONField()
#     table = models.ForeignKey(FlexTable, on_delete=models.CASCADE, related_name="flex_field")

#     def __str__(self):
#         return self.field_name
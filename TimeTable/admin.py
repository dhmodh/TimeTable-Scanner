from django.contrib import admin
from .models import UserCreationModel, ScanTimeTableModel, DeveloperModel, SubjectFaculty
# Register your models here.

admin.site.register(UserCreationModel)
admin.site.register(ScanTimeTableModel)
admin.site.register(DeveloperModel)
admin.site.register(SubjectFaculty)
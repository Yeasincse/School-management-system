from django.contrib import admin
from . import models

admin.site.register(models.UserProfile)
admin.site.register(models.AvailableUser)

admin.site.register(models.School)
admin.site.register(models.Class)
admin.site.register(models.Section)

admin.site.register(models.Teacher)
admin.site.register(models.Parent)
admin.site.register(models.Student)
admin.site.register(models.Librarian)
admin.site.register(models.Subject)

from django.db import models

from account import models as mod


class ClassRoutine(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    section = models.ForeignKey(mod.Section, on_delete=models.CASCADE)
    subject = models.ForeignKey(mod.Subject, on_delete=models.CASCADE)

    day = models.CharField(max_length=30, null=True, blank=True)
    period = models.IntegerField(null=True, blank=True)
    start_hour = models.TimeField(null=True, blank=True)
    end_hour = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.day) + "-" + str(self.period)


class ExamRoutine(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    subject = models.ForeignKey(mod.Subject, on_delete=models.CASCADE)

    exam_name = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    start_hour = models.TimeField(null=True, blank=True)
    end_hour = models.TimeField(null=True, blank=True)

    def __str__(self):
        return str(self.school) + "-" + str(self.classes.name) + "-" + str(self.date)


#office notice model
class Notice(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    classes = models.ForeignKey(mod.Class, on_delete=models.CASCADE)
    user = models.ForeignKey(mod.UserProfile, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.classes.name) + "-" + str(self.user.username)


#gallary image upload model
class GallaryImage(models.Model):
    school = models.ForeignKey(mod.School, on_delete=models.CASCADE)
    user = models.ForeignKey(mod.UserProfile, on_delete=models.CASCADE)

    description = models.TextField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='school/gallary/', null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.school.name) + "-" + str(self.user.username)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(GallaryImage, self).delete(*args, **kwargs)
        storage.delete(path)

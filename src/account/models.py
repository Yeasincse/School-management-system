from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# available registration scope
class AvailableUser(models.Model):
    """available registration scope for this application"""

    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


# multi school model
class School(models.Model):
    """School model for register many school"""

    name = models.CharField(max_length=255, null=True, blank=True, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    logo = models.ImageField(upload_to='school/logo/', null=True, blank=True)
    banner = models.ImageField(upload_to='school/banner/', null=True, blank=True)
    address = models.TextField(max_length=1000, blank=True, null=True)
    website = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


# class model
class Class(models.Model):
    """Add class referring to particular school."""

    school = models.ForeignKey(School, on_delete=models.CASCADE)

    # class name means for : if class 1 we need to write 'one'.
    name = models.CharField(max_length=255, null=True, blank=True)

    # class name means for : if class 1 we need to write 1.
    name_with_int = models.IntegerField(null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.school) + " - " + str(self.name_with_int)


# section model
class Section(models.Model):
    """Add section reffering to particular school and particular class.
        We consider one class has many section with name.
    """

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.school.name) + " - " + str(self.classes.name_with_int) + " : " + str(self.name)

#subjects
class Subject(models.Model):
    """Add class subjects"""

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.school) + "-" + str(self.classes) + ":" + self.name

# teacher registration
class Teacher(models.Model):
    position = models.CharField(max_length=255, null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    gender = models.CharField(max_length=255, default='male', null=True, blank=True)

    def __str__(self):
        return self.position


# parent registration
class Parent(models.Model):
    profession = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.profession


# students registration
class Student(models.Model):
    roll = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, default='male', null=True, blank=True)
    school_bus = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.roll

# librarian registration
class Librarian(models.Model):
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(default='male', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.gender


# user profile manager
class UserProfileManager(BaseUserManager):
    """Helps django work with our custom user model"""

    def create_user(self, username, email, name=None, phone=None, address=None, account_type=None, photo=None, school=None, teacher=None, parent=None, classes=None, section=None, librarian=None, password=None):
        """creates a new user profile objecs"""

        if not email:
            raise ValueError('User must have an email address!')

        if not username:
            raise ValueError('User must have an username!')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, name=name, phone=phone, address=address, account_type=account_type, photo=photo, school=school, teacher=teacher, parent=parent, classes=classes, section=section, librarian=librarian)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """creates and saves a new super user with given details"""

        user = self.create_user(username=username, email=email, password=password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


# user profile model
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a user profile inside our system"""

    member_type = models.ForeignKey(AvailableUser, default=1, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(max_length=1000, null=True, blank=True)

    # account type is the post of the official
    account_type = models.CharField(max_length=255, default='admin', blank=True, null=True)

    photo = models.ImageField(upload_to='profile/picture/', default='no-img.jpg', null=True, blank=True)

    # for account type school and other's common fields
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # for member type teacher
    teacher = models.ForeignKey(Teacher, null=True, blank=True)

    # for member type parent
    parent = models.ForeignKey(Parent, null=True, blank=True)

    # for member type student
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, blank=True)

    # for member type librarian
    librarian = models.ForeignKey(Librarian, null=True, blank=True)

    added_on = models.DateTimeField(auto_now_add=True)

    is_school = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def get_full_name(self):
        """Used to get a users full name."""

        return self.username

    def get_short_name(self):
        """Used to get a users short name."""

        return self.username

    def __str__(self):
        """Django uses this when it needs to convert the object to a string"""

        return self.username + "-" + str(self.member_type)



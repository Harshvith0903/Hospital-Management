from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    GENDER_CHOICE = (
        ('male', 'male'),
        ('female', 'female')
    )
    username = models.CharField(max_length=255, default='Null', unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default='null')
    age = models.IntegerField(default=10)
    contact = models.CharField(max_length=13, default='+000000000000')

    def __str__(self):
        return self.username

class Doctor(models.Model):
    GENDER_CHOICE = (
        ('male', 'male'),
        ('female', 'female')
    )
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default='null')
    age = models.IntegerField()
    education = models.CharField(max_length=300, default='No data')
    speciality = models.CharField(max_length=255, default='Null')

    def __str__(self):
        return "Dr. "+ self.name

class Hospital(models.Model):
    name = models.CharField(max_length=255, unique=True, default='Null')
    address = models.CharField(max_length=1000, unique=True, default='Null')
    phone_number = models.CharField(max_length=13, default='+000000000000')
    email_address = models.CharField(max_length=255, default='Null')
    city = models.CharField(max_length=255, default='Null')
    def __str__(self):
        return self.name
    
class DocInHospital(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Emergency(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255, default="NULL")
    emergency = models.CharField(max_length=300, default='Null')
    description = models.CharField(max_length=300, default='Null')

    def __str__(self):
        return self.id


class Appointment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255, default="NULL")
    description = models.CharField(max_length=255, default="Null")
    appointment_date = models.DateTimeField()
    def __str__(self):
        return self.patient_name
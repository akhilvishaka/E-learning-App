from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def discount(self):
        discount = (self.price / 100) * 10
        return discount

    def __str__(self):
        return self.name


class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgary'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Order(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    levels = models.PositiveIntegerField()
    ORDER_STATUS_CHOICES = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    order_status = models.CharField(default=1, max_length=15)
    order_date = models.DateField()

    def __str__(self):
        return self.student.username

    def total_cost(self):
        return Course.objects.aggregate('price')

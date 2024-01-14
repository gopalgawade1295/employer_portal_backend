from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings


class Company(models.Model):
    companyname = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=300, null=True, blank=True)
    district = models.CharField(max_length=300, null=True, blank=True)
    taluka = models.CharField(max_length=300, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pincode = models.DecimalField(
        max_digits=6, decimal_places=0, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    isVerified = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.companyname


class Posts(models.Model):
    companyreq = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True)
    jobname = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True, default=0)
    uid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return str(self.jobname)


class Usercompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    companynew=models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    companyname = models.CharField(max_length=300, null=True, blank=True)
    state = models.CharField(max_length=300, null=True, blank=True)
    district = models.CharField(max_length=300, null=True, blank=True)
    taluka = models.CharField(max_length=300, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pincode = models.DecimalField(
        max_digits=6, decimal_places=0, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    isVerified = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.companyname


class Userposts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    companyreq = models.ForeignKey(
        Company, on_delete=models.CASCADE, null=True)
    companynew = models.ForeignKey(
        Usercompany, on_delete=models.CASCADE, null=True)
    jobname = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    count = models.IntegerField(null=True, blank=True, default=0)
    uid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return str(self.jobname)

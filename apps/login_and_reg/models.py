from sre_constants import error
from django.db import models
import re

class User_Manager(models.Manager):
    def basic_validator(post_data):
        errors = {}
        NAME_REGEX = re.compile(r'^[A-Za-Z\'\s\.\-]{2.32}$')
        EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\._\-]+@[A-Za-z0-9\.\_\-]+\.[A-Za-z0-9]+$')
        PASSWORD_REGEX = re.compile(r'^.{8,64}$')

        if not NAME_REGEX.match(post_data['first_name']) or not NAME_REGEX.match(post_data['last_name']):
            errors['Invalid name'] = "First and last name must be between 2 and 32 valid characters"

        if not EMAIL_REGEX.match(post_data['email']):
            errors['invalid_email'] = "Email is invalid"

        if not PASSWORD_REGEX.match(post_data['password']):
            errors['password'] = "Password must be at least 8 characters"

        if post_data['confirm'] != post_data['password']:
            errors['password_no_match'] = "Password fields do not match"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)

    objects = User_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
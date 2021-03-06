from django.db import models
import re

class User_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        NAME_REGEX = re.compile(r'^[A-Za-z\'\s\.\-]{2,32}$')
        EMAIL_REGEX = re.compile(r'^[A-Za-z0-9\._\-]+@[A-Za-z0-9\.\_\-]+\.[A-Za-z0-9]+$')
        PASSWORD_REGEX = re.compile(r'^.{8,64}$')

        if 'email' in post_data:
            if not NAME_REGEX.match(post_data['first_name']) or not NAME_REGEX.match(post_data['last_name']):
                errors['Invalid name'] = "First and last name must be between 2 and 32 valid characters"

            if not EMAIL_REGEX.match(post_data['email']):
                errors['invalid_email'] = "Email is invalid"

            if User.objects.filter(email = post_data['email'].lower()):
                errors['duplicate_email'] = "Email already in use"

        if 'password' in post_data:
            if not PASSWORD_REGEX.match(post_data['password']):
                errors['password'] = "Password must be at least 8 characters"

            if post_data['confirm'] != post_data['password']:
                errors['password_no_match'] = "Password fields do not match"

        if 'user_level' in post_data:
            if int(post_data['user_level']) < 0 or int(post_data['user_level']) > 9:
                errors['user_level'] = "Invalid user_level"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    description = models.TextField(default="")
    user_level = models.IntegerField()
        # 9: Owner
        # 7: Admin
        # 1: Normal
        # 0: Unregistered

    #Foreign Keys:
        # messages
        # messages_posted
        # comments
    objects = User_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def role(self):
        roles = {
            '9': "Owner",
            '7': "Admin",
            '1': "Normal",
            '0': "Deactivated",
        }
        return roles[ str(self.user_level) ]

    def date_year_created(self):
        return self.created_at.date().strftime('%b %-d, %Y')

    def most_recent_post(self):

        recent_message = self.messages_posted.order_by('-created_at').first()
        recent_comment = self.comments.order_by('-created_at').first()

        if recent_message != None and recent_comment == None:
            return recent_message
        elif recent_comment != None and recent_message == None:
            return recent_comment
        else:
            print("Comparing comment times")
            print(f'Recent message: {recent_message.created_at}')
            print(f'Recent comment: {recent_comment.created_at}')
            if recent_message.created_at > recent_comment.created_at:
                return recent_message
            else:
                return recent_comment
from django.db import models
from ..login_and_reg.models import *

class Message_Comment_Manager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['text']) < 1:
            errors['no_text'] = "Please enter a message"
        
        return errors

class Message(models.Model):
    text = models.TextField()
    recipient = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="messages_posted", on_delete=models.CASCADE)

    #Foreign Keys:
        # comments
    objects = Message_Comment_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def time_passed(self):
        return "Time passed placeholder"

class Comment(models.Model):
    text = models.TextField()
    message = models.ForeignKey(Message, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

    objects = Message_Comment_Manager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def time_passed(self):
        return "Time passed placeholder"
        #add hover to see actual time?
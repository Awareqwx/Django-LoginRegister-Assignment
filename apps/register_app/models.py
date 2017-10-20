# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def registerValidate(self, post):
        errors = []
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post.get("firstname", "")) < 2:
            errors.append("First Name must be longer than 1 character")
        if len(post.get("lastname", "")) < 2:
            errors.append("Last Name must be longer than 1 character")
        if len(post.get("email", "")) <= 0:
            errors.append("Email cannot be blank")
        elif not EMAIL_REGEX.match(post.get("email", "")):
            errors.append("Please enter a valid email")
        if len(post.get("password", "")) < 8:
            errors.append("Password must be at least 8 characters")
        elif post.get("password", "") != post.get("pwconfirm", ""):
            errors.append("Passwords did not match")
        return errors
    def loginValidate(self, post):
        errors = []
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post.get("email", "")):
            errors.append("Please enter a valid email")
        if not len(post.get("password", "")):
            errors.append("Please enter a password")
        return errors
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=60)
    objects = UserManager()
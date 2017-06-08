from __future__ import unicode_literals
from django.db import models

import bcrypt
import re

class UserManager(models.Manager):
    def email_validation(self, email):
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if(email_regex.match(email)):
            return True
        else:
            return False


    def login(self, email, password):
        errors = []
        if not(self.email_validation(email)):
            errors.append('Valid email required')
        
        else:
            user = User.objects.get(email=email)

            # check passwords match
            # password = password.encode('utf8')
            if user and bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
                return {
                    'user': {
                        'id': user.id,
                        }
                }
            else: 
                errors.append('Incorrect password')

        return {'errors': errors}

    def register(self, info):
        errors = []

        # Validations
        if not('name' in info) or len(info['name']) < 2:
            errors.append('Name required; No fewer than 2 characters; letters only')

        if not('email' in info) or not(self.email_validation(info['email'])):
            errors.append('Valid email required')

        
        if not('dob' in info) or len(info['dob']) < 4:
            errors.append('Date of birth required')

        if not('password' in info) or not('password_confirm' in info) or len(info['password']) < 8 or not(info['password'] == info['password_confirm']):
            errors.append('Password required; No fewer than 8 characters in length; Passwords must match')

        if len(errors) == 0:
            # Check if email is already saved
            current_uesrs = User.objects.filter(email = info['email'])

            if len(current_uesrs) > 0:
                errors.append('Email taken')
            else:
                # Password encryption
                info['password'] = info['password'].encode('utf8')
                info['password'] = bcrypt.hashpw(info['password'], bcrypt.gensalt())

                # Save new user to DB
                User.objects.create(
                    name = info['name'],
                    email = info['email'],
                    password = info['password'],
                    d_o_b = info['dob']
                )

                added_user = User.objects.get(email=info['email'])
                
                return {
                    'new_user': added_user
                }

        return {
            'errors': errors
        }

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=100)
    d_o_b = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
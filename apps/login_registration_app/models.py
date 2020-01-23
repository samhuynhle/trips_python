from django.db import models
from time import localtime, strftime, strptime
from datetime import date, datetime
import re
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        all_users = User.objects.all()
        all_users_emails = []
        for x in all_users:
            all_users_emails.append(x.email)


        if postData['register_login'] == 'register':
            birthday = datetime.strptime(postData['birthday'], '%Y-%M-%d')
            age = calculate_age(birthday)

            if len(postData['first_name']) < 2:
                errors['title'] = "User first name should be more than 3 characters"
            if len(postData['last_name']) < 2:
                errors['title'] = "User last name should be more than 3 characters"
            if not EMAIL_REGEX.match(postData['email']):            
                errors['email'] = ("Invalid email address!")
            if postData['email'] in all_users_emails:
                errors['title'] = "Email alreay exists"
            if postData['birthday'] > strftime("%Y-%m-%d", localtime()):
                errors['birthday'] = "Birthday should be in the past"
            if age < 13:
                errors['age'] = "Must be 13 years old or older"
            if len(postData['password']) < 6:
                errors['password_length'] = "Password should be more than 6 characters"
            if postData['password'] != postData['confirm_password']:
                errors['password'] = "Password does not match Confirm Password!"

            return errors

        if postData['register_login'] == 'login':
            if postData['email'] not in all_users_emails:
                errors['title'] = "Email does not exist"
                return errors
            current_user = User.objects.get(email = postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), current_user.password.encode()):
                print("Password OK")
            else:
                errors['password'] = "Invalid password"
            return errors

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    birthday = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __repr__(self):
        return f"<User object: {self.id}>"

def calculate_age(born):
    today = date.today()
    return today.year - born.year - \
           ((today.month, today.day) < (born.month, born.day))
from django.db import models


from django.contrib.auth.models import User



# Create your models here.
class user_table(models.Model):
    LOGIN=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    designation=models.CharField(max_length=200)
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()


class complaint_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=1000)
    reply=models.CharField(max_length=1000)
    date=models.DateField()

class tips_table(models.Model):
    title=models.CharField(max_length=200)
    tipdetails=models.CharField(max_length=1000)
    date=models.DateField()

class feedback_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    rating=models.FloatField()
    date=models.DateField()
    feedback = models.CharField(max_length=1000)

class image_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    image_path=models.CharField(max_length=200)
    output_file=models.CharField(max_length=200)
    date=models.DateField()

class text_table(models.Model):
    USER=models.ForeignKey(user_table,on_delete=models.CASCADE)
    text_input=models.CharField(max_length=2000)
    output_format=models.CharField(max_length=200)
    generated_code=models.CharField(max_length=5000)
    date=models.DateField()














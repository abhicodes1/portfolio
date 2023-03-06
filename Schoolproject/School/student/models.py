from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

# Create your models here.
class_choices= (
    ("I","I"),
    ("II","II"),
    ("III","III"),
    ("IV","IV"),
    ("V","V"),
    ("VI","VI"),
    ("VII","VII"),
    ("VIII","VIII"), 
    ("IX","IX"),        
    ("X","X"), 
    ("XI","XI"), 
    ("XII","XII"),
    #("ID,"humanReadable") called choicelist  
)

fee_choices=(
    ('1','1st month'),
    ('2','2nd month'),
    ('3','3rd month'),
    ('4','4th month'),
    ('5','5th month'),
    ('6','6th month'),
    ('7','7th month'),
    ('8','8th month'),
    ('9','9th month'),
    ('10','10th month'),
    ('11','11th month'),
    ('12','12th month'),
)

attendance_choices=(
    ('present','present'),
    ('absent','absent'),
)

class stu_cls_model(models.Model):
    class_name=models.CharField(choices=class_choices,max_length=20, null= True, default=1)
    mothly_fee=models.PositiveIntegerField()
    def __str__(self):
        return self.class_name

class Student(User):
    fathername= models.CharField(max_length=40)
    clas=models.ForeignKey(stu_cls_model, on_delete=models.CASCADE,null=True, blank= True)
    address=models.CharField(max_length=200)
    contact= models.CharField(max_length=15)
    fee_status=models.CharField(max_length=20,choices=fee_choices,default=1)
    fee=models.BigIntegerField(default=200)
    gen_cat= models.BooleanField(default=False)
    admitted_on=models.DateTimeField(auto_now=True)
    roll= models.BigIntegerField(null=True)
    fee_received_by=models.CharField(max_length=30,null= True)
    is_present_today=models.CharField(max_length=15, default="absent", blank = True)
   
class attendance(models.Model):
    name=models.CharField(max_length=30, null=True, blank=True)
    attdate=models.CharField(max_length=20, null=True, blank= True)
    is_present=models.CharField(max_length=20, null=True, blank= True)
    
    def __str__(self):
        return self.name 

class notification(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    text= models.TextField()
    users= models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    is_read= models.BooleanField(default=False)
    
    def __str__(self):
        return self.text


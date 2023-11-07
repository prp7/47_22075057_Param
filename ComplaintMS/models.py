from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser,PermissionsMixin
from django.db.models.query import QuerySet
from django.utils import timezone
from .manager import CustomUserManager
from enum import Enum
from datetime import timedelta,datetime
from djtriggers.models import Trigger

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    class Types(models.TextChoices):
        Administrator = "Administrator","ADMINISTRATOR"
        Student = "Student","STUDENT"

    default_type = Types.Student

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()

    type = models.CharField('Type', max_length=255, choices=Types.choices, default=default_type)

    def __str__(self):
        return self.email
    

    def changeType(self):
        self.type=self.Types.Administrator
    

    def save(self,*args,**kwargs):
        if not self.id:
            self.type = self.default_type
        return super().save(*args,**kwargs)

class AdministratorAdditional(models.Model):
    user = models.OneToOneField(CustomUser,on_delete = models.CASCADE)
    phone = models.CharField(max_length=13,null=True)
    domain = models.ForeignKey('Domain',on_delete=models.SET_NULL,null=True)

class AdministratorManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type = CustomUser.Types.Administrator) 
    

class StudentManager(models.Manager):
    def get_queryset(self,*args,**kwargs):
        return super().get_queryset(*args,**kwargs).filter(type = CustomUser.Types.Student)

class Administrator(CustomUser):
    default_type= CustomUser.Types.Administrator
    objects = AdministratorManager()

    class Meta:
        proxy = True

    @property
    def showAdditional(self):
        return self.AdministratorAdditional

class Student(CustomUser):
    default_type = CustomUser.Types.Student
    objects = StudentManager()

    class Meta:
        proxy = True
    # @property
    # def showAdditional(self):
    #     return self.StudentAdditional
    

class Domain(models.Model):
    class Domain_Choices(Enum):
        Hostel='Hostel'
        Library='Library'
        Department='Department'

    
    domain = models.CharField(max_length=20,
                            choices=[(D.name,D.value) for D in Domain_Choices],
                            default=Domain_Choices.Hostel.value)
    domain_name = models.CharField(max_length=50,null=False)
    
    def __str__(self):
        return f'{self.domain_name} ({self.domain})'

class Category(models.Model):
    class Category_Choices(Enum):
        Electricity='Electricity'
        Carpentry='Carpentry'
        Plumbing='Plumbing'
        Food='Food'
        Water='Water'
        Cleaning='Cleaning'
    name = models.CharField(
        max_length=50,
        choices=[(C.name,C.value) for C in Category_Choices],
        default=Category_Choices.Cleaning.value
    )
    def __str__(self):
        return self.name

class Complaints(models.Model):
    class Status_Choices(Enum):
        Opened = 'Opened'
        In_progress='In_progress'
        Resolved = 'Resolved'
        Closed = 'Closed'
    
    issuer = models.ForeignKey(Student,on_delete=models.SET_NULL,null=True,related_name='issuer')
    domain = models.ForeignKey(Domain,on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    issue = models.TextField()
    status = models.CharField(
        max_length=50,
        choices = [(S.name,S.value) for S in Status_Choices],
        default = Status_Choices.Opened.value
    )
    date_issued=models.DateTimeField(auto_now_add=True)
    date_resolved=models.DateTimeField(null=True,blank=True)
    date_assigned = models.DateTimeField(null=True,blank=True)
    is_unaddressed= models.BooleanField(default=True)
    is_deleted=models.BooleanField(default=False)
    assignee = models.ForeignKey('Workers',on_delete=models.SET_NULL,null=True)
    assigner=models.ForeignKey(Administrator,on_delete=models.SET_NULL,null=True,related_name='assigner')

    def __str__(self):
        return f'{self.issuer.name} ({self.date_issued})'
    
    def addressed(self):
        self.is_unaddressed=False

class Workers(models.Model):
    class WStatus_Choices(Enum):
        Available = 'Available'
        On_leave='On_leave'
        Occupied = 'Occupied'
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    status = models.CharField(max_length=20,choices=[(D.name,D.value) for D in WStatus_Choices],default='Available')
    task_count=models.IntegerField(default=0)
    leave_rsn=models.TextField(blank=True)
    date_from=models.DateField(null=True)
    date_to=models.DateField(null=True)

    def __str__ (self):
        return self.name
    
    def inc_count(self):
        self.task_count=self.task_count+1
    def dec_count(self):
        if(self.task_count):
            self.task_count=self.task_count-1

class leave_trigger(Trigger):
    class Meta:
        # There is no trigger specific data so make a proxy model.
        # This ensures no additional db table is created.
        proxy = True
    typed = 'leave_trigger'
    worker_id=0
    def _process(self, dictionary={'w_id':worker_id}):
        print('Trigger is working','worker_id:',sep='  ')
        w_obj=None
        w_obj=Workers.objects.get(id=dictionary['w_id'])
        if w_obj:
            if(w_obj.status=='On_leave'):
                w_obj.status='Available'
            if( not w_obj.date_from):
                w_obj.date_from=None
            if( not w_obj.date_to):
                w_obj.date_to=None
            if not w_obj.leave_rsn:
                w_obj.leave_rsn=""
            w_obj.save()

            
class Reviews(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    complaint = models.ForeignKey(Complaints,on_delete=models.SET_NULL,null=True)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'review {self.student.name} #{self.complaint.pk}'

    
    

    

# Create your models here.







# domain_dict={
#     'Hostel':['Aryabhatta','Satish Dhawan','Vishweshvaraiya','Limbdi'],
#     'Department':['CSE','ECE','EEE','APM'],
#     'Library':['SDL']
#     }
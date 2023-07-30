from django.db import models
from django.contrib.auth.models import User
#from PIL import Image
# Create your models here.
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

class Category(models.Model):
    title = models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username



class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.user.username

class Service(models.Model):
    title = models.CharField(max_length=100)
    available = models.BooleanField(default=False)
    basic_price = models.FloatField()
    release_date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=1000)
    def __str__(self):
        return self.title
    
class Tool(models.Model):
    tool_name = models.CharField(max_length=25)
    def __str__(self):
        return self.tool_name
    
class Project(models.Model):
    tool = models.ManyToManyField(Tool,null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE,null=True, blank=True)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    description = models.CharField(max_length=1000,null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    expected_end_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    pricing = models.FloatField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    ALL_STATUS = (
        ('O','Ongoing'),
        ('F','Finished'),
        ('U','Under negotiation'),
    )
    status = models.CharField(max_length=1, choices=ALL_STATUS,default=3)

class Price_proposal(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    pricing_proposal = models.FloatField()
    completion_duration_proposal  = models.CharField(max_length=30)
    ALL_STATUS = (
        ('E','Accepted'),
        ('R','Rejected'),
        ('P','Pending'),
    )
    status = models.CharField(max_length=1, choices=ALL_STATUS)
    def __str__(self):
        return self.title
    
class Test(models.Model):
    title = models.CharField(max_length=100)
    discription = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    
class Skill(models.Model):
    title = models.CharField(max_length=100)
    required_grade = models.FloatField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Service_skill(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

class Has_service(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    Score_rating = models.FloatField()
    Delay_compliance = models.FloatField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    ALL_STATUS = (
        ('E','Enabled'),
        ('D','Disabled'),
        ('P','Pending'),
    )
    status = models.CharField(max_length=1, choices=ALL_STATUS)

class Test_result(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    test_result = models.FloatField()

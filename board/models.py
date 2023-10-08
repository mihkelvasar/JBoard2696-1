from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .functions import validate_motivation
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_of_birth = models.DateField(default=None, null=True, help_text="YYYY-MM-DD")
    email = models.EmailField(blank=True)
    first_name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    company_name = models.CharField(blank=True, max_length=200)
    creg_number = models.CharField(blank=True, max_length=8)
    company_descript = models.TextField(blank=True, max_length=500)
    is_seeker = models.BooleanField(default=False, help_text="Registering to seek employees? Tick this!")
    # User groups Seeker and Jobless use the same User and UserProfile models,
    # just Seeker has access to more fields when registering or editing.


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    def __str__(self):
        return f"User {self.user.username}'s Profile. {self.user.username} represents a company: {self.company_name}"
    #Upon creation of a User object, a corresponding UserProfile object is also created.
    #This renders all User objects, including superusers, created before migrations, unusable and throwing errors. 



class Curriculum(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cv_fname = models.CharField(blank=True, max_length=100)
    cv_lname = models.CharField(blank=True, max_length=100)
    cv_dob = models.DateField(default=None, null=True, help_text="YYYY-MM-DD")
    cv_email = models.EmailField(blank=True)
    cv_date = models.DateField(auto_now=True)
    cv_education = models.TextField(max_length=500)
    cv_career = models.TextField(max_length=700)
    cv_skills = models.TextField(max_length=500)
    cv_other = models.TextField(null=True, max_length=700)

    def __str__(self):
        return f"User {self.cv_lname}'s CV, last updated at {self.cv_date}"
    #Every user should only have one CV


class JobPosition(models.Model):
    job_user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=100)
    job_email = models.EmailField(blank=True, max_length=100)
    job_source = models.CharField(null=True, max_length=100)
    job_desc = models.TextField(max_length=500)
    job_field = models.CharField(max_length=100)
    job_skills = models.TextField(max_length=500)
    job_date = models.DateField(auto_now=True)
    job_about = models.TextField(blank=True, max_length=500)
    published = models.BooleanField(default=True, help_text="Untick to save as draft")

    def get_absolute_url(self):
        return reverse("onejob", kwargs={"pk": self.pk})
    

class JobApply(models.Model):
    apply_id = models.AutoField(primary_key=True)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    sourcejob = models.ForeignKey(JobPosition, on_delete=models.CASCADE)
    motivation = models.TextField(max_length=700, default="Why do you want to work for us?", validators=[validate_motivation])
    applydate = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.applicant.username + "Job application"
    #Modeled after blog comment examples. 
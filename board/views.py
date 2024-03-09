from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from .models import *
from .forms import *
from . import forms
from .functions import *
#superuser - pixelad
#pw - samantha23

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.

def front(request):
    job_list = JobPosition.objects.filter(published=True).order_by("job_date") #shows only posts which are not drafts
    context = {"job_list" : job_list}
    return render(request, "board/front.html", context) 
    

def sign_up(request): 
    if request.method =="POST":
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user.userprofile.first_name = user_form.cleaned_data.get("first_name")
            user.userprofile.last_name = user_form.cleaned_data.get("last_name")
            user.userprofile.email = user_form.cleaned_data.get("email")
            user.userprofile.date_of_birth = user_form.cleaned_data.get("date_of_birth")
            user.userprofile.is_seeker = user_form.cleaned_data.get("is_seeker")
            user.userprofile.company_name = user_form.cleaned_data.get("company_name")
            user.userprofile.creg_number = user_form.cleaned_data.get("creg_number")
            user.save()
            my_jobless = Group.objects.get(name="Jobless")
            my_seeker = Group.objects.get(name="Seeker")
            if user.userprofile.is_seeker == True:
                my_seeker.user_set.add(user)
            else:
                my_jobless.user_set.add(user)
            return redirect("board:front")
        
    else:
        user_form = RegisterForm()
        return render(request, 'board/registration.html', {'user_form' : user_form})      
    #OPTION 8 - CRUNCHYDATA JUNE 22, 2020 BLOG POST - WORKS

def login_page(request):
    form = forms.LoginForm()
    if request.method =="POST":
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                if user.is_active:
                    request.session.set_expiry(86400)
                    login(request, user)
                    if user.groups.filter(name="Jobless").exists():
                        return redirect('board:userhome')
                    elif user.groups.filter(name="Seeker").exists():
                        return redirect('board:seekerview')
                    else:
                        return redirect('board:front')
            else:
                message = "Did you use the right username and password?"
                return render(request, 'board/login.html', {'form': form, "message" : message})
    else:
        return render(request, 'board/login.html', {'form': form})

@login_required   
def logout_request(request):
    logout(request)
    return redirect("board:front")

@login_required
@user_passes_test(is_seeker)
def seekerview(request): #html exists
    current_user = request.user
    j = None
    seeker_job_list = JobPosition.objects.filter(job_user=current_user)
    for i in seeker_job_list:
            j = i.job_id
    applications = JobApply.objects.filter(sourcejob=j)
    context={
        "current_user" : current_user,
        "seeker_job_list" : seeker_job_list,
        "applications" : applications,
        
    }
    return render(request, "board/seekerview.html", context=context)

@login_required
@user_passes_test(is_seeker)
def jobcreate(request): #html exists
    employer = request.user
    employer_profile = employer.userprofile

    if request.method=="POST":
        form = JobPositionForm(request.POST, files=request.FILES)
        if form.is_valid():
            newjob = form.save(commit=False)
            newjob.job_user = employer
            newjob.email = employer_profile.email
            newjob.job_source = employer_profile.company_name
            newjob.job_about = employer_profile.company_descript
            newjob.save()
            return redirect("board:seekerview") 
    else:
        form = JobPositionForm()
        return render(request, 'board/jobcreate.html', {"form" : form})
    

def singlejobview(request, pk): #html exists
    try:
        job_one = JobPosition.objects.get(job_id=pk) 
    except JobPosition.DoesNotExist:
        raise Http404("The job posting does not exist")
    return render(request, "board/openingsingle.html", {"job_one" : job_one})

@login_required
@user_passes_test(is_seeker)
def seekeroneview(request, pk):
    try:
        job_one = JobPosition.objects.get(job_id=pk)
        applications = JobApply.objects.filter(sourcejob=job_one) 
    except JobPosition.DoesNotExist:
        raise Http404("The job posting does not exist")
    return render(request, "board/seekeroneview.html", {"job_one" : job_one, "applications" : applications})

@login_required
@user_passes_test(is_seeker)
def jobpublish(request, pk): 
    opening = JobPosition.objects.get(job_id=pk)
    if request.method == "POST":
        if opening.published == False:
            opening.published = True
            opening.save()
            return redirect ("board:seekerview")

@login_required
@user_passes_test(is_seeker)
def jobunpublish(request, pk): 
    opening = JobPosition.objects.get(job_id=pk)
    if request.method == "POST":
        if opening.published == True:
            opening.published = False
            opening.save()
            return redirect ("board:seekerview")

@login_required
@user_passes_test(is_seeker)
def jobdelete(request, pk): #Html exists.
    opening = JobPosition.objects.get(job_id=pk)
    if request.method == "POST":
        opening.delete()
        return redirect("board:seekerview")
    else:
        return redirect("board:seekerview")

@login_required
@user_passes_test(is_seeker)
def jobedit(request, pk): #html exists. 
    employer = request.user
    employer_profile = employer.userprofile
    job =JobPosition.objects.get(job_id=pk)
    if request.method=="POST":
        form = JobPositionForm(request.POST)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.job_user = employer
            edit.job_source = employer_profile.company_name
            edit.job_id = job.job_id
            edit.save()
            return redirect("board:seekerview")
        else:
            form = JobPositionForm(initial=model_to_dict(job))
            return render(request, 'board/jobedit.html', {'form' : form})
    else:
        form = JobPositionForm(initial=model_to_dict(job))
        return render(request, 'board/jobedit.html', {'form' : form})


@login_required
@user_passes_test(is_jobless)
def userview(request): #html exists
    apply_list = None
    try:
        jobless = request.user
        message = "You have not created a CV yet"
        seevee = Curriculum.objects.get(profile=jobless)
        apply_list = JobApply.objects.filter(applicant=jobless)
    except Curriculum.DoesNotExist:
        return render(request, "board/userview.html", {"jobless" : jobless, "message" : message, "apply_list" : apply_list})
    return render(request, "board/userview.html", {"jobless" : jobless, "seevee" : seevee, "apply_list" : apply_list})


@login_required
@user_passes_test(is_jobless)
def cvcreate(request):
    employer = request.user
    employer_profile = employer.userprofile
    if request.method=="POST":
        form = CurriculumForm(request.POST)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.profile = employer
            cv.cv_email = employer_profile.email
            cv.cv_fname = employer_profile.first_name
            cv.cv_lname = employer_profile.last_name
            cv.cv_dob = employer_profile.date_of_birth
            cv.save()
            return redirect ("board:seecv")
        else:
            message = "Please check your input for errors"
            form = CurriculumForm()
            return render(request, 'board/newcv.html', {"form" : form, "message" : message})
    else:
        form = CurriculumForm()
        return render(request, 'board/newcv.html', {"form" : form})

@login_required
@user_passes_test(is_jobless)
def cvview(request): #html exists
    try:
        employer = request.user
        seevee = Curriculum.objects.get(profile=employer)
    except Curriculum.DoesNotExist:
        raise Http404("You have not created a CV yet")
    return render(request, "board/seecv.html", {"seevee" : seevee})


@login_required
@user_passes_test(is_jobless)
def cvedit(request): #HTML exists
    employer = request.user
    employer_profile = employer.userprofile
    notseevee = employer.curriculum #Is it the one-to-one why I cannot access it by objects.get?
    #seevee = Curriculum.objects.get(profile=employer)   
    if request.method == "POST":
        form = CurriculumForm(request.POST)
        if form.is_valid():
            cve = form.save(commit=False)
            cve.profile = employer
            cve.cv_email = employer_profile.email
            cve.cv_fname = employer_profile.first_name
            cve.cv_lname = employer_profile.last_name
            cve.cv_dob = employer_profile.date_of_birth
            cve.save()
            return redirect("board:seecv")
        else:
            form = CurriculumForm(initial=model_to_dict(notseevee))
            return render(request, "board/newcv.html", {'form' : form, 'notseevee' : notseevee})
    else:
        form = CurriculumForm(initial=model_to_dict(notseevee))
        return render(request, "board/newcv.html", {'form' : form, 'notseevee' : notseevee})



@login_required
def change_password(request):
    if request.method=="POST":
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            userd = request.user
            if is_jobless(userd):
                return redirect("board:userhome")
            elif is_seeker(userd):
                return redirect("board:seekerview")
    else:
        password_form = PasswordChangeForm(request.user)
    return render(request, "board/change-password.html", {'password_form' : password_form})


@login_required
@user_passes_test(is_jobless)
def useredit(request): #No html yet
    userb = request.user
    userb_profile = userb.userprofile
    errd = None
    if request.method == "POST":
        account_form = UpdateUserForm(request.POST)
        profile_form = UserProfileEdit(request.POST)
        if profile_form.is_valid():
            usd = account_form.save(commit=False)
            usd.id = userb.id 
            usd.password = userb.password 
            usd.save()
            k = profile_form.save(commit=False)
            k.user = userb
            k.save()
            #messages.success(request, "profile updated successfully")
            return redirect("board:userhome")
        else:
            errd = profile_form.errors
            account_form = UpdateUserForm(initial=model_to_dict(userb))
            profile_form = UserProfileEdit(initial=model_to_dict(userb_profile))
            return render(request, "board/useredit.html", {"profile_form" : profile_form, "account_form" : account_form, 'errd' : errd})
    else:
        account_form = UpdateUserForm(initial=model_to_dict(userb))
        profile_form = UserProfileEdit(initial=model_to_dict(userb_profile))
        return render(request, "board/useredit.html", {"profile_form" : profile_form, "account_form" : account_form})
    


@login_required
@user_passes_test(is_seeker)
def seekeredit(request): #No html yet
    seeker = request.user
    seeker_profile = seeker.userprofile
    errd = None
    if request.method == "POST":
        account_form = UpdateUserForm(request.POST)
        profile_form = SeekerProfileEdit(request.POST)
        if profile_form.is_valid() and account_form.is_valid():
            ede = account_form.save(commit=False)
            ede.id = seeker.id
            ede.password = seeker.password
            ede.save()
            k = profile_form.save(commit=False)
            k.user = seeker
            k.save()
            #messages.success(request, "profile updated successfully")
            return redirect("board:seekerview")
        else:
            #err = account_form.errors
            errd = profile_form.errors
            account_form = UpdateUserForm(initial=model_to_dict(seeker))
            profile_form = SeekerProfileEdit(initial=model_to_dict(seeker_profile))
            return render(request, "board/seekeredit.html", {"profile_form" : profile_form, "account_form" : account_form, 'errd' : errd})
    else:
        account_form = UpdateUserForm(initial=model_to_dict(seeker))
        profile_form = SeekerProfileEdit(initial=model_to_dict(seeker_profile))
        return render(request, "board/seekeredit.html", {"profile_form" : profile_form, "account_form" : account_form})
    


@login_required
@user_passes_test(is_jobless)
def jobapply(request, pk):
    job_object = JobPosition.objects.get(job_id=pk)
    if request.method=="POST":
        form = MotivationForm(request.POST)
        if form.is_valid():
            new_letter = form.save(commit=False)
            new_letter.applicant = request.user
            new_letter.sourcejob = job_object
            new_letter.save()
            #job_object.jobapply_set.add(new_letter) #create a _set object for a nested list -
            #  gave up on trying to get nested lists for seekerview to work
            return redirect ("board:front")
        else:
            form = MotivationForm() #probably not needed, because model.field has a validation check.
            return render(request, "board/motivation.html", {'form' : form})
    else:
        form = MotivationForm()
        return render(request, "board/motivation.html", {'form' : form})
   

@login_required
@user_passes_test(is_jobless)
def applycancel(request, pk):
    application = JobApply.objects.get(apply_id=pk)
    if request.method == "POST":
        if application.is_active == True:
            application.is_active = False
            application.save()
            return redirect ("board:userhome")
        # view to automatically delete application is too complicated to implement.
        # view to delete applications requires additional signaling for the seekerview.
        # rescinding one is enough for demonstration purposes
        # In a fielded app, there would be periodic task to clean up inactive objects anyway


@login_required        
def seeapply(request, pk):
    try:
        application = JobApply.objects.get(apply_id=pk)
        user = application.applicant
        seevee = Curriculum.objects.get(profile=user)
        observer = request.user
    except JobApply.DoesNotExist:
        raise Http404("You have not created a CV yet")
    context= {
        "application" : application,
        "seevee" : seevee,
        "user" : user,
        "observer" : observer
        }
    return render(request, "board/seeapply.html", context)
    #Shows both cv data as well as motivation letter


@login_required
def cvexport(request): #No html yet
    return HttpResponse("You clicked a button to export your CV. Too bad there is no backend for it yet. But buttons exist.")
    #use reportlab
    #looked over reportlab documentations and it feels like a week's worth of work just to get the cv properly drawn

    


#add messages for successes and failures

#add css, maybe only header and footer for buttons and links.


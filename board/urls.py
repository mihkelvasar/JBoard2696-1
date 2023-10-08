from django.urls import path

from . import views

app_name = "board"
urlpatterns = [
    
    path("", views.index, name="index"), #just for testing
    path("front/", views.front, name="front"), #front page of the job board. 
    path("front/<int:pk>", views.singlejobview), #view a single job with or without logging in
    path("login/", views.login_page, name="login"), #log in a User or a Seeker
    path("logout", views.logout_request, name="logout"),
    path("register/", views.sign_up, name="register"), #register a new User
    path("password-change/", views.change_password, name="password-change"),

    path("seekerview/", views.seekerview, name="seekerview"), #seeker home page
    path("seekeredit/", views.seekeredit, name="seekeredit"), #seeker edit profile
    path("seekeroneview/<int:pk>", views.seekeroneview),
    path("jobcreate/", views.jobcreate, name="jobcreate"),
    path("jobedit/<int:pk>", views.jobedit, name="edit_job"),
    path("jobpublish/<int:pk>", views.jobpublish, name="publishjob"),
    path("jobunpublish/<int:pk>", views.jobunpublish, name="unpublishjob"),
    path("jobdelete/<int:pk>", views.jobdelete, name="deletejob"),

    path("userview/", views.userview, name="userhome"), #User home page
    path("useredit/", views.useredit, name="useredit"), #User edit profile
    path("cvcreate/", views.cvcreate, name="newcv"), #create a cv, edit a cv
    path("cvview/", views.cvview, name="seecv"), #look at User's current CV
    path("cvedit/", views.cvedit, name="editcv"),
    
    path("seeapply/<int:pk>", views.seeapply, name="seeapply"), #see application + cv
    path("jobapply/<int:pk>", views.jobapply, name="applyjob"), #apply to a job
    path("applycancel/<int:pk>", views.applycancel, name="applycancel"), #cancel application
    path("motivation/", views.jobapply, name="motivation"), #i need a html, do i need a path?
    
    path("cvexport/", views.cvexport, name="exportcv"), #HttpResponse only
]
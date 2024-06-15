# JBoard2696-1

## What is this?
This my final project for SDA Academy's Python From Scratch course of 2023.
This is an MVP of a Job Board web app written in Python using the Django 4.2 framework.
It uses the sqlite database built into Django

## What does it do?
Users can register to the site and based on data entered on registration, they are separated
into 2 different user groups: Job Posters and Job Seekers.  
Upon login, belonging in either group is checked against and User is directed to appropriate dashboard.  
Users of type Job Posters can edit profile data, CRUD 'job openings' and see who has applied to
their 'job openings' or if an application has been rescinded.  
Users of type Job Seekers can edit profile data, create and update 'CVs' see 'job openings' and apply to them, forwarding their 'CV' and entering a motivation letter to go along. They can also see which jobs they have applied to and rescind their application, making it unavailable to access for Job Posters. 

There is a fully functional (but completely without styling) front end for users to interact with as well as somewhat functional admin view.

## But why?
Originally I was part of a 4 person team but when team lead took 2 weeks to develop a database schema, I decided to do it solo. I wrote it over 14 days and 11 hours per day.  
It showcases basic understanding of Django projects, and interacting with relational databases within framework as well as different relations types. I tried to write it as simple and functional as possible with no complexity for complexity's sake.  
That's why it uses function-based views, no slugs in urls and using sqlite instead of some external sql database. That's also the reason why no real UI design, just text and buttons.

## What's next?
### This project is currently inactive
Doing this project, I learned that many web apps can be reduced to a front end interactions and database operations. Once you have done one or three Django projects, you have done them all, only the details differ.

Working  with this project is currently not a priority.  
But I would like to:  
*fix the errors  
*add even a basic front end design with css and javascript, or maybe some framework.  
*add a full functional testing of the front end using Selenium, preferably written in some other language  
*add unittesting based on Django itself  
*rework the CV and motivation letter objects to take files instead of text input. Then read data from files.  
*export job postings, profiles as pdfs.  
*upload and process images  

## Updates
I figured out basic MarkDown, so I am doing proper ReadMes for all my projects.

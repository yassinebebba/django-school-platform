# django-school-platform

## Description

A complete website (Frontend and Backend) using Django Framework, that allows schools to organise their work.
It comprises of administration, teachers and students with a custom Admin Panel.
Teachers can create, read, update and delete assessments and also grade them. 
and a bunch more cool stuff...
* More features will be added.

## Installation

* Download the repository files from github
* In installed apps in settings add these apps

        INSTALLED_APPS = [
            'management.apps.ManagementConfig'
            'main.apps.MainConfig',
            'students.apps.StudentsConfig',
            'teachers.apps.TeachersConfig',
            
            # ...
        ]

* Comment all code in (views, url, admin, models, signals, forms) in all apps except for:
    * Don't comment main/urls.py
    * In management/urls.py comment all paths inside the urlpatterns list but don't comment the list
    
            urlpatterns = [
                # Comment all paths
            ]

* Open CMD and cd to the folder where manage.py is located
* Use these commands:

            > manage.py makemigrations managment
            > manage.py migrate management
            > manage.py makemigrations
            > manage.py migrate

* Create a superuser:

        > manage.py createsuperuser
        
        # All of these fields are required
        # ['identifier', 'email', 'first_name', 'last_name', 'gender']
        # Admin idenfifier start at this tag (admin10000000) 'admin' + 8 digits
        # it is advisable that you use that identifier for the first admin
        # alternatively you can change that behaviour in the custom user model in the managemnt app
        
* In the same terminal type > manage.py runserver (You shouldn't encounter any problems)
* Login to your admin account and start experimenting with it
    * The admin panel is customised, so you get all CRUD functionalities:
        * Students
        * Teachers
        * Courses
        * and more...
> Note: students ID and teachers ID starts at 20000000 and prof10000000 respectively.
> All identifiers are unique and auto increment when creating a new user.

> Note: When creating an account there will be no option for setting the 
> interested account password, it is all done through the reset password link
> so make sure you supply an active email address. A random password will be set adn the user
> should reset their password.
> Alternately, if you are in a development environment you can use the terminal use the django shell,
> get the interested account instance and then user instance.set_password('Your password here')

> Note: set your email host, port, address and password in settings.py and make sure you enable 
> access to your email, because the email provider won't trust the connection that was made from django.
> The configuration are for Gmail 

## Teacher Panel

In the teacher panel you can create, update, remove and delete assessments.
When you create an assessment a signal will be sent to all students in that class and
create instances with that exam in the ExamGrade table that also provide 2 other fields for
the grade and feedback of the teacher. The teacher will get a link for his/her assessment
in the view assessment page, in the detail view of the interested assessment the teacher
get table with all students that were assigned the interested assessment, ready to be marked
and given feedback, it also could be updated (marked) again should any mistake occur. 

## Student Panel

In the student panel, students can view their assessments outcome and feedback from the teacher.


    
        
 
            
        
        

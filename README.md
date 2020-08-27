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

 
            
        
        

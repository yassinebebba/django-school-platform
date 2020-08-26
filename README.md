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

            
        
        

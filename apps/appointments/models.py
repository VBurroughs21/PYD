from __future__ import unicode_literals
from django.core.validators import MaxValueValidator
from django.db import models
from datetime import datetime
from ..users.models import User

class AppointmentManager(models.Manager):
    def create_appointment(self, user_input):
        errors = self.validations(user_input)

        if len(errors) > 0:
            return {'errors': errors}
        else:
            # Create appointment
            user = User.objects.get(id = user_input['id'])
            appointment = Appointment.objects.create(task = user_input['task'], user = user, status = "Pending", appoint_date = user_input['appoint_date'], appoint_time = user_input['appoint_time'])
            appointment.save()
            
            return {'sucess': ["Appointment created"]}

    def update_appointment(self, appointment):
        errors = self.validations(appointment)

        if len(errors) > 0:
            return {'errors': errors}
        else:
            a = Appointment.objects.get(id = appointment['id'])
            a.task = appointment['task']
            a.status = appointment['status']
            a.appoint_date = appointment['appoint_date']
            a.appoint_time = appointment['appoint_time']
            a.save()
            
            return {'sucess': ["Appointment edits saved"]}


    def validations(self, user_input):
        errors = []

        if not('task' in user_input):
            errors.append('Task Required')

        if not('appoint_time' in user_input):
            errors.append('Time Required')
        
        if not('appoint_date' in user_input):
            errors.append('Date Required')
        else:
            present = datetime.now().strftime('%Y-%m-%d') 

            if not(present <= user_input['appoint_date']):
                errors.append('Date must be in the future')
        
        return errors

        

class Appointment(models.Model):
    task = models.TextField(max_length=1000)
    status = models.TextField(max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appoint_date = models.DateField()
    appoint_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AppointmentManager()






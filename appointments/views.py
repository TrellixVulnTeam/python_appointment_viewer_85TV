# model
from .models import Appointment
# json utils
import json
from .utils import convert_json, get_client_ip
# views and http
from django.http import HttpResponse
from django.views.generic import View
# template
from django.template import loader
from urllib.parse import parse_qs



def index(request):
  template = loader.get_template('appointments/index.html')
  userIP = get_client_ip(request)
  print(userIP)
  return HttpResponse(template.render())



def appointmentUser(request, user):
  if (request.method == "GET"):
    # Get users matching the url from the database
    userAppointments = Appointment.objects.filter(user=str(user))
    
    jsonData = convert_json(userAppointments)

    return HttpResponse(jsonData, content_type='application/json')



class Appointments(View):
  
  # Get all appointments 
  def get(self, request):
    if (request.method == "GET"):
      query = parse_qs(request.body)
      print(query, 'REQUEST BODY')
      appointments = Appointment.objects.all()
      jsonData = convert_json(appointments)
      
      return HttpResponse(jsonData, content_type='application/json')



  # Post appointment
  def post(self, request):

    if (request.method == "POST"):

      print(request.POST)

      appointment = request.POST

      # Check for missing fields

      missingfields = []
      requiredfields = ['user', 'datetime', 'description']

      for field in requiredfields:
        if (not field in appointment):
          missingfields.append(field)
      
      # Respond with missing fields if empty
      
      if (len(missingfields) > 0):
        missing = json.dumps({'missing_fields': missingfields})
        return HttpResponse(missing, status=400, content_type='application/json')

      else:
        
        # Save the appointment

        apptToSave = Appointment.objects.create(user=appointment['user'], description=appointment['description'],datetime=appointment['datetime'])
        print(apptToSave.id)

        # Write the id to the response object to send to the client
        appointmentResponse = {
          'user': appointment['user'],
          'datetime': appointment['datetime'],
          'description': appointment['description'],
          'id': apptToSave['id']
        }

        jsonResponse = json.dumps(appointmentResponse)
        
        # Return the saved appointment as confirmation
        return HttpResponse(jsonResponse, status=202, content_type='application/json')
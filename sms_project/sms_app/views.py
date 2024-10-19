import requests
from django.shortcuts import render
from .forms import SMSSendForm
from .models import SMS
from django.contrib import messages
import json  # Import json for JSON handling

# NALO API URL and parameters
NALO_API_URL = "https://sms.nalosolutions.com/smsbackend/Resl_Nalo/send-message/"
NALO_API_KEY = "(!ng1_8z2b3uvd(_gfxi((o69ln7os94x)hbszruprrnsbj_zm@_fridazkandb)"  # Your API key

def home(request):
    if request.method == 'POST':
        form = SMSSendForm(request.POST)
        if form.is_valid():
            to = form.cleaned_data['to']
            message_body = form.cleaned_data['message']
            # Format the destination number for NALO API
            destination = to.replace("+", "") 
            
            # Prepare the JSON payload as per NALO's documentation
            payload = {
                'key': NALO_API_KEY,
                'msisdn': destination,
                'message': message_body,
                'sender_id': 'Test'  # Ensure this is correct
            }
            # Make the request to NALO API
            response = requests.post(NALO_API_URL, json=payload)
            
            # Parse response and handle accordingly
            response_data = response.json()

            if response_data.get('status') == "1701":
                # Save the SMS log to the database
                sms = SMS.objects.create(to=to, message=message_body, status="sent")
                messages.success(request, f"Message sent successfully! Job ID: {response_data.get('job_id')}")
            else:
                messages.error(request, f"Error Sending SMS: {response_data}")
            
    else: 
        form = SMSSendForm()
        
    return render(request, 'sms_app/index.html', {'form': form})

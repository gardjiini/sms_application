from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import SMS
import json

NALO_API_URL = "https://sms.nalosolutions.com/smsbackend/Resl_Nalo/send-message/"
API_KEY = "(!ng1_8z2b3uvd(_gfxi((o69ln7os94x)hbszruprrnsbj_zm@_fridazkandb)"  # Your API key
CALLBACK_URL = " https://36c3-197-251-147-210.ngrok-free.app/callback/"

def index(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')  # The phone number(s) input
        message = request.POST.get('message')  # The message input

        # Prepare the API request data
        api_url = "https://sms.nalosolutions.com/smsbackend/Resl_Nalo/send-message/"
        payload = {
            "key": API_KEY,  # Your auth key
            "msisdn": phone,  # Use the phone number(s) from the form
            "message": message,  # Use the message from the form
            "sender_id": "Test",  # Sender ID
            "callback_url": "https://9c8c-154-160-0-196.ngrok-free.app/sms-callback/"  # Add callback URL here
        }

        # Make the POST request to the SMS API
        try:
            response = requests.post(api_url, json=payload)

            # Redirect after the POST without showing any success/error message
            return redirect('index')
        except requests.exceptions.RequestException as e:
            return redirect('index')  # Redirect after POST even if there's an error

    return render(request, 'index.html')  # Render the index page

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body of the request
            data = json.loads(request.body)
            print("Received data:", data)  # Print the received data for troubleshooting

            # Extract fields from the incoming data
            recipient_number = data.get('destination')
            message = data.get('message', 'Your message here')  # Adjust as needed
            status_desc = data.get('status_desc')
            job_id = data['mid']  # Assuming 'mid' is always present
            network = data.get('network')
            submit_date = parse_datetime(data['submit_date'].replace(',', ' ')) if data.get('submit_date') else None
            deliv_date = parse_datetime(data['deliv_date'].replace(',', ' ')) if data.get('deliv_date') else None
            source = data.get('source')

            # Clear the existing records in the SMS table (to show only the latest)
            SMS.objects.all().delete()

            # Create a new SMS record
            sms_record = SMS.objects.create(
                to=recipient_number,
                message=message,
                status=status_desc,
                job_id=job_id,
                network=network,
                submit_date=submit_date,
                deliv_date=deliv_date,
                source=source,
            )

            print("SMS record created:", sms_record)  # Print the created SMS record for troubleshooting

            return JsonResponse({'success': True, 'sms_id': sms_record.id})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def fetch_sms_callbacks(request):
    # Fetch the latest callback from the database
    latest_callback = SMS.objects.order_by('-timestamp').first()

    if latest_callback:
        db_callback = {
            "phone_number": latest_callback.to,
            "message": latest_callback.message,
            "status": latest_callback.status,
            "timestamp": latest_callback.timestamp.isoformat() if latest_callback.timestamp else "No Data",
            "network": latest_callback.network if latest_callback.network else "No Data",
            "submit_date": latest_callback.submit_date.isoformat() if latest_callback.submit_date else "No Data",
            "deliv_date": latest_callback.deliv_date.isoformat() if latest_callback.deliv_date else "No Data",
            "source": latest_callback.source if latest_callback.source else "No Data",
        }
    else:
        db_callback = {
            "phone_number": "No Data",
            "message": "No Data",
            "status": "No Data",
            "timestamp": "No Data",
            "network": "No Data",
            "submit_date": "No Data",
            "deliv_date": "No Data",
            "source": "No Data",
        }

    # Return the response as JSON
    return JsonResponse({"db_callback": db_callback})

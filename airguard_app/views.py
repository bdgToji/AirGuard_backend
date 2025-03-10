from datetime import datetime
import json

from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm
from .models import SensorData, AirSystem, Button
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from airguard_app.models import SensorData

# Create your views here.


@csrf_exempt
def collect_sensor_data_json(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            air_system_id = data.get('air_system_id')
            air_system = AirSystem.objects.get(id=air_system_id)

            sensor_data = {
                'air_system': air_system,
                'water_level': int(data.get('water_level', 0)),
                'temperature': float(data.get('temperature', 0)),
                'humidity': float(data.get('humidity', 0)),
                'oxygen': float(data.get('oxygen', 0.00)),
                'pollution': float(data.get('pollution', 0.00)),
                'ozone': int(data.get('ozone', 0)),
                'light': int(data.get('light', 0)),
                'uv_light': float(data.get('uv_light', 0.00)),
                'quality': int(data.get('quality', 0)),
                'current_date_time': datetime.strptime(
                    data.get('current_date_time', ''), '%Y/%m/%d %H:%M:%S'
                ),
                'flow_rate': float(data.get('flow_rate', 0.00)),
                'total_milli_liters': int(data.get('total_milli_liters', 0)),
                'percentage': int(data.get('percentage', 0)),
                'liquid_level': int(data.get('liquid_level', 0)),
                'tds_value': float(data.get('tds_value', 0.00)),
            }

            # Save data to the database
            SensorData.objects.create(**sensor_data)

            return JsonResponse({"status": "success", "message": "Data saved successfully."}, status=201)
        except AirSystem.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Air system not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error saving data: {str(e)}"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)


@csrf_exempt
def collect_sensor_data(request):
    if request.method == 'POST':
        try:
            data = {
                'user': request.user,
                'water_level': int(request.POST.get('water_level', 0)),
                'temperature': float(request.POST.get('temperature', 0)),
                'humidity': float(request.POST.get('humidity', 0)),
                'oxygen': float(request.POST.get('oxygen', 0.00)),
                'pollution': float(request.POST.get('pollution', 0.00)),
                'ozone': int(request.POST.get('ozone', 0)),
                'light': int(request.POST.get('light', 0)),
                'uv_light': float(request.POST.get('uv_light', 0.00)),
                'quality': int(request.POST.get('quality', 0)),
                # 'current_date_time': datetime.strptime(request.POST.get('current_date_time', ''), '%Y/%m/%d %H:%M:%S'),
                'current_date_time': datetime.now(),
                'flow_rate': float(request.POST.get('flow_rate', 0.00)),
                'total_milli_liters': int(request.POST.get('total_milli_liters', 0)),
                'percentage': int(request.POST.get('percentage', 0)),
                'liquid_level': int(request.POST.get('liquid_level', 0)),
                'tds_value': float(request.POST.get('tds_value', 0.00)),
            }

            SensorData.objects.create(**data)
            return JsonResponse({"status": "success", "message": "Data saved successfully"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Error saving data: {str(e)}"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"})


def index(request):
    data = SensorData.objects.order_by('-current_date_time')[:10]
    return render(request, 'index.html', {'data': data})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if request.user.is_authenticated:
            return redirect('index')
        if form.is_valid():
            user = form.save()  # Save the user to the database
            #login(request, user)  # Automatically log in the user after registration
            return redirect('login')  # Redirect to the dashboard or any other page
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required()
def user_dashboard(request):
    # user_air_systems = AirSystem.objects.filter(user=request.user)
    # context = {'air_systems': user_air_systems}
    #
    # return render(request, 'dashboard.html', context)
    user_air_systems = AirSystem.objects.filter(user=request.user)

    selected_system_id = request.GET.get('system_id')

    if selected_system_id:
        selected_system = get_object_or_404(user_air_systems, id=selected_system_id)
    else:
        selected_system = user_air_systems.first()

    latest_sensor_data = SensorData.objects.filter(air_system=selected_system).order_by('-current_date_time').first() if selected_system else None

    buttons = selected_system.buttons.all() if selected_system else []

    context = {
        'air_systems': user_air_systems,
        'selected_system': selected_system,
        'latest_sensor_data': latest_sensor_data,
        'buttons': buttons,
    }

    return render(request, 'dashboard.html', context)


@login_required()
def toggle_button(request, button_id):
    button = get_object_or_404(Button, id=button_id, air_system__user=request.user)

    button.is_on = not button.is_on
    button.save()

    return redirect(f"{reverse('dashboard')}?system_id={button.air_system.id}")
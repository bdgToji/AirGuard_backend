from datetime import datetime

from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from airguard_app.models import SensorData

# Create your views here.


@csrf_exempt
def collect_sensor_data(request):
    if request.method == 'POST':
        try:
            data = {
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

from django.db import models

# Create your models here.


class SensorData(models.Model):
    water_level = models.IntegerField(default=0)
    temperature = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    oxygen = models.FloatField(default=0.00)
    pollution = models.FloatField(default=0.00)
    ozone = models.IntegerField(default=0)
    light = models.IntegerField(default=0)
    uv_light = models.FloatField(default=0.00)
    quality = models.IntegerField(default=0)
    current_date_time = models.DateTimeField()
    flow_rate = models.FloatField(default=0.00)
    total_milli_liters = models.IntegerField(default=0)
    percentage = models.IntegerField(default=0)
    liquid_level = models.IntegerField(default=0)
    tds_value = models.FloatField(default=0.00)

    def __str__(self):
        return f"Sensor Data at {self.current_date_time}: Temp={self.temperature}, Hum={self.humidity}, AIQ={self.quality}"

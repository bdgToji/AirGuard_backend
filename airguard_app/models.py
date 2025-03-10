from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class AirSystem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.user.username})"


# class Button(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     air_system = models.ForeignKey(AirSystem, on_delete=models.CASCADE)
#     is_on = models.BooleanField(default=False)

class Button(models.Model):
    class ButtonType(models.TextChoices):
        PLANT_LIGHT = 'PLANT_LIGHT', 'Plant Light'
        PLANT_HEATING = 'PLANT_HEATING', 'Plant Heating'
        PLANT_COOLING = 'PLANT_COOLING', 'Plant Cooling'
        DEHUMIDIFIER = 'DEHUMIDIFIER', 'Dehumidifier'
        HUMIDIFIER = 'HUMIDIFIER', 'Humidifier'
        PM10_FILTER = 'PM10_FILTER', 'PM10 Filter'
        DUST_FILTER = 'DUST_FILTER', 'Dust and Other Particles Filter'

    air_system = models.ForeignKey(AirSystem, on_delete=models.CASCADE, related_name='buttons')
    is_on = models.BooleanField(default=False)
    button_type = models.CharField(max_length=30, choices=ButtonType.choices)

    class Meta:
        unique_together = ('air_system', 'button_type')

    def __str__(self):
        return f"{self.air_system.name} - {self.get_button_type_display()}"


@receiver(post_save, sender=AirSystem)
def create_buttons_for_air_system(sender, instance, created, **kwargs):
    if created:
        for button_type in Button.ButtonType.values:
            Button.objects.create(air_system=instance, button_type=button_type)


class SensorData(models.Model):
    air_system = models.ForeignKey(AirSystem, on_delete=models.CASCADE)
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
        return f"Sensor Data for {self.air_system.name} at {self.current_date_time}"

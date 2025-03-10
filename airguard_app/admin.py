from django.contrib import admin
from .models import SensorData, AirSystem, Button

# Register your models here.


class ButtonInline(admin.TabularInline):
    model = Button
    extra = 0
    readonly_fields = ('button_type',)
    can_delete = False


class AirSystemAdmin(admin.ModelAdmin):
    list_display = ('user',)
    inlines = [ButtonInline]


class ButtonAdmin(admin.ModelAdmin):
    list_display = ('air_system', 'button_type', 'is_on')
    list_filter = ('button_type', 'is_on')


class SensorDataAdmin(admin.ModelAdmin):
    list_display = (
        'current_date_time', 'temperature', 'humidity', 'oxygen',
        'pollution', 'ozone', 'light', 'uv_light', 'quality',
        'water_level', 'flow_rate', 'total_milli_liters',
        'percentage', 'liquid_level', 'tds_value'
    )

    # list_filter = ('quality')
    # search_fields = ('current_date_time')

    # def has_add_permission(self, request):
    #     if request.user.is_superuser:
    #         return True
    #     return False
    #
    # def has_change_permission(self, request, obj=None):
    #     if obj and obj.user == request.user:
    #         return True
    #     return False
    #
    # def has_delete_permission(self, request, obj=None):
    #     if request.user.is_superuser:
    #         return True
    #     return False


admin.site.register(SensorData, SensorDataAdmin)
admin.site.register(AirSystem, AirSystemAdmin)
admin.site.register(Button, ButtonAdmin)

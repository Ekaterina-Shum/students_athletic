from django.contrib import admin
from .models import ParticipantsSportEvent

@admin.register(ParticipantsSportEvent)
class ParticipantsSportEventAdmin(admin.ModelAdmin):
    list_display = ('event',)
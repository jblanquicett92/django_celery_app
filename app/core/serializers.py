from rest_framework import serializers
from .models import Event, Notification

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ('id', 'moved_to', 'received_timestamp',)

class EventExcludeIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('file_name', 'file_path', 'moved_to', 'received_timestamp')
        

class NotificationSerializer(serializers.ModelSerializer):
    event_data=EventExcludeIDSerializer()
    class Meta:
        model = Notification
        
        exclude = ('id',)
        

        

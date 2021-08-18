from rest_framework import status
from rest_framework.response import Response

from ..models import Notification
from ..serializers import NotificationSerializer

class NotificationController:
    
    def create_notification(date, uuid, event_type, event_data, elapsed_time):
        notification=Notification.objects.create(
            date=date,
            uuid=uuid,
            event_type=event_type,
            event_data=event_data,
            elapsed_time=elapsed_time
        )    
        notification.save()
        return notification

    def read_notification(request, id):
        try:
            queryset = Notification.objects.filter(uuid=id)
        except Notification.DoesNotExist:
            return Response({'result': 'we couldn’t find the notification'}, status=status.HTTP_404_NOT_FOUND)
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list_notification(request):
        queryset = Notification.objects.all()
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .controller.EventController import EventController
from .controller.NotificationController import NotificationController
from .serializers import EventSerializer, NotificationSerializer
from .tasks import proccess_header_uppercase_columns

class EventFileView(APIView):
    serializer_class=EventSerializer

    def post(self, request, *args, **kwargs):
        
        data_for_process=EventController.receive(request)
        if data_for_process['work_bucket'] is not None:
            proccess_header_uppercase_columns.apply_async((data_for_process['work_bucket'], data_for_process['file_name'], data_for_process['file_path']), countdown=1)
            return Response({'result':data_for_process['result']}, status=status.HTTP_200_OK)
        return Response({'result':data_for_process['result']}, status=status.HTTP_400_BAD_REQUEST)

class NotificationView(APIView):
    serializer_class=NotificationSerializer
    
    def get(self, request, id=None):
        if id:
            return NotificationController.read_notification(request, id)
        else:
            return NotificationController.list_notification(request)


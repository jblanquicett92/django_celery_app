from django.db import models

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    file_name=models.CharField(max_length=25)
    file_path=models.CharField(max_length=255)
    moved_to=models.CharField(max_length=20)
    received_timestamp=models.CharField(max_length=32)
    
    def __str__(self):
        return f'id: {self.id} file_name: {self.file_name} file_path: {self.file_path} moved_to: {self.moved_to}'
    

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    date=models.DateField()    
    uuid=models.CharField(max_length=32)
    event_type=models.CharField(max_length=25)
    event_data=models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='event')
    elapsed_time=models.CharField(max_length=45)
        
    def __str__(self):
        return f'id: {self.id} date: {self.date} uuid: {self.uuid} event_type: {self.event_type}'
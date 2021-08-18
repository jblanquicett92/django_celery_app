import pandas as pd

from ..test.TestEvent import TestEvent as te
from ..models import Event
import time

class EventController:
    
    def create_event(file_path, file_name, old_file_path):
        event= Event.objects.create(
            file_name=file_name,
            file_path=old_file_path,
            moved_to=file_path,
            received_timestamp=f'{time.time()}'
        )
        event.save()
        return event


    def receive(request):

        data = request.data
        file_name = data['file_name']
        file_path = data['file_path']

        file_exists = te.is_file_exist(te, file_path, file_name)
        path_exists = te.is_path_exist(te, file_path)

        if path_exists and file_exists:

            if te.is_csv(te, file_path, file_name):
                
                url = f'{file_path}/{file_name}'
                df = pd.read_csv(url)

                if te.is_path_exist(te, te.work_bucket):
                    df.to_csv(f'{te.work_bucket}/{file_name}')
                    
                    
                    return {'work_bucket':te.work_bucket, 'file_name':file_name, 'file_path':file_path, 'result':'File will be proccesed'}
                else:
                    return {'work_bucket':None, 'result':'Destination path is errored'}       
            else:
                return {'work_bucket':None, 'result':'file isnt valid .csv'}
        else:
            return {'work_bucket':None, 'result':{'path exists': path_exists, 'file exists': file_exists} }

from core.models import Event
from django.test import TestCase

from os import path
import pandas as pd
import  time, os


class TestEvent(TestCase):

    input_bucket='/app/bucket/data-bucket/input/UUID'
    work_bucket='/app/bucket/work-bucket/UUID'
    processed_bucket='/app/bucket/procesed-data/UUID'
    metadata_bucket='/app/bucket/metadata/UUID'
    
    def setUp(self):
        
        Event.objects.create(
            file_name='a.pdf',#bad
            file_path=self.input_bucket ,#ok
            moved_to=self.work_bucket,
            received_timestamp=f'{time.time()}'
        )
        
        Event.objects.create(
            file_name='b.csv',#bad
            file_path=self.input_bucket ,#ok
            moved_to=self.work_bucket,
            received_timestamp=f'{time.time()}'
        )
        Event.objects.create(
            file_name='c.csv',#bad
            file_path=self.input_bucket ,#ok
            moved_to=self.work_bucket,
            received_timestamp=f'{time.time()}'
        )
        Event.objects.create(
            file_name='titanic_educido.csv',#bad
            file_path=self.input_bucket ,#ok
            moved_to=self.work_bucket,
            received_timestamp=f'{time.time()}'
        )
        Event.objects.create(
            file_name='titanic_reducido.csv',#ok
            file_path=self.input_bucket ,#ok
            moved_to=self.work_bucket,
            received_timestamp=f'{time.time()}'
        )
        Event.objects.create(
            file_name='titanic_reducido_sin_vacios.csv',#ok
            file_path=self.input_bucket ,#ok
            moved_to=self.work_bucket,
            received_timestamp=f'{time.time()}'
        )
         
    
    def test_file_exists(self):
        
        self.assertEqual(self.is_file_exist(self.input_bucket, 'titanic_reducido.csv') , True)
        self.assertEqual(self.is_file_exist(self.input_bucket, 'titanic_reducido_sin_vacios.csv') , True)
        self.assertEqual(self.is_file_exist(self.input_bucket, 'prueba_dockerizada.csv') , True)
        self.assertEqual(self.is_file_exist(self.input_bucket, 'no.csv') , False)
        self.assertEqual(self.is_file_exist(self.input_bucket, 'error.csv') , False)
    
    def test_origin_path_exists(self):
        
        self.assertEqual(self.is_path_exist(self.input_bucket) , True)
        self.assertEqual(self.is_path_exist(self.work_bucket) , True)
        self.assertEqual(self.is_path_exist(self.processed_bucket) , True)
        self.assertEqual(self.is_path_exist(self.metadata_bucket) , True)

    
    def test_destination_path_exists(self):
        
        self.assertEqual(self.is_path_exist(self.work_bucket) , True)
        self.assertEqual(self.is_path_exist(self.processed_bucket) , True)
        self.assertEqual(self.is_path_exist(self.metadata_bucket) , True)
        
    
    def test_is_csv(self):

        
        self.assertEqual(self.is_csv(self.input_bucket, 'titanic_error.csv') , False)
        self.assertEqual(self.is_csv(self.input_bucket, 'titanic_reducido.csv') , True)
        
    
    def test_is_csv_blank(self):

        self.assertEqual(self.is_csv_blank(self.input_bucket, 'titanic_reducido_sin_vacios.csv') , False)
        self.assertEqual(self.is_csv_blank(self.input_bucket, 'titanic_reducido.csv') , True)


    def test_is_header_upper(self):

        self.assertEqual(self.is_header_upper(self.input_bucket, 'titanic_reducido_sin_vacios.csv') , True)
        self.assertEqual(self.is_header_upper(self.input_bucket, 'titanic_reducido.csv') , True)


    def is_csv_blank(self, file_path, file_name):
        df=pd.read_csv(f'{file_path}/{file_name}')
        print(df.head())
        print(df.isnull().values.any())
        return df.isnull().values.any()
    
    def is_csv(self, file_path, file_name):
        try:
            df= pd.read_csv(f'{file_path}/{file_name}')
            
        except:
            return False
        return True

    def is_file_exist(self, file_path, file_name):
        return path.exists(f'{file_path}/{file_name}')

    def is_path_exist(self, file_path):        
        return path.exists(f'{file_path}')


    def is_header_upper(self, file_path, file_name):
        df=pd.read_csv(f'{file_path}/{file_name}')
        df=self.header_upper(df)        
        list_upper_header=df.columns.str.isupper()
        print(df)
        return next(filter(lambda x: x == False, list_upper_header ), True)
    
    def header_upper(self, df):
        df.columns = df.columns.str.upper()
        return df
        
from __future__ import absolute_import, unicode_literals

import pandas as pd
from celery import shared_task
import datetime
from .test.TestEvent import TestEvent as te
from .controller.EventController import EventController
from .controller.NotificationController import NotificationController
import os

def sub_process_metadata_file(task_start, task_end, last_value, new_value, original_line_numbers, original_file_size, path, new_file_name):
    metadata = {'info': [
        f'task_start: {task_start}',
        f'task_end: {task_end}',
        f'last_value: {last_value}',
        f'new_value: {new_value}',
        f'original_line_numbers: {original_line_numbers}',
        f'original_file_size: {original_file_size}bytes']
    }
    df = pd.DataFrame(data=metadata)
    df['info'].to_csv(f'{path}{new_file_name}.txt',
                      header=None, index=None, sep=' ', mode='a')


@shared_task
def proccess_header_uppercase_columns(file_path, file_name, old_file_path):
    os.remove(f'{te.input_bucket}/{file_name}')
    #print(f'{te.input_bucket}/{file_name}')
    date = datetime.datetime.now()
    uuid = proccess_header_uppercase_columns.request.id

    event = EventController.create_event(file_path, file_name, old_file_path)
    elapsed_time = f'{datetime.datetime.now() - date}'

    NotificationController.create_notification(
        date, uuid, "FILERECEIVED", event, elapsed_time)

    if te.is_csv_blank(te, file_path, file_name) == False:
        df = pd.read_csv(f'{file_path}/{file_name}')
        last_value = df.columns
        df = te.header_upper(te, df)
        new_value = df.columns
        if te.is_path_exist(te, te.processed_bucket) and te.is_path_exist(te, f'{te.metadata_bucket}/'):
            # ini proccess data
            df.to_csv(f'{te.processed_bucket}/{file_name}')
            elapsed_time = f'{datetime.datetime.now() - date}'
            event = EventController.create_event(
                te.processed_bucket, file_name, file_path)
            NotificationController.create_notification(
                date, uuid, "FILEPROCESSED", event, elapsed_time)
            task_end = datetime.datetime.now()
            df_memory = df.memory_usage(index=True).sum()
            sub_process_metadata_file(
                date, task_end, last_value, new_value, df.size, df_memory, f'{te.metadata_bucket}/', uuid)
    else:
        df = pd.read_csv(f'{file_path}/{file_name}')
        df.to_csv(f'{te.processed_bucket}{file_name}')
        event = EventController.create_event("", file_name, file_path)
        NotificationController.create_notification(
            date, uuid, "FILEERRORED", event, elapsed_time)

    return uuid

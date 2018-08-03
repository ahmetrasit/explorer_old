from django.core import serializers
from manager.models import *
from manager import views
from .requestHandler import requestHandler as rh
import os
import re
import time
import random
import json
import html

class taskManager:

    def __init__(self):
        pass


    #main function to submit request
    def submitRequest(self, reference_data_points, step_id, other_parameters, input_files = [], input_parameters=[], step_type=''):
        if len(reference_data_points) > 0:  #implementing only *:* and 1:1
            new_data_points = [(reference, self.createDataPointFromReference(reference, step_id, input_parameters)) for reference in reference_data_points]
            status = self.createTaskFromReference(new_data_points, step_id, input_parameters, self.multiTaskStep(step_id))
        else:   #request from upload
            samples = self.purifySamples(input_files, input_parameters)
            new_data_points = [(sample, self.createDataPointFromUpload(sample, input_parameters, other_parameters)) for sample in samples]
            status = self.createTaskFromUpload(reference_data_points, step_id, new_data_points, input_parameters, other_parameters, step_type)



    def createTaskFromReference(self, new_data_points, step_id, input_parameters, multi_task):
        processed_script = self.getDataPointRecords(step_id)
        if multi_task:
            for data_point in new_data_points:
                pass
        else:
            pass
        pass


    def createTaskFromUpload(self, reference_data_points, step_id, new_data_points, input_parameters, other_parameters, step_type):
        if int(step_id) < 0: #means just upload
            pass
        else:   #means real step
            processed_script = self.getDataPointRecords(step_id)
            if step_type == '*:*':
                for data_point in new_data_points:
                    pass
            elif step_type == '1:1':
                pass
            else:
                pass


    def multiTaskStep(self, step_id):
        if int(step_id) > -1:
            if Step.objects.filter(pk=step_id).values_list('input_output_relationship', flat=True)[0] == '*:*':
                return True
            return False
        else:
            return True


    def purifySamples(self, input_files, input_parameters):
        print(input_parameters)
        exclude = ['selected_upload_step', 'data_category', 'step_type']
        input_fields = [field for field in input_parameters if field not in exclude]
        if any([with_filename for with_filename in input_fields if re.search(r'_sample_name$', with_filename)]):
            samples = []
            for file in input_files:
                file_regex = '^{}_'.format(file.split("/")[-1])
                curr_sample = {re.sub(file_regex, '', field):input_parameters[field][0] for field in input_fields if re.search(file_regex, field)}
                samples.append((file, curr_sample))
            return samples
        else:
            samples = []
            print(input_parameters)
            for i in range(len(input_parameters['sample_name'])):
                curr_sample = {field:input_parameters[field][i] for field in input_fields}
                samples.append(('', curr_sample))
            return samples


    def createDataPointFromReference(self, reference, step_id, input_parameters):
        try:
            print(reference)
            data_point_folder = views.requestNewFolder(self.username, 'data_point')
            print(data_point_folder)
            os.mkdir(data_point_folder)
            selected_step = Step.objects.get(pk=step_id)

            reference_data_point = DataPoint.objects.get(pk=reference)
            reference_data_point.pk = None
            reference_data_point.major_types = selected_step.output_major_data_category
            reference_data_point.folder_path = data_point_folder
            reference_data_point.ancestry = reference_data_point.ancestry + ',' + reference
            reference_data_point.save()
            self.modifyPermissions(data_point_folder)
            return data_point_folder
        except Exception as e:
            print('Error creating data point folder:{} for {}'.format(data_point_folder, e))


    def createDataPointFromUpload(self, sample, input_parameters, other_parameters):
        filename, parameters = sample

        try:
            data_point_folder = views.requestNewFolder(self.username, 'data_point')
            os.mkdir(data_point_folder)

            other_parameters['folder_path'] = data_point_folder
            other_parameters['sample_name'] = parameters['sample_name']
            other_parameters['description'] = parameters['description']
            other_parameters['type'] = parameters['type']
            self.createDataPointRecord(data_point_folder, other_parameters)
            self.modifyPermissions(data_point_folder)
            return data_point_folder
        except Exception as e:
                print('Error creating data point folder:{} for {}'.format(data_point_folder, e))


    def createDataPointRecord(self, data_point_folder, other_parameters):
        data_point_fields = [str(field).split(".")[-1] for field in DataPoint._meta.get_fields() if '.created_on' not in str(field)][1:] #excluding id

        new_data_point = DataPoint()
        for field in data_point_fields:
            value = other_parameters[field] if field in other_parameters else ''
            value = int(value or 0) if '_id' in field else value
            setattr(new_data_point, field, value)
        new_data_point.save()
        print('saved')


    def getDataPointRecords(self, step_id):
        if int(step_id )> -1:
            step = Step.objects.filter(pk=step_id)
        else:
            step = {}
        #process step_id
        #return inputs, outputs, types
        pass


    def modifyPermissions(self, data_point_folder):
        pass



    #these will be executed just before a task starts:
    #task_folder = views.requestNewFolder(self.username, 'task')
    #new_input_files = self.linkInputFiles(input_files, task_folder)

    #task manager should perform this at the time of execution
    #! a task might be dependent on an uncompleted task
    def linkInputFiles(self, input_files, folder):
        new_input_files = []
        for file in input_files:
            try:
                os.symlink(file, folder+file.split("/")[-1])
                new_input_files.append(folder+file.split("/")[-1])
            except Exception as e:
                print('Error:{} for {}'.format(file, e))
        return new_input_files
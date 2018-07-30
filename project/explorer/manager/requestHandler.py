from django.core import serializers
from manager.models import *
from manager import views
import os
import re
import time
import random
import json
import html

class requestHandler:

    def __init__(self, username):
        self.username = username


    #main function to submit request
    def submitRequest(self, step_id, input_files, input_parameters={}, other_parameters={}):
        for index, curr in enumerate([step_id, input_files, input_parameters, other_parameters]):
            print(index, list(curr))

        data_point_folder = self.createDataPoint(step_id, input_files, input_parameters)
        processed_script = self.replacePlaceholders(step_id, input_files, input_parameters, data_point_folder)
        self.createTask(username, processed_script, step_id, input_files, input_parameters, data_point_folder, other_parameters)


    def createDataPoint(self, step_id, input_files, input_parameters):
        data_point_folder = views.requestNewFolder(self.username, 'data_point')
        try:
            os.mkdir(data_point_folder)
        except Exception as e:
                print('Error creating data point folder:{} for {}'.format(data_point_folder, e))

        self.linkInputFiles(input_files, data_point_folder)
        self.createDataPointRecord(step_id, data_point_folder)
        self.modifyPermissions(username, data_point_folder)
        return data_point_folder


    def replacePlaceholders(self, step_id, input_files, input_parameters, data_point_folder):
        #return processed_script
        pass


    def createTask(self, username, processed_script, step_id, input_files, input_parameters, data_point_folder, other_parameters):
        #create initial record in Task database
        pass


    def createDataPointRecord(self, step_id, data_point_folder):
        inputs, outputs, types = self.getDataPointRecords(step_id)
        pass


    def getDataPointRecords(self, step_id):
        #process step_id
        #return inputs, outputs, types
        pass


    def modifyPermissions(self, username, data_point_folder):
        pass


    def linkInputFiles(self, input_files, data_point_folder):
        print('lif')
        for file in input_files:
            try:
                os.symlink(file, data_point_folder+file.split("/")[-1])
            except Exception as e:
                print('Error:{} for {}'.format(file, e))

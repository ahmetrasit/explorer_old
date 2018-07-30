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
        print(dir(views))


    #main function to submit request
    def submitRequest(self, username, step_id, input_files, input_parameters={}, other_parameters={}):
        for index, curr in enumerate([username, step_id, input_files, input_parameters, other_parameters]):
            print(index, list(curr))
        print('inside sr')
        data_point_folder = self.createDataPoint(step_id, input_files, input_parameters)
        processed_script = self.replacePlaceholders(step_id, input_files, input_parameters, data_point_folder)
        self.createTask(username, processed_script, step_id, input_files, input_parameters, data_point_folder, other_parameters)


    def createDataPoint(self, username, step_id, input_files):
        data_point_folder = views.requestNewFolder(self.username, 'data_point')
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
        pass

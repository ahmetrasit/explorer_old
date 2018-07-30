from django.core import serializers
from manager.models import *
import os
import re
import time
import random
import json
import html

class requestHandler:

    #main function to submit request
    def submitRequest(username, step_id, input_files, input_parameters={}, other_parameters={}):
        print('inside sr')
        data_point_folder = createDataPoint(step_id, input_files, input_parameters)
        processed_script = replacePlaceholders(step_id, input_files, input_parameters, data_point_folder)
        createTask(username, processed_script, step_id, input_files, input_parameters, data_point_folder, other_parameters)


    def createDataPoint(username, step_id, input_files):
        data_point_folder = requestNewFolder()
        linkInputFiles(input_files, folder)
        createDataPointRecord(step_id, data_point_folder)
        modifyPermissions(username, data_point_folder)
        return data_point_folder


    def replacePlaceholders(step_id, input_files, input_parameters, data_point_folder):
        #return processed_script
        pass


    def createTask(username, processed_script, step_id, input_files, input_parameters, data_point_folder, other_parameters):
        #create initial record in Task database
        pass


    def createDataPointRecord(step_id, data_point_folder):
        inputs, outputs, types = getDataPointRecords(step_id)
        pass


    def getDataPointRecords(step_id):
        #process step_id
        #return inputs, outputs, types
        pass


    def modifyPermissions(username, data_point_folder):
        pass

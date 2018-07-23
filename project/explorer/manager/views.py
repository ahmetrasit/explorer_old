from django.shortcuts import render, render_to_response
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from django.http import JsonResponse
from .models import *
from .forms import *
import os
import re
import time
import random
import json
import html


def homepage(request):
    render_dict = getConfigDict(request)
    render_dict['step_form'] = StepForm(initial={'access_list': 'public', 'status':'tested', 'special':'regular', 'no_of_outputs':'one'})
    return render(request, 'homepage.html', render_dict)


@login_required
def addStep(request):
    render_dict = getConfigDict(request)
    form = StepForm
    render_dict['step_form']=form(initial={'access_list': 'public', 'status':'tested', 'special':'regular', 'no_of_outputs':'one'})
    if request.method == 'POST':
        formInput = form(request.POST)
        if formInput.is_valid():
            step_folder = getFolderName(request.user.username, 'step')
            step_filenames = []
            for i in range(len(request.FILES.getlist('stepFiles'))):
                file = request.FILES.getlist('stepFiles')[i]
                filename = str(file)
                step_filenames.append(filename)
                success = handle_uploaded_file(file, filename, step_folder, request.user.username)
            temp_form = formInput.save(commit=False)
            temp_form.created_by = request.user.username
            temp_form.input_major_data_category, temp_form.output_major_data_category, temp_form.script = getScriptInputOutputCategory(formInput.cleaned_data['raw_script'])
            temp_form.subfolder_path = step_folder
            temp_form.dependencies = '_|_'.join(step_filenames)
            temp_form.save()
            message = 'Step successfully added'
        else:
            message = 'Cannot create step.'
        render_dict['message'] = message
        render_dict['step_form']=formInput

    step_fields = ['short_name', 'created_for', 'access_list', 'description', 'status', 'special', 'created_by']
    render_dict['steps'] = Step.objects.all().values(*step_fields)[::-1]
    render_dict['step_fields'] = step_fields
    return render(request, 'addStep.html', render_dict)


def getFolderName(username, type):
    #temp:temporary, perm:permanent
    types = {'upload':'temp', 'task':'temp', 'step':'perm', 'data_point':'perm'}
    folderName = '!'
    if type in types:
        curr_time = int(time.time())
        rand_num = random.randint(111111,999999)
        folderName = 'static/{}/{}_{}_{}'.format(types[type], username, curr_time, rand_num)

    return folderName




def getScriptInputOutputCategory(raw_script):
    script = html.unescape(raw_script)
    script = re.sub(r'<\/?span[^>]*>', '', script)
    script = re.sub(r'<\/?p[^_>]*>', '', script)
    inputs = re.findall(r'(<[fsid][smyp]_[\w.-]+)\W', script)
    input_major_data_category = '_|_'.join([re.sub(r'^<\w\w_', '', curr) for curr in inputs if re.match('<f', curr)])
    outputs = re.findall(r'(>[f]_[\w.-]+)\W', script)
    output_major_data_category = '_|_'.join([re.sub(r'^>f_', '', curr) for curr in outputs if re.match('>f', curr)])

    return input_major_data_category, output_major_data_category, script




@login_required
def addUser(request):
    render_dict = getConfigDict(request)
    form = AddUserForm
    render_dict['form']=form()
    if request.method == 'POST':
        formInput = form(request.POST)
        if formInput.is_valid():
            if createSystemUser(formInput.cleaned_data["username"]):
                formInput.save()
                message = 'User successfully added'
            else:
                message = "cannot create system user"
        else:
            message = 'Cannot create user.'
        render_dict['message'] = message
        render_dict['form']=formInput

    users_fields = ['username', 'role', 'credit', 'score']
    render_dict['users'] = CustomUser.objects.exclude(username='admin').values(*users_fields)[::-1]
    render_dict['users_fields'] = users_fields
    return render(request, 'addUser.html', render_dict)


@login_required
def addDataCategory(request):
    render_dict = getConfigDict(request)
    form = MajorDataCategoryForm

    render_dict['form']=form()
    if request.method == 'POST':
        formInput = form(request.POST)
        if formInput.is_valid():
            formInput.save()
            message = 'Data category successfully added'
        else:
            message = 'Cannot add data category'

        render_dict['message'] = message
        render_dict['form']=formInput

    data_category_fields = ['category', 'description']
    render_dict['data_categories'] = MajorDataCategory.objects.all().values(*data_category_fields)[::-1]
    render_dict['data_category_fields'] = data_category_fields
    return render(request, 'addDataCategory.html', render_dict)



def createSystemUser(username):
    return False


@login_required
def editMainConfiguration(request):
    try:
        last = model_to_dict(MainConfiguration.objects.last())
        del last['id']
    except:
        last = None
    render_dict = getConfigDict(request)
    form = MainConfigurationForm
    render_dict['form']=form(initial=last)
    if request.method == 'POST':
        formInput = form(request.POST)
        if formInput.is_valid():
            if not last == formInput.cleaned_data:
                formInput.save()
                message = 'Main configuration successfully updated.'
            else:
                message = 'Nothing changed from previous state.'
        else:
            message = 'Input parameters are not valid, please check.'
        render_dict['message'] = message
    try:
        last = model_to_dict(MainConfiguration.objects.last())
    except:
        last=None
    render_dict['form']=form(initial=last)
    render_dict['configs'] = serializers.serialize('python', MainConfiguration.objects.all())[::-1]
    return render(request, 'configMain.html', render_dict)


def getConfigDict(request):
    render_dict = {'user':request.user, 'no_of_samples':0}
    #render_dict['login_form'] = PickyAuthenticationForm()
    last = MainConfiguration.objects.last()
    if last:
        system_config = model_to_dict(last)
        for key in ['team_name', 'intro_message']:
            render_dict[key] = system_config[key]
    return render_dict



def getInputs(script):
	inputs = []
	io_types = {'f':'file', 'i':'html_input', 'd':'database', 's':'select'}
	for item in re.compile("\s+").split(script):
		match = re.match("<([a-z])_([a-z-]+)_([a-z_-]+)", item)
		if match:
			io_type = io_types[match.group(1)]
			data_type = match.group(2)
			data_name = match.group(3)
			inputs.append(':'.join([io_type, data_type, data_name]))
	return ';'.join(inputs)


def getOutputs(script):
	outputs = []
	io_types = {'f':'file', 'i':'html_input', 'd':'database', 's':'select'}
	for item in re.compile("\s+").split(script):
		match = re.match(">([a-z])_([a-z-]+)_([a-z_-]+)", item)
		if match:
			io_type = io_types[match.group(1)]
			data_type = match.group(2)
			data_name = match.group(3)
			outputs.append(':'.join([io_type, data_type, data_name]))
	return ';'.join(outputs)


def getParameters(script):
	parameters= []
	for item in re.compile("\s+").split(script):
		match = re.match("-p_([a-z-]+)", item)
		if match:
			parameter_type = match.group(1)
			parameters.append(parameter_type)
	return ';'.join(parameters)


@csrf_exempt
def uploadFASTQ(request):
    success = False
    if request.method == 'POST':
        for i in range(len(request.FILES.getlist('filesToUpload'))):
            file = request.FILES.getlist('filesToUpload')[i]
            filename = str(file)
            random_folder = str(int(time.time())) + str(random.randint(111111, 999999)) + '/'
            success = success and handle_uploaded_file(file, filename, random_folder, request.user.username)
    return HttpResponse()


@csrf_exempt
def handle_uploaded_file(f, filename, foldername, username):
    try:
        os.mkdir(foldername)
    except Exception as e:
        print('Error:{} for {}'.format(foldername, e))
    try:
        with open(foldername + '/' +  filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return True
    except Exception as e:
        print('Error:{} for {}'.format(filename, e))
        return False

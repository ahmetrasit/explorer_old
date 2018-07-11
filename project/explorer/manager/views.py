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

def homepage(request):
    render_dict = getConfigDict(request)
    return render(request, 'homepage.html', render_dict)

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


def createSystemUser(username):
    print(username)
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


@csrf_exempt
def createProcess(request):
    print('db', Workflow.objects.all())
    if request.POST['bashProcessID'].strip() not in Workflow.objects.values_list('process_id', flat=True):
        try:
            bash_process = Workflow(
				process_id = request.POST['bashProcessID'].strip(),
    			name = request.POST['bashProcessName'].strip(),
                category = 'bash',
                status = 'approved',
                inputs = getInputs(request.POST['bashProcessScript'].strip().lower()),
                outputs = getOutputs(request.POST['bashProcessScript'].strip().lower()),
                parameters = getParameters(request.POST['bashProcessScript'].strip().lower()),
                description = request.POST['bashProcessDescription'].strip(),
                content = request.POST['bashProcessScript'].strip(),
                created_by = request.user.username
    		)
            bash_process.save()
            return HttpResponse('<div class="btn btn-success btn-block">Bash Process Successfully Created</div>')
        except Exception as e:
            return HttpResponse('<div class="btn btn-danger btn-block">There is a problem on server side!'+str(e)+'</div>')
    else:
        return HttpResponse('<div class="btn btn-danger btn-block">There is already a process with the same id!</div>')



def getInputs(script):
	inputs = []
	io_types = {'f':'file', 'i':'html_input', 'd':'database', 's':'select'}
	for item in re.compile("\s+").split(script):
		match = re.match("<([a-z])_([a-z-]+)_([a-z_-]+)", item)
		if match:
			io_type = io_types[match.group(1)]
			data_type = match.group(2)
			data_name = match.group(3)
			print('inputs', io_type, data_type, data_name)
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
			print('outputs', io_type, data_type, data_name)
			outputs.append(':'.join([io_type, data_type, data_name]))
	return ';'.join(outputs)


def getParameters(script):
	parameters= []
	for item in re.compile("\s+").split(script):
		match = re.match("-p_([a-z-]+)", item)
		if match:
			parameter_type = match.group(1)
			print('parameter',parameter_type)
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
def handle_uploaded_file(f, filename, random_folder, username):
    print(os.getcwd(), os.listdir('./'))
    os.mkdir('static/temporary/' + random_folder)
    with open('static/temporary/' + random_folder + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True

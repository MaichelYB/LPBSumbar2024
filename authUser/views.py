from django.shortcuts import render
from .forms import Login, Register
from datetime import datetime
from django.http import JsonResponse
from .models import UserProfile
from django.db.transaction import TransactionManagementError
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import json
import bcrypt

# Create your views here.
@csrf_exempt 
def register(request):
    # check if the request method is POST, IF NOT RETURN ERROR
    if request.method == "POST":
        jsonBody = json.loads(request.body)
        form = Register(jsonBody)
        # check if the form is valid, IF NOT RETURN ERROR
        if form.is_valid():
            userProfile = UserProfile()
            birth_date = jsonBody['birth_date']
            # convert birth date to date time
            try:
                dateTime = datetime.strptime(birth_date, '%d-%m-%Y')
                # store extra data here
                userProfile.birth_date = dateTime
            except ValueError:
                return JsonResponse({'status':'false','message':"not valid date time"}, status=500)
            
            user = User.objects.create_user(jsonBody['username'], jsonBody['email'], jsonBody['password'])
            try:
                user.save()
                userProfile.user_id = user.id
                userProfile.save()
                return JsonResponse({'status':'true','message':"user registered"}, status=200)
            except (TransactionManagementError, IntegrityError) as e:
                return JsonResponse({'status': 'false', 'message': str(e.__cause__)}, status = 500)
        return JsonResponse({'status':'false','message':"form not valid"}, status=500)
    return JsonResponse({'status':'false','message':"request method not valid"}, status=500)

@csrf_exempt 
def login_view(request):
    if request.method == 'POST':
        jsonBody = json.loads(request.body)
        form = Login(jsonBody)
        UserModel = get_user_model()
        # check if the form is valid, IF NOT RETURN ERROR
        if form.is_valid():
            email = jsonBody['email']
            passwordText = jsonBody['password']
            try:
                user = UserModel.objects.get(email=email)
            except ObjectDoesNotExist as e:
                return JsonResponse({'status': 'false', 'message': "user name or password invalid"}, status = 500)
            
            userLogin = authenticate(username=user.__dict__['username'], password=jsonBody['password'])
            if user is not None:
                return JsonResponse({'status':'true','message':"login success"}, status=200)
            
            return JsonResponse({'status': 'false', 'message': "failed login"}, status = 500)
        return JsonResponse({'status':'false','message':"form not valid"}, status=500)
    return JsonResponse({'status':'false','message':"request method not valid"}, status=500)
    
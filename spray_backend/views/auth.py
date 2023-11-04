from spray_backend.utils.common_imports import *
from spray_backend.utils.common_functions import *
from django.contrib.auth import authenticate, login, logout
from spray_backend.forms import CreateUserForm
from spray_backend.utils.auth import *
from django.middleware.csrf import rotate_token


@api_view(['GET'])
def temp_csrf_token(request):
    if request.method == 'GET':
        # retrieve token that will be the temp token
        token = get_token(request)
        # Store the token in the session
        request.session['csrf_token'] = token
        # Rotate the token for security (optional but recommended)
        # rotate_token(request)
        return Response({'csrfToken': token}, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.data)
        if form.is_valid():
            form.save()
            person_serializer = PersonSerializer(data=request.data)
            if person_serializer.is_valid():
                person_instance = person_serializer.save()
                # retrieve new token that will be the user's token for rest of session
                token = get_token(request)
                # Store the token in the session
                request.session['csrf_token'] = token
                data = {
                    'csrfToken': token,
                    'user': get_auth_user_data(person_instance),
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                print(person_serializer.errors)
        else:
            print(form.errors)


@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        csrf_token = request.META.get("HTTP_X_CSRFTOKEN")
        print(csrf_token)
        print(request.session.get("csrf_token"))
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            person = Person.objects.get(username=username)
            # retrieve new token that will be the user's token for rest of session
            token = get_token(request)
            # Store the token in the session
            request.session['csrf_token'] = token
            data = {
                'csrfToken': token,
                'user': get_auth_user_data(person),
                'gym': get_auth_gym_data(person),
                'spraywalls': get_auth_spraywalls_data(person),
                'headshotImage': get_auth_headshot_data(person),
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])  # Use POST method for logout
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return Response(status=status.HTTP_200_OK)

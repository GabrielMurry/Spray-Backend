from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm
from .models import SprayWall, Person, Boulder
from spray_backend.models import Movie
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import GymSerializer, SprayWallSerializer, BoulderSerializer, PersonSerializer
from .helperFunctions.composite import base64_string_to_image, increase_drawing_opacity, mask_drawing, combine_images, image_to_base64_string
from django.middleware.csrf import get_token

def movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    if movie is not None:
        return render(request, 'movies/movie.html', {'movie': movie})
    else:
        raise Http404('Movie does not exist')
    
@api_view(['GET'])
def csrf_token_view(request):
    if request.method == 'GET':
        csrf_token = get_token(request)
        print(csrf_token)
        return Response({'csrfToken': csrf_token})
    
@api_view(['POST'])
def signup_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.data)
        if form.is_valid():
            form.save()
            serializer = PersonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                csrf_token = get_token(request)
                username = request.data.get('username')
                return Response({'csrfToken': csrf_token, 'username': username}, status=status.HTTP_200_OK)
            else:
                print(serializer.errors)
        else:
            print(form.errors)

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            csrf_token = get_token(request)
            return Response({'csrfToken': csrf_token, 'username': username}, status=status.HTTP_200_OK)
        else:
            return Response('Username or password is incorrect')

@api_view(['GET'])
def logout_user(request):
    logout(request)
    return Response('logged out')
    
@api_view(['POST'])    
def composite(request):
    drawing_image, photo_image = base64_string_to_image(request.data.get('drawing'), request.data.get('photo'))
    drawing_image = increase_drawing_opacity(drawing_image)
    drawing_image = mask_drawing(drawing_image, photo_image)
    result = combine_images(drawing_image, photo_image)
    data_uri = 'data:image/png;base64,' + image_to_base64_string(result)
    return Response(data_uri)

@api_view(['POST'])
def add_gym(request, username):
    if request.method == 'POST':
        # Add Gym
        gym_serializer = GymSerializer(data=request.data.get('gym'))
        if gym_serializer.is_valid():
            gym_instance = gym_serializer.save() # Save the gym instance and get the saved object
            gym_id = gym_instance.id  # Access the ID of the recently created gym
            request.data['spraywall']['gym'] = gym_id # Insert recently created gym_id as a reference for spraywall's gym foreign key
            # Add Spray Wall
            spraywall_serializer = SprayWallSerializer(data=request.data.get('spraywall'))
            if spraywall_serializer.is_valid():
                spraywall_instance = spraywall_serializer.save()
                spraywall_id = spraywall_instance.id
                # Update Person data: person's gym_id foreign key and spraywall_id foreign key --> signifies person's default Gym and Wall
                person = Person.objects.get(username=username)
                person_data = {
                    'gym': gym_id,
                    'spraywall': spraywall_id
                }
                person_serializer = PersonSerializer(instance=person, data=person_data, partial=True) # partial=True allows for partial updates
                if person_serializer.is_valid():
                    person_serializer.save()
                    csrf_token = get_token(request)
                    return Response({'csrfToken': csrf_token}, status=status.HTTP_200_OK)
                else:
                    print(person_serializer.errors)
            else:
                print(spraywall_serializer.errors)
        else:
            print(gym_serializer.errors)

@api_view(['GET'])
def home(request, username):
    if request.method == 'GET':
        person = Person.objects.get(username=username)
        gym_name = person.gym.name
        spraywall_name = person.spraywall.name
        spraywall_id = person.spraywall.id
        image_uri = 'data:image/png;base64,' + person.spraywall.spraywall_image_data
        image_width = person.spraywall.spraywall_image_width
        image_height = person.spraywall.spraywall_image_height
        data = { 'gymName': gym_name, 'spraywallName': spraywall_name, 'spraywallId': spraywall_id, 'imageUri': image_uri, 'imageWidth': image_width, 'imageHeight': image_height }
        csrf_token = get_token(request)
        return Response({'csrfToken': csrf_token, 'data': data}, status=status.HTTP_200_OK)
        
@api_view(['GET', 'POST'])
def spraywall(request):
    if request.method == 'POST':
        serializer = SprayWallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # pass data back in response
            return Response('hi')
    if request.method == 'GET':
        print('hi')
        queryset = SprayWall.objects.filter(id=2)
        print(queryset)
        serializer = SprayWallSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def add_boulder(request, username):
    if request.method == 'POST':
        person = Person.objects.get(username=username)
        request.data['spraywall'] = person.spraywall.id
        request.data['setter_person'] = person.id
        serializer = BoulderSerializer(data=request.data)
        if serializer.is_valid():
            boulder_instance = serializer.save()
            boulder = Boulder.objects.get(id=boulder_instance.id)
            data = {
                'name': boulder.name, 
                'description': boulder.description, 
                'matching': boulder.matching, 
                'publish': boulder.publish,
                'setter_person__username': boulder.setter_person.username,
                'first_ascent_person__username': boulder.first_ascent_person.username if boulder.first_ascent_person else None,
                'sends': boulder.sends,
                'grade': boulder.grade,
                'rating': boulder.rating,
                'likes_count': boulder.likes_count,
                'id': boulder.id
            }
            csrf_token = get_token(request)
            return Response({'csrfToken': csrf_token, 'data': data}, status=status.HTTP_200_OK)
        
@api_view(['GET'])
def list(request, spraywall_id):
    if request.method == 'GET':
        # get all boulders on the specified spraywall
        boulders = Boulder.objects.filter(spraywall=spraywall_id)
        # get everything except image data, image width, image height --> image data takes very long to load especially when grabbing every single boulder
        data = [
            {
                'id': boulder.id, 
                'name': boulder.name, 
                'description': boulder.description, 
                'matching': boulder.matching, 
                'publish': boulder.publish, 
                'setter': boulder.setter_person.username, 
                'firstAscent': boulder.first_ascent_person.username if boulder.first_ascent_person else None, 
                'sends': boulder.sends, 
                'grade': boulder.grade, 
                'rating': boulder.rating, 
                'likes': boulder.likes_count
            } for boulder in boulders
        ]
        csrf_token = get_token(request)
        return Response({'csrfToken': csrf_token, 'data': data}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def boulder_image(request, boulder_id):
    if request.method == 'GET':
        boulder = Boulder.objects.get(pk=boulder_id)
        data = { 
            'image_uri': "data:image/png;base64," + boulder.boulder_image_data,
            'image_width': boulder.boulder_image_width,
            'image_height': boulder.boulder_image_height 
        }
        csrf_token = get_token(request)
        return Response({'csrfToken': csrf_token, 'data': data}, status=status.HTTP_200_OK)
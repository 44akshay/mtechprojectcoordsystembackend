# from rest_framework.decorators import api_view,authentication_classes,permission_classes
# from rest_framework.authentication import SessionAuthentication,TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

# from rest_framework.response import Response
# from .serializers import UserSerializer
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
# import re


# @api_view(['POST'])
# def login(request):
#     user = get_object_or_404(User,username = request.data['username'])
#     print(user.email)
#     print(user.password)
#     print(user.username)

#     print("hello")
#     print(request.data['password'])
#     if not user.username.endswith('@nitc.ac.in'):
#         return Response({"detail": "Invalid email domain"}, status=status.HTTP_400_BAD_REQUEST)

#     if not user.check_password(request.data.get('password')):
#         return Response({"detail":"Not Found"},status = status.HTTP_404_NOT_FOUND)
    
#     #email_regex = r'^m\d{6}[a-zA-Z]{2}@nitc.ac.in$'
#     email_regex = r'^[a-zA-Z]+_m\d{6}[a-zA-Z]{2}@nitc.ac.in$'
#     print("regex")
#     if  re.match(email_regex, user.username):
#         role = 'Student'
#     else:
#         role = 'Faculty'
#     print("token")
#     token,created = Token.objects.get_or_create(user=user)
#     serializer = UserSerializer(instance=user)
#    # serialiser.data.role = role
#   #  print(serializer)
#     return Response({"token":token.key,"user":serializer.data,"role":role})

# @api_view(['GET'])
# @authentication_classes([SessionAuthentication,TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     print(request.user)

#     user = get_object_or_404(User,email = request.user.email)
#     if user:
#         serializer = UserSerializer(instance=user)
#         # email_regex = r'^m\d{6}[a-zA-Z]{2}@nitc.ac.in$'
#         email_regex = r'^[a-zA-Z]+_m\d{6}[a-zA-Z]{2}@nitc.ac.in$'

#         if  re.match(email_regex, user.username):
#             role = 'Student'
#         else:
#             role = 'Faculty'
#     #user = get_object_or_404(User,username = request.data['username'])

#         print(serializer.data)

#         return Response({"user":serializer.data,"role":role})
#     else:
#         return Response({"detail":"Not Found"},status = status.HTTP_404_NOT_FOUND)

#    # return Response("passed for {}".format(request.user.email))




from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from .serializers import UserSerializer,LimitSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from projects.models import Limits
from django.shortcuts import get_object_or_404
import re
from  faculty.models import *
@api_view(['POST'])
def login(request):
    print("hello world")
    user = get_object_or_404(User,username = request.data['username'])
    print(user.email)
    print(user.password)
    print(user.username)

    print("hello")
    print(request.data['password'])
    if not user.username.endswith('@nitc.ac.in'):
        return Response({"detail": "Invalid email domain"}, status=status.HTTP_400_BAD_REQUEST)

    if not user.check_password(request.data.get('password')):
        return Response({"detail":"Not Found"},status = status.HTTP_404_NOT_FOUND)
    
    #email_regex = r'^m\d{6}[a-zA-Z]{2}@nitc.ac.in$'
    email_regex = r'^[a-zA-Z]+_m\d{6}[a-zA-Z]{2}@nitc.ac.in$'
    print("regex")
    a=[]
    token,created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    if  re.match(email_regex, user.username):
        role = 'Student'
        return Response({"token":token.key,"user":serializer.data,"role":role})  
    else:
        print("token")
        print(Faculty.objects.get(email=user.username))
        role = 'Faculty'
        ob=Faculty.objects.get(email=user.username)
        a.append(ob.isguide)
        a.append(ob.ischair)
        a.append(ob.isprojcoo)
        print(ob.dept)
        print(a)
        return Response({"token":token.key,"user":serializer.data,"role":role,"listofroles":a})
    
   # serialiser.data.role = role
  #  print(serializer)

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    print(request.user)
    user = get_object_or_404(User,email = request.user.email)
    if user:
        serializer = UserSerializer(instance=user)
        # email_regex = r'^m\d{6}[a-zA-Z]{2}@nitc.ac.in$'
        email_regex = r'^[a-zA-Z]+_m\d{6}[a-zA-Z]{2}@nitc.ac.in$'

        if  re.match(email_regex, user.username):
            role = 'Student'
            print(serializer.data)

            return Response({"user":serializer.data,"role":role})
        else:
            role = 'Faculty'
            a=[]
            print("token")
            print(Faculty.objects.get(email=user.username))
            ob=Faculty.objects.get(email=user.username)
            print(ob.dept)
            a.append(ob.isguide)
            a.append(ob.ischair)
            a.append(ob.isprojcoo)
            print(a)
            print(serializer.data)
            return Response({"user":serializer.data,"role":role,"listofroles":a})
    else:
        return Response({"detail":"Not Found"},status = status.HTTP_404_NOT_FOUND)

   # return Response("passed for {}".format(request.user.email))

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def getLimits(request):
    limit_object = Limits.objects.get(Limit="Limit")
    limit_serializer = LimitSerializer(limit_object)
    limit_serializer_data = limit_serializer.data
    return Response({"limit":limit_serializer_data},status=200)

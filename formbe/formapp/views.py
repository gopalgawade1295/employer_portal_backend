from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Company, Posts, Usercompany, Userposts
from django.contrib.auth.models import User
from .serializers import CompanySerializer, UsercompanySerializer, PostsSerializer, UserSerializer, UserSerializerWithToken, UserpostsSerializer
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password

# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def userRegister(request):
    data = request.data

    userexist = Company.objects.filter(email=data['email'])
    if not userexist.exists():
        message = {
            'data': 'Please submit employer registration form for approval.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

    usercompanyexist = Company.objects.get(email=data['email'])
    # usercompanyexist.isVerified==True

    if usercompanyexist.isVerified == True:
        try:
            user = User.objects.create(
                first_name=data['name'],
                username=data['email'],
                email=data['email'],
                password=make_password(data['password'])
            )

            newuser = User.objects.get(email=data['email'])
            companyreg = Company.objects.get(email=data['email'])

            companydata = Usercompany.objects.create(
                user=newuser,
                companyname=companyreg.companyname,
                companynew=usercompanyexist,
                state=companyreg.state,
                district=companyreg.district,
                taluka=companyreg.taluka,
                address=companyreg.address,
                pincode=companyreg.pincode,
                name=companyreg.name,
                email=companyreg.email,
                mobile=companyreg.mobile
            )

            companyregnew = Usercompany.objects.get(email=data['email'])
            companyposts = Posts.objects.all()
            companyinfos = companyposts.filter(companyreq=companyreg)
            serializerdata = PostsSerializer(companyinfos, many=True)

            for i in serializerdata.data:
                Userposts.objects.create(
                    user=newuser,
                    companyreq=companyreg,
                    companynew=companyregnew,
                    jobname=i['jobname'],
                    description=i['description'],
                    count=i['count']
                )

            serializer = UserSerializerWithToken(user, many=False)
            return Response({'data': 'Registration Successful!'})
        except:
            message = {'data': 'Something went wrong!'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
    elif usercompanyexist.isVerified == False:
        message = {'data': 'Your request is approved yet!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    else:
        message = {'data': 'No employer data exist!'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def getRoutes(request):
    return Response('Hello...')


@api_view(['POST'])
def registerCompany(request):
    data = request.data

    companyphoneexist = Company.objects.filter(mobile=data['mobile'])
    if companyphoneexist.exists():
        return Response({'data': 'Employer already registered with this mobile number.'}, status=status.HTTP_400_BAD_REQUEST)

    companyemailexist = Company.objects.filter(email=data['email'])
    if companyemailexist.exists():
        return Response({'data': 'Employer already registered with this email.'}, status=status.HTTP_400_BAD_REQUEST)

    companydata = Company.objects.create(
        companyname=data['companyname'],
        state=data['state'],
        district=data['district'],
        taluka=data['taluka'],
        address=data['address'],
        pincode=data['pincode'],
        name=data['name'],
        email=data['email'],
        mobile=data['mobile'],
    )

    serializer = CompanySerializer(companydata, many=False)
    return Response({'data': serializer.data})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getCompanies(request):
    companies = Usercompany.objects.all()
    serializer = UsercompanySerializer(companies, many=True)
    return Response({'companies': serializer.data})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getCompaniesNotApprove(request):
    companies = Company.objects.filter(isVerified=False)
    serializer = CompanySerializer(companies, many=True)
    return Response({'companies': serializer.data})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getCompaniesNotOnPortals(request):
    emailA = list(Usercompany.objects.values_list('email', flat=True))
    emailB = list(Company.objects.values_list('email', flat=True))
    email_list = list(set(emailB).difference(emailA))
    for i in email_list:
        companies = Company.objects.filter(isVerified=True, email=i)

    serializer = CompanySerializer(companies, many=True)
    return Response({'data': serializer.data})


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def getMyCompanyDetails(request):
    data = request.data
    usercompanyexist = Usercompany.objects.get(email=data['email'])
    serializer = UsercompanySerializer(usercompanyexist, many=False)
    return Response({'data': serializer.data})


@api_view(['POST'])
def getMyCompanyPosts(request):
    data = request.data
    userpostexist = Userposts.objects.filter(user=data['user'])
    serializer = UserpostsSerializer(userpostexist, many=True)
    return Response({'data': serializer.data})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def acceptRequest(request):
    companies = Company.objects.all()
    serializer = CompanySerializer(companies, many=True)
    return Response({'companies': serializer.data})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getPosts(request):
    jobposts = Posts.objects.all()
    serializer = PostsSerializer(jobposts, many=True)
    return Response({'jobposts': serializer.data})


@api_view(['POST'])
def registerPosts(request):
    data = request.data
    companyregistered = Company.objects.get(uid=data['id'])
    companyposts = data['posts']

    for i in companyposts:
        post = Posts.objects.create(
            companyreq=companyregistered,
            jobname=i['jobname'],
            description=i['description'],
            count=i['count']
        )

    serializer = PostsSerializer(post, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def registerUserPosts(request):
    data = request.data
    user = User.objects.get(id=data['user'])
    companyA = Company.objects.get(uid=data['companynew'])
    companyB = Usercompany.objects.get(uid=data['companyreq'])
    serializer = UsercompanySerializer(companyB, many=False)
    # return Response(serializer.data)

    Userposts.objects.create(
        user=user,
        companynew=companyB,
        companyreq=companyA,
        jobname=data['jobname'],
        description=data['description'],
        count=data['count'],
    )

    return Response(serializer.data)


@api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
def editPost(request):
    data = request.data
    post = Userposts.objects.get(uid=data['uid'])
    try:
        serializer = UserpostsSerializer(post, data=data, partial=True)
        if not serializer.is_valid():
            return Response({'data': 'Something went wrong!'})
        serializer.save()
        return Response({'data': 'Post updated successfully!'})
    except:
        return Response({'data': 'Something went wrong!'})


@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def deletePost(request,pk):
    data = request.data
    post = Userposts.objects.get(uid=pk)
    try:
        serializer = UserpostsSerializer(post, data=data, partial=True)
        if not serializer.is_valid():
            return Response({'data': 'Something went wrong!'})
        post.delete()
        return Response({'data': 'Post deleted successfully!'})
    except:
        return Response({'data': 'Something went wrong!'})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response({'data': serializer.data})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response({'data': serializer.data})


@api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
def approveCompany(request):
    data = request.data
    usercompanyexist = Usercompany.objects.get(email=data['email'])
    user = User.objects.get(id=data['user'])
    if user.is_staff == True:
        if usercompanyexist.isVerified == False:
            usercompanyexist.isVerified = True
            usercompanyexist.save()
            return Response({'data': 'Account activated successfully.'})
        else:
            usercompanyexist.isVerified = False
            usercompanyexist.save()
            return Response({'data': 'Account deactivated successfully.'})
    else:
        return Response({'data': 'You have not access to Activate/Deactivate Company.'})

    # serializer = CompanySerializer(usercompanyexist, many=False)
    return Response({'data': 'Success'})


@api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
def approveRequest(request):
    data = request.data
    usercompanyexist = Company.objects.get(email=data['email'])
    user = User.objects.get(id=data['user'])
    if user.is_staff == True:
        if usercompanyexist.isVerified == False:
            usercompanyexist.isVerified = True
            usercompanyexist.save()
            return Response({'data': 'Request accepted successfully.'})
        else:
            usercompanyexist.isVerified = False
            usercompanyexist.save()
            return Response({'data': 'Request declined successfully.'})
    else:
        return Response({'data': 'You have not access to Activate/Deactivate Company.'})
    return Response({'data': 'Success'})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProfileOveriew(request):
    return Response(
        {
            'Total': Usercompany.objects.count(),
            'Accepted': Usercompany.objects.filter(isVerified=True).count(),
            'Deactivated': Usercompany.objects.filter(isVerified=False).count(),
            'New_Requests': Company.objects.filter(isVerified=False).count(),
            'Request_Accepted': Company.objects.filter(isVerified=True).count(),
        }
    )

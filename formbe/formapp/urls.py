from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes, name='routes'),
    path('user/login/', views.MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('user/register/', views.userRegister, name='userregister'),
    path('user/profile/', views.getUserProfile, name='userprofile'),
    path('company/register/', views.registerCompany, name='companyregister'),
    path('company/posts/', views.registerPosts, name='companyposts'),
    path('companies/', views.getCompanies, name='companies'),
    path('mycompany/', views.getMyCompanyDetails, name='mycompany'),
    path('company/allposts/', views.getPosts, name='companyallposts'),
    path('company/myposts/', views.getMyCompanyPosts, name='myposts'),
    path('company/createpost/', views.registerUserPosts, name='createpost'),
    path('user/approve/', views.approveCompany, name='approvecompany'),
    path('company/approve/', views.approveRequest, name='approverequest'),
    path('overview/', views.getProfileOveriew, name='overview'),
    path('companies/notapproved/', views.getCompaniesNotApprove, name='companiesnotapproved'),
    path('companies/notinportal/', views.getCompaniesNotOnPortals, name='companiesnotinportal'),
    path('company/edit/', views.editPost, name='companyedit'),
    path('company/delete/<str:pk>', views.deletePost, name='companydelete'),
]

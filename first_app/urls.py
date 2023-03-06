

from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
#from .views import my_view

router = DefaultRouter()
router.register("register1",views.UserViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('Beeline/',views.BeelineListView.as_view()),
    path('Beeline/<int:pk>',views.BeelineDetailListView.as_view()),
    path('Profile/',views.ProfileListView.as_view()),
    path('Profile/<int:pk>',views.ProfileDetailListView.as_view()),
    path('addbeeline/',views.BeelineUploadView.as_view()),
    path('addprofile/',views.ProfileUploadView.as_view()),
    path('UpdataBeeline/<int:pk>',views.UpdataBeelineView.as_view(),name="updated_beeline"),
    path('UpdataProfileView/<int:pk>',views.UpdataProfileView.as_view(),name="updated_profile"),

    #path('practie_count/',views.PracticeCount.as_view()),
    path('overall/',views.OverallCount.as_view()),
    path('OverallProfileCount/',views.OverallProfileCount.as_view()),

    path('login/',views.LoginView.as_view(),name="login"),
    path('password/',views.PasswordReset.as_view(),name="password"),
    path('createUser/',views.Register.as_view(),name="Register"),

    path('mail_new_beeline/',views.New_beeline_Mail.as_view()),
    path('mail_new_profile/',views.New_profile_Mail.as_view()),
    path('mail_updated_beeline/',views.Update_Beeline_Mail.as_view()),
    path('mail_updated_profile/',views.Updated_profile_Mail.as_view()),
    path('mail_delete_profile/<int:pk>',views.Profile_delete_Mail.as_view(),name="mail_profile_beeline"),
    path('mail_delete_beeline/<int:pk>',views.Beeline_delete_Mail.as_view(),name="mail_delete_beeline"),
    path('mail_contact_us/',views.Contact_Us_Mail.as_view()),
    #path('AutomaticClose/',views.AutomaticClose.as_view()),
    path('SendCrendentials/',views.SendCrendentials.as_view()),
    #path('my-url/', my_view, name='my_view'),
    path('ResetPasswordMail/',views.ResetPasswordMail.as_view()),

    path('alertsendmail/',views.AlertMail.as_view()),

    path('EditUserInfo/<int:pk>',views.EditUserInfo.as_view(),name="edituserinfo"),
    
    
    

    
    
    
    
]
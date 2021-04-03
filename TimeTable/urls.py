from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from TimeTable import views

urlpatterns = [
    path('',views.homePage, name = 'homePage'),
    path('timetablescan/',views.scanTimeTable, name = 'scanTimeTable'),
    path('searchdata/',views.searchData, name = 'searchData'),
    path('displayuserdata/',views.displayUserData, name = 'displayUserData'),
    path('loginpage/',views.loginPage, name = 'loginPage'),
    path('registrationpage/',views.registrationPage, name = 'registrationPage'),
    path('logoutpage/',views.logoutPage, name = 'logoutPage'),
    path('contactUs/' ,views.contactPage, name = 'contactPage'),
    path('aboutUs/' ,views.aboutUs, name = 'aboutUs'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

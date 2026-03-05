# urls.py
from django.urls import path
from .views import (
    home,
    user_login,
    custom_logout,
    signup,
    landing_page,
    report_list,
    add_report,
    add_rv,
    rv_list,
    edit_report,
    delete_report,
    delete_rv,
    edit_rv,
)


urlpatterns = [
    path('', home, name='home'),  # Home page
    path('accounts/login/', user_login, name='login'),  # Login page
    path('logout/', custom_logout, name='custom_logout'), 
    path('accounts/signup/', signup, name='signup'),  # Registration page
    path('landing_page/', landing_page, name='landing_page'),  # Landing page after login
    path('report_list/', report_list, name='report_list'),  # Corrected URL for reports list
    path('add_report/', add_report, name='add_report'),  # Add report
    path('add_rv/', add_rv, name='add_rv'),  # Add RV (Person)
    path('rv_list/', rv_list, name='rv_list'), 
    path('edit_report/<int:id>/', edit_report, name='edit_report'),
    path('reports/delete/<int:report_id>/', delete_report, name='delete_report'),  # List of persons
    path('edit_rv/<int:id>/', edit_rv, name='edit_rv'),
    path('delete_rv/<int:id>/', delete_rv, name='delete_rv'),
]
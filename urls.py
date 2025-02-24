from django.urls import path
from .views import TestplanWizard, create_testplan_steps, hello_view
from . import api_views

urlpatterns = [
    # Existing URLs from the current project
    path('create/<int:reservation_id>/', TestplanWizard.as_view(), name='create_testplan'),
    path('create_steps/<int:testplan_id>/', create_testplan_steps, name='create_testplan_steps'),
    path('hello/', hello_view, name='hello'),

    # API endpoints
    path('api/templates_list/', api_views.templates_list, name='templates_list'),
    path('api/predefined_steps_list/', api_views.predefined_steps_list, name='predefined_steps_list'),
    path('api/load_template/<int:template_id>/', api_views.load_template, name='load_template'),
    path('api/save_predefined_step/', api_views.save_predefined_step, name='save_predefined_step'),
    path('api/save_template/', api_views.save_template, name='save_template'),
]
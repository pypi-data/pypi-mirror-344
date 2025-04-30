from . import views
from django.urls import path

urlpatterns = [
    path("exports/insurees", views.export_insurees),
    path("imports/insurees", views.import_insurees),
]

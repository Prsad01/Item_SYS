from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from Item_app.views import ItemView

router = DefaultRouter()

router.register('items',ItemView)
urlpatterns = [
   
]+router.urls

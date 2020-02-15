from dateutil import parser
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import datetime
from .forms import CreateRoomForm
from .models import Room, Booking

# Create your views here.

from dateutil import parser
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import datetime
from .forms import CreateRoomForm
from .models import Room, Booking


class MakeReservationView(View):
    def get(self, request, id):
        room = get_object_or_404(Room, pk=id)
        template_name = 'make_reservation.html'
        ctx = {
            'room': room
        }

        return render(request, template_name, ctx)

    def post(self, request, id):
        room = get_object_or_404(Room, pk=id)
        template_name = 'make_reservation.html'
        minimal_date = datetime.datetime.now().date()

        if request.POST.get('book'):
            booking_date = parser.parse(request.POST.get('booking_date')).date()
            if booking_date > minimal_date:
                try:
                    Booking.objects.get(date=parser.parse(request.POST.get('booking_date')).date())
                except ObjectDoesNotExist:
                    Booking.objects.create(
                        date=parser.parse(request.POST.get('booking_date')).date(),
                        comment=request.POST.get('comment'),
                        room=room)
                    ctx = {
                        'msg': f"""You've successfully booked a room {room.name} 
                                    for {parser.parse(request.POST.get('booking_date')).date()}."""
                    }
                else:
                    ctx = {
                        'msg': "That room has been already booked."
                    }
            else:
                ctx = {
                    'msg': "Please choose a correct date."
                }

        return render(request, template_name, ctx)

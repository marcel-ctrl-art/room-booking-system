from dateutil import parser
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView
import datetime

from .forms import CreateRoomForm
from .models import Room, Booking


class MakeReservationView(View):
    """Book a particular room for a selected day."""

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


class CreateRoomView(View):
    """Add a new room to the database."""

    def get(self, request):
        template_name = 'create_room.html'
        form = CreateRoomForm
        return render(request, template_name, {'form': form})

    def post(self, request):
        template_name = 'create_room.html'
        form = CreateRoomForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            capacity = form.cleaned_data['capacity']
            has_projector = form.cleaned_data['has_projector']

            if not Room.objects.filter(name=form.cleaned_data['name']).exists():
                new_room = Room.objects.create(name=name, capacity=capacity, has_projector=has_projector)
                new_room.save()
                ctx = {'msg': 'New room has been added successfuly to our database',
                       'form': form}
            else:
                ctx = {'msg': 'That room already exists in our database'}

        return render(request, template_name, ctx)


class RoomDetailsView(View):
    """Display data of particular room."""

    def get(self, request, id):
        room = get_object_or_404(Room, pk=id)
        template_name = 'room_details.html'
        ctx = {
            'room': room,
        }
        return render(request, template_name, ctx)


class UpdateRoomView(View):
    """Edit data of existing model instance."""

    def get(self, request, id):
        room = get_object_or_404(Room, pk=id)
        template_name = 'update_room.html'
        form = CreateRoomForm(instance=room)
        ctx = {
            'room': room,
            'form': form,
        }
        return render(request, template_name, ctx)

    def post(self, request, id):
        room = get_object_or_404(Room, pk=id)
        form = CreateRoomForm(request.POST, instance=room)

        if form.is_valid():
            obj = form.save()
            obj.save()

        return redirect('room_details', id=room.id)


class AllRoomsView(View):
    """View to display all existing rooms within their booking status."""

    def get(self, request):
        rooms = Room.objects.all().order_by('name')
        template_name = 'all_rooms.html'
        today = datetime.datetime.now().date()

        for room in rooms:
            try:
                Booking.objects.get(date=today).filter(room=room)
            except ObjectDoesNotExist:
                status = 'available'
            else:
                status = 'booked'

        ctx = {
            'rooms': rooms,
            'status': status,
        }

        return render(request, template_name, ctx)


class DeleteRoomView(View):
    """Delete chosen room."""

    def get(self, request, id):
        room = get_object_or_404(Room, pk=id)
        msg = f"You are about to delete a following room: {room.name}"
        template_name = 'delete_room.html'
        ctx = {
            'room': room,
            'msg': msg,
        }
        return render(request, template_name, ctx)

    def post(self, request, id):
        room_to_del = get_object_or_404(Room, pk=id)

        if request.POST.get('delete'):
            room_to_del.delete()
            return redirect('deleted_room')

        elif request.POST.get('no_delete'):
            return redirect('/')


class DeletedRoomView(View):
    """A view deleting a model instance."""

    def get(self, request):
        tempalte_name = 'deleted_room_view.html'
        return render(request, tempalte_name)


class SearchRoomView(View):

    def get(self, request):
        pass


class HomeView(TemplateView):
    template_name = 'home.html'
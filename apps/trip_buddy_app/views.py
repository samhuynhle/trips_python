from django.shortcuts import render, redirect
from .models import *
from apps.login_registration_app.models import *
from django.contrib import messages
from datetime import *

from datetime import date, datetime, timezone

def dashboard_display(request):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_user_trips = Trip.objects.filter(creator = current_user)
    current_user_joined_trips = current_user.travelers.all()
    all_other_trips = Trip.objects.exclude(creator = current_user)

    context = {
        'current_user': current_user,
        'current_user_trips': current_user_trips,
        'current_user_joined_trips' : current_user_joined_trips,
        'all_other_trips': all_other_trips,

    }

    return render(request, 'trip_buddy_app/dashboard.html', context)

def create_trip_display(request):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])

    context = {
        'current_user': current_user
    }

    return render(request, 'trip_buddy_app/display_create_trip.html', context)

def edit_trip_display(request, trip_id):
    if request.session['user_id'] == 'logged out':
        return redirect('/')


    current_user = User.objects.get(id=request.session['user_id'])
    current_trip = Trip.objects.get(id=trip_id) 

    if current_user.id != current_trip.creator.id:
        return redirect('/')

    request.session['current_trip'] = trip_id

    start_date = current_trip.start_date
    end_date = current_trip.end_date

    context = {
        'current_user': current_user,
        'current_trip': current_trip,
        'current_trip_start_date': str(start_date),
        'current_trip_end_date': str(end_date)
    }

    return render(request, 'trip_buddy_app/display_edit_trip.html', context)

def create_trip_process(request):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])

    errors = Trip.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/trips/new")
    else:
        new_trip = Trip.objects.create(
            destination= request.POST['destination'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
            plan=request.POST['plan'],
            creator=current_user)
        
        new_trip.save()

        return redirect('/dashboard')

def edit_trip_process(request, trip_id):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_trip = Trip.objects.get(id=request.POST['trip_id'])

    errors = Trip.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect("/trips/edit")
    else:
        current_trip.destination = request.POST['destination']
        current_trip.start_date = request.POST['start_date']
        current_trip.end_date = request.POST['end_date']
        current_trip.plan = request.POST['plan']
        
        current_trip.save()

        return redirect('/dashboard')

def trip_display(request, trip_id):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_trip = Trip.objects.get(id=trip_id)
    current_user = User.objects.get(id=request.session['user_id'])

    list_of_trips_travelers = current_trip.travelers.all()

    context = {
        'current_user': current_user,
        'current_trip': current_trip,
        'current_trip_travelers': list_of_trips_travelers,
    }

    return render(request, 'trip_buddy_app/display_trip_details.html', context)

def user_join_trip(request, trip_id):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_trip = Trip.objects.get(id=trip_id)

    current_trip.travelers.add(current_user)

    return redirect('/dashboard')

def user_leave_trip(request, trip_id):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_trip = Trip.objects.get(id=trip_id)

    current_trip.travelers.remove(current_user)

    return redirect('/dashboard')

def remove_trip(request, trip_id):
    if request.session['user_id'] == 'logged out':
        return redirect('/')

    current_user = User.objects.get(id=request.session['user_id'])
    current_trip = Trip.objects.get(id=trip_id)

    if current_trip.creator.id != current_user.id:
        return redirect('/')
    else:
        current_trip.delete()
        return redirect('/dashboard')
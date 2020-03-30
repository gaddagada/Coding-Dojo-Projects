from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from .models import *
from django.contrib import messages 
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
    return render(request, 'trip_buddy_app/index.html')

# Register new user
def register(request):
    #handling logic if correct input isn't provided 
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else: 
        if request.method =="POST":
            # Hashing passwords to bycrypt so outsiders can't view information saved in DB
            password = request.POST['pw']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            # Using query commands used in Django ORM to create instances of the attrubutes specified in the models.py file
            new_user = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], pw_hash=pw_hash.decode())
            # Save the input in session created by the new_user temporary defined in line above to a variable so it can be easily accessed
            request.session['userid'] = new_user.id
                #print('user:id -',new_user.id)
            # Notifying the user that just registered 
            messages.success=(request, "Successfully registered")
        return redirect("/traveldashboard/")   
        #return redirect("/success")
    return redirect("/")

# Login
def login(request):
    if request.method == 'POST':
        email = User.objects.filter(email = request.POST['email'])
        if email: 
            user = email[0]
            if bcrypt.checkpw(request.POST['pw'].encode(), user.pw_hash.encode()):
                request.session['userid'] = user.id
                currentUser = User.objects.get(id=user.id)
                messages.success=(request, "Successfully logged in")
                #return redirect("/success")
                #return redirect('/traveldashboard/')
                context = {
                    'trips' : Trip.objects.filter(trip_members=request.session['userid']),
                    'other_trips' : Trip.objects.exclude(trip_members=request.session['userid']),
                    "currentUser" : currentUser
                }     
                return render(request, 'trip_buddy_app/travels.html', context)
                #return render(request, 'trip_buddy_app/travels.html')
            else: 
                messages.error(request, "Incorrect password")
                return redirect('/')
        
    return HttpResponse("User does not exist")

# Display success page.
def set_password(self, pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    self.password_hash = pwhash.decode('utf8')

def success(request):
    if 'userid' not in request.session:
        return redirect('/')
    else: 
        num = request.session['userid']
        context = {
            "user" : User.objects.get(id=num)
        }
        return render(request, 'trip_buddy_app/success.html', context)

# Logout
def logout(request): 
    request.session.clear()
    return redirect('/')



def addTrip(request):

    if request.method =="POST":
        # get current user
        num = request.session['userid']
        currentUser = User.objects.get(id=num)
        context = {
            "currentUser" : currentUser         
        }
        
        # # Using query commands used in Django ORM to create instances of the attributes specified in the models.py file
        # new_trip = Organization.objects.create(org_name = orgName, description = orgDesc, created_by=currentUser.first_name +" " + currentUser.last_name)
        # # new_org.user.add(currentUser)
        # # Notifying the User that just youregistered 
        # messages.success=(request, "Successfully added new Organization")
    
    return render(request, 'trip_buddy_app/addTrip.html')
        #return render(request, 'trip_buddy_app/addTrip.html')

        #return HttpResponseRedirect(request, "trip_buddy_app/addTrip.html", context)

def saveTrip(request):

    if request.method =="POST":
        paramDestination = request.POST['destination']
        paramDateFrom = request.POST['date_from']
        paramDateTo = request.POST['date_to']
        paramPlan = request.POST['plan'] 
        paramUsedId = request.session['userid']
        currentUser = User.objects.get(id=paramUsedId)
        context = {
            "currentUser" : currentUser
        }

        result = Trip.objects.trip_validator(request.POST)
        errors = result['errors']
        if result["status"] == True:
            #If everything is ok save the trip
            newtrip = Trip.objects.create(
            destination=paramDestination, start_date=paramDateFrom, end_date=paramDateTo, plan=paramPlan, created_by=currentUser)
            newtrip.trip_members.add(currentUser)
            newtrip.save()
            messages.success=(request, "Successfully added new trip")
            return redirect("/traveldashboard/")
        else:
            if len(errors) > 0:
                for error in errors:
                    messages.error(request, error)
                return render(request, 'trip_buddy_app/addTrip.html')
    
    return redirect("/traveldashboard/") 

def showtraveldashboard(request):

        num = request.session['userid']
        currentUser = User.objects.get(id=num)       
        print("currentUser.id----------------->" + str(currentUser.id))
        #print("current_org.user.id----------------->" + str(current_org.user.get(id=currentUser.id).id))
        #current_members = current_org.user.all()
        context = {
        'trips' : Trip.objects.filter(trip_members=request.session['userid']),
        'other_trips' : Trip.objects.exclude(trip_members=request.session['userid']),
        "currentUser" : currentUser
        }     
        return render(request, 'trip_buddy_app/travels.html', context)

def joinTrip(request, id):
    trip = Trip.objects.get(id=id)
    #print("Trip.objects.get(id=id).created_by_id) " + str(Trip.objects.get(id=id).created_by_id))
    trip.trip_members.add(User.objects.get(id=request.session['userid']))
    return redirect('/traveldashboard/')

def cancelTrip(request, id):
    trip = Trip.objects.get(id=id)
    #print("cancelTrip ------>1111 " + str(Trip.objects.get(id=id).created_by_id))
    #print("cancelTrip ------>2222 " + str(Trip.objects.get(id=id).created_by_id))
    trip.trip_members.add(User.objects.filter(joined_trips=id).exclude(id=(Trip.objects.get(id=id).created_by_id)))    
    print("canceled the trip ------------2222")
    return redirect('/traveldashboard/')

def showDestination(request, id):
    context = {
        'trip' : Trip.objects.get(id=id),
        'planner' : User.objects.get(id=(Trip.objects.get(id=id).created_by_id)).last_name,
        'others' : User.objects.filter(joined_trips=id).exclude(id=(Trip.objects.get(id=id).created_by_id))
    }
    return render(request, "trip_buddy_app/destination.html", context)

def removeTrip(request, id):
    trip = Trip.objects.get(id=id)
    trip.delete()
    return redirect('/traveldashboard/')


def editTrip(request, id):
    trip = Trip.objects.get(id=id)
    context = {
        'trip' : Trip.objects.get(id=id)        
    }
    return render(request, "trip_buddy_app/editTrip.html", context)


def updateTrip(request, id):

    if request.method =="POST":
        trip = Trip.objects.get(id=id)
        num = request.session['userid']
        currentUser = User.objects.get(id=num)
        #print("updateTrip--------------11111>"+ str(trip.id))
        result = Trip.objects.trip_validator(request.POST)
        print(result["status"] )
        print(result["errors"] )
        errors = result['errors']
        if result["status"] == True:
            print("updateTripd--------------2222>"+ str(trip.id))
            #If everything is ok save the trip
            trip.destination=request.POST['destination']
            trip.start_date=request.POST['date_from'] 
            trip.end_date=request.POST['date_to']
            trip.plan=request.POST['plan']
            print("updateTripd--------------3333>"+ str(trip.id))
            #logger.debug("-------------->Updating trip no :" + str(trip.id))
            trip.save() 
            messages.success=(request, "Successfully updated the trip")
            #logger.debug("-------------->Updating trip no :" + str(trip.id))
            return redirect("/traveldashboard/")
        else:
            print("updateTripd--------------4444>"+ str(trip.id))
            for error in errors:
                messages.error(request, error)
            context = {
            "currentUser" : currentUser,
            "messages" : messages
            }
            return redirect(request, "trip_buddy_app/editTrip.html", context)


    return redirect("/traveldashboard/") 
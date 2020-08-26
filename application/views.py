from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
import json

# main page function

def index(request):
    all_places = place_information.objects.all()

    for i in all_places:
        print(i.place_type)
        # if i.end_date_time and i.end_date_time >= datetime.now():
        if i.place_type=="temporary" and i.end_date_time and i.end_date_time.strftime('%Y-%m-%d %H:%M:%S')<datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            i.delete()
    
    # all_places.save()



    return redirect("show")


def add_sec_imgs(request):

    if request.method == 'POST':
        place_id = request.POST['place_id']
        print(place_id)

        get_place = place_information.objects.get(id=int(place_id))
        
        if 'image2' in request.FILES:
            img_1 = request.FILES['image2']
            get_place.sec_place_1 = img_1
            print(img_1)

        if 'image3' in request.FILES:
            img_2 = request.FILES['image3']
            get_place.sec_place_2 = img_2
            print(img_2)

        if 'image4' in request.FILES:
            img_3 = request.FILES['image4']
            get_place.sec_place_3 = img_3
            print(img_3)

        if 'image5' in request.FILES:
            img_4 = request.FILES['image5']
            get_place.sec_place_4 = img_4
            print(img_4)

        get_place.save()
       
        return redirect("place/"+place_id)

# perticular place

def place(request, id):
    focused_place = place_information.objects.get(id=id)
    context = {
        'place': focused_place
    }

    count_sec_images = 0
    if focused_place.sec_place_1:
        count_sec_images += 1

    if focused_place.sec_place_2:
        count_sec_images += 1
    
    if focused_place.sec_place_3:
        count_sec_images += 1
    
    if focused_place.sec_place_4:
        count_sec_images += 1
    
    context['count_sec_images'] = count_sec_images


    return render(request, 'place.html', context)


# Show all pins places with info
def show(request):
    context = {}

    if 'type' in request.GET:
        if request.GET['type']=='temporary':
            context['all_places'] = place_information.objects.filter(place_type='temporary')
        elif request.GET['type']=='permanent':
            context['all_places'] = place_information.objects.filter(place_type='permanent')
        else:
            context['all_places'] = place_information.objects.all()
    else:
        context['all_places'] = place_information.objects.all()
        
    return render(request, 'show.html', context)


def add_videos(request):
    if request.method == 'POST':
        place_id = request.POST['place_id1']
        video = request.FILES['video1']

        get_place = place_information.objects.get(id=int(place_id))
        get_place.video = video
        get_place.save()

        return redirect("place/"+place_id)



# add pin place

def add(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == 'POST':
        place_image = request.FILES['image']
        place_name = request.POST['lc_name']
        place_description = request.POST['lc_details']
        place_longitude = request.POST['longitude']
        place_latitude = request.POST['latitude']
        place_ratings = request.POST['lc_rating']
        place_type = request.POST['lc_type']

        # end_datetime = request.POST['lc_end_date']

        if 'lc_start_date' in request.POST and 'lc_end_date' in request.POST and request.POST['lc_start_date']!="" and request.POST['lc_end_date']!="":
            start_date_time = request.POST['lc_start_date']
            end_date_time = request.POST['lc_end_date']

            print(type(start_date_time))
            print(end_date_time)

            new_place = place_information(
                place_image=place_image, 
                place_name=place_name,
                place_description=place_description,
                place_longitude=place_longitude,
                place_latitude=place_latitude,
                place_ratings=place_ratings,
                place_type=place_type,
                added_by=request.user,
                start_date_time=start_date_time,
                end_date_time=end_date_time
            )
            new_place.save()

            print("Going into temporary condition")


        else:
            new_place = place_information(
                place_image=place_image, 
                place_name=place_name,
                place_description=place_description,
                place_longitude=place_longitude,
                place_latitude=place_latitude,
                place_ratings=place_ratings,
                place_type=place_type,
                added_by=request.user,
            )

            new_place.save()

        
        if 'image2' in request.FILES:
            img_1 = request.FILES['image2']
            new_place.sec_place_1 = img_1
          
        if 'image3' in request.FILES:
            img_2 = request.FILES['image3']
            new_place.sec_place_2 = img_2

        if 'image4' in request.FILES:
            img_3 = request.FILES['image4']
            new_place.sec_place_3 = img_3

        if 'image5' in request.FILES:
            img_4 = request.FILES['image5']
            new_place.sec_place_4 = img_4

        if 'video1' in request.FILES:
            video = request.FILES['video1']
            new_place.video = video

        new_place.save()


        return redirect("index")

    return render(request, 'main.html')


def myplaces(request):
    if not request.user.is_authenticated:
        return redirect("login")

    all_places = place_information.objects.filter(added_by=request.user)

    context = {
        'all_places': all_places
    }

    return render(request, 'places.html', context)


def removing(request, id):
    try:
        target_place = place_information.objects.get(id=id)
        target_place.delete()
        return redirect("myplaces")
    except:
        return redirect("myplaces")

# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
        }
        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered number already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


    
    return render(request, "signup.html")


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")


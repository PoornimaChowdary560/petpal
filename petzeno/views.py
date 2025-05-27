from django.shortcuts import render,redirect,get_object_or_404
from .models import User,Pet,Wishlist,Order,Form,SuccessStory
from django.contrib import messages
"""from django.contrib.auth.decorators import login_required"""


def signup(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        p1=request.POST['password']
        p2=request.POST['confirm_password']
        phone=request.POST['phone']
        role=request.POST['role']
        if p1==p2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already exist')
                return redirect('signup')
            if User.objects.filter(name=name).exists():
                messages.info(request,'user already exist')
                return redirect('signup')
            else:
                User.objects.create(name=name,email=email,password=p1,phone=phone,role=role)
                return redirect('login')
        else:
            messages.info(request,'password not matched')
            return redirect('signup')
    return render(request,'signup.html')

def login(request): 
    if request.method=='POST':
        name=request.POST['name']
        password=request.POST['password']
        if User.objects.filter(name=name,password=password).exists():
            user=User.objects.get(name=name,password=password)
            if user.password==password:
                request.session["id"]=user.id
                request.session["role"]=user.role
                request.session["name"]=user.name
                request.session["phone"]=user.phone
                request.session["email"]=user.email
                request.session["password"]=user.password
                """login(request,user)"""
                if user.role=='admin':
                    return redirect('adhome')
                elif user.role=='buyer':
                    return redirect('bhome')
                elif user.role=='seller':
                    return redirect('shome')
                else:
                    return redirect('home')
                '''return redirect('home')'''
            else:
                messages.info(request,'username or password incorrect')
                return redirect('login')
        else:
            messages.info(request,'username or password incorrect ')
            return redirect('login')
    return render(request,'login.html')

def start(request):
    if "id"  in request.session:
        user=User.objects.get(id=request.session["id"])
        if user.role=="seller":
            return redirect("shome")
        elif user.role=="buyer":
            return redirect("bhome")
        elif user.role=="admin":
            return redirect("adhome")
        else:
            return redirect("home")
    else:
        return render(request,'start.html')


def logout(request):
    request.session.flush()
    return redirect("login")

def home(request):
    return render(request,'home.html')

def shome(request):
    id=request.session['id']
    seller=User.objects.get(id=id)
    requests = Order.objects.filter(seller=seller, request_status="pending")
    return render(request, 'shome.html', {'requests': requests})
    

def bhome(request):
    id=request.session['id']
    buyer=User.objects.get(id=id)
    orders = Order.objects.filter(buyer=buyer, request_status="accepted", payment_status=False)
    return render(request, 'bhome.html', {'orders': orders})


def adhome(request):
    return render(request,'adhome.html')

def adopt(request):
    return render(request,'adaptionprocess.html')

def avail(request):
    
    pets=Pet.objects.filter(adoption_status="available")
    name=request.session['name']
    user=User.objects.get(name=name)
    context={
        'pets':pets,
        'user':user,

    }
    return render(request,'availablepets.html',context)

def contact(request):
    return render(request,'contact.html')


def uploadpet(request):
    if request.method == "POST":
        name = request.POST.get('name')
        photo = request.FILES.get('photo')
        species = request.POST.get('species')
        """breed = request.POST.get('breed')"""
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        health_status = request.POST.get('health_status')
        personality_traits = request.POST.get('personality_traits')
        adoption_status = request.POST.get('adoption_status')
        location=request.POST.get('location')
        user = User.objects.get(id=request.session['id'])  # Assuming session stores user ID
        cost = request.POST.get('cost')
        if species == "other":
            species = request.POST.get("other_species", "").strip()
            breed = request.POST.get("other_breed", "").strip()

        else:
            breed = request.POST.get('breed')
            if breed == "other":
                breed = request.POST.get("other_breed_input", "").strip()
        """if species == "other" and other_species:
            species = other_species

        # Handle "Other" breed
        if breed == "other" and other_breed:
            breed = other_breed"""
        pet = Pet.objects.create(
        
            name=name,
            photo=photo,
            species=species,
            breed=breed,
            age=age,
            gender=gender,
            health_status=health_status,
            personality_traits=personality_traits,
            adoption_status=adoption_status,
            location=location,
            user=user,
            cost=cost
        )
        return redirect('shome')

    return render(request, 'uploadpet.html')

def mypetlist(request):
    id=request.session['id']
    user=User.objects.get(id=id)
    total_pets = Pet.objects.filter(user=user)  # Fetch all pets of the seller
    pending_pets = total_pets.filter(adoption_status='pending')  # Filter pending status pets
    sold_pets = total_pets.filter(adoption_status='sold')  # Filter sold pets

    context = {
        'total_pets': total_pets.count(),
        'pending_pets': pending_pets.count(),
        'sold_pets': sold_pets.count(),
        'pets': total_pets,  # Passing all pets to display details
    }
    return render(request,'mypetlist.html',context)


def successstories(request):
    stories = SuccessStory.objects.order_by('-created_at')
    return render(request,'success.html', {'stories': stories})

def submit_story(request):
    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        owner_name = request.POST.get('owner_name')
        story = request.POST.get('story')
        image = request.FILES.get('image')  # Optional

        SuccessStory.objects.create(
            pet_name=pet_name,
            owner_name=owner_name,
            story=story,
            image=image if image else 'default_pet.jpg'
        )
        return redirect('successstories')

    return render(request, 'submit_story.html')
def viewedit(request):
    id=request.session['id']
    user=User.objects.get(id=id)
    seller_pets = Pet.objects.filter(user=user)  # Show only seller's pets
    return render(request, 'viewedit.html', {'pets': seller_pets})

def editpet(request, id):
    pet = get_object_or_404(Pet, id=id)

    if request.method == "POST":
        pet.name = request.POST.get("name")
        pet.age = request.POST.get("age")
        pet.breed = request.POST.get("breed")
        pet.species = request.POST.get("species")
        pet.gender = request.POST.get("gender")
        pet.cost = request.POST.get("cost")
        pet.location = request.POST.get("location")
        pet.health_status = request.POST.get("health_status")
        pet.personality_traits = request.POST.get("personality_traits")
        adoption_status = request.POST.get("adoption_status")
        if adoption_status in ['available', 'pending', 'adopted']:
            pet.adoption_status = adoption_status

        # If a new image is uploaded, update it
        if "photo" in request.FILES:
            pet.photo = request.FILES["photo"]

        pet.save()
        messages.success(request, "Pet details updated successfully!")
        return redirect("viewedit")  # Redirect to seller home page after edit

    return render(request, "edit.html", {"pet": pet})

def deletepet(request, id):
    pet = get_object_or_404(Pet, id=id)
    pet.delete()
    role=request.session['role']
    if role =='admin':
        messages.success(request, "Pet deleted successfully!")
        return redirect("allusers")  # Redirect after deletion
    else:
        messages.success(request, "Pet deleted successfully!")
        return redirect("viewedit")  # Redirect after deletion

def deleteuser(request, id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request, "Pet deleted successfully!")
    return redirect("allusers")  # Redirect after deletion


def update_profile(request):

    user = User.objects.get(id=request.session['id'])  # Get the logged-in user

    if request.method == "POST":
        user.name = request.POST['name']
        user.phone = request.POST['phone']
        user.email = request.POST['email']
        user.password = request.POST['password']  # Store raw password (not recommended for real apps)
        user.save()

        # Flush session and redirect to login
        request.session.flush()
        messages.success(request, "Profile updated successfully. Please log in again.")
        return redirect('login')

    return render(request, 'updateprofile.html', {'user': user})

def totalpetdetails(request,id):
    pets=Pet.objects.get(id=id)
    return render(request,'totaldetails.html',{'pets':pets})

def search_pets(request):
    query = request.GET.get('query', '')  # Get search input
    species = request.GET.get('species', '')  # Get species filter
    breed = request.GET.get('breed', '')  # Get breed filter
    location = request.GET.get('location', '')  # Get location filter

    pets = Pet.objects.all()

    if query:
        pets = pets.filter(name__icontains=query)  # Search pet name
    if species:
        pets = pets.filter(species__icontains=species)
    if breed:
        pets = pets.filter(breed__icontains=breed)
    if location:
        pets = pets.filter(location__icontains=location)

    return render(request, 'search_results.html', {'pets': pets, 'query': query})
                                
def add_to_wishlist(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    user_id=request.session['id']#instead of this we can use request.user
    user=User.objects.get(id=user_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, pet=pet)
    if created:
        messages.success(request, "Pet added to wishlist!")
    else:
        messages.warning(request, "Pet is already in your wishlist!")
    return redirect('wishlist')  # Redirect to wishlist page

def remove_from_wishlist(request,item_id):
    item=get_object_or_404(Wishlist,id=item_id)
    item.delete()
    messages.success(request,"pet remove from wishlist successfully")
    return redirect('wishlist')

"""def add_to_wishlist(request, pet_id):
    pet = Pet.objects.get(id=pet_id)
    user = request.session['id']
    
    if user.role == 'buyer':  # Only allow buyers
        wishlist_item, created = Wishlist.objects.get_or_create(user=user, pet=pet)
        if created:
            message="pet added successfully"
            return redirect('wishlist')  # Redirect to wishlist page
        else:
            message="pet is already in your wishlist"
            return redirect('wishlist')
        return redirect('pet_detail', pet_id=pet.id)"""

"""@login_required"""
def wishlist(request):
    user_id=request.session['id']
    user=User.objects.get(id=user_id)
    items = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist.html', {'items':items})

from django.http import HttpResponse
def book_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    buyer = get_object_or_404(User, id=request.session.get('id'))

    if pet.adoption_status == 'available':
        order = Order.objects.create(
            pet=pet,
            buyer=buyer,
            seller=pet.user
        )
        pet.adoption_status = 'pending'
        pet.save()
        return redirect("add_address", order_id=order.id)
    else:
        # If pet is not available, show a message or redirect
        return HttpResponse("Sorry, this pet is no longer available for booking.", status=400)
    
    

def buyer_order_history(request):
    buyer = User.objects.get(id=request.session['id'])
    orders = Order.objects.filter(buyer=buyer)
    return render(request, 'buyer_order_history.html', {'orders': orders})

def seller_orders(request):
    seller = User.objects.get(id=request.session['id'])
    orders = Order.objects.filter(seller=seller, request_status='pending')
    return render(request, 'seller_orders.html', {'orders': orders})

def accept_request(request, request_id):
    adoption_request = Order.objects.get(id=request_id)
    adoption_request.request_status = 'accepted'
    adoption_request.save()
    return redirect('seller_orders')
def reject_request(request, request_id):
    adoption_request = Order.objects.get(id=request_id)
    adoption_request.request_status = 'rejected'
    adoption_request.save()
    pet=adoption_request.pet
    pet.adoption_status='available'
    pet.save()
    return redirect('seller_orders')

def make_payment(request, request_id):
    if request.method == 'POST':
        adoption_request = Order.objects.get(id=request_id)
        amount= request.POST['amount']
        amount=float(amount)
        pet=adoption_request.pet
        cost=pet.cost
        if (cost==amount):
            adoption_request.payment_amount =amount
            adoption_request.payment_status = True
            adoption_request.save()
           #pet.adoption_status="adopted"
           #pet.save()
            messages.success(request, "Payment successful! Pet adoption completed.")
        else:
            messages.error(request, "Please enter a valid payment amount.")
        return redirect('buyer_order_history')
def order_history(request):
    id=request.session['id']
    seller=User.objects.get(id=id)
    orders=Order.objects.filter(seller=seller,payment_status=True)
    return render(request,'seller_order_history.html',{'orders':orders,})
def allpets(request):
    id=request.session['id']
    user=User.objects.get(id=id)
    pets=Pet.objects.all()
    context={
        'user':user,
        'pets':pets,
    }
    return render(request,'allpets.html',context)

def allusers(request):
    users=User.objects.all()
    return render(request,'allusers.html',{'users':users})

def payment_track(request):
    order=Order.objects.all()
    return render(request,'payment.html',{'orders':order})
def status_change(request,pet_id):
    if request.method == 'POST':
        pet=Pet.objects.get(id=pet_id)
        pet.adoption_status='adopted'
        pet.save()
        return redirect('payment_track')

def adoption_requests(request):
    order=Order.objects.filter(request_status='pending')
    return render(request,'adoption_request.html',{'orders':order})

def cancel_order(request,request_id):
    adoption_request = Order.objects.get(id=request_id)
    pet=adoption_request.pet
    pet.adoption_status='available'
    pet.save()
    adoption_request.delete()
    return redirect("buyer_order_history")

def add_address(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        full_name = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        street = request.POST.get("street")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zipcode = request.POST.get("zipcode")
        details, created = Form.objects.get_or_create(
            id=order,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            street=street,
            city=city,
            state=state,
            zipcode=zipcode,
        )
        if created:
            messages.success(request,"address  added")
        else:
            messages.warning(request,"address already addedd")
        return redirect("buyer_order_history")
    return render(request,'order_form.html')
    

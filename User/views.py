from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile


def HomePage(request):
    user_id = request.session.get('user_id')  # Get logged-in user ID from session
    user_profile = None

    if user_id:
        user_profile = UserProfile.objects.filter(id=user_id).first()  # Check if user registered

    return render(request, 'home.html', {'user_profile': user_profile, 'user_id': user_id})


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('login')

    return render(request, 'signup.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id  # Store user session

            # ✅ Redirect to Dashboard Instead of Profile
            return redirect('dashboard')
        else:
            messages.error(request, "⚠️ Username or Password is incorrect!")
            return redirect('login')

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Register Page (Public Access)


# About Page (Public Access)
def AboutPage(request):
    return render(request, 'about.html')


# Contact Page (Public Access)
def ContactPage(request):
    return render(request, 'contact.html')


def RegisterPage(request):
    return render(request, 'register.html')


from io import BytesIO
import qrcode
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm


def register(request):
    qr_code_url = None  # Initialize QR Code URL as None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save()  # ✅ First, save user data to generate an ID

            # ✅ Generate QR Code with Correct URL
            profile_url = f"http://192.168.247.40:8000/profile/{user_profile.id}/"
            qr = qrcode.make(profile_url)

            # ✅ Save QR Code Image
            qr_io = BytesIO()
            qr.save(qr_io, format='PNG')
            user_profile.qr_code.save(f"qr_{user_profile.id}.png", ContentFile(qr_io.getvalue()), save=True)

            # ✅ Store QR Code URL to send to the template
            qr_code_url = user_profile.qr_code.url

            return redirect('profile', user_id=user_profile.id)  # ✅ Redirect to Profile Page

        else:
            print("❌ Form Errors:", form.errors)  # Debugging Output

    else:
        form = UserProfileForm()

    return render(request, 'register.html', {'form': form, 'qr_code_url': qr_code_url})


from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from .models import UserProfile, Payment

from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from .models import UserProfile, Payment

from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import UserProfile, Payment

from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import UserProfile, Payment  # Ensure models are imported


def profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)

    # Fetch transactions in descending order (latest first)
    transactions = Payment.objects.filter(user=user_profile).order_by('-created_at')

    # Calculate FasTag balance safely (default to 0.00 if no payments)
    balance = transactions.aggregate(Sum('amount'))['amount__sum'] or 0.00

    return render(request, 'profile.html', {
        'user': user_profile,
        'transactions': transactions,  # Renamed for clarity
        'balance': balance
    })


from django.shortcuts import render, redirect
from .models import UserProfile, Payment
import uuid

from django.shortcuts import get_object_or_404, redirect
import uuid

from django.shortcuts import render, get_object_or_404, redirect
import uuid
from .models import UserProfile, Payment

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
import uuid
from .models import UserProfile, Payment


def make_payment(request):
    if request.method == 'POST':
        print("Received POST data:", request.POST)  # Debugging

        user_id = request.POST.get('user_id')
        amount = request.POST.get('amount')

        if not user_id or not amount:
            return HttpResponse("User ID or amount is missing.", status=400)

        # Ensure user exists
        try:
            user = get_object_or_404(UserProfile, id=user_id)
        except:
            return HttpResponse("UserProfile not found.", status=404)

        # Generate a unique transaction ID
        transaction_id = str(uuid.uuid4())

        # Create Payment
        Payment.objects.create(user=user, amount=amount, transaction_id=transaction_id)

        return redirect('profile', user_id=user.id)

    return HttpResponse("Invalid request method.", status=405)


def qr_display(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    return redirect('home')  # Redirect to home instead


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Payment


def admin_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Only admins can log in
            login(request, user)
            return redirect("admin_dashboard")
        else:
            return render(request, "admin_login.html", {"error": "Invalid credentials or not an admin"})

    return render(request, "admin_login.html")


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # Import Q for filtering
from .models import UserProfile  # Ensure correct model is used

from django.shortcuts import render, redirect
from django.db.models import Q
from User.models import UserProfile, Payment


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect("admin_login")

    users = UserProfile.objects.all()

    search_query = request.GET.get("search", "")
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(vehicle_number__icontains=search_query)
        )

    # Attach transactions for each user
    for user in users:
        user.transactions = Payment.objects.filter(user=user).order_by('-created_at')

    return render(request, "admin_dashboard.html", {"users": users})


@login_required
def admin_logout(request):
    logout(request)
    return redirect("admin_login")


from django.shortcuts import get_object_or_404


@login_required
def delete_user(request, user_id):
    if not request.user.is_staff:
        return redirect("admin_login")

    user = get_object_or_404(UserProfile, id=user_id)
    user.delete()
    return redirect("admin_dashboard")


from django.contrib.auth.decorators import login_required


@login_required
def update_profile(request):
    try:
        user_profile = UserProfile.objects.get(id=request.user.id)
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect("profile", user_id=request.user.id)

    if request.method == "POST":
        user_profile.first_name = request.POST["first_name"]
        user_profile.last_name = request.POST["last_name"]
        user_profile.mobile = request.POST["mobile"]
        user_profile.email = request.POST["email"]
        user_profile.vehicle_name = request.POST["vehicle_name"]
        user_profile.vehicle_number = request.POST["vehicle_number"]
        user_profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect("profile", user_id=request.user.id)

    return render(request, "update_profile.html", {"user": user_profile})


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile  # Import your UserProfile model


@login_required
def stop_service(request):
    if request.method == "POST":
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.is_active = False  # Mark user as inactive (you can add this field in your model)
        user_profile.save()

        messages.success(request, "Your service has been stopped successfully.")
        return redirect("home")  # Redirect to home page or login page

    return redirect("profile", user_id=request.user.id)


from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile  # Import your User model


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.vehicle_number = request.POST['vehicle_number']
        user.status = request.POST['status']
        user.save()
        return redirect('admin_dashboard')  # Redirect to admin panel after update

    return render(request, 'edit_user.html', {'user': user})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from .models import UserProfile

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from User.models import UserProfile


@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        user_id = request.session.get('user_id')  # Get logged-in user ID from session
        if not user_id:
            return redirect('login')  # Redirect if user not logged in

        try:
            user_profile = UserProfile.objects.get(id=user_id)  # Fetch user profile

            # Save new profile picture
            user_profile.profile_picture = request.FILES['profile_picture']
            user_profile.save()

            return redirect('profile', user_id=user_id)  # Redirect to profile page

        except UserProfile.DoesNotExist:
            return render(request, 'error.html', {'error': 'User profile not found'})

    return redirect('profile')  # Redirect if no file uploaded


@login_required
def remove_profile_image(request):
    if request.method == "POST":
        user_profile = request.user.userprofile
        # Delete current profile image
        if user_profile.profile_image:
            default_storage.delete(user_profile.profile_image.path)
            user_profile.profile_image = None
            user_profile.save()
    return redirect('profile', user_id=request.user.id)


from django.shortcuts import render, redirect
from .models import UserProfile

from django.shortcuts import render, redirect
from django.contrib.auth.models import User  # Import User model

from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile


from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile

from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile


from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile

from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile

def dashboard(request):
    if not request.session.get('user_id'):
        return redirect('login')

    user_id = request.session['user_id']

    # Try to fetch the UserProfile, if not exist return None
    user_profile = UserProfile.objects.filter(id=user_id).first()

    # If no UserProfile exists, the user has not registered for FasTag yet
    is_registered = user_profile is not None and user_profile.vehicle_number and user_profile.qr_code

    return render(request, 'dashboard.html', {
        'user': user_profile,  # Can be None if not registered
        'is_registered': is_registered,
    })


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile, Payment  # Import Payment model if needed

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile  # Removed Payment since it's not needed


def process_payment(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        amount = request.POST.get("amount")

        if not user_id or not amount:
            messages.error(request, "User ID or amount is missing.")
            return redirect("profile", user_id=request.user.id)

        try:
            user = UserProfile.objects.get(id=user_id)

            # Store the payment
            Payment.objects.create(user=user, amount=float(amount), status="Success")

            messages.success(request, f"₹{amount} added to your balance successfully!")
            return redirect("profile", user_id=user_id)

        except UserProfile.DoesNotExist:
            messages.error(request, "User profile not found.")
            return redirect("profile", user_id=request.user.id)

    return redirect("profile", user_id=request.user.id)


import qrcode
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import UserProfile


def generate_qr(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    # Get the current server IP (Change this to your actual server IP)
    server_ip = "http://192.168.247.40:8000"


    # QR Code Data
    qr_data = f"{server_ip}/profile/{user.id}"

    # Generate QR Code
    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    # Return QR Code as Image Response
    return HttpResponse(buffer.getvalue(), content_type="image/png")

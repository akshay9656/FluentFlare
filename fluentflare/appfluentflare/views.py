from decimal import Decimal
import os
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
import openai
from appfluentflare.models import Login
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import *
from django.http import JsonResponse
from django.conf import settings 
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import update_session_auth_hash
from django.utils.translation import gettext_lazy as _

Login = get_user_model()
openai.api_key = settings.OPENAI_API_KEY

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)

def is_admin(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_admin)
def myadminpage(request):


    admin_name = request.session.get('admin_name', 'Unknown Admin')
  
    totalregusers=UserRegister.objects.all().count()
    date_28_days_ago = timezone.now() - timedelta(days=28)
    recent_users = UserRegister.objects.filter(join_date__gte=date_28_days_ago)
    recent_users_count = recent_users.count()
    enrolled_users = UserRegister.objects.filter(enrolled=True).count()
    not_enrolled_users = UserRegister.objects.filter(enrolled=False).count()
    messages=Usermessage.objects.filter(replied=False).count()
    promoter_count = Login.objects.filter(userType='promoter',userregister__isnull=False).count()
    totaltask=DayTasks.objects.all().count()
    admins = Login.objects.filter(is_staff=True)
    promoters = Login.objects.filter(userType='promoter',userregister__isnull=False).select_related('userregister')

    notes = AdminMessage.objects.all().order_by('-timestamp')

    if request.method == 'POST':
        print('33333333333333333333333333333333333333')
        notebox = request.POST.get('notebox')
        heloo=request.user

        print(heloo)
        print(notebox)
        if notebox:
            AdminMessage.objects.create(user=request.user, content=notebox)
        return redirect('myadminpage')



    context={
        "totalregusers":totalregusers,
        'recent_users_count':recent_users_count,
        'enrolled_users':enrolled_users,
        'not_enrolled_users':not_enrolled_users, 
        'messages':messages,
        'promoter_count':promoter_count,
        'totaltask':totaltask,
        'admins':admins, 
        'promoters':promoters, 
        'admin_name':admin_name,
        'notes':notes,
    }
    return render(request,'myadminpage.html',context)

@user_passes_test(is_admin)
def toggle_admin_status(request, id):
    print('3333333333333333333555555555555')
    print(id)
    user = get_object_or_404(Login, id=id)
    
    if user.is_staff:

        user.is_staff = False
        user.is_superuser = False
        messages.success(request, f"{user.username} is now a normal user.")
    else:

        user.is_staff = True
        user.is_superuser = True
        messages.success(request, f"{user.username} is now an admin.")
    
 
    user.save()
    

    return redirect('allusers')

@user_passes_test(is_admin)
def toggle_promoter_status(request, user_id):
    if request.method == 'GET':
        user = get_object_or_404(Login, id=user_id)
        if user.userType == 'user':
            user.userType = 'promoter'
            messages.success(request, f"{user.username} has been promoted to Promoter.")
        else:
            user.userType = 'user'
            messages.success(request, f"{user.username} has been demoted to Regular User.")
        user.save()
    return redirect('allusers') 

@user_passes_test(is_admin)
def addtask(request): 
    if request.method == 'POST':
  
        title = request.POST.get('title')
        Quotefortask = request.POST.get('Quotefortask')
        imagefortask = request.FILES.get('imagefortask')
        topic = request.POST.get('topic')
        timeduration = request.POST.get('timeduration')
        headingforexercise = request.POST.get('headingforexercise')
        exercise1 = request.POST.get('exercise1')
        exercise1ans = request.POST.get('exercise1ans')
        exercise2 = request.POST.get('exercise2')
        exercise2ans = request.POST.get('exercise2ans')
        exercise3 = request.POST.get('exercise3')
        exercise3ans = request.POST.get('exercise3ans')

     
        new_task = DayTasks.objects.create(
            title=title,
            Quotefortask=Quotefortask,
            imagefortask=imagefortask,
            topic=topic,
            timeduration=timeduration,
            headingforexercise=headingforexercise,
            exercise1=exercise1,
            exercise1ans=exercise1ans,
            exercise2=exercise2,
            exercise2ans=exercise2ans,
            exercise3=exercise3,
            exercise3ans=exercise3ans
        )
        new_task.save()

    
    task=DayTasks.objects.all().order_by('id')
    context={
        'task':task,
    }
    return render(request,'addtask.html',context)

@user_passes_test(is_admin)
def delete_task(request, task_id):

    try:
        task = get_object_or_404(DayTasks, id=task_id)
        task.delete()
        messages.success(request, "Task successfully deleted.")
    except DayTasks.DoesNotExist:
        messages.error(request, "Task does not exist.")
        return redirect('addtask')
    return redirect('addtask')

@user_passes_test(is_admin)
def changepayment(request):

    if request.method == 'POST':
  
        Payment = request.POST.get('Payment')
        QRCode = request.FILES['QRcode']
        offerQRCode = request.FILES['offerQRcode']
        existing_qr_code1 = PaymentPrice.objects.filter(payment_QRCODE__isnull=False)
        existing_qr_code2 = PaymentPrice.objects.filter(offer_payment_QRCODE__isnull=False)

        for qr in existing_qr_code1:
            if qr.payment_QRCODE:
                qr.payment_QRCODE.delete(save=False)

        for qr in existing_qr_code2:
            if qr.offer_payment_QRCODE:
                qr.offer_payment_QRCODE.delete(save=False)




        obj = PaymentPrice.objects.create(amount=Payment, payment_QRCODE=QRCode, offer_payment_QRCODE=offerQRCode)
        obj.save()
        
    return render(request,'changepayment.html')

@user_passes_test(is_admin)
def changegrouplink(request):

    if request.method == 'POST':
  
        link = request.POST.get('Group')

        obj=groupLink.objects.create(link=link)
        obj.save()
        
    return render(request,'changegrouplink.html')

@user_passes_test(is_admin)
def allusers(request):

    fullname = request.GET.get('fullname', '')
    email = request.GET.get('email', '')
    username = request.GET.get('username', '')
    redeem_code = request.GET.get('redeem_code', '')

    AllUsers = UserRegister.objects.all()

    if fullname:
        AllUsers = AllUsers.filter(user_fullname__icontains=fullname)
    
    if email:
        AllUsers = AllUsers.filter(user_email__icontains=email)
    
    if username:
        AllUsers = AllUsers.filter(user_username__icontains=username)
    
    if redeem_code:
        AllUsers = AllUsers.filter(redeem_code__icontains=redeem_code)

    AllUsers = AllUsers.order_by('-join_date')

    context = {
        'AllUsers': AllUsers,
    }
    
    return render(request, 'allusers.html', context)

@user_passes_test(is_admin)
def delete_user(request, user_id):
    
    try:
        user_register = get_object_or_404(UserRegister, user__id=user_id)
        login_user = user_register.user
        user_register.delete()
        if login_user:
            login_user.delete()
        messages.success(request, "User successfully deleted.")
    except UserRegister.DoesNotExist:
        messages.error(request, "User does not exist.")
        
    
    return redirect('allusers')

@user_passes_test(is_admin)
def lastmonthusers(request):
    date_28_days_ago = timezone.now() - timedelta(days=28)
    recent_users = UserRegister.objects.filter(join_date__gte=date_28_days_ago).order_by('-join_date')

    return render(request,'lastmonthusers.html',{'recent_users':recent_users})

@user_passes_test(is_admin)
def enrolledusers(request):
    username_search = request.POST.get('username_search', '')
    redeem_code_search = request.POST.get('redeem_code_search', '')
    
    # Filter enrolled users based on search criteria
    enrolled_users = UserRegister.objects.filter(enrolled=True).order_by('-join_date')

    if username_search:
        enrolled_users = enrolled_users.filter(user_username__icontains=username_search)
    if redeem_code_search:
        enrolled_users = enrolled_users.filter(redeem_code__icontains=redeem_code_search)

    # Handle unenroll users
    if request.method == "POST" and 'unenroll_submit' in request.POST:
        # Get the list of unchecked users to unenroll
        unenroll_user_ids = request.POST.getlist('unenroll_user')
        
        # Unenroll users who are not checked
        all_users = enrolled_users.values_list('id', flat=True)
        users_to_unenroll = set(all_users) - set(map(int, unenroll_user_ids))
        
        # Unenroll those users
        UserRegister.objects.filter(id__in=users_to_unenroll).update(enrolled=False)

        return redirect('enrolledusers')  # Redirect to the same page to see updated list

    context = {
        'enrolled_users': enrolled_users,
        'username_search': username_search,
        'redeem_code_search': redeem_code_search,
    }
    return render(request, 'enrolledusers.html', context) 

@user_passes_test(is_admin)
def notenrolledusers(request):

    username_query = request.GET.get('username', '')
    redeem_code_query = request.GET.get('redeem_code', '')

    # Filter users based on the search queries
    not_enrolled_users = UserRegister.objects.filter(enrolled=False).order_by('-join_date')

    if username_query:
        not_enrolled_users = not_enrolled_users.filter(user_username__icontains=username_query)
    if redeem_code_query:
        not_enrolled_users = not_enrolled_users.filter(redeem_code__icontains=redeem_code_query)

    # Handle the enrollment of users
    if request.method == 'POST':
        enroll_user_ids = request.POST.getlist('enroll_user')
        UserRegister.objects.filter(id__in=enroll_user_ids).update(enrolled=True)

        # Optionally, you can redirect to the same view or another after enrolling users
        return redirect('notenrolledusers')  # Change to your view name

    context = {
        'not_enrolled_users': not_enrolled_users,
    }
    return render(request, 'notenrolledusers.html', context)

@user_passes_test(is_admin)
def newmessages(request):

    newmessage = Usermessage.objects.filter(replied=False).order_by('message_recieved')

    return render(request,'newmessages.html',{'newmessage':newmessage})

@user_passes_test(is_admin)
def changemessagestatus(request,id):

    message = get_object_or_404(Usermessage, id=id)
    message.replied = True
    message.save()

    return redirect('newmessages')

@user_passes_test(is_admin)  
def showpromoters(request):

    username_search = request.POST.get('username_search', '')
    email_search = request.POST.get('email_search', '')
    promoters = Login.objects.filter(userType='promoter').select_related('userregister').order_by('-id')
    
    if username_search:
        promoters = promoters.filter(userregister__user_username__icontains=username_search)

    if email_search:
        promoters = promoters.filter(userregister__user_email__icontains=email_search)


    
    

    if request.method == "POST" and 'update_per_user' in request.POST:
        user_id = request.POST.get('user_id')
        user_register = get_object_or_404(UserRegister, id=user_id)
        new_amount_per_user = request.POST.get('howmuchperuser')
        if new_amount_per_user:
            user_register.howmuchperuser = new_amount_per_user
            user_register.save()

            return redirect('showpromoters')

    if request.method == "POST" and 'update_amount_paid' in request.POST:
        user_id = request.POST.get('user_id')
        user_register = get_object_or_404(UserRegister, id=user_id)
        new_total_amount = request.POST.get('amountpaid')
        if new_total_amount:
            try:
                # Add the new amount to the current amountpaid value
                new_total_amount = Decimal(new_total_amount)  # Convert to Decimal
                user_register.amountpaid += new_total_amount  # Add to the existing amountpaid
                user_register.save()

                
                promoter_id = user_register.id
                print('4555555555555555555555555576')
                print(promoter_id)
                promoter_payment = Promoterpayment.objects.filter(user=promoter_id,requested=True)
                if promoter_payment.exists():
                    print(promoter_payment)
                    promoter_payment.update(requested=False)


            except InvalidOperation:
                print('666666666666666666666666666666666')
                pass

            return redirect('showpromoters')


    promoter_data = []

    for promoter in promoters:
        try:
            
            promoter_username = promoter.userregister.user_username

            users_with_redeem_code = UserRegister.objects.filter(redeem_code=promoter_username)
            total_users = users_with_redeem_code.count()
            enrolled_users = users_with_redeem_code.filter(enrolled=True).count()

            promoter_id = promoter.userregister.id
            promoter_payment = Promoterpayment.objects.filter(user=promoter_id).order_by('-id').first()

            promoter_data.append({
                'promoter': promoter,
                'total_users': total_users,
                'enrolled_users': enrolled_users,
                'promoter_payment': promoter_payment,
            })
        except ObjectDoesNotExist:
            
            continue

    
    return render(request,'showpromoters.html',{'promoter_data':promoter_data})

def promoter_dashboard(request, promoter_username):

    promoter = UserRegister.objects.filter(user_username=promoter_username).first()
    users_with_redeem_code = UserRegister.objects.filter(redeem_code=promoter_username)
    total_users = users_with_redeem_code.count()
    enrolled_users = users_with_redeem_code.filter(enrolled=True).count()

    current_amount= enrolled_users * promoter.howmuchperuser - promoter.amountpaid
    total_amount = (enrolled_users * promoter.howmuchperuser)

    if request.method == "POST" and 'change_profile_pic' in request.POST:
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
                
            if promoter.profile_pic:
                existing_pic_path = os.path.join(settings.MEDIA_ROOT, str(promoter.profile_pic))
                if os.path.exists(existing_pic_path):
                    os.remove(existing_pic_path)  
            # Save the new profile picture
            promoter.profile_pic = profile_pic
            promoter.save()
            messages.success(request, "Profile picture updated successfully!")
            return redirect('promoter_dashboard', promoter_username=promoter_username)
        else:
            messages.error(request, "Please upload a valid image.")
            return redirect('promoter_dashboard', promoter_username=promoter_username)
    
        
    if request.method == "POST" and 'requestpayment' in request.POST:
        print('55555555555555555555555555555555')
        promoter_id = promoter.id
        promoterID = UserRegister.objects.get(id=promoter_id)
        request_amount = request.POST.get('reqamount')
        print(request_amount)

        obj = Promoterpayment.objects.create(user=promoterID,requested=True,amount=request_amount)
        obj.save()
        print(request_amount)
        messages.success(request, 'Payment Request send Successfully, Payment will be Processed within 24hr')
        return redirect('promoter_dashboard', promoter_username=promoter_username)
   
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        # Check if old password is correct
        if not request.user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('promoter_dashboard', promoter_username=promoter_username)
        # Check if new passwords match
        elif new_password1 != new_password2:
            messages.error(request, 'New passwords do not match.')
            return redirect('promoter_dashboard', promoter_username=promoter_username)
        else:
            # Set the new password
            request.user.set_password(new_password1)
            request.user.save()
            # Keep the user logged in after changing the password
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('promoter_dashboard', promoter_username=promoter_username)


    context = {

        'promoter': promoter,
        'current_amount': current_amount,
        'total_users': total_users,
        'total_amount': total_amount,
        'enrolled_users': enrolled_users,
        'promoter_username': promoter_username,

    }

    return render(request, 'promoter_dashboard.html', context)

def index(request):
    user1=""
    if "userID" in request.session:
        u_id=request.session["userID"]
        user1=UserRegister.objects.get(user=u_id)
        
    reviews=Review.objects.filter(rating__gt=3)

    context={
        'userhomebutton':user1,
        'reviews':reviews,
    }

    return render(request, 'index.html',context)

def contactUs(request):
    user1=""
    if "userID" in request.session:
        u_id=request.session["userID"]
        user1=UserRegister.objects.get(user=u_id)
        
    
    if request.POST and 'sendmessage' in request.POST:
        name = request.POST["name"]
        email = request.POST["email"]
        message = request.POST["message"]

        if name and email and message:
            try:
                obj = Usermessage.objects.create(name=name, email=email, message=message)
                obj.save()
                messages.success(request, 'message Recieved successfully!, We will get back to you within 24 hours')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        else:
            messages.error(request, 'All fields are required.')
        
    context={
        'userhomebutton':user1,
    }
    return render(request, 'contactUs.html',context)

def user_dashboard(request):

    if 'userID' not in request.session:
        return redirect('login')
    u_id = request.session["userID"]
    user1 = UserRegister.objects.get(user__id=u_id)

    show_congrats_modal = request.session.pop('show_congrats_modal', False)

    try:
        if request.method == 'POST':
            if 'detail-submit' in request.POST:
                user_fullname1 = request.POST.get('user_username', user1.user_fullname)
                user_email1 = request.POST.get('user_email', user1.user_email)

                user_profile = UserRegister.objects.get(user__id=u_id)

                user_profile.user_fullname = user_fullname1
                user_profile.user_email = user_email1
                user_profile.save()
                return redirect('user_dashboard')
            
            if 'changepassworduser' in request.POST:
                print('44444444444444444444444444444444')
                old_password = request.POST.get('old_password')
                new_password = request.POST.get('new_password1')
                confirm_password = request.POST.get('new_password2')
                print(old_password)
                print(new_password)
                if not request.user.check_password(old_password):
                    messages.error(request, 'Old password is incorrect.')
                    return redirect('user_dashboard')

                if new_password != confirm_password:
                    messages.error(request, 'New passwords do not match.')
                    return redirect('user_dashboard')

                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully.')
                return redirect('user_dashboard')

            
    except:
        return redirect('user_dashboard')


    try:
        progress_number = ProgressBar.objects.get(user=user1)
    except ProgressBar.DoesNotExist:
        progress_number = 0

    try:

        if request.method == 'POST' and request.FILES['profile_pic']:
            user_profile = UserRegister.objects.get(user__id=u_id)
            if user_profile.profile_pic:
            
                existing_pic_path = os.path.join(settings.MEDIA_ROOT, str(user_profile.profile_pic))
                if os.path.exists(existing_pic_path):
                    os.remove(existing_pic_path)

            user_profile.profile_pic = request.FILES['profile_pic']
            user_profile.save()
            return redirect('user_dashboard')
    except:
        return redirect('user_dashboard')
    
    

    context={
        'progress_number':progress_number,
        'user1':user1,
        'show_congrats_modal': show_congrats_modal,
    }
    return render(request, 'user_dashboard.html',context)

def register(request):
    if request.method == 'POST':
        fullname = request.POST.get("name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        language = request.POST.get("language") 
        password = request.POST.get("password")
        confirm_password = request.POST.get("retypePassword")
        redeem_code = request.POST.get("redeem_code", None)

        errors = []

    
        if len(username) < 6:
            errors.append("Username must be at least 6 characters long.")
        
        if password != confirm_password:
            errors.append("Passwords do not match.")
        
        
        if UserRegister.objects.filter(user_email=email).exists():
            errors.append("An account with this email already exists. Please use a different email.")
        
        
        if language == "" or language == "Select Your Language":
            errors.append("Please select a language.")

        if redeem_code:
            try:
                promoter_user = Login.objects.get(username=redeem_code, userType='promoter')
            except Login.DoesNotExist:
                errors.append("Redeem code Expired. use a different one or register without it.")
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('register')

        
        try:
            login = Login.objects.create_user(username=username, password=password, userType='user', viewpassword=password)
            login.save()
            obj = UserRegister.objects.create(user=login,
                                              user_fullname=fullname,
                                              user_email=email,
                                              user_username=username,
                                              user_language=language,
                                              redeem_code=redeem_code,
                                              user_password=password)
            obj.save()
            return redirect('login')
        
        except IntegrityError:
            messages.error(request, 'Username is already taken. Please choose a different one.')
            return render(request, 'register.html')

    return render(request, 'register.html')

@csrf_protect
def login_view(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        remember_me = request.POST.get('remember-me', False)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  
            request.session["userID"] = user.id
            
            if not remember_me:
                request.session.set_expiry(0)

       
            if user.is_superuser:
                request.session['admin_name'] = user.get_full_name() if user.get_full_name() else user.username
                return redirect('myadminpage')
            
        
            if user.userType == 'promoter':
                return redirect('promoter_dashboard', promoter_username=user.username)
            
           
            try:
                user_register = UserRegister.objects.get(user=user)

              
                if user_register.enrolled:
                    messages.success(request, "Logged In Successfully!")
                    return redirect('UserHome')  
                else:
                    messages.success(request, "Your Account Was Activated Successfully! Enroll Your Course Now")
                    return redirect('paymentDecisionPage')  

            except UserRegister.DoesNotExist:
               
                messages.error(request, "User registration details not found. Please register first.")
                return redirect('register')  
            
        else:
          
            messages.error(request, "Invalid username or wrong password")
            return redirect('login')  
    
    return render(request, 'login.html')

def signOut(request):
    logout(request)

    return redirect('index')

def paymentDecisionPage(request):

    u_id = request.session.get("userID")
    user = UserRegister.objects.get(user__id=u_id)
    redeemcode = user.redeem_code
    obj = PaymentPrice.objects.latest('id')
    price = int(obj.amount / 100)
    
    discounted_price = None

    if redeemcode:

        # Apply 20% discount
        discounted_price = int(price * 0.80)


    context = {
        'price': price,
        'discounted_price': discounted_price,
    }
    return render(request, 'paymentDecisionPage.html', context)

def paymentpage(request):

    u_id = request.session.get("userID")
    user = UserRegister.objects.get(user__id=u_id)

    redeemcode = user.redeem_code
    obj = PaymentPrice.objects.latest('id')
    price = int(obj.amount / 100)  

 
    discounted_price = None

    if redeemcode:
     
        discounted_price = int(price * 0.80)

    context = {
        'obj': obj,
        'price': price,
        'discounted_price': discounted_price, 
    }
    return render(request, 'paymentpage.html', context)
  
def UserHome(request):
    
    user=""
    if "userID" in request.session:
        u_id=request.session["userID"]
        user=UserRegister.objects.get(user__id=u_id)
    
        try:
            courseredirect = Courseredirect.objects.get(user=user)
        except Courseredirect.DoesNotExist:
            courseredirect = False
    else:
        return redirect('index')

    context = {
        'courseredirect': courseredirect,
    }        
    return render(request,'UserHome.html',context)

def GrammerPage(request):

    

    try:
        u_id=request.session["userID"]
        user_profile=UserRegister.objects.get(user__id=u_id)
        user_language = user_profile.user_language

    except UserRegister.DoesNotExist:
        user_language = None 
 
    return render(request,'GrammerPage.html',{'language': user_language})

def privacypolicy(request):

    return render(request,'privacypolicy.html')

def termsofservice(request):

    return render(request,'termsofservice.html')

def sample(request):
    return render(request,'sample.html')

def review_audio_with_chatgpt(file_path):
    with default_storage.open(file_path, 'rb') as audio:
        try:
            transcript = openai.Audio.transcribe('whisper-1', audio)
            review_text = generate_review(transcript['text'])
            return review_text
        except openai.error.InvalidRequestError as e:
            raise e
  
def generate_review(transcript):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful language expert."},
        {"role": "user", "content": f"Please briefly evaluate the following speech transcript: '{transcript}'. Identify specific mistakes in grammar and pronunciation, and explain why they are incorrect. Provide short suggestions for improvement to help the speaker enhance their English speaking skills."}
    ],
        max_tokens=500
    )
    return response.choices[0].message['content']

def review_audio_with_chatgpt_topic(file_path):
    with default_storage.open(file_path, 'rb') as audio:
        try:
            transcript = openai.Audio.transcribe('whisper-1', audio)
            review_text = generate_review_topic(transcript['text'])
            return review_text
        except openai.error.InvalidRequestError as e:
            raise e

def generate_review_topic(transcript):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful language expert."},
        {"role": "user", "content": f"Please briefly evaluate the following speech transcript: '{transcript}'. Identify specific mistakes in grammar and pronunciation, and explain why they are incorrect. Provide short suggestions for improvement to help the speaker enhance their English speaking skills."}
    ],
        max_tokens=500
    )
    return response.choices[0].message['content']

def get_word_meaning(word):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"What's the meaning of '{word}', within less words"}
        ],
        max_tokens=30
    )
    return response.choices[0].message['content']

@login_required
def taskpage(request,id):
            
    meaning = ""
    word = ""
    review = ""
    reviewtopic= ""
    whatsapp_link=""

    answeris= None
    answeris2= None
    answeris3= None

    correctanswer1=""
    correctanswer2=""
    correctanswer3=""
    
    usersecondanswer=""
    userfirstanswer=""
    userthirdanswer=""
    u_id = request.session["userID"]
    user = UserRegister.objects.get(user__id=u_id)
    taskdetails=DayTasks.objects.get(id=id)

    if request.POST and 'wordmeaning' in request.POST:
        word = request.POST["word"]
        print(word)
        if word:
            meaning = get_word_meaning(word)

    try:
        if id in [1, 10, 20, 30, 40]:
            if request.POST and 'audioFilebut' in request.POST:

                
                if request.FILES.get('audioFile'):
                    delete_all_files_from_folder('uploads/')
                    audio_file = request.FILES['audioFile']
                    print(audio_file)
                    
                    file_path = default_storage.save('uploads/' + audio_file.name, ContentFile(audio_file.read()))

                    
                    review = review_audio_with_chatgpt(file_path)

                    

    
            if request.POST and 'audioFilebutTopic' in request.POST:

                if request.FILES.get('audioFile'):
                    delete_all_files_from_folder('uploadsTopic/')
                    
                    audio_file = request.FILES['audioFile']
                    print(audio_file)
                    
                    file_path = default_storage.save('uploadsTopic/' + audio_file.name, ContentFile(audio_file.read()))

                    
                    reviewtopic = review_audio_with_chatgpt_topic(file_path)                    

    except Exception as e:
        print(f"Error: {e}")
        pass

    if request.method == "POST" and 'submituserfirstans' in request.POST:
        
        userfirstanswer = request.POST.get("userfirstanswer")
        
        correctanswer1=taskdetails.exercise1ans
        

        if userfirstanswer:
            if (taskdetails.exercise1ans.strip().lower() == userfirstanswer.strip().lower()):
                answeris=True
            else:
                answeris=False
                                    
    if request.method == "POST" and 'submitusersecondans' in request.POST:
        
        usersecondanswer = request.POST.get("usersecondanswer")
        
        
        correctanswer2=taskdetails.exercise2ans

        if usersecondanswer:
            if (taskdetails.exercise2ans.strip().lower() == usersecondanswer.strip().lower()):
                answeris2=True
            else:
                answeris2=False

    if request.method == "POST" and 'submituserthirdans' in request.POST:
        
        userthirdanswer = request.POST.get("userthirdanswer")
        
        
        correctanswer3=taskdetails.exercise3ans

        if userthirdanswer:
            if (taskdetails.exercise3ans.strip().lower() == userthirdanswer.strip().lower()):
                answeris3=True
            else:
                answeris3=False

    if id == 20:
        u_id = request.session["userID"]
        user = UserRegister.objects.get(user__id=u_id)
        if user.whatsapp == False:
            user.whatsapp = True
            user.save()
            try:
                whatsapp_group = groupLink.objects.latest('id')
                whatsapp_link = whatsapp_group.link
            except groupLink.DoesNotExist:
                whatsapp_link = None          

    if user.whatsapp==True:
        
        try:
            whatsapp_group = groupLink.objects.latest('id')
            whatsapp_link = whatsapp_group.link
        except groupLink.DoesNotExist:
            whatsapp_link = None 

    page = request.GET.get('page')


    context={
        'word': word,
        'page':page,
        'meaning': meaning,
        'result': review,
        'taskdetails':taskdetails,
        'reviewtopic':reviewtopic,
        'answeris':answeris,
        'answeris2':answeris2,
        'answeris3':answeris3,
        'correctanswer1':correctanswer1,
        'userfirstanswer':userfirstanswer,
        'usersecondanswer':usersecondanswer,
        'userthirdanswer':userthirdanswer,
        "correctanswer2":correctanswer2,
        "correctanswer3":correctanswer3,
        'whatsapp_link': whatsapp_link,
    }
    
    return render(request, 'taskpage.html', context)

def delete_all_files_from_folder(folder_path):

    if default_storage.exists(folder_path):
       
        files = default_storage.listdir(folder_path)[1] 
        for file_name in files:
            
            file_path = os.path.join(folder_path, file_name)
          
            default_storage.delete(file_path)

@login_required
def FirstTask(request):
    u_id = request.session["userID"]
    user = UserRegister.objects.get(user__id=u_id)
    
    try:
        changeclick, created = Courseredirect.objects.get_or_create(user=user)
        changeclick.clicked = True
        changeclick.save()
    except ObjectDoesNotExist:
        
        pass

    tasks = DayTasks.objects.all().order_by('id')
    user_tasks_status = UserTaskStatus.objects.filter(user=user)

    
    unlocked_tasks = []
    if user_tasks_status.exists():
        for status in user_tasks_status:
            if status.completed:
                unlocked_tasks.append(status.task.id)
            else:
                break
        # Also unlock the next task if the last completed task is in unlocked_tasks
        last_completed_task_id = unlocked_tasks[-1] if unlocked_tasks else None
        if last_completed_task_id:
            next_task = DayTasks.objects.filter(id__gt=last_completed_task_id).first()
            if next_task:
                unlocked_tasks.append(next_task.id)
    else:
        unlocked_tasks.append(tasks[0].id)

    # Loop through tasks to set unlocked status
    for i, task in enumerate(tasks):
        if task.id in unlocked_tasks:
            task.unlocked = True
        else:
            task.unlocked = False

    page = request.GET.get('page', 1)
    task_paginator = Paginator(tasks, 6)
    tasks = task_paginator.get_page(page)
    
    context = {
        'tasks': tasks,
        'page': page,
    }
    return render(request, 'FirstTask.html', context)

@login_required
def complete_task(request, task_id):
    
    u_id = request.session["userID"]
    user1 = UserRegister.objects.get(user__id=u_id)
    if task_id >= 40:
        request.session['show_congrats_modal'] = True  # Set session variable to show the modal
        return redirect('user_dashboard')
    
    task = get_object_or_404(DayTasks, id=task_id)
    user_task_status, created = UserTaskStatus.objects.get_or_create(user=user1, task=task)
    user_task_status.completed = True
    user_task_status.save()

    tasks = DayTasks.objects.all()
    total_tasks = tasks.count()
    
    completed_tasks = UserTaskStatus.objects.filter(user=user1,completed=True).count()
    
    progress_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    try:
        progress_bar = ProgressBar.objects.get(user=user1)
        progress_bar.percentage = progress_percentage
        progress_bar.save()
    except:
        progress_bar = ProgressBar.objects.create(user=user1, percentage=progress_percentage)
        progress_bar.save()
    
    page = request.GET.get('page')

    if page is None or page == 'None':
        current_page = 1  
    else:
    
        try:
            current_page = int(page)
        except ValueError:
            current_page = 1 

    if task_id in (6, 12, 18, 24, 30, 36):
        current_page += 1 

    redirect_url = f"{reverse('FirstTask')}?page={current_page}"
    return redirect(redirect_url)
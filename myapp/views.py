import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.core.files.storage.filesystem import FileSystemStorage
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

from myapp.chkng1 import generate_html
from myapp.chkng2 import generate_image
from vision2code import settings
from .models import *
from .newcode import image_based_gen
from datetime import datetime
from .chkng3 import generate_code_from_image
# Create your views here.
def loginn(request):
    logout(request)
    if request.method == "POST":
       username = request.POST['username']
       password=request.POST['password']
       user=authenticate(username=username,password=password)
       if user is not None:
           if user.groups.filter(name='admin').exists():
               login(request,user)
               return redirect('/myapp/admin_home')
           if user.groups.filter(name='user').exists():
               login(request,user)
               return redirect('/myapp/user_home')




    return render(request,'login.html')



def logout_get(request):
    logout(request)
    return redirect('/myapp/login')
    # return render(request, 'login.html')

def forgot_get(request):
    return render(request,'forgot.html')

def forgotPassword_otp(request):
    email=request.POST['email']
    try:
        user=User.objects.get(email=email)
    except User.DoesNotExist:
        messages.warning(request,'Email doesnt match')
        return redirect('/myapp/login')
    otp=random.randint(100000,999999)
    request.session['otp']=str(otp)
    request.session['email'] = email

    send_mail('Your Verification Code',
    f'Your verification code is {otp}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False)
    messages.success(request,'OTP sent To your Mail')
    return redirect('/myapp/verifyOtp')

def verifyOtp(request):
    return render(request,'otpverification.html')

def verifyOtpPost(request):
    entered_otp=request.POST['entered_otp']
    if request.session.get('otp') == entered_otp:
        messages.success(request,'otp verified')
        return redirect('/myapp/new_password')
    else:
        messages.warning(request,'Invalid OTP!!')
        return redirect('/myapp/login')

def new_password(request):
    return render(request,'new_password.html')

def changePassword(request):
    newpassword=request.POST['newPassword']
    confirmPassword=request.POST['confirmPassword']
    if newpassword == confirmPassword:
        email=request.session.get('email')
        user = User.objects.get(email=email)
        user.set_password(confirmPassword)
        user.save()
        messages.success(request, 'Password Updated Successfully')
        return redirect('/myapp/login')
    else:
        messages.warning(request, 'The password doesnt match!!')
        return redirect('/myapp/new_password')
# def forgot_password(request):
#     if request.method == "POST":
#         email = request.POST.get('email').strip()
#         print("Entered:", email)
#
#         users = User.objects.all()
#         print("All emails in DB:")
#         for u in users:
#             print(u.email)
#
#         user = User.objects.filter(email__iexact=email).first()
#
#         if user:
#             print("MATCH FOUND")
#             return redirect('/myapp/reset_password/{user.id}')
#         else:
#             print("NO MATCH")
#             messages.error(request, "Email not found")
#         return redirect('/myapp/reset_password/{user.id}')
#     return render(request,'forgot_password.html')
# def reset_password(request, id):
#     if request.method == "POST":
#         password = request.POST.get('password')
#
#         user = User.objects.get(id=id)
#         user.password = password   # (use hashing if needed)
#         user.save()
#
#         messages.success(request, "Password updated successfully")
#
#         return redirect('/myapp/login')
#
#     return render(request, 'reset_password.html')

def user_signup(request):
    return render(request,'user/signup.html')


def user_signup_post(request):
    name=request.POST['name']
    designation=request.POST['des']
    email=request.POST['email']
    phone=request.POST['phn']
    username=request.POST['user']
    password=request.POST['password']


    user=User()
    user.username=username
    user.password=make_password(password)
    user.first_name=name
    user.email=email
    user.save()

    user.groups.add(Group.objects.get(name="user"))

    ob=user_table()
    ob.LOGIN=user
    ob.name=name
    ob.designation=designation
    ob.email=email
    ob.phone=phone
    ob.save()

    return redirect("/myapp/login")





from django.db.models import Avg, Count
@login_required(login_url='/myapp/login')
def admin_home(request):
    ob=complaint_table.objects.filter(reply="pending")
    request.session['cc']=str(len(ob))
    user_id = request.user.id
    feedback_stats = feedback_table.objects.aggregate(
        avg_rating=Avg('rating'),
        total_feedbacks=Count('id')
    )

    context = {
        'avg': round(feedback_stats['avg_rating'] or 0, 1),
        'tf': feedback_stats['total_feedbacks']
   ,
        'user': user_table.objects.all().count(),
        'c': complaint_table.objects.all().count(),
    }

    return render(request,'admin/admin_home.html',context)

@login_required(login_url='/myapp/login')
def admin_change_p(request):
    return render(request,'admin/changepassword.html')

@login_required(login_url='/myapp/login')
def admin_change_p_post(request):
    if not request.user.is_authenticated:
        messages.error(request,"you must be logged in to change your password.")
        return redirect('/myapp/admin_change_p')

    current_password=request.POST['current_password']
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']
    if check_password(current_password,request.user.password):
        if new_password==confirm_password:
            user=request.user
            user.set_password(confirm_password)
            user.save()
            messages.success(request,"Password Changed Successfully")
            return redirect('/myapp/admin_change_p')
        else:
            messages.error(request,"New Password And Confirm Password Do Not Match ")
            return redirect('/myapp/admin_change_p')
    else:
        messages.error(request, "Current Password is Incorrect")
        return redirect('/myapp/admin_change_p')

@login_required(login_url='/myapp/login')
def admin_fb(request):
    ob=feedback_table.objects.all()
    return render(request,'admin/feedback.html',{"feedback":ob})

@login_required(login_url='/myapp/login')
def admin_reply(request,id):
    request.session['cid']=id
    return render(request,'admin/reply.html')

@login_required(login_url='/myapp/login')
def admin_reply_post(request):
    message=request.POST['message']
    ob=complaint_table.objects.get(id=request.session['cid'])
    ob.reply=message
    ob.save()
    return redirect("/myapp/admin_view_com")

@login_required(login_url='/myapp/login')
def admin_tips(request):
    ob=tips_table.objects.all()
    return render(request,'admin/tips.html',{"tips":ob})

@login_required(login_url='/myapp/login')
def admin_tips_post(request):
    tip=request.POST['tip']
    des=request.POST['des']
    ob=tips_table()
    ob.title=tip
    ob.tipdetails=des
    ob.date=datetime.today()
    ob.save()
    return redirect("/myapp/admin_tips")

@login_required(login_url='/myapp/login')
def delete_tip(request,id):
    tip = tips_table.objects.get(id=id)
    tip.delete()
    messages.success(request,"Tip deleted successfully")
    return redirect('/myapp/admin_tips')
    # return redirect('/myapp/user_home')

@login_required(login_url='/myapp/login')
def delete_user(request,id):
    tip = User.objects.get(id=id)
    tip.delete()
    messages.success(request,"User deleted successfully")
    return redirect('/myapp/admin_view_user')
    # return redirect('/myapp/user_home')

@login_required(login_url='/myapp/login')
def admin_view_com(request):
    ob=complaint_table.objects.all()
    return render(request,'admin/view complaint.html',{"complaint":ob})

@login_required(login_url='/myapp/login')
def admin_view_user(request):
    ob=user_table.objects.all()
    return render(request,'admin/viewuser.html',{"user":ob})


@login_required(login_url='/myapp/login')
def user_home(request):
    user_id = request.user.id

    context = {
        'data': complaint_table.objects.filter(USER__LOGIN_id=user_id).count(),
        'd': feedback_table.objects.filter(USER__LOGIN_id=user_id).count(),
        'b': image_table.objects.filter(USER__LOGIN_id=user_id).count(),
        'l': text_table.objects.filter(USER__LOGIN_id=user_id).count(),
        'date':datetime.now().today()
    }

    return render(request, 'user/userhome.html', context)


#
# @login_required(login_url='/myapp/login')
# def user_home(request):
#     ab = complaint_table.objects.count().filter(USER__LOGIN_id=request.user.id)
#     ba = feedback_table.objects.count().filter(USER__LOGIN_id=request.user.id)
#     c = image_table.objects.count().filter(USER__LOGIN_id=request.user.id)
#     b=text_table.objects.count().filter(USER__LOGIN_id=request.user.id)
#     return render(request,'user/userhome.html',{'data':ab,'d':ba,'b':c,'l':b})

@login_required(login_url='/myapp/login')
def user_change_p(request):
    return render(request,'user/changepassword.html')

@login_required(login_url='/myapp/login')
def user_change_p_post(request):
    if not request.user.is_authenticated:
        messages.error(request,"you must be logged in to change your password.")
        return redirect('/myapp/user_change_p')

    current_password=request.POST['current_password']
    new_password=request.POST['new_password']
    confirm_password=request.POST['confirm_password']
    if check_password(current_password,request.user.password):
        if new_password==confirm_password:
            user=request.user
            user.set_password(confirm_password)
            user.save()
            messages.success(request,"Password Changed Successfully")
            return redirect('/myapp/user_change_p')
        else:
            messages.error(request,"New Password And Confirm Password Do Not Match ")
            return redirect('/myapp/user_change_p')
    else:
        messages.error(request, "Current Password is Incorrect")
        return redirect('/myapp/user_change_p')

@login_required(login_url='/myapp/login')
def user_complaint(request):
    ob = complaint_table.objects.filter(USER__LOGIN__id=request.user.id)
    return render(request,'user/complaint.html',{"complaint":ob})

@login_required(login_url='/myapp/login')
def user_fb(request):
    return render(request,'user/feedback.html')

@login_required(login_url='/myapp/login')
def user_fb_post(request):
    feedback=request.POST['feedback']
    rating=request.POST['rating']


    ob=feedback_table()
    ob.feedback=feedback
    ob.USER=user_table.objects.get(LOGIN__id=request.user.id)
    ob.rating=rating
    ob.date=datetime.today()
    ob.save()
    messages.success(request, 'Feedback send Successfully')
    return redirect("/myapp/user_fb")

@login_required(login_url='/myapp/login')
def user_img_his(request):
    ob=image_table.objects.filter(USER__LOGIN__id=request.user.id).order_by("-id")
    return render(request,'user/imagehistory.html',{"image":ob})

def delete_his(request,id):
    tip = text_table.objects.get(id=id)
    tip.delete()
    messages.success(request,"History deleted successfully")
    return redirect('/myapp/user_img_to_code')

@login_required(login_url='/myapp/login')
def user_img_to_code(request):
    return render(request,'user/imagetocode.html')

# def  user_img_to_code_post(request):
#     img=request.FILES['imageInput']
#     fs=FileSystemStorage()
#     fn=fs.save(img.name,img)
#     print(fn)
#     res=generate_code_from_image(r"C:\Users\DELL\PycharmProjects\vision2code\media/"+fn,"")
#     fnn=datetime.now().strftime("%Y%m%d%H%M%S")+".html"
#     try:
#         # Write HTML content to file
#         with open(r"C:\Users\DELL\PycharmProjects\vision2code\media/"+fnn, "w", encoding="utf-8") as file:
#             file.write(res)
#         # print(f"✅ HTML file '{filename}' created successfully at: {os.path.abspath(filename)}")
#     except OSError as e:
#         print(f"❌ Error writing file: {e}")
#     ob=image_table()
#     ob.USER=user_table.objects.get(LOGIN__id=request.user.id)
#     ob.image_path=fn
#     ob.output_file=fnn
#     ob.date=datetime.today()
#     ob.save()
#     return redirect('/myapp/user_img_to_code')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from datetime import datetime

@login_required(login_url='/myapp/login')
def user_img_to_code_post(request):
    img = request.FILES['imageInput']
    specification=request.POST['specification']
    fs = FileSystemStorage()
    fn = fs.save(img.name, img)
    type=request.POST['type']
    des=image_based_gen(r"C:\Users\DELL\PycharmProjects\vision2code\media/" + fn)
    res = generate_code_from_image(
        r"C:\Users\DELL\PycharmProjects\vision2code\media/" + fn, des,type,specification
    )

    res = res.replace("```html", "").replace("```", "")

    fnn = datetime.now().strftime("%Y%m%d%H%M%S")
    res = res.replace("```html", "").replace("```", "")
    res = res.replace("```dart", "").replace("```", "")
    res = res.replace("```react", "").replace("```", "")

    fnn = datetime.now().strftime("%Y%m%d%H%M%S")
    if type == "html":
        fnn += ".html"
    if type == "react":
        fnn += ".js"
    if type == "flutter":
        fnn += ".dart"
    try:
        with open(
            r"C:\Users\DELL\PycharmProjects\vision2code\media/" + fnn,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(res)
    except OSError as e:
        print(f"Error writing file: {e}")

    # Save to DB
    ob = image_table()
    ob.USER = user_table.objects.get(LOGIN__id=request.user.id)
    ob.image_path = fn
    ob.output_file = fnn
    ob.date = datetime.today()
    ob.save()

    return render(request, 'user/view_image_code_result.html', {"data": res,"fn":fnn})

@login_required(login_url='/myapp/login')
def user_text_to_code(request):
    return render(request,'user/texttocode.html')

@login_required(login_url='/myapp/login')
def user_textcode_his(request):
    ob=text_table.objects.filter(USER__LOGIN__id=request.user.id).order_by("-id")
    return render(request,'user/textcodehistory.html',{"text":ob})

def delete_his(request,id):
    tip = text_table.objects.get(id=id)
    tip.delete()
    messages.success(request,"History deleted successfully")
    return redirect('/myapp/user_text_to_code')

@login_required(login_url='/myapp/login')
def user_img_his(request):
    ob=image_table.objects.filter(USER__LOGIN__id=request.user.id).order_by('-id')
    return render(request,'user/imagehistory.html',{"image":ob})

# @login_required(login_url='/myapp/login')
# def user_text_to_code_post(request):
#     des=request.POST['des']
#     type=request.POST['type']
#     data=generate_html(des,type)
#     data = data.replace("```html", "").replace("```", "").strip()
#     return render(request,'user/view_code_result.html',{"data":data})
#

# @login_required(login_url='/myapp/login')
# def user_text_to_code_post(request):
#     des = request.POST.get('des')
#     type_val = request.POST.get('type')
#
#     data = generate_html(des, type_val)
#
#     # Handle the error cases from our function
#     if data == "ERROR:LIMIT_REACHED":
#         messages.error(request, "Free limit reached. Please wait a minute before trying again.")
#         return render(request, 'user/view_code_result.html', {"data": "API limit reached. Try again later."})
#
#     if "ERROR" in data:
#         messages.error(request, "An unexpected error occurred with the AI model.")
#         return render(request, 'user/view_code_result.html', {"data": "Something went wrong."})
#
#     # Clean the data if successful
#     data = data.replace("```html", "").replace("```", "").strip()
#
#
#     obj=text_table()
#     obj.USER=user_table.objects.get(LOGIN=request.user.id)
#     obj.text_input=
#     obj.output_format=
#     obj.generated_code=
#     obj.date=datetime.now().today()
#     obj.save()
#
#     return render(request, 'user/view_code_result.html', {"data": data})


@login_required(login_url='/myapp/login')
def user_text_to_code_post(request):
    des = request.POST.get('des')
    type_val = request.POST.get('type')

    data = generate_html(des, type_val)
    if data == "ERROR:LIMIT_REACHED":
        messages.error(request, " Please wait a minute before trying again.")
        return render(request, 'user/view_code_result.html', {"data": "API limit reached. Try again later."})

    if "ERROR" in data:
        messages.error(request, "An unexpected error occurred with the AI model.")
        return render(request, 'user/view_code_result.html', {"data": "Something went wrong."})

    data = data.replace("```html", "").replace("```", "").strip()
    filename=datetime.now().strftime("%Y%m%d%H%M%S")
    if type_val== "html":
        filename+=".html"
    if type_val== "java":
        filename+=".java"
    if type_val== "flutter":
        filename+=".dart"
    if type_val== "react":
        filename+=".js"

    try:
        # Write HTML content to file
        with open(r"C:\Users\DELL\PycharmProjects\vision2code\media/"+filename, "w", encoding="utf-8") as file:
            file.write(data)

    except OSError as e:
        print(f"❌ Error writing file: {e}")

    obj = text_table()
    obj.USER = user_table.objects.get(LOGIN__id=request.user.id)
    obj.text_input = des
    obj.output_format = type_val
    obj.generated_code = filename
    obj.date = datetime.now()
    obj.save()

    return render(request, 'user/view_code_result.html', {"data": data,"fn":filename})



# @login_required(login_url='/myapp/login')
# def user_img_to_code_post(request):
#     image= request.FILES.get('image')
#     type_val = request.POST.get('type')
#
#     data = generate_image(image, type_val)
#
#     # Handle the error cases from our function
#     if data == "ERROR:LIMIT_REACHED":
#         messages.error(request, "Free limit reached. Please wait a minute before trying again.")
#         return render(request, 'user/view_code_result.html', {"data": "API limit reached. Try again later."})
#
#     if "ERROR" in data:
#         messages.error(request, "An unexpected error occurred with the AI model.")
#         return render(request, 'user/view_code_result.html', {"data": "Something went wrong."})
#
#     # Clean the data if successful
#     data = data.replace("```html", "").replace("```", "").strip()
#
#     return render(request, 'user/view_code_result.html', {"data": data})
#







@login_required(login_url='/myapp/login')
def user_send_comp(request):
    return render(request,'user/sendcomplaint.html')

@login_required(login_url='/myapp/login')
def user_view_tips(request):
    ob = tips_table.objects.all
    return render(request,'user/userviewtips.html',{"tips": ob})

@login_required(login_url='/myapp/login')
def user_send_comp_post(request):
    complaint=request.POST['complaint']
    ob=complaint_table()
    ob.complaint=complaint
    ob.reply='pending'
    ob.date=datetime.now()
    ob.USER=user_table.objects.get(LOGIN_id=request.user.id)
    ob.save()
    messages.success(request,"Complaint Send Success")
    return redirect("/myapp/user_send_comp")

@login_required(login_url='/myapp/login')
def user_view_prof(request):
    ob=user_table.objects.filter(LOGIN_id=request.user.id)
    return render(request,'user/viewprofile.html',{"users":ob})

@login_required(login_url='/myapp/login')
def user_prof_edit(request):
    ob=user_table.objects.filter(LOGIN_id=request.user.id)
    return render(request,'user/prof_edit.html',{"users":ob})

@login_required(login_url='/myapp/login')
def user_prof_edit_post(request):
    name=request.POST['name']
    designation=request.POST['des']
    email=request.POST['email']
    phone=request.POST['phn']
    ob=user_table.objects.get(LOGIN__id=request.user.id)
    ob.name=name
    ob.designation=designation
    ob.email=email
    ob.phone=phone
    ob.save()
    # ✅ SUCCESS MESSAGE
    messages.success(request, "Your profile updated successfully")

   # stay on same page
    return redirect("/myapp/user_prof_edit")
    # return redirect('/myapp/user_home')

@login_required(login_url='/myapp/login')
def user_gen_code(request):
    return render(request,'user/user_gen_code.html')
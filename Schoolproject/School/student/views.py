from.context_processors import*
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login , logout
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from .forms import *
from .models import *
from student import signals
import datetime
from django.core import serializers
from django.utils.safestring import mark_safe # to prevent string url in json from  encoding in template
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.

#homepage for students
@login_required(login_url="signin")
def home(request):  
    if request.method=="POST":
        attnd_status=request.POST.get('second')
        name=request.POST.get('third')
        noti_read= request.POST.get("noti_read")
        print(request.POST)
        print("attnd= ", attnd_status, "name= ",name ,"date is = ",datetime.date.today(), "notification_status", noti_read)
        if noti_read:
            n_data=notification.objects.filter(is_read= False).update(is_read=True)
            print("unread notficationsss ==========",n_data)
            
        chk_attn=attendance.objects.filter(name=name,attdate=datetime.date.today())
        print("attendence status===============", chk_attn)
        if chk_attn:
            data= Student.objects.filter(username = request.user) # filter gets full multiquery by machtibng the input with stored data
            print("cccccattendenceccccc",chk_attn)
            context = {
            'info':data,
            'attn_status':chk_attn,
            }
            return  render(request,"home.html",context,context_instance=RequestContext(request,processors=[get_notifications]))
        c=attendance.objects.create(name=name,is_present=attnd_status,attdate=datetime.date.today())
        d=Student.objects.filter(first_name__icontains=name,is_staff=False,is_superuser=False)
        response = {
        'att_marked': "Present" 
        }
        print("Response=", response)
        return JsonResponse(response, status=200, safe=False)
            
    chk_attn=attendance.objects.filter(name=request.user.first_name, attdate=datetime.date.today())       
    data= Student.objects.filter(username = request.user) #filter gets full multiquery by machtibng the input with stored data
    print("ggggggggggggggg",data)
    context = {
        'info':data,
        'attn_status':chk_attn
    }
    return  render(request, "home.html",context)
    

#homepage for accounts
@login_required(login_url="signin")
@staff_member_required
def accountshome(request):
    students= Student.objects.filter(is_staff=False,is_superuser=False)
    return render(request,"achome.html",{"details":students})

#homepage for admins
@login_required(login_url="signin")
@user_passes_test(lambda u: u.is_superuser)
def adminhome(request):
    stu= Student.objects.filter(is_staff=False,is_superuser=False)
    return render(request,"adhome.html",{"details":stu})

    

def signin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("adhome")
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("achome")
    if request.user.is_authenticated:
        return redirect("home")
    
    elif request.method=="POST":
        email=request.POST['email']
        pw=request.POST['password']
        mail = Student.objects.filter(email=email) #filter always return a multiquery set containing object and get only return for single object (getting an object)
        print(mail)
        if mail:
            user=authenticate(request,username=mail.first().username,password=pw)
            print(user, "line 17 executed")
            
        else:
            print(mail)
            messages.error(request,'Email/Password incorrect')
            return render(request, "login.html")            
        if user.is_authenticated :
            login(request,user)
            if user.is_superuser:
                return redirect ("adhome")
            if user.is_staff:
                return redirect ("achome")
            return redirect ("home")
        else:
            print("user not found")
            messages.error(request,'Email/Password incorrect')
            return render(request, "login.html")
    else:
        print("if 1")    
        return render(request, "login.html")
    
def signup(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("adhome")
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("achome")
    if request.user.is_authenticated:
        return redirect("home")
    if request.method== "POST":
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        email=request.POST['email']
        phone=request.POST['contact']
        pw=request.POST['password1']
        pw2=request.POST['password2']
        father=request.POST['fathername']
        cls=request.POST['class']
        adrss=request.POST['address']
        if fname.strip()=="" or lname.strip()=="" or email.strip()=="" or phone.strip()=="" or pw.strip()=="" or father.strip()=="" or cls.strip()=="" or adrss.strip()=="" :
            messages.error(request," Data must not be empty")
            return redirect("signup")
        if pw==pw2:
            d=stu_cls_model.objects.get(id=cls)
            print("d",   d)
            user=Student.objects.create(first_name=fname,last_name=lname,username=fname+lname,email=email,contact=phone,password=pw,fathername=father,clas=d,address=adrss,fee=d.mothly_fee)
            messages.success(request, f"New account created with : {email}")
            print(user,"user created successfully")
            user.set_password(pw)
            user.save()
            return redirect('signin')   
        else:
            messages.error(request,"Passwords did not match, Try Again!")
            return redirect("signup")
            
    d=stu_cls_model.objects.all()
    print(d,"model data")
    return render(request, "register.html",{'end':d}) #context to show class choices directly from model

@login_required(login_url="signin")
#update details feature for students
def update(request):
    if request.method=="POST":
        address=request.POST["address"]
        contact=request.POST["contact"]
        email=request.POST["email"]
        print(address.strip()," empty address")
        print(request.POST," empty data")
        if address.strip()=="" or contact.strip()=="" or email.strip()=="":
            messages.error(request," Data must not be empty")
            return redirect("update")
        else:
            user=Student.objects.filter(username=request.user).update(address=address,contact=contact,email=email)
            print(user)
           
            print(update," user updated")
            messages.success(request, "Details updated sucessfully")
            # signals.stu_details_updated.send(sender='Student updated his details', task_id=124)  #Using Signals we have import signals file in top
        
            return redirect("home")
    else:
        user=Student.objects.get(username=request.user.username)
        print(user)
        return render(request,"update.html",{"user":user})
    
@staff_member_required
@login_required(login_url="signin")
#update fee feature for accounts only
def updatefee(request,id):
    if request.method=="POST":
        feee=request.POST.get ('totalfee')
        receiver=request.POST.get('receiving_user')
        feefor=request.POST.get("totalmonth")
        if feee.strip()=="" and receiver.strip()=="" and  feefor.strip()=="":
            messages.error(request," Please enter some data ")
            return redirect("updatefee")
        
        print("receiver= ",receiver,"and month is", feefor )
        user=Student.objects.filter(id=id).update(fee=feee,fee_received_by=receiver,fee_status=feefor)
        for_noti=User.objects.filter(id=id)
        print(for_noti,"noti.usersssssssssssssss")
        n=notification.objects.create(text=" Your Fee is updated !!", users=for_noti.first())
        print(user," user updated")
        messages.success(request, "Details updated sucessfully")
        return redirect("achome")
    else:
        d=Student.objects.filter(id=id)
        if d:   
            d1 = d.first()
            print(d1)
        return render(request,"updateFee.html",{"month":fee_choices,"data":d1})
    

#pending update option for admin
@login_required(login_url="signin")
@user_passes_test(lambda u: u.is_superuser)       
def adupdate(request,id):
    if request.method=="POST":
        address=request.POST["address"]
        contact=request.POST["nmbr"]
        father=request.POST["fathername"]
        if address.strip()=="" and contact.strip()=="" and  father.strip()=="":
            messages.error(request," Please select an option ")
            return redirect("adupdate")
        print(address,"   ",contact," and ", father)
        data=Student.objects.filter(id=id).update(fathername= father,address=address,contact=contact)
        print(data," user updated")
        messages.success(request, "Details updated sucessfully")
        return redirect("achome")
    else:
        d = Student.objects.filter(id=id)
        if d:
            data=d.first()
    print(data)
    return render(request,"adupdate.html",{"data":data})

#pending delete option for admin
@login_required(login_url="signin")
@user_passes_test(lambda u: u.is_superuser)       
def adelete(request,id):   
    d= Student.objects.filter(id=id)
    print(" Student to be deleted = ",d)
    d.delete()
    return redirect ("adhome")


#search option for admin and accounts(without ajax commented out ones)
@login_required(login_url="signin")
def search(request):
    if request.method=="POST":
        txt= request.POST.get("search_txt")
        print("reeeeequestqqqqqqqqqqqqqqq",request.POST)
        print("text is:",txt)
        if txt.strip()=="":
            if request.user.is_authenticated and request.user.is_superuser:
                print("ifStrip1")
                messages.error(request," Try again, Enter name to search")
                data=Student.objects.filter(is_staff=False,is_superuser=False)
                return render(request,"me.html" ,{"details":data})
            else:
                print("if3")
            if request.user.is_authenticated and request.user.is_staff:
                messages.error(request," Try again, Enter name to seaxch ")
                return redirect("achome")
            else:
                print("if4")
        else:
            print("if2")    
            querryset=Student.objects.filter(Q(first_name__icontains=txt,is_staff=False,is_superuser=False) | Q(last_name__icontains=txt,is_staff=False,is_superuser=False) |  Q(username__icontains=txt,is_staff=False,is_superuser=False))
            print("fetched seacrh data",querryset.first().id)
            # data= serializers.serialize('json',list(querryset))
            # print("DDDDDAAAAAAAAAAATTTTTTAAAAAA",data)
            if request.user.is_authenticated and request.user.is_superuser:

                # // Returing results  a diff table template render method 
                # return render(request,"me.html",{"details":querryset})
                
                #// using Json response as alternate
                x = '<tr border="2"><th>First name</th><th>Last name</th>       <th>Email</th>       <th>Phone_number</th>       <th>Father_Name</th>       <th>Address</th><th>Is General Category</th><th>Class</th><th>Fee submitted</th>       <th>Fee Received by</th>       <th>Received For</th>       <th>Attendece for <p id="date">1/12/2023</p></th><th>Actions</th></tr>'
                print(id,"IDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD") 
                url1 = str(reverse('adupdate',kwargs={'id':querryset.first().id }))  # using reverese to send urls to django to prevent escaping
                url2= str(reverse('adelete',kwargs={'id': querryset.first().id}))
                print(url1) 
                print(url2)
                for i in querryset:
                    x += "<tr>"
                    x += "<td> " + str(i.first_name) + "</td>"
                    x += "<td> " + str(i.last_name) + "</td>"
                    x += "<td> " + str(i.email) + "</td>"
                    x += "<td> " + str(i.contact) + "</td>"
                    x += "<td> " + str(i.fathername) + "</td>"
                    x += "<td> " + str(i.address) + "</td>"
                    x += "<td> " + str(i.gen_cat) + "</td>"
                    x += "<td> " + str(i.clas) + "</td>"
                    x += "<td> " + str(i.fee) + "</td>"
                    x += "<td> " + str(i.fee_received_by) + "</td>"
                    x += "<td> " + str(i.fee_status) + "</td>"
                    x += "<td> " + str(i.is_present_today) + "</td>"
                    x += "<td> " + f"<a href= '{mark_safe(url1)}'> Update  </a> <span> <a href= '{mark_safe(url2)}' > Delete  </a> </span> " + "</td>"
                    x += "</tr>"
                    print("RRRRRRRRRRRRRRRRRRRRRRRRRRRR",x)

                return JsonResponse(x , status=200 , safe=False)
            
            if request.user.is_authenticated and request.user.is_staff:
                print("if5")
                return redirect('achome')
            
    else:
        print("if1")
        logout(request.user)
        return redirect('login')

    

        
    
        
            

            
        
        
        
        

    

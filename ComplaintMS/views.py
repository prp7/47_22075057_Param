from django.shortcuts import render,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import re
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q
from django.utils import  timezone

User = get_user_model()

# Create your views here

def my_login_student(request):
    if request.method == "POST":
        data = request.POST
        email = data.get('user_email')
        password = data.get('user_password')


        user1 = Student.objects.filter(email = email)
        if user1.exists():
            user = authenticate(email=email, password=password)
            if user is None:
                messages.error(request, "invalid email or password")
                return redirect("my_login_student")
            else:
                login(request, user)
                print("User logged in successfully")
                return redirect('student_interface')
        else:
            messages.error(request, "email is not registered!")
            print("email is not registered!")
            return redirect("my_login_student")


    return render(request, 'student_login.html')




def my_login_administrator(request):
    if request.method == "POST":
        data = request.POST
        email = data.get('user_email')
        password = data.get('user_password')


        user1 = Administrator.objects.filter(email = email)
        if user1.exists():
            user = authenticate(email=email, password=password)
            if user is None:
                messages.error(request, "invalid email or password")
                return redirect("my_login_administrator")
            else:
                login(request, user)
                print("User logged in successfully")
                return redirect('administrator_interface')
        else:
            messages.error(request, "email is not registered!")
            print("email is not registered!")
            return redirect("my_login_administrator")


    return render(request, 'administrator_login.html')

def my_signup_administrator(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('user_name')
        email = data.get('user_email')
        domain = data.get('domain')
        domain_name = data.get('domain_name')
        phone = data.get('user_phone')
        password = data.get('user_password')
        password1 = data.get('user_password1')
        regexp = '@i{1,2}tbhu\.ac\.in$'


        print(domain)
        print(domain_name)
        print(phone)
        domain_obj = Domain.objects.get(Q(domain=domain),Q(domain_name=domain_name))


        if not re.search(regexp,email):
            messages.info(request,"please use institute email only")
            print("please use institute email only")
            return redirect("my_signup_administrator")


        if password!=password1:
            messages.info(request,"make sure your password and confirmation password are the same")
            print("make sure your password and confirmation password are the same")
            return redirect("my_signup_administrator")


        user = Administrator.objects.filter(email = email)
        if user.exists():
            messages.error(request,"User already registered")
            print("User already registered")
            return redirect("my_login_administrator")
        else:
            user1 = User.objects.create(
                name = name,
                email = email
            )
            user1.set_password(password)
            user1.save()
            user1.changeType()
            user1.save()


            user1_additional = AdministratorAdditional.objects.create(
                user = user1,
                domain = domain_obj,
                phone = phone,
            )
            user1_additional.save()
            print("User registered successfully")
            return redirect('my_login_administrator')            
       
    return render(request, 'administrator_signup.html')





def my_signup_student(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('user_name')
        email = data.get('user_email')
        password = data.get('user_password')
        password1 = data.get('user_password1')
        regexp = '@i{1,2}tbhu\.ac\.in$'
        if not re.search(regexp,email):
            messages.info(request,"please use institute email only")
            print("please use institute email only")
            return redirect("my_signup_student")


        if password!=password1:
            messages.info(request,"make sure your password and confirmation password are the same")
            print("make sure your password and confirmation password are the same")
            return redirect("my_signup_student")


        user = User.objects.filter(email = email)
        if user.exists():
            messages.error(request,"User already registered")
            print("User already registered")
            return redirect("my_login_student")
        else:
            user1 = User.objects.create(
                name = name,
                email = email
            )
            user1.set_password(password)
            user1.save()
            print("User registered successfully")
            return redirect('my_login_student')            
       


    return render(request, 'student_signup.html')





@ login_required(login_url='my_login_student')
def new_complaint(request):
    if not request.user.type == 'Student' :
        return messages.info(request,"You don't have permission to access this page.")  

    if request.method == 'POST':
        student = request.user
        # domain = request.POST.get('domain')
        domain_name= request.POST.get('domain_names')
        category = request.POST.get('category')
        description = request.POST.get('description')
        print(domain_name)
        domain_obj=Domain.objects.get(domain_name=domain_name)
        category_obj= Category.objects.get(name=category)

        if domain_name and category and description:
            complaint = Complaints(issuer=student, domain=domain_obj, category=category_obj, issue=description)
            complaint.save()
            return redirect('student_interface')

    return render(request, 'complaint_form.html')

@ login_required(login_url='my_login_student')
def student_interface(request):
    return render(request, 'student_interface.html')

@ login_required(login_url='my_login_administrator')
def administrator_interface(request):
    print('rendering admin interface')
    return render(request, 'administrator_interface.html')

def home(request):
    return render(request, 'home.html')

def login_page(request):
    return render(request, 'login_page.html')

def signup_page(request):
    return render(request, 'signup_page.html')

def my_logout_student(request):
    logout(request)
    return redirect('home')

def my_logout_administrator(request):
    logout(request)
    return redirect('home')

@ login_required(login_url='my_login_administrator')
def unaddressed_complaints(request):
    admin=request.user
    admin_obj=AdministratorAdditional.objects.get(user=admin)
    dom_obj=admin_obj.domain
    complaints=Complaints.objects.filter(Q(is_unaddressed=True),Q(domain=dom_obj))
    return render(request,'unaddressed_complaints.html',context={'complaints':complaints})

@ login_required(login_url='my_login_administrator')
def assign_worker(request,complaint_id):
    cmp_obj=Complaints.objects.get(id=complaint_id)
    available_workers=Workers.objects.filter(Q(status='Available'),Q(category=cmp_obj.category))
    occupied_workers=Workers.objects.filter(Q(status='Occupied'),Q(category=cmp_obj.category)).order_by('task_count')
    
    if request.method == 'POST':
        print("I reached here1")
        data=request.POST
        admin=request.user
        print("I reached here")
        worker_id1=data.get('worker1')
        worker_id2=data.get('worker2')
        print(worker_id1)
        print(worker_id2)
        worker_id=worker_id1
        if(worker_id1 is None):
            worker_id=worker_id2

        worker_obj=Workers.objects.get(id=worker_id)
        cmp_obj.is_unaddressed=False
        cmp_obj.status='In_progress'
        cmp_obj.assigner=admin
        cmp_obj.assignee=worker_obj
        cmp_obj.date_assigned=timezone.now()
        cmp_obj.save()

        worker_obj.status='Occupied'
        worker_obj.inc_count()
        worker_obj.save()
        return redirect('unaddressed_complaints')
    return render(request,'assign_worker.html',context={'cmp':cmp_obj,
                                                        'available_workers':available_workers,
                                                        'occupied_workers':occupied_workers})

@ login_required(login_url='my_login_administrator')
def assigned_complaints(request):
    admin=request.user
    admin_obj=AdministratorAdditional.objects.get(user=admin)
    dom_obj=admin_obj.domain
    complaints=Complaints.objects.filter(Q(is_unaddressed=False),Q(domain=dom_obj),Q(status='In_progress'))

    if request.method=='POST':
        data=request.POST
        complaint_id=data.get('complaint_id')
        print(complaint_id)
        cmp_obj=Complaints.objects.get(id=complaint_id)
        cmp_obj.status='Resolved'
        cmp_obj.date_resolved=timezone.now()
        cmp_obj.save()

        w_obj=cmp_obj.assignee
        print(w_obj.task_count)
        if w_obj.task_count==1 :
            w_obj.dec_count()
            w_obj.status='Available'
        else:
            w_obj.dec_count()
        w_obj.save()
    return render(request,'assigned_complaints.html',context={'complaints':complaints})


@ login_required(login_url='my_login_administrator')
def resolved_complaints_admin(request):
    admin=request.user
    admin_obj=AdministratorAdditional.objects.get(user=admin)
    dom_obj=admin_obj.domain
    complaints=Complaints.objects.filter(Q(status='Resolved'),Q(domain=dom_obj))
    return render(request,'resolved_complaints_admin.html',context={'complaints':complaints})

@ login_required(login_url='my_login_administrator')
def register_worker(request):
    if request.method == "POST":
        data = request.POST
        name = data.get('worker_name')
        phone = data.get('worker_phone')
        category = data.get('worker_category')
        # print(name, phone, category)
        worker = Workers.objects.filter(phone = phone)
        if worker.exists():
            messages.error(request, "Worker with this phone number already exists")
            return redirect('register_worker')
        else:
            category1 = Category.objects.get(name = category)
            worker1 = Workers.objects.create(
                name = name,
                phone = phone,
                category = category1
            )
            worker1.save()
            return redirect('administrator_interface')
    catagories = Category.objects.all()
    context = {
        'catagories': catagories,
    }
    return render(request, 'add_worker.html',context)


@ login_required(login_url='my_login_administrator')
def all_workers(request):
    workers = Workers.objects.all()
    context = {'workers':workers}
    if request.method=='POST':
        data=request.POST
        wid=data.get('worker_id')
        w_obj=Workers.objects.get(id=wid)
        if w_obj.status=='Available' or w_obj.status=='On_leave':
            w_obj.delete()
        else:
            messages.info(request,'Occupied Worker cannot be removed.')
    return render(request,'all_workers.html',context)


def grant_leave(request,worker_id):
    w_obj=Workers.objects.get(id=worker_id)
    context= {'worker':w_obj}
    if request.method=='POST':
        data=request.POST
        leave_rsn=data.get('rsn')
        date_from=data.get('from')
        date_to=data.get('to')
        print(leave_rsn,date_from,date_to)
        w_obj.leave_rsn=leave_rsn
        w_obj.date_from=date_from
        w_obj.date_to=date_to
        w_obj.status='On_leave'
        w_obj.save()
        try:
            trigger=leave_trigger()
            trigger.worker_id=worker_id
            trigger.save()
            print(trigger.worker_id)
            trigger.process_after = timezone.now() + timedelta(minutes=2)
            print(trigger.worker_id)
        except:
            print("alas! no trigger")
        return redirect('all_workers')
    return render(request,'grant_leave.html',context)







@ login_required(login_url='my_login_student')
def resolved_complaints(request):
    if request.method=="POST":
        data = request.POST
        id = data.get('complaint_id')
        print(id)
        x = Complaints.objects.get(id = id)
        x.is_deleted = True
        x.save()
        return redirect("resolved_complaints")
    student = request.user
    resolved_complaints = Complaints.objects.filter(Q(issuer = student),Q(status = 'Resolved'),Q(is_deleted = False))
    context = {
        'resolved_complaints': resolved_complaints,
        'student': student
    }
    return render(request,'resolved_complaints.html',context)




@ login_required(login_url='my_login_student')
def unresolved_complaints(request):
    if request.method == "POST":
        print("here")
        data = request.POST
        id = data.get('complaint_id')
        x = Complaints.objects.get(id = id)
        # print(x[0])
        if x.status == "Opened":
            x.is_deleted = True
            x.save()
            return redirect('unresolved_complaints')
        else:
            messages.info(request,"In progress complaints can't be deleted")
       
    student = request.user
    unresolved_complaints = Complaints.objects.filter(Q(issuer = student),(Q(status = 'Opened') | Q(status = 'In_progress')),Q(is_deleted = False))
    context = {
        'student': student,
        'unresolved_complaints': unresolved_complaints,
    }
    return render(request, 'unresolved_complaints.html', context)


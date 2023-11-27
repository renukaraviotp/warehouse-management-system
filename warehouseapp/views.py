from django.shortcuts import render,redirect
import random
from django.contrib import messages
from .models import Client,Delivery,Notification,Product,Orders,AddressForm,Delivery1
from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from email import message
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
from . import forms,models
import os
from django.contrib.auth.decorators import login_required
# Create your views here.

def home_view(request):
    products=models.Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    if request.user.is_authenticated:
        return HttpResponseRedirect('login1')
    return render(request,'index.html',{'products':products,'product_count_in_cart':product_count_in_cart})

# login page view
def index(request):
    return render(request,'login.html')

# admin home page
def admin(request):
    return render(request,'admin.html')

# client home page
def client(request):
    return render(request,'client.html')

# delivery home page
def delivery(request):
    return render(request,'delivery.html')

# client signup page 
def client_signup(request):
    return render(request,'client_signup.html')

# delivery signup page
def delivery_signup(request):
    return render(request,'delivery_signup.html')

# client signup function
def client_reg(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        age = request.POST['age']
        address=request.POST['address']
        contact = request.POST['contact']
        image = request.FILES['photo'] 
        password='123'
        # password=request.POST['password']
        # password = str(random.randint(100000, 999999))
        user_type = request.POST['text']
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This email already exists!!!!!!')
            return redirect('client_signup')
        else:
            user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,password=password,email=email_id,user_type=user_type)
            user.save()
                
            
            member=Client(age=age,number=contact,photo=image,address=address,user=user)
            member.save()
            # subject='Your Approval has been Successfull'
            # message=f'We have received your application and the admin has approved your application. Your username and password are:\nUsername:{user_name}\nPassword:{password}'
            # recipient=email_id
            # send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
            return redirect('/')
                # messages.info(request, 'You have successfully registered')
          
    return render(request,'client_signup.html')

# client approve function
def client_approve(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email'] 
        contact = request.POST['contact']
        image = request.FILES['photo'] 
        
        # password=request.POST['password']
        # password = str(random.randint(100000, 999999))
        user_type = request.POST['text']
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This email already exists!!!!!!')
            return redirect('client_signup')
        else:
            user=Delivery1(first_name=first_name,last_name=last_name,username=user_name,email=email_id,number=contact,user_type=user_type,client=True)
            user.save() 
            return redirect('/')
                # messages.info(request, 'You have successfully registered')
          
    return render(request,'client_signup.html')

# def approvedetails(request):
#     a=Client1.objects.all()
#     return render(request,'approve.html',{'a':a})

def approval(request,pk):
    s=Notification.objects.all() 
    c=Delivery1.objects.get(id=pk)
    if c.client==True:
        pas=str(random.randint(100000,999999))
        use=CustomUser.objects.create_user(email=c.email,username=c.username,password=pas,first_name=c.first_name,last_name=c.last_name,user_type=c.user_type)
        usr=Client(number=c.number,photo=c.image,age=1) 
        c.is_approved=True
        c.save()
        usr.user=use 
        usr.save()
        c.delete()
        subject="Your Approval has been Successful"
        message=f'Dear {use.first_name} {use.last_name}, \n We have received your application and it has been approved. \n Here is your username and password: \n username: {use.username} ''\n password={}'.format(pas)
        recipient=use.email 
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
        return render(request,'admin.html',locals())
    elif c.delivery==True:
        pas=str(random.randint(100000,999999))
        use=CustomUser.objects.create_user(email=c.email,username=c.username,password=pas,first_name=c.first_name,last_name=c.last_name,user_type=c.user_type)
        usr=Delivery(number=c.number,image=c.image)
        c.is_approved=True
        c.save()
        usr.user=use 
        usr.save()
        c.delete()
        subject="Your Approval has been Successful"
        message=f'Dear {use.first_name} {use.last_name}, \n We have received your application and it has been approved. \n Here is your username and password: \n username: {use.username} ''\n password={}'.format(pas)
        recipient=use.email 
        send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
        return render(request,'admin.html',locals())

def disapproval(request,pk):
    p=Delivery1.objects.get(id=pk) 
    p.delete()
    return redirect('/') 

def show_notification(request):
    s=Client.objects.all()
    return render(request,'approve.html',{'s':s})

# delivery approve function
def delivery_approve(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        contact = request.POST['contact']
        image = request.FILES.get('image')
        
        # password = str(random.randint(100000, 999999))
        user_type = '2'
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This email already exists!!!!!!')
            return redirect('delivery_signup')
        else:
            user=Delivery1(first_name=first_name,last_name=last_name,username=user_name,email=email_id,number=contact,image=image,user_type=user_type,delivery=True)
            user.save() 
            # send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
            return redirect('/')
    return render(request,'delivery_signup.html')

# delivery sign up original 
def delivery_reg(request):
    if request.method == 'POST':
        first_name = request.POST['fname']
        user_name = request.POST['uname']
        last_name = request.POST['lname']
        email_id = request.POST['email']
        contact = request.POST['contact']
        password='123'
        image = request.FILES.get('image')
        
        # password = str(random.randint(100000, 999999))
        user_type ='2' 
        if CustomUser.objects.filter(email=email_id).exists():
            messages.info(request, 'This email already exists!!!!!!')
            return redirect('delivery_signup')
        else:
            user=CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=user_name,password=password,email=email_id,user_type=user_type)
            user.save()      
            member=Delivery(number=contact,image=image,user=user)
            member.save()
                # messages.info(request, 'You have successfully registered')
            # subject='Your Approval has been Successfull'
            # message=f'We have received your application and the admin has approved your application. Your username and password are:\nUsername:{user_name}\nPassword:{password}'
            # recipient=email_id
            # send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
            return redirect('/')
    return render(request,'delivery_signup.html')

def approvedetails(request):
    a=Delivery1.objects.filter(is_approved=False) 
    return render(request,'approve.html',{'a':a})

# def approval(request,pk):
#     s=Notification.objects.all() 
#     c=Delivery1.objects.get(id=pk) 
#     c=Client1.objects.get(id=pk)
#     pas=str(random.randint(100000,999999))
#     use=CustomUser.objects.create_user(email=c.email,username=c.username,password=pas,first_name=c.first_name,last_name=c.last_name,user_type=c.user_type)
#     usr=Delivery(number=c.number,image=c.image)
#     usr=Client(number=c.number,image=c.photo)
    
#     usr.user=use 
#     usr.save()
#     c.delete()
#     subject="Your Approval has been Successful"
#     message=f'Dear {use.first_name} {use.last_name}, \n We have received your application and it has been approved. \n Here is your username and password: \n username: {use.username} ''\n password={}'.format(pas)
#     recipient=use.email 
#     send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
#     return render(request,'admin.html',locals())

# def disapproval(request,pk):
#     p=Delivery1.objects.get(id=pk) 
#     p=Client1.objects.get(id=pk)
#     p.delete()
#     return redirect('approvedetails') 

# def show_notification(request):
#     s=Delivery.objects.all()
#     s=Client.objects.all()
#     return render(request,'approve.html',{'s':s})
    

# login function
def login1(request):
    if request.method=='POST':
        user_name=request.POST.get('username')
        print(user_name)
        password1=request.POST.get('password')
        print(password1)
        user=authenticate(username=user_name,password=password1)
           
        if user is not None:
            if user.user_type == '1':
                login(request,user)
                return render(request,'admin.html')
            elif user.user_type == '2':
                auth.login(request,user)
                return redirect('delivery')
            else:
                auth.login(request,user)
                return redirect('customer_home_view')
        else:
            messages.info(request,"Invalid username or password")
            return redirect('/')
    return render(request,'login.html') 
    
def show_nofification(request):
    s=Notification.objects.all()
    return render(request,'notification.html',{'s':s})

def approveaction(request,pk):
           n=Notification.objects.get(id=pk)
           n.sender.password = str(random.radint(100000,999999))
           n.save()
           subject='Your Approval has been successful'
           message=f' Dear {n.sender.first_name}{n.sender.last_name}, \n We have received your application and it has been approved. \n Here is your username and password: \n username{n.sender.username} \n  password :{n.sender.password} thanku for joining'
           recipient=n.sender.email
           send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient])
           message.info(request,)
           
def logoutt(request):
    logout(request)
    return redirect('home_view')

#########################################
###########  Admin Views ################
#########################################
def admin_dashboard_view(request):
    # for cards on dashboard
    customercount=Client.objects.all().count()
    productcount=Product.objects.all().count()
    ordercount=Orders.objects.all().count()

    # for recent order tables
    orders=Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    # for order in orders:
    #     ordered_product=Product.objects.filter(id=order.product.id)
    #     ordered_by=Client.objects.all().filter(id = order.client.id)
    #     ordered_products.append(ordered_product)
    #     ordered_bys.append(ordered_by)

    mydict={
    'customercount':customercount,
    'productcount':productcount,
    'ordercount':ordercount,
    'data':zip(ordered_products,ordered_bys,orders),
    }
    return render(request,'admin.html',context=mydict)

def admin_products_view(request):
    products=Product.objects.all()
    return render(request,'add_product.html',{'products':products})

def admin_add_product_view(request):
    if request.method=='POST':
        pname = request.POST['pname']
        des = request.POST['des']
        price = request.POST['price']
        qty=request.POST['qty']
        image = request.FILES.get('image')
        product=Product(name=pname,description=des,price=price,product_image=image,qty=qty)
        product.save()
        return redirect('admin_products_view')
    return render(request,'add_pro.html')

def delete_product_view(request,pk):
    product=Product.objects.get(id=pk)
    product.delete()
    return redirect('admin_products_view')



def update_product_view(request,pk):
    product=Product.objects.get(id=pk)
    if request.method=='POST':
        product=Product.objects.get(id=pk)
        product.name=request.POST['pname']
        product.description=request.POST['des']
        product.price=request.POST['price']
        product.qty=request.POST['qty']
        if len(request.FILES)!=0:
            if len(product.product_image)>0: 
                os.remove(product.product_image.path)
            else:
                product.product_image = request.FILES['image']
            product.product_image=request.FILES['image']
        product.save()
        return redirect('admin_products_view')
    return render(request,'edit_product.html',{'prd':product})

def admin_view_booking_view(request):
    orders=Orders.objects.all()
    ordered_products=[]
    ordered_bys=[]
    for order in orders: 
        ordered_product=Product.objects.all().filter(id=order.product.id) 
        ordered_by=Client.objects.all().filter(id = order.client.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'listoforders.html',{'data':zip(ordered_products,ordered_bys,orders)})



def delete_order_view(request,pk):
    order=models.Orders.objects.get(id=pk)
    order.delete()
    return redirect('admin_view_booking_view')

def view_customer_view(request):
    customers=Client.objects.all()
    return render(request,'customer.html',{'customers':customers})

# admin delete customer
def delete_customer_view(request,pk):
    customer=Client.objects.get(id=pk)
    user=CustomUser.objects.get(id=customer.user_id)
    user.delete()
    customer.delete()
    return redirect('view_customer_view')

def view_delivery_view(request):
    delivery=Delivery.objects.all()
    return render(request,'admin_delivery.html',{'delivery':delivery})

def delete_delivery_view(request,pk):
    delivery=Delivery.objects.get(id=pk)
    user=CustomUser.objects.get(id=delivery.user_id)
    user.delete()
    delivery.delete()
    return redirect('view_delivery_view')


########################################################
########### Client Views ###############################
########################################################

def search_view(request):
    # whatever user write in search box we get in query
    query = request.GET['query']
    products=Product.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # word variable will be shown in html when user click on search button
    word="Searched Result :"

    if request.user.is_authenticated:
        return render(request,'client.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})
    return render(request,'index.html',{'products':products,'word':word,'product_count_in_cart':product_count_in_cart})

def customer_home_view(request):
    products=Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    return render(request,'client.html',{'products':products,'product_count_in_cart':product_count_in_cart})


def add_to_cart_view(request,pk):
    products=Product.objects.all()

    #for cart counter, fetching products ids added by customer from cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=1

    response = render(request, 'index.html',{'products':products,'product_count_in_cart':product_count_in_cart})

    #adding product id to cookies
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids=="":
            product_ids=str(pk)
        else:
            product_ids=product_ids+"|"+str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product=models.Product.objects.get(id=pk)
    messages.info(request, product.name + ' added to cart successfully!')

    return response



# for checkout of cart
def cart_view(request):
    #for cart counter
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # fetching product details from db whose id is present in cookie
    products=None
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=models.Product.objects.all().filter(id__in = product_id_in_cart)

            #for total price shown in cart
            for p in products:
                total=total+p.price
    return render(request,'cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})


def remove_from_cart_view(request,pk):
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    # removing product id from cookie
    total=0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart=product_ids.split('|')
        product_id_in_cart=list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products=models.Product.objects.all().filter(id__in = product_id_in_cart)
        #for total price shown in cart after removing product
        for p in products:
            total=total+p.price

        #  for update coookie value after removing product id in cart
        value=""
        for i in range(len(product_id_in_cart)):
            if i==0:
                value=value+product_id_in_cart[0]
            else:
                value=value+"|"+product_id_in_cart[i]
        response = render(request, 'cart.html',{'products':products,'total':total,'product_count_in_cart':product_count_in_cart})
        if value=="":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids',value)
        return response

def customer_address_view(request):
    # this is for checking whether product is present in cart or not
    # if there is no product in cart we will not show address form
    product_in_cart=False
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_in_cart=True
    #for counter in cart
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0

    if request.method=='POST':
        email = request.POST['email']
        mobile = request.POST['number']
        address=request.POST['number'] 
        delivery=request.POST['delivery']
        addressForm=AddressForm(Email=email,Mobile=mobile,Address=address,Delivery_method=delivery)
        addressForm.save()
        # if addressForm.is_valid():
            # here we are taking address, email, mobile at time of order placement
            # we are not taking it from customer account table because
            # these thing can be changes
        # email = addressForm.cleaned_data['Email']
        # mobile=addressForm.cleaned_data['Mobile']
        # address = addressForm.cleaned_data['Address']
            #for showing total price on payment page.....accessing id from cookies then fetching  price of product from db
        total=0
        if 'product_ids' in request.COOKIES:
                product_ids = request.COOKIES['product_ids']
                if product_ids != "":
                    product_id_in_cart=product_ids.split('|')
                    products=models.Product.objects.all().filter(id__in = product_id_in_cart)
                    for p in products:
                        total=total+p.price

        response = render(request,'payment.html',{'total':total})
        response.set_cookie('email',email)
        response.set_cookie('mobile',mobile)
        response.set_cookie('address',address)
        return response
    return render(request,'address.html',{'product_in_cart':product_in_cart,'product_count_in_cart':product_count_in_cart})

def payment_success_view(request):
    # place order | after successful payment
    # fetch customer  mobile, address, Email
    # fetch product id from cookies then respective details from db
    # then create order objects and store in db
    # after that delete cookies because after order placed...cart should be empty
    customer=Client.objects.get(user_id=request.user.id) 
    products=None
    email=None
    mobile=None
    address=None
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart=product_ids.split('|')
            products=Product.objects.all().filter(id__in = product_id_in_cart)
            # Here get products list that will be ordered by one customer at a time
    
     
    # these things can be change so accessing at the time of order...
    if 'email' in request.COOKIES:
        email=request.COOKIES['email']
    if 'mobile' in request.COOKIES:
        mobile=request.COOKIES['mobile']
    if 'address' in request.COOKIES:
        address=request.COOKIES['address']
    

    # here placing number of orders as much there is a products
    # suppose if  have 5 items in cart and we place order....so 5 rows will be created in orders table
    # there will be lot of redundant data in orders table...but its become more complicated if we normalize it
    for product in products:
        Orders.objects.create(client=customer,product=product,status='Pending',email=email,mobile=mobile,address=address)

    # after order placed cookies should be deleted
    response = render(request,'payment_success.html')
    response.delete_cookie('product_ids')
    response.delete_cookie('email')
    response.delete_cookie('mobile')
    response.delete_cookie('address')
    pas=str(random.randint(100000,999999)) 
    subject="Your Order is placed"
    message=f'Dear Sir/Madam, \n We have received your Order. ''\n Here is your tracking ID :{}'.format(pas)
    recipient=customer.user.email 
    send_mail(subject,message,settings.EMAIL_HOST_USER,[recipient]) 
    return response
   
    

def my_order_view(request):
    
    customer=Client.objects.get(user_id=request.user.id)
    orders=Orders.objects.all().filter(client_id = customer)
    ordered_products=[]
    for order in orders:
        ordered_product=Product.objects.all().filter(id=order.product.id)
        ordered_products.append(ordered_product)

    return render(request,'my_order.html',{'data':zip(ordered_products,orders)})

def my_profile_view(request):
    customer=Client.objects.get(user_id=request.user.id)
    return render(request,'my_profile.html',{'customer':customer})

def edit_profile_view(request):
    customer=Client.objects.get(user_id=request.user.id) 
    user=CustomUser.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer) 
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return redirect('my_profile_view') 
    return render(request,'edit_profile.html',context=mydict)


#################################################################
#------------Delivery module views------------------------------#
#################################################################
def delivery_order(request):
    orders=Orders.objects.all()
    ordered_products=[] 
    ordered_bys=[]
    for order in orders:
        ordered_product=Product.objects.all().filter(id=order.product.id)
        ordered_by=Client.objects.all().filter(id = order.client.id)
        ordered_products.append(ordered_product)
        ordered_bys.append(ordered_by)
    return render(request,'delivery_order.html',{'data':zip(ordered_products,ordered_bys,orders)})

def update_order_view(request,pk):
    order=Orders.objects.get(id=pk) 
    if request.method=='POST':
        status=request.POST['status']
        order.status=status
        order.save() 
        return redirect('delivery_order')
    return render(request,'status_update.html',{'order':order}) 
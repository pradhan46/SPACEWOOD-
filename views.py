from django.shortcuts import render, redirect 
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from .models.product1 import Product1
from .models.order import Order
from .models.OI import OI
from .models.customer import Customer
from .models.ShippingAddress import ShippingAddress
from .models.customized import Customized
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
import razorpay


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successfull')
            request.session['user_id'] = user.id
            request.session['email'] = user.email

            
            return redirect('index')
            
        
        else:
            messages.error(request,'invalid credentials')
            
            return redirect('login')
    else:
        return render(request,'login.html')
           
        

        

def index(request):

    
    return render(request, 'index.html',{'titles': 'Django', 'link':'http://127.0.0.1:8000/'})

def reg(request):

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']  
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username taken')
                return redirect('reg')
            elif User.objects.filter(email=email).exists():
                 messages.error(request,'email taken')
            else:

                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save();
                print('user created')
                return redirect('login')
        else:
            print('password not matching..')
            return redirect('reg')
        return redirect('/')
    else:
        return render(request, 'reg.html')

def contact(request):
  
    return render(request, "contact.html",{'titles': 'contact', 'link':'http://127.0.0.1:8000/'})

def logout(request):
    auth.logout(request)
    return redirect('/')

def customize(request):

    if request.method=='POST':
    

        product_type = request.POST.get('product_type','')
        type_of_wood =  request.POST.get('type_of_wood','')
        length = request.POST.get('length','')
        width = request.POST.get('width','')
        brief_about_the_Product = request.POST.get(' brief_about_the_Product','')

        customized = Customized(product_type=product_type,type_of_wood= type_of_wood,length=length,width=width, brief_about_the_Product= brief_about_the_Product)
        customized.save()
    



    return render(request, 'customize.html')

def category(request):
    return render(request, "category.html",{'titles': 'category', 'link':'http://127.0.0.1:8000/'})

def aboutus(request):
    return render(request, "aboutus.html",{'title': 'aboutus', 'link':'http://127.0.0.1:8000/' })
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.oi_set.all()


        
        
    else:
        items = []
        order = {'get_cart_total':0 ,'get_cart_items': 0,'shipping':False}
    context = {'items':items, 'order':order}
    
    if request.method=='POST':
       
        name = request.POST.get('name','')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        address= request.POST.get('address','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zipcode = request.POST.get('zipcode','')

        shippingAddress = ShippingAddress(name=name,email=email,phone=phone,address=address,city=city,state=state,zipcode=zipcode,amount=amount)
        shippingAddress.save()
     
        
        
        return redirect('payment')
    

    return render(request, "checkout.html",context)





def p(request):
    prds = Product1.get_all_products();
    

    
    return render(request, 'p.html',{'products': prds, 'title': 'p', 'link':'http://127.0.0.1:8000/'})


   
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.oi_set.all()


        
        
    else:
        items = []
        order = {'get_cart_total':0 ,'get_cart_items': 0,'shipping':False}
    context = {'items':items, 'order':order}
    return render(request, 'cart.html',context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)


    customer = request.user.customer
    product = Product1.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    oi,created = OI.objects.get_or_create(order=order, product=product)

    if action == 'add':
        oi.quantity = (oi.quantity + 1)
    elif action == 'remove':
        oi.quantity = (oi.quantity - 1)

    oi.save()

    if oi.quantity <= 0:
        oi.delete()
    

    return JsonResponse("Item was added", safe=False)

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

@csrf_exempt

def success(request,):
    template = render_to_string('email_template.html',{'name':request.user.username})

    email = EmailMessage(
        'Thank you for purchasing with Spacewood',
        template,
        settings.EMAIL_HOST_USER,
        [request.user.email], 
        )
    email.fail_silenty = False
    email.send()
    return render(request,"success.html")

def payment(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.oi_set.all()


        
        
    else:
        items = []
        order = {'get_cart_total':0 ,'shipping':False}
    context = {'items':items, 'order':order}

    if request.method == "POST":
        amount = 50000
        order_currency = 'INR'
        client = razorpay.Client(
            auth=('rzp_test_WH0WKp01H6mAab','cT1h3jhCGwMlZYjRVKG1yPvN'))
        payment = client.order.create({'amount':amount,'currency':'INR', 'payment_capture': '1'})
    
    return render(request, "payment.html",context)

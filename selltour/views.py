from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import *
from django.views.generic import ListView, DetailView
from django.template.defaulttags import register
import json
from django.http import JsonResponse
from django.core.mail import send_mail
from datetime import date
from django.db.models import Count

@register.filter
def get_range(value):
    return range(int(value))

@register.filter
def get_range2(value1, value2):
    return range(value1, value2, 1)

# Create your views here.
def homepage (resquest):
    tours = Tour.objects.annotate(Count('information_guess')).order_by('-information_guess__count')[:3]
    content ={'tours':tours}
    return render (resquest, 'index.html', content)




def detail (resquest):
    content = {}
    return render (resquest, 'product.html', content)

class ItemDetailView(DetailView):
    model = Tour
    template_name = "details.html"
    
    
    def get_context_data(self, *args, **kwargs):
        context = super(ItemDetailView, self).get_context_data(*args, **kwargs)
        tour = Tour.objects.get(slug=self.kwargs['slug'])
        context['image_list'] = Image_of_Tour.objects.filter(tour =tour.id_Tour)
        return context
    
    

def information_order(resquest):
    content ={}
    return render (resquest, 'order.html', content)

class order(DetailView):
    model = Tour
    template_name = "order.html"
    
def get_create_Customer(name, email, phone):

        customer_infor = Customer(name_Customer = name, email = email, phone_Number = phone)
        customer_infor.save()
        

def order_tour(request, slug):
    # INFORMATION OF Customer
    
    name = request.POST.get('contact_name', False)
    email = request.POST.get('email', False)
    phone = request.POST.get('mobilephone', False)
    print(phone)
    customer_infor = Customer.objects.filter(name_Customer = name, email = email, phone_Number = phone)
    if not customer_infor.exists() :
        #Nếu khách hàng ko có thì tạo
        get_create_Customer(name, email, phone)

    #lay đối tượng khách hàng
    customer = Customer.objects.get(name_Customer = name, email = email, phone_Number = phone)
    
    # lấy đối tượng tour  được chọn
    tour = Tour.objects.get(slug=slug)

    quantity = request.POST.get('quantity', False)
    total_Money = request.POST.get('amount', False)


    information_order = Order_Tour.objects.filter(tour = tour )
    if not information_order.exists():
        # tạo mới tượng tour  được đặt
        information_order = Order_Tour(tour = tour, customer = customer, Quantity = quantity, Toal_Money= total_Money)
        information_order.save()

        # lấy đối tượng tour  được đặt
    information_order = Order_Tour.objects.filter(tour = tour )

    for i in range(0, int(quantity)):
        full_name = request.POST.get("["+str(i)+"]."+"full_name", False)
        gender = request.POST.get("["+str(i)+"]."+"gender", False)
        birthday = request.POST.get("["+str(i)+"]."+"ngaysinh", False)
       
        guess = Information_Guess(tour = tour, customer =customer,  name_Guess = full_name, sex = bool(gender), birthday= birthday)
        guess.save()
    
    information_guess = Information_Guess.objects.filter(tour = tour, customer = customer)
    
    context={
        'customer':customer,
        'tour':tour,
        'infrmation_order':information_order,
        'information_guess':information_guess
    }
    return render(request, 'checkout.html', context)


def search (request):
    name_city = request.GET.get('city', False)
    departure = request.GET.get('departure', False)
    budget = request.GET.get('budget', False)

    try:
        tours =[]
        if name_city == "" and budget == "" :
            
            list_tour = Tour.objects.filter(origin_Place = departure)
            for tour in list_tour:
                tours.append(tour)

        elif name_city == "" and departure == "" :
            list_tour = Tour.objects.filter(price_Tour = budget)
            for tour in list_tour:
                tours.append(tour)

        elif budget == "" and departure == "" :
            city = City.objects.get(name_City = name_city)
            throughs = Through.objects.filter(city = city.id_City)
            
            for through in throughs:
                tour = Tour.objects.get(name_Tour = through.tour)
                tours.append(tour)

        elif name_city == "" :
            
            list_tour = Tour.objects.filter(price_Tour = budget, origin_Place = departure)
            for tour in list_tour:
                tours.append(tour)

        elif budget == "" :
            city = City.objects.get(name_City = name_city)
            throughs = Through.objects.filter(city = city.id_City)
            for through in throughs:
                tour = Tour.objects.get(name_Tour = through.tour, origin_Place= departure)
                tours.append(tour)

        elif departure == "" :
            #city = City.objects.get(name_City = name_city)
            throughs = Through.objects.filter(city__name_City = name_city)
            for through in throughs:
                tour = Tour.objects.get(name_Tour = through.tour, price_Tour = budget)
                tours.append(tour)
        else :
            city = City.objects.get(name_City = name_city)
            throughs = Through.objects.filter(city = city.id_City)
            for through in throughs:
                tour = Tour.objects.get(name_Tour = through.tour, price_Tour = budget, origin_Place=departure)
                tours.append(tour)

        print("day la noi dung:")
        for tour in tours:
            print(tour)
        content = {
            'tours':tours
        }
    except :
        return HttpResponse("city can't find")
    return render(request, 'seach.html', content)

def paymentComplete(request):
    body = json.loads(request.body)
    print(body)
    send_mail("Hello from datdao123", "You completed payment", 'daoducdat633@gmail.com', [body], fail_silently=False)
    print("Gui email thanh cong")
    return render(request, 'index.html' )

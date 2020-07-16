from django.shortcuts import render, get_object_or_404
from .models import *
from django.views.generic import ListView, DetailView
from django.template.defaulttags import register

@register.filter
def get_range(value):
    return range(int(value))

@register.filter
def get_range2(value1, value2):
    return range(value1, value2, 1)

# Create your views here.
def homepage (resquest):
    tours = Tour.objects.all()
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
    phone = request.POST.get('phone', False)
    #customer_infor = Customer.objects.get(name_Customer = name, email = email, phone_Number = phone)
    #if customer_infor == None :
        #Nếu khách hàng ko có thì tạo
        #get_create_Customer(name, email, phone)

    #lay đối tượng khách hàng
    #customer = Customer.objects.get(name_Customer = name, email = email, phone_Number = phone)
    
    # lấy đối tượng tour  được chọn
    #tour = Tour.objects.get(slug=slug)

    quantity = request.POST.get('quantity', False)
    total_Money = request.POST.get('amount', False)

    # tạo mới tượng tour  được đặt
    #information_order = Order_Tour(tour = tour, customer = customer, Quantity = quantity, Toal_Money= total_Money)
    #information_order.save()

    # lấy đối tượng tour  được đặt
    #information_order = Order_Tour.objects.filter(tour = tour )

    #for i in range(0, quantity):

    
    context={
        #'quantity':quantity
    }
    return render(request, 'checkout.html', context)


def seach (request):
    name_city = request.GET['city']
    print (name_city)
    city = City.objects.get(name_City = name_city)
    throughs = Through.objects.filter(city = city.id_City)
    tours =[]
    for through in throughs:
        tour = Tour.objects.get(name_Tour = through.tour)
        tours.append(tour)
    content = {
        'tours':tours
    }
    return render(request, 'seach.html', content)



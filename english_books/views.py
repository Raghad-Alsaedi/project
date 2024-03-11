from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Items,ItemDetails,Cart
#from .forms import CreateUserForm,LoginUserForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.

def show_english_books(requset):
    template=loader.get_template('show_english_books.html')
    book=ItemDetails.objects.select_related('itemsid')
    print(book.query)
    return HttpResponse(template.render({'book':book,'requset':requset}))

def add_to_cart_(requset,id):
     currentuser=requset.user
     discount=2
     state=False
     book=ItemDetails.objects.select_related('itemsid').filter(id=id)
     for item in book:
           net=item.total-discount
     cart = Cart(
      Id_product=item.id,
      Id_user=currentuser.id,
      price=item.price,
      qty=item.qty,
      tax=item.tax,
      total=item.total,
      discount=discount,
      net=net,
      status=state
)
     currentuser=requset.user.id
     count=Cart.objects.filter(Id_user=currentuser).count()
     print(count)
     cart.save()
     requset.session['countcart']=count
     return redirect("/show_english_books") 


def details_(requset,id):
    template=loader.get_template('details.html')
    currentuser=requset.user
    print(currentuser.id)
    book=ItemDetails.objects.select_related('itemsid').filter(id=id)
    context={
        'book':book,
        'requset':requset
    }
    return HttpResponse(template.render(context))

@login_required(login_url='/auth_login/')
def checkout(request):
       template=loader.get_template('checkout.html')
       current_user = request.user.id
       cart=Cart.objects.all().filter(Id_user=current_user).first()
       product=Items.objects.get(id=cart.Id_product)
       context={
            'cart':cart,
            'productname':product,
            'request':request
       }
       return HttpResponse(template.render(context=context)) 

from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    quantity = request.POST.get('quantity')
    override = request.POST.get('override')

    
    cart.add(product=product,
                 quantity=quantity,
                 override_quantity=override)
        
   
    return redirect('cart:cart_detail')



@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        product = item['product']  # Obtenemos el producto
        item['update_quantity_form'] = CartAddProductForm(product=product, initial={
            'quantity': item['quantity'],
            'override': True
        })
    return render(request, 'cart/detail.html', {'cart': cart})


# Create your views here.

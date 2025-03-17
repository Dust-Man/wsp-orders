from django.shortcuts import get_object_or_404, render
from cart.cart import Cart
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.http import JsonResponse

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    # Obtener el término de búsqueda
    search_query = request.GET.get('q', '')

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    # Si es una solicitud AJAX, devolver JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        products_data = [
            {
                'name': product.name,
                'price': str(product.price),
                'image': product.image.url if product.image else '',
                'url': product.get_absolute_url(),
                'prefix': product.prefix,
                'description':product.description,
            }
            for product in products
        ]
        return JsonResponse({'products': products_data})

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form =  CartAddProductForm(product=product) 
   
    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})
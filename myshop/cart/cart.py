from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Add a product to the cart or update its quantity."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': str(Decimal('0')),
                'price': str(product.price),
                'prefix': str(product.prefix)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = str(quantity)
        else:
            current_quantity = Decimal(self.cart[product_id]['quantity'])
            new_quantity = current_quantity + Decimal(quantity)
            self.cart[product_id]['quantity'] = str(new_quantity)

        self.save()

    def save(self):
        """Mark the session as modified to ensure it gets saved."""
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and retrieve the products from the database."""
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['quantity'] = Decimal(item['quantity'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return len(self.cart)

    def get_total_price(self):
        """Calculate total price of the cart."""
        return sum(
            Decimal(item['price']) * Decimal(item['quantity'])
            for item in self.cart.values()
        )

    def clear(self):
        """Remove cart from session."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

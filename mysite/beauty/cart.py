from beauty.models import Product

class Cart():
    def __init__(self, request): 
        self.session = request.session
       
    
        cart = self.session.get('session_key')
       
       
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
       
       
        self.cart = cart


    def add(self, product, quantity):


        product_id = str(product.id)
        product_qty = (quantity)
        
        if product_id in self.cart:
            pass
        else:
           
            self.cart[product_id] = int(product_qty)
        self.session.modified = True 
   
    def __len__(self): 
        return len(self.cart)
   

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)


        return products
   
    def get_quants(self):
        quantities = self.cart
        return quantities
   
    def update(self, product, quantity): #coming from the views post
        product_id = str(product.id)  #{'4':3}
        product_qty = int(quantity) #Converts product ID to string and quantity to int for consistent storage
        # Get cart
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty #call ourcart and pass what we want to update in[]
        self.session.modified = True
        thing = self.cart #Marks the session as modified and returns the updated cart.
        return thing 

    
    def delete(self, product):
        product_id = str(product) #{'4':3,'2':1}
        #delete from dic/cart
        if product_id in self.cart: #Removes the product from the cart if it exists.
            del self.cart[product_id]
       
        self.session.modified = True   
     
    def cart_total(self):

       product_ids = self.cart.keys()

       products = Product.objects.filter(id__in=product_ids)

       quantities = self.cart

       total = 0

       for product in products:

        product_id = str(product.id)

        if product_id in quantities:

            qty = quantities[product_id]

            total += product.price * qty

        return total

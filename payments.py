import os
import dotenv
import stripe

#configuracion del entorno
dotenv.load_dotenv()
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

stripe.api_key = STRIPE_SECRET_KEY

# Crear un método de pago

def create_payment_method() -> str:
    try:
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "token": "tok_visa",}
        )
        print("¡Éxito! Aquí está el ID de tu método de pago:", payment_method.id)
        return payment_method.id
    except stripe.error.CardError as e:
        print("Error", e.user_message)

# Crear un pago

def create_payment(client_id: str, payment_method_id: str, product_id: str, amount: int, currency: str):
    try:
        payment = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            customer=client_id,
            payment_method=payment_method_id,
            payment_method_types=["card"],
            confirm=True,
            metadata={"product_id": product_id},
        )

        print("¡Éxito! Aquí está el ID de tu pago:", payment.id)
    except stripe.error.CardError as e:
        print("Error", e.user_message)
    except stripe.error.CardError as e:
        print("Error", e.user_message)

# Crear un usuario
def create_user(name, email):
        try:
            client = stripe.Customer.create(
                name=name,
                email=email,
            )
            print("¡Éxito! Aquí está el ID de tu usuario:",name, client.id)
            return client.id
        except stripe.error.CardError as e:
            print("Error", e.user_message)

# Añadir un método de pago a un usuario
        
def add_payment_method_to_user(client_id, payment_method_id):
            try:
                stripe.PaymentMethod.attach(
                    payment_method_id,
                    customer=client_id,
                )
                print("¡Éxito! Método de pago añadido a usuario")
            except stripe.error.CardError as e:
                print("Error", e.user_message)

# obtener productos

def get_product():   

    products = stripe.Product.list(limit=1)
    return products["data"][0]["id"]  

def get_product_price(product_id):
    price = stripe.Price.list(product=product_id, limit=1)

    price_id = price["data"][0]["id"]
    amount = price["data"][0]["unit_amount"]
    currency = price["data"][0]["currency"]

    return price_id, amount, currency

        

        
client_id = create_user("paco", "pacofb70@gmail.com")

paiment_method_id = create_payment_method()

add_payment_method_to_user( client_id, paiment_method_id)

product_id = get_product()

price_id, amount, currency = get_product_price(product_id)

create_payment(client_id, paiment_method_id, product_id, amount, currency)
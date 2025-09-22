import json

import stripe

from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from stripe_api import models

MAIN_COUNTRIES = [
    # North America
    "US",
    "CA",
    "MX",
    # Europe (major economies + EU core)
    "GB",
    "DE",
    "FR",
    "IT",
    "ES",
    "NL",
    "SE",
    "CH",
    "BE",
    "IE",
    "AT",
    "DK",
    "NO",
    # Asia-Pacific
    "JP",
    "CN",
    "IN",
    "KR",
    "SG",
    "AU",
    "NZ",
    "HK",
    # Latin America (biggest online commerce markets)
    "BR",
    "AR",
    "CL",
    "CO",
    "PE",
    # Middle East
    "AE",
    "SA",
    "IL",
    "TR",
    "QA",
    # Africa (mainly South Africa)
    "ZA",
]


@method_decorator(csrf_exempt, name="dispatch")
class Api(View):

    def post(self, request):

        # Get json data
        request_json = json.loads(request.body)

        # Get weg page and user
        web_page = request_json["url"]
        web_page_success = request_json.get("url_success", web_page + "?done=true")
        username = request_json["user"]
        currency = request_json.get("currency", "usd")
        collect_phone = request_json.get("collect_phone", False)
        collect_billing_address = request_json.get("collect_billing_address", False)
        print(">>> currency", currency)
        user = models.Credentilas.objects.filter(username=username).first()

        # Set api key
        stripe.api_key = user.secret_key

        # Loop for each product
        buy_itemas = []
        for product_name, product_data in request_json["products"].items():

            # Create products
            stripe_product = stripe.Product.create(
                name=product_name,
                description=product_data["description"],
                images=[product_data["image_url"]],
            )

            # Create product price
            stripe_price = stripe.Price.create(
                unit_amount=int(product_data["price"] * 100),
                currency=currency,
                product=stripe_product["id"],
                tax_behavior="exclusive",
            )

            # Save current product
            buy_itemas.append(
                {"price": stripe_price["id"], "quantity": product_data["amount"]}
            )

        try:
            # Create payments page
            
            stripe_checkout_data = {
                "line_items": buy_itemas,
                "mode": "payment",
                "success_url": web_page_success,
                "cancel_url": web_page,
                "customer_email": request_json.get("email"),
                "customer_creation": "always",  # ensures a customer object is created,
                "client_reference_id": username,
            }
            
            if collect_phone:
                stripe_checkout_data["phone_number_collection"] = {"enabled": True}
            
            if collect_billing_address:
                stripe_checkout_data["shipping_address_collection"] = {
                    "allowed_countries": MAIN_COUNTRIES
                }
                stripe_checkout_data["billing_address_collection"] = "required"
            
            checkout_session = stripe.checkout.Session.create(**stripe_checkout_data)
        except Exception as e:
            # Redirect to page with error message
            return JsonResponse({"error": str(e)})
        else:
            # Redirect to payments page
            return JsonResponse({"stripe_url": checkout_session.url})

"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product
from bangazonreports.views import Connection


def expensive_product_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    *
                FROM
                    bangazonapi_product
                WHERE price>1000
            """)

            dataset = db_cursor.fetchall()

            expensive_products = []

            for row in dataset:
                # Crete a Game instance and set its properties
                product = Product()
                product.id = row["id"]
                product.name = row["name"]
                product.description = row["description"]
                product.price = row["price"]
                product.location = row["location"]
                product.quantity = row["quantity"]

                # oid = row["order_id"]

                expensive_products.append(product)


        # Get only the values from the dictionary and create a list from them
        # list_of_completed_orders = dataset.values()

        # Specify the Django template and provide data context
        template = 'products/list_of_expensive_products.html'
        context = {
            'expensiveproduct_list': expensive_products
        }

        return render(request, template, context)

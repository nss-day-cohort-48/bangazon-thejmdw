"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection


def completed_order_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    o.id as order_id,
                    pt.merchant_name,
                    u.first_name || ' ' || u.last_name AS full_name,
                    SUM(p.price) as total
                FROM
                    bangazonapi_order o
                JOIN
                    bangazonapi_customer c ON c.id = o.customer_id
                JOIN
                    auth_user u ON c.user_id = u.id
                JOIN
                    bangazonapi_payment pt ON pt.id = o.payment_type_id
                JOIN
                    bangazonapi_orderproduct op ON op.order_id = o.id
                JOIN
                    bangazonapi_product p ON p.id = op.product_id
                GROUP BY order_id
            """)

            dataset = db_cursor.fetchall()

            completed_orders = []

            for row in dataset:
                # Crete a Game instance and set its properties
                order = Order()
                order.id = row["order_id"]
                order.customer_name = row["full_name"]
                order.total = row["total"]
                order.payment = row["merchant_name"]

                # oid = row["order_id"]

                completed_orders.append(order)


        # Get only the values from the dictionary and create a list from them
        # list_of_completed_orders = dataset.values()

        # Specify the Django template and provide data context
        template = 'orders/list_of_completed_orders.html'
        context = {
            'completedorder_list': completed_orders
        }

        return render(request, template, context)

"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Order
from bangazonreports.views import Connection


def incomplete_order_list(request):
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
                    u.first_name || ' ' || u.last_name AS full_name,
                    SUM(p.price) as total
                FROM
                    bangazonapi_order o
                JOIN
                    bangazonapi_customer c ON c.id = o.customer_id
                JOIN
                    auth_user u ON c.user_id = u.id
                JOIN
                    bangazonapi_orderproduct op ON op.order_id = o.id
                JOIN
                    bangazonapi_product p ON p.id = op.product_id
                WHERE
                    o.payment_type_id IS NULL
                GROUP BY order_id
            """)

            dataset = db_cursor.fetchall()

            incomplete_orders = []

            for row in dataset:
                # Crete a Game instance and set its properties
                order = Order()
                order.id = row["order_id"]
                order.customer_name = row["full_name"]
                order.total = row["total"]

                # oid = row["order_id"]

                incomplete_orders.append(order)


        # Get only the values from the dictionary and create a list from them
        # list_of_completed_orders = dataset.values()

        # Specify the Django template and provide data context
        template = 'orders/list_of_incomplete_orders.html'
        context = {
            'incompleteorder_list': incomplete_orders
        }

        return render(request, template, context)

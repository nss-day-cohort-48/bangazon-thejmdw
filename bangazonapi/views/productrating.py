"""
   Author: Daniel Krusch
   Purpose: To convert product rating data to json
   Methods: GET, POST
"""

"""View module for handling requests about product Ratings"""
from bangazonapi.models.customer import Customer
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import ProductRating, Product, Customer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProductRatingSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product rating"""
    class Meta:
        model = ProductRating
        url = serializers.HyperlinkedIdentityField(
            view_name='productrating',
            lookup_field='id'
        )
        fields = ('id', 'url', 'customer', 'product', 'rating')


class ProductRatings(ViewSet):
    """Ratings for products"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product rating instance
        """
        new_product_rating = ProductRating()

        new_product_rating.customer = Customer.objects.get(user=request.auth.user)
        new_product_rating.product = Product.objects.get(id=request.data["product"])
        new_product_rating.rating = request.data["rating"]
        new_product_rating.save()

        serializer = ProductRatingSerializer(new_product_rating, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single rating"""
        try:
            rating = ProductRating.objects.get(pk=pk)
            serializer = ProductRatingSerializer(rating, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to Productrating resource"""
        product_rating = ProductRating.objects.all()

        # Support filtering Productratings by area id
        # name = self.request.query_params.get('name', None)
        # if name is not None:
        #     ProductRatings = ProductRatings.filter(name=name)

        serializer = ProductRatingSerializer(
            product_rating, many=True, context={'request': request})
        return Response(serializer.data)

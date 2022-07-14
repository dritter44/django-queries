import django.db.models
from audioop import avg
from .models import Product
from django.db.models import Avg, Max
from django.db.models.functions import Length

class ProductCrud:
    @classmethod
    def get_all_products(cls):
        return Product.objects.all()

    @classmethod
    def find_by_model(cls,input):
        return Product.objects.get(model=input)

    #finds the last record inserted in the db
    @classmethod
    def last_record(cls):
        return Product.objects.last()

    #finds a list of products by rating
    @classmethod
    def by_rating(cls,input):
        return Product.objects.filter(rating=input)

    #finds products within a rating range
    @classmethod
    def by_rating_range(cls,input1, input2):
        return Product.objects.filter(rating__range=(input1,input2))

    #finds products by rating and color value
    @classmethod
    def by_rating_and_color(cls,rating_for, color_value_for):
        return Product.objects.filter(rating = rating_for, color=color_value_for)

    #finds products by rating or color value
    @classmethod
    def by_rating_or_color(cls,rating_for, color_value_for):
        return Product.objects.filter(rating=rating_for) | Product.objects.filter(color = color_value_for)

    #finds products where color has no value
    #ask questions on this one
    @classmethod
    def no_color_count(cls):
        return Product.objects.filter(color__isnull=True).count()

    #"""returns products below a price or above a rating"""
    @classmethod
    def below_price_or_above_rating(cls, targ_price, targ_rating):
        return Product.objects.filter(price_cents__lt=targ_price) | Product.objects.filter(rating__gt=targ_rating)

    #"""returns products ordered by category alphabetical and decending price"""
    @classmethod
    def ordered_by_category_alphabetical_order_and_then_price_decending(cls):
        return Product.objects.order_by('category','-price_cents')

    #"""returns products made by manufacturers with names containing an input string"""
    @classmethod
    def products_by_manufacturer_with_name_like(cls,input):
        return Product.objects.filter(manufacturer__icontains=input)

    #returns a list of manufacturer names that match query
    @classmethod
    def manufacturer_names_for_query(cls,input):
        data = Product.objects.filter(manufacturer__icontains=input)
        return data.values_list('manufacturer', flat = True)

    #returns products that are not in a category
    @classmethod
    def not_in_a_category(cls,input):
        return Product.objects.exclude(category=input)

    #returns products that are not in a category up to a limit
    @classmethod
    def limited_not_in_a_category(cls,input1,input2):
        return Product.objects.exclude(category=input1)[:input2]

    #returns an array of manufacturers for a category
    @classmethod
    def category_manufacturers(cls,input):
        data = Product.objects.filter(category=input)
        return data.values_list('manufacturer',flat=True)

    #returns the average
    @classmethod
    def average_category_rating(cls, input):
        return Product.objects.filter(category=input).aggregate(Avg('rating'))

    #returns the highest price
    @classmethod
    def greatest_price(cls):
        return Product.objects.all().aggregate(Max('price_cents'))

    #returns the id of the product with the longest model name
    @classmethod
    def longest_model_name(cls):
        data = Product.objects.alias(len_of_name=Length('model')).order_by('-len_of_name')
        return data[0].id

    #returns products ordered by the length of their model name
    @classmethod
    def ordered_by_model_length(cls):
        return Product.objects.alias(len_of_name=Length('model')).order_by('len_of_name')



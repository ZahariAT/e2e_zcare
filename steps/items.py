from behave import given, when, then

from utilities.client import Client
from utilities.user import User


# Given STEPS

@given('at least {quantity:d} of "{product}"')
def given_at_least_quantity_of_product(context, quantity, product):
    try:
        products = context.root_user.search_items(product)
    except Exception:
        raise ValueError('Product not available on server!')

    product = products[0]
    quantity = quantity + product.quantity
    product.update(
        {'quantity': quantity, 'name': product.name, 'price': product.price, 'category': product.category.id})


# When STEPS

@when('the user searches for "{product}"')
def when_user_searches_for_product(context, product):
    context.relevant_products = context.test_user.search_items(product)


@when('the user buys {quantity:d} of "{product}"')
def when_user_buys_product(context, quantity, product):
    product = [p for p in context.relevant_products if p.name == product][0]
    context.initial_product_quantity = product.quantity
    context.test_user.buy_item(product, quantity)
    context.product = product
    context.quantity = quantity


# Then STEPS

@then('"{product}" should be found')
def then_product_should_be_found(context, product):
    assert context.relevant_products, f'Product {product} not found!'
    assert product in [p.name for p in context.relevant_products]


@then('the user should find {quantity:d} order in his order history')
def then_user_should_have_an_order_in_order_history(context, quantity):
    length_of_history = len(context.test_user.order_history())
    assert length_of_history == quantity, f'Expected to find {quantity} but found {length_of_history}!'


@then('the quantity of the product should be with {quantity:d} less')
def then_product_quantity_should_be_less(context, quantity):
    assert context.product.quantity == context.initial_product_quantity - quantity, f'Expected to find quantity to be with {quantity} less!'

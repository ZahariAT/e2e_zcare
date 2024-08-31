import os

from behave import fixture, use_fixture
# from selenium import webdriver
from utilities.user import User
from utilities.client import Client


# @fixture
# def browser(context):
#     options = webdriver.ChromeOptions()
#     # options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--no-sandbox')
#     options.add_argument('--disable-dev-shm-usage')
#
#     context.browser = webdriver.Chrome(options=options)
#     yield
#     context.browser.quit()


@fixture
def root_user(context):
    context.root_user = User(Client(context.config.userdata.get('service_url')),
                             int(context.config.userdata.get('access_token_timeout')))
    context.root_user.api_login(context.config.userdata.get('admin_username'),
                                context.config.userdata.get('admin_password'))


def before_all(context):
    # use_fixture(browser, context)
    use_fixture(root_user, context)

# def before_scenario(context, scenario):
#     use_fixture(browser, context)

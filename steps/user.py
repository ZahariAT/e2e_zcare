import uuid
import re
import requests

from behave import given, when, then

from utilities.user import User
from utilities.client import Client
from utilities.mail import check_email_arrived, decode_body

# Given STEPS

@given('a new user')
def given_new_user(context):
    name = context.config.userdata.get('email_user').split('@')[0] + '+' + str(uuid.uuid4())[:4]
    context.email = name + '@' + context.config.userdata.get('email_user').split('@')[1]
    context.password = 'strongpassword123'
    context.data = {
        'email': context.email,
        'name': 'Test User',
        'password': context.password,
        'password2': context.password,
    }
    context.test_user = User(Client(context.config.userdata.get('service_url')),
                             int(context.config.userdata.get('access_token_timeout')))


@given('an anonymous user')
def given_anonymous_user(context):
    context.test_user = User(Client(context.config.userdata.get('service_url')),
                             int(context.config.userdata.get('access_token_timeout')))



# WHEN STEPS

@when('the user follows the activation link')
def when_user_follows_activation_link(context):
    activation_link = re.search("(?P<url>https?://[^\s]+)", context.email_body).group("url")
    context.activation_response = requests.get(activation_link)


@when('the user registers')
def when_user_registers(context):
    context.test_user.register(**context.data)


@when('the user logs in')
def when_user_logs_in(context):
    context.test_user.api_login(context.email, context.password)


# THEN STEPS

@then('the user should receive an email with the subject "{subject}" within {timeout:d} seconds')
def then_user_should_receive_email(context, subject, timeout):
    context.email_message = check_email_arrived(
        username=context.config.userdata.get('email_user'),
        password=context.config.userdata.get('email_password'),
        subject=subject,
        recipient_email=context.email,
        timeout=timeout,
    )
    assert context.email_message is not None, f"No email with subject '{subject}' received within {timeout} seconds"


@then('the email should contain "{content}"')
def then_email_should_contain_content(context, content):
    assert context.email_message is not None, "No email was received to check the content"

    context.email_body = decode_body(context.email_message)

    assert content in context.email_body, f"Expected content '{content}' not found in email body"


@then('the user should be activated')
def then_user_is_activated(context):
    assert context.activation_response.status_code == 200, f'Expected status code 200 but got {context.activation_response.status_code}'

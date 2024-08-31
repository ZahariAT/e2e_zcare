Feature: User Registration and Email Verification

  Scenario: Register a new user and buy product as them
    Given a new user
    And at least 5 of "Analgin"

    When the user registers
    Then the user should receive an email with the subject "Activate Your Account" within 60 seconds
    And the email should contain "Please click the activation link"

    When the user follows the activation link
    Then the user should be activated

    When the user logs in
    And the user searches for "Analgin"
    Then "Analgin" should be found

    When the user buys 5 of "Analgin"
    Then the user should find 1 order in his order history

  Scenario: Buy product as anonymous user
    Given an anonymous user
    And at least 5 of "Analgin"

    When the user searches for "Analgin"
    Then "Analgin" should be found

    When the user buys 5 of "Analgin"
    Then the quantity of the product should be with 5 less

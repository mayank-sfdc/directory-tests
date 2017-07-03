Feature: Trade Profile


    @ED-1659
    @registration
    Scenario Outline: Supplier should receive a verification email after successful registration - export status is "<current>"
      Given "Peter Alder" is an unauthenticated supplier

      When "Peter Alder" randomly selects an active company without a Directory Profile identified by an alias "Company X"
      And "Peter Alder" confirms that "Company X" is the correct one
      And "Peter Alder" confirms that the export status of "Company X" is "<current>"
      And "Peter Alder" creates a SSO/great.gov.uk account for "Company X" using valid credentials

      Then "Peter Alder" should be told about the verification email
      And "Peter Alder" should receive an email verification msg entitled "Your great.gov.uk account: Please Confirm Your E-mail Address"

      Examples:
        | current                        |
        | Yes, in the last year          |
        | Yes, 1 to 2 years ago          |
        | Yes, but more than 2 years ago |
        | No, but we are preparing to    |


    @ED-1692
    @verification
    @email
    Scenario: Unauthenticated Suppliers should be able to verify their email address via confirmation link sent in an email
      Given "Annette Geissinger" is an unauthenticated supplier
      And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" received the email verification message with the email confirmation link

      When "Annette Geissinger" decides to confirm her email address by using the email confirmation link
      And "Annette Geissinger" confirms the email address

      Then "Annette Geissinger" should be prompted to build and improve your Directory Profile


  @ED-1757
  @verification
  @login
  Scenario: Suppliers without verified email should be told to verify the email address first before being able to log in
    Given "Annette Geissinger" is an unauthenticated supplier
    And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"

    When "Annette Geissinger" attempts to sign in to Find a Buyer profile

    Then "Annette Geissinger" should be told that she needs to verify her email address first


    @ED-1716
    @profile
    Scenario: Supplier should be able to build the Directory Profile once the email address is confirmed
      Given "Annette Geissinger" is an unauthenticated supplier
      And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" confirmed her email address

      When "Annette Geissinger" provides valid details of selected company
      And "Annette Geissinger" selects random sector the company is interested in working in
      And "Annette Geissinger" provides her full name which will be used to sent the verification letter
      And "Annette Geissinger" confirms the details which will be used to sent the verification letter

      Then "Annette Geissinger" should be on edit Company's Directory Profile page
      And "Annette Geissinger" should be told that her company has no description


    @ED-1722
    @verification
    @letter
    Scenario: Supplier should be able to verify company using code sent in the verification letter
      Given "Annette Geissinger" is an unauthenticated supplier
      And "Annette Geissinger" created a SSO/great.gov.uk account associated with randomly selected company "Company X"
      And "Annette Geissinger" confirmed her email address
      And "Annette Geissinger" built the company profile
      And "Annette Geissinger" set the company description

      When "Annette Geissinger" verifies the company with the verification code from the letter sent after Directory Profile was created

      Then "Annette Geissinger" should be on edit Company's Directory Profile page
      And "Annette Geissinger" should be told that her company is published


    @ED-1727
    @publish
    @FAS
    Scenario: Once verified Company's Directory Profile should be published on FAS
      Given "Peter Alder" has created and verified profile for randomly selected company "Y"

      When "Peter Alder" decides to view published Directory Profile

      Then "Peter Alder" should be on FAS Directory Profile page of company "Y"


    @ED-1740
    @registration
    Scenario: Some suppliers are not appropriate to feature in the Find a Buyer service
      Given "Peter Alder" is an unauthenticated supplier

      When "Peter Alder" randomly selects an active company without a Directory Profile identified by an alias "Company X"
      And "Peter Alder" confirms that "Company X" is the correct one
      And "Peter Alder" decides that the export status of his company is "No, we are not planning to sell overseas"

      Then "Peter Alder" should be told that his company is currently not appropriate to feature in the FAB service


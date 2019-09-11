@home-page
Feature: Domestic - Home Page

  Background:
    Given basic authentication is done for "Domestic - Home" page

  @ED-2366
  @sections
  Scenario: Any Exporter should see the "Beta bar, Hero, EU Exit enquiries banner, Advice, Services, Case Studies, Business is Great, Error Reporting" sections on the home page
      Given "Robert" visits the "Domestic - Home" page
      Then "Robert" should see following sections
        | Sections                 |
        | Header                   |
        | SSO links - logged out   |
        | Beta bar                 |
        | Hero                     |
        | EU Exit enquiries banner |
        | Export Community         |
        | Advice                   |
        | Services                 |
        | Case Studies             |
        | Business is Great        |
        | Error Reporting          |
        | Footer                   |


  @ED-3014
  @video
  Scenario: Any Exporter should be able to play promotional video on the Home page
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to watch "6" seconds of the promotional video

    Then "Robert" should be able to watch at least first "5" seconds of the promotional video


  @ED-3014
  @video
  Scenario: Any Exporter should be able to close the window with promotional video on the Home page
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to watch "6" seconds of the promotional video
    And "Robert" closes the window with promotional video

    Then "Robert" should not see the window with promotional video


  @ED-3083
  @decommissioned
  @language-selector
  Scenario: Visitor should be able to open and close the language selector on "Domestic - Home" page
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" opens up the language selector
    Then "Robert" should see the language selector

    When "Robert" closes the language selector
    Then "Robert" should not see the language selector


  @ED-3083
  @decommissioned
  @language-selector
  @accessibility
  Scenario: Keyboard users should be able to open and close the language selector using just the keyboard on "Domestic - Home" page
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" opens up the language selector using his keyboard
    Then "Robert" should see the language selector

    When "Robert" closes the language selector using his keyboard
    Then "Robert" should not see the language selector


  @ED-3083
  @decommissioned
  @language-selector
  Scenario Outline: Visitors should be able to view go to International page after changing language to "<preferred_language>" on the Domestic Home Page
    Given "Robert" visits the "Domestic - Home" page

    When "Robert" decides to view the page in "<preferred_language>"

    Then "Robert" should be on the "International - Landing" page
    # ATM International page doesn't support translations
    # And "Robert" should see the page in "<preferred_language>"

    Examples: available languages
      | preferred_language |
      | English            |
      | 简体中文            |
      | Deutsch            |
      | 日本語              |
      | Español            |
      | Português          |
      | العربيّة            |
      | Français           |

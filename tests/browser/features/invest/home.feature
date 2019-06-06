@home-page
@no-sso-email-verification-required
Feature: Invest home page

  Background:
    Given basic authentication is done for "Invest - Home" page

  @dev-only
  @CMS-157
  Scenario: Visitors should be able to view "Invest home" page
    Given "Robert" visits the "Invest - home" page

    Then "Robert" should see following sections
      | Sections                     |
      | Header                       |
      | Breadcrumbs                  |
      | EU exit news banner          |
      | Benefits                     |
      | UK setup guides              |
      | Sectors                      |
      | High-Potential Opportunities |
      | How we help                  |
      | Contact us                   |
      | Error reporting              |
      | Footer                       |

  @stage-only
  @CMS-157
  Scenario: Visitors should be able to view "Invest home" page
    Given "Robert" visits the "Invest - home" page

    Then "Robert" should see following sections
      | Sections                     |
      | Header                       |
      | Breadcrumbs                  |
      | UK setup guides              |
      | Sectors                      |
      | High-Potential Opportunities |
      | How we help                  |
      | Contact us                   |
      | Error reporting              |
      | Footer                       |


  @CMS-157
  Scenario Outline: Overseas businesses should be able to learn more about "<selected>" UK Industry
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to find out out more about "Invest - <selected> - industry"

    Then "Robert" should be on the "Invest - <selected> - industry" page
    And "Robert" should see content specific to "Invest - <selected> - industry" page

    Examples: promoted industries
      | selected                 |
      | Automotive               |
      | Health and life sciences |
      | Technology               |


  @CMS-157
  Scenario: Overseas businesses should be able to also learn more about UK Industries other than the promoted ones
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to "see more industries"

    Then "Robert" should be on the "Invest - Industries" page


  @CMS-157
  Scenario: Overseas businesses should be able to learn how to set up in the UK
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to "Get started in the UK"

    Then "Robert" should be on the "International - How to set up in the UK" page


  @ISD
  Scenario: Overseas businesses should be able to learn how to find a UK specialist
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to "Get help to set up or expand in the UK"

    Then "Robert" should be on the "Find a Supplier - UK support directory" page


  @HPO
  Scenario Outline: Overseas businesses should be able to learn about "<selected>" High-Potential Opportunities
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to find out more about "<selected>"

    Then "Robert" should be on the "Invest - <selected> - hpo" page
    And "Robert" should see content specific to "Invest - <selected> - hpo" page

    Examples: UK Setup Guides
      | selected                 |
      | Advanced food production |
      | Lightweight structures   |
      | Rail infrastructure      |

@home-page
@no-sso-email-verification-required
Feature: Invest - landing page

  Background:
    Given basic authentication is done for "International - Landing" page

  @dev-only
  @CMS-157
  Scenario: Visitors should be able to view "Invest home" page
    Given "Robert" visits the "Invest - home" page

    Then "Robert" should see following sections
      | Sections                     |
      | Header                       |
      | Hero                         |
      | Breadcrumbs                  |
      | Benefits                     |
      | Sectors                      |
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
      | Hero                         |
      | Breadcrumbs                  |
      | Benefits                     |
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

    Then "Robert" should be on the "International - <selected> - industry" page

    @dev-only
    Examples: promoted industries available via International site
      | selected                      |
      | Financial services            |
      | Engineering and manufacturing |
      | Technology                    |

    @stage-only
    Examples: promoted industries available via International site
      | selected                            |
      | Financial and professional services |
      | Engineering and manufacturing       |
      | Technology                          |


  @CMS-157
  Scenario: Overseas businesses should be able to also learn more about UK Industries other than the promoted ones
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to "see more industries"

    Then "Robert" should be on the "International - Industries" page


  @CMS-157
  Scenario: Overseas businesses should be able to learn how to set up in the UK
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to find out more about "UK setup guide"

    Then "Robert" should be on the "International - How to set up in the UK" page


  @HPO
  @stage-only
  Scenario Outline: Overseas businesses should be able to learn about "<selected>" High-Potential Opportunities
    Given "Robert" visits the "Invest - home" page

    When "Robert" decides to find out more about "<selected>"

    Then "Robert" should be on the "Invest - <selected> - hpo" page
    And "Robert" should see content specific to "Invest - <selected> - hpo" page

    Examples: UK Setup Guides
      | selected                          |
      | High productivity food production |
      | Lightweight structures            |
      | Rail infrastructure               |
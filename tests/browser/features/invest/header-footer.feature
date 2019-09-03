@header-footer
Feature: Header-Footer

  Background:
    Given basic authentication is done for "International - Landing" page
    Given basic authentication is done for "Invest - Home" page

  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should see correct UK Government logo, with Union Jack, in the page header and footer on "<selected>" page
    Given "Robert" visits the "<selected>" page

    Then "Robert" should be on the "<expected>" page
    And "Robert" should see correct UK Government logo in page "header"
    And "Robert" should see correct UK Government logo in page "footer"
    And "Robert" should see the correct favicon

    @dev-only
    Examples:
      | selected                | expected                                |
      | Invest - Home           | Invest - Home                           |
      | Invest - Contact Us     | Invest - Contact Us                     |
      | Invest - UK Setup Guide | International - How to set up in the UK |

    @stage-only
    Examples:
      | selected                | expected                                |
      | Invest - Home           | Invest - Home                           |
      | Invest - Contact Us     | Invest - Contact Us                     |
      | Invest - UK Setup Guide | International - How to set up in the UK |

    @uat-only
    Examples:
      | selected                | expected                                |
      | Invest - Home           | Invest - Home                           |
      | Invest - Contact Us     | Invest - Contact Us                     |
      | Invest - UK Setup Guide | International - How to set up in the UK |


  @CMS-158
  @header
  @footer
  @home-page
  @<specific>
  Scenario Outline: Visitors should be able to get to the "<specific>" page via "<section>" link
    Given "Robert" visits the "Invest - Home" page

    When "Robert" decides to use "<specific>" link from page "Invest - <section>"

    Then "Robert" should be on the "<expected>" page

    Examples:
      | specific           | section | expected                   |
      | Invest             | header  | Invest - Home              |
      | Find a UK Supplier | header  | Find a Supplier - Home     |


  @CMS-158
  @logo
  @header
  @footer
  Scenario Outline: Visitors should be able to get to the International home page from "Invest - <selected>" page by using UK Government logo in the page header
    Given "Robert" visits the "Invest - <selected>" page

    When "Robert" decides to click on "Invest in Great logo"

    Then "Robert" should be on the "International - Landing" page

    Examples:
      | selected   |
      | Home       |
      | Contact Us |

@markets
@allure.suite:Domestic
Feature: Domestic - Market guides

  Background:
    Given basic authentication is done for "Domestic - Home" page


  Scenario: Visitors should be able to view all available markets
    Given "Joel" visits the "Domestic - Home" page

    When "Joel" decides to find out more about "Markets"

    Then "Joel" should be on the "Domestic - markets listing" page


  Scenario: Visitors should be able to view all available markets
    Given "Joel" visits the "Domestic - Markets listing" page

    When "Joel" selects a random market

    Then "Joel" should be on the "Domestic - Markets - Guide" page
    And "Joel" should see following sections
      | Sections                    |
      | Header                      |
      | Hero                        |
      | Breadcrumbs                 |
      | Description                 |
      | Opportunities for exporters |
      | Doing business in           |
      | Next steps                  |
      | Error Reporting             |
      | Footer                      |


  Scenario Outline: Visitors which decided to "<follow up>" after they read about random market should get to "<expected>" page
    Given "Joel" is on randomly selected Market page

    When "Joel" decides to "<follow up>"

    Then "Joel" should be on the "Domestic - <expected>" page

    Examples: next step
      | follow up                                    | expected          |
      | Read more advice about doing business abroad | Advice landing    |
      | Get in touch with one of our trade advisers  | New Office Finder |


  @stage-only
  @check-duties-and-customs
  Scenario Outline: Visitors which decided to "<follow up>" after they read about random market should get to "<expected>" page
    Given "Joel" visits the "Domestic - <country> - guide" page

    When "Joel" decides to "Check duties and customs procedures for exporting goods"

    Then "Joel" should be on the "Check duties and customs - Search product code" page

    Examples: next step
      | country |
      | Brazil  |
      | Germany |
      | Italy   |
      | Japan   |
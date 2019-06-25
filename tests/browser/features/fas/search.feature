@search
Feature: Trade - Search

  Background:
    Given basic authentication is done for "Find a Supplier - Home" page

  @bug
  @TT-1512
  @fixed
  Scenario: Buyers should be able to find UK suppliers using arbitrary search term
    Given "Robert" visits the "Find a Supplier - Home" page

    When "Robert" searches for companies using "food" keyword

    Then "Robert" should be on the "Find a Supplier - Search results" page
    And "Robert" should see following sections
      | Sections        |
      | Header          |
      | Search form     |
      | Filters         |
      | Results         |
      | Footer          |
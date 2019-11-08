@hpo
@stage-only
Feature: Invest - High Potential Opportunities

  Background:
    Given basic authentication is done for "International - Landing" page

  @TT-442
  Scenario Outline: Investors should be able to view "HPO - <selected>" page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO" page

    Then "Annette Geissinger" should see following sections
      | Sections               |
      | Header                 |
      | Hero                   |
      | Contact us             |
      | Proposition one        |
      | Opportunity list       |
      | Proposition two        |
      | Competitive advantages |
#      | Testimonial            |  # this is not present on these 2 pages
      | Case studies           |
      | Other opportunities    |
      | Error reporting        |
      | Footer                 |
    And "Annette Geissinger" should not see following section
      | section          |
      | Breadcrumbs      |

    Examples: HPO pages
      | selected                          |
      | High productivity food production |
      | Lightweight structures            |


  @TT-442
  Scenario Outline: Investors should be able to view "HPO - <selected>" page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO" page

    Then "Annette Geissinger" should see following sections
      | Sections               |
      | Header                 |
      | Hero                   |
      | Contact us             |
      | Proposition one        |
      | Opportunity list       |
      | Proposition two        |
      | Competitive advantages |
      | Testimonial            |
      | Case studies           |
      | Other opportunities    |
      | Error reporting        |
      | Footer                 |
    And "Annette Geissinger" should not see following section
      | section          |
      | Breadcrumbs      |

    Examples: HPO pages
      | selected               |
      | Rail infrastructure    |


  @TT-442
  @contact-us
  Scenario Outline: Investors should be able to reach "Contact us" page from "HPO - <selected>" page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO" page

    When "Annette Geissinger" decides to "Get in touch"

    Then "Annette Geissinger" should be on the "Invest - Contact us - Contact us" page
    And "Annette Geissinger" should see that "<selected> checkbox" in the form is "selected"
    And "Annette Geissinger" should see following sections
      | sections         |
      | Form             |
      | Error reporting  |

    Examples: HPO pages
      | selected                          |
      | High productivity food production |

    @full
    Examples: HPO pages
      | selected                 |
      | Lightweight structures   |
      | Rail infrastructure      |


  @TT-442
  @related-opportunities
  Scenario Outline: Investors should be able to view "Other investment opportunities" from "HPO - <selected>" page
    Given "Annette Geissinger" visits the "Invest - <selected> - HPO" page

    When "Annette Geissinger" decides to use "<specific> opportunity" link

    Then "Annette Geissinger" should be on the "Invest - <expected opportunity> - HPO" page

    Examples: HPO pages
      | selected                          | specific | expected opportunity              |
      | High productivity food production | first    | Lightweight structures            |
      | Lightweight structures            | second   | Rail infrastructure               |
      | Rail infrastructure               | first    | High productivity food production |

    @full
    Examples: HPO pages
      | selected                          | specific | expected opportunity              |
      | High productivity food production | second   | Rail infrastructure               |
      | Lightweight structures            | first    | High productivity food production |
      | Rail infrastructure               | second   | Lightweight structures            |


  @bug
  @TT-879
  @fixed
  @TT-443
  @bug
  @TT-1509
  @fixed
  @dev-only
  @captcha
  @contact-us
  Scenario Outline: Investors should be able to contact us via "<selected>" HPO page
    Given "Annette Geissinger" visits the "Invest - <selected> - Contact us" page

    When "Annette Geissinger" fills out and submits the form

    Then "Annette Geissinger" should be on the "Invest - Thank you for your enquiry - Contact us" page
    And "Annette Geissinger" should receive HPO enquiry confirmation email
    And HPO Agent should receive HPO enquiry email from "Annette Geissinger"
    And "Annette Geissinger" should see following sections
      | Sections         |
      | Confirmation     |
      | Documents        |
      | Error reporting  |

    Examples: HPO pages
      | selected                          |
      | High productivity food production |

    @full
    Examples: HPO pages
      | selected                 |
      | Lightweight structures   |
      | Rail infrastructure      |

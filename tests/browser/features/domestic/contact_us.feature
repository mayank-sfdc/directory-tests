@contact-us
Feature: Domestic - Contact us

  Background:
    Given basic authentication is done for "Domestic - Home" page

  @TT-758
  @enquirer-location
  Scenario: Enquirers should see all expected contact location options on the "Domestic - Contact us"
    Given "Robert" visits the "Domestic - Contact us" page

    Then "Robert" should be on the "Domestic - Contact us" page
    And "Robert" should see following form choices
      | radio elements |
      | The UK         |
      | Outside the UK |


  @TT-758
  @enquirer-location
  @domestic-enquiry-page
  Scenario: Domestic Enquirers should see all expected contact options on the "Domestic - What can we help you with?" page
    Given "Robert" visits the "Domestic - Contact us" page

    When "Robert" says that his business is in "The UK"

    Then "Robert" should be on the "Domestic - What can we help you with? - Domestic Contact us" page
    And "Robert" should see following form choices
      | radio elements                            |
      | Find your local trade office              |
      | Advice to export from the UK              |
      | Great.gov.uk account and services support |
      | UK Export Finance (UKEF)                  |
      | Brexit enquiries                          |
      | Events                                    |
      | Defence and Security Organisation (DSO)   |
      | Other                                     |


  @TT-363
  @office-finder
  Scenario: Domestic Enquirers should be able to get to the "New Office finder - Home" page
    Given "Robert" visits the "Domestic - Contact us" page

    When "Robert" says that his business is in "the UK"
    And "Robert" chooses "Find your local trade office" option

    Then "Robert" should be on the "Domestic - New Office Finder" page


  @TT-363
  @office-finder
  Scenario Outline: Domestic Enquirers should be able to get to find contact details for "<appropriate>" office in "<city>"
    Given "Robert" visits the "Domestic - New Office Finder" page

    When "Robert" searches for local trade office near "<post-code>"

    Then "Robert" should be on the "Domestic - New Office Finder - search results" page
    And "Robert" should see contact details for "<appropriate>" office in "<city>"

    Examples: postcodes and trade offices
      | post-code | appropriate                  | city        |
      | LL57 1ST  | Business Wales               | Sarn Mynach |
      | LE5 3BF   | DIT East Midlands            | Leicester   |

    @full
    Examples: postcodes and trade offices
      | post-code | appropriate                  | city        |
      | AL10 8EP  | DIT East of England          | Hatfield    |
      | SW1A 2AA  | DIT London                   | London      |
      | DH1 1SQ   | DIT North East               | Durham      |
      | M15 6PQ   | DIT North West               | Manchester  |
      | PO15 5DE  | DIT South East               | Fareham     |
      | BS1 4RL   | DIT South West               | Bristol     |
      | B3 2RT    | DIT West Midlands            | Birmingham  |
      | S70 2PS   | DIT Yorkshire and the Humber | Barnsley    |
      | BT2 8DN   | Invest NI                    | Belfast     |
      | G3 6AP    | Scottish Enterprise          | Glasgow     |


  @wip
  @TT-363
  @office-finder
  Scenario: Domestic Enquirers should be able to get to the NEW Office finder page
    Given "Robert" visits the "Domestic - New Office Finder" page

    When "Robert" found his local trade office by providing his company's postcode
    And "Robert" decides to "Contact the local trade office"

    Then "Robert" should be on the "Domestic - Short contact form (Office Finder)" page


  @wip
  @TT-363
  @captcha
  @dev-only
  @office-finder
  Scenario: Domestic Enquirers should be able to contact
    Given "Robert" got to the "Short contact-us form" page via "Find local trade office"

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Thank you for your enquiry" page
    And an email is submitted to "appropriate local office based on the postcode provided"


  @TT-758
  @exporting-from-the-UK
  Scenario: Domestic Enquirers should be able to get to the "Long (Export Advice Comment) - Contact us" form
    Given "Robert" visits the "Domestic - Contact us" page

    When "Robert" says that his business is in "the UK"
    And "Robert" chooses "Advice to export from the UK" option

    Then "Robert" should be on the "Domestic - Long (Export Advice Comment) - Contact us" page


  @TT-758
  @ita
  @captcha
  @dev-only
  @exporting-from-the-UK
  Scenario: Domestic Enquirers should be able to contact relevant ITA based on the postcode provided
    Given "Robert" got to the "Domestic - Long (Export Advice Comment)" page via "The UK -> Advice to export from the UK"

    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Domestic - Long (Personal details) - Contact us" page
    When "Robert" fills out and submits the form
    Then "Robert" should be on the "Domestic - Long (Business details) - Contact us" page
    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Domestic - Thank you for your enquiry" page
    And "Robert" should receive "Thank you for your enquiry" confirmation email
    # TODO check if this email is being actually sent
#    And an email is submitted to relevant "ITA" (based on the postcode provided)


  @TT-758
  @account-support
  Scenario: Domestic enquirers should see all expected help options on the "Great.gov.uk account and services support" page
    Given "Robert" got to the "Domestic - Great.gov.uk account and services support" page via "The UK -> Great.gov.uk account and services support"

    Then "Robert" should see following form choices
      | radio elements               |
      | Export opportunities service |
      | Your account on Great.gov.uk |
      | Other                        |


  @TT-758
  @exopps
  @account-support
  Scenario: Domestic enquirers should see all expected help options for "Export opportunities service"
    Given "Robert" got to the "Domestic - Export opportunities service" page via "The UK -> Great.gov.uk account and services support -> Export opportunities service"

    Then "Robert" should see following form choices
      | radio elements                                              |
      | I haven't had a response from the opportunity I applied for |
      | My daily alerts are not relevant to me                      |
      | Other                                                       |


  @TT-758
  @greatgovuk-account
  @account-support
  Scenario: Domestic enquirers should see all expected help options for "Great.gov.uk account"
    Given "Robert" got to the "Domestic - Great.gov.uk account" page via "The UK -> Great.gov.uk account and services support -> Your account on Great.gov.uk"

    Then "Robert" should see following form choices
      | radio elements                                                 |
      | I have not received an email confirmation                      |
      | I need to reset my password                                    |
      | My Companies House login is not working                        |
      | I do not know where to enter my verification code              |
      | I have not received my letter containing the verification code |
      | I have not received a verification code                        |
      | Other                                                          |


  @TT-758
  @short-domestic
  @account-support
  Scenario: Domestic enquirers should be able to get to the "Short Contact Us" form via "The UK -> Great.gov.uk account and services support -> Other"
    Given "Robert" got to the "Domestic - Great.gov.uk account and services support" page via "The UK -> Great.gov.uk account and services support"

    When "Robert" chooses "Other" option

    Then "Robert" should be on the "Domestic - Short contact form (Tell us how we can help)" page


  @TT-758
  @short-domestic
  @greatgovuk-account
  @support
  Scenario: Domestic enquirers should be able to get to the "Short Contact Us" form via "The UK -> Great.gov.uk account and services support -> Your account on Great.gov.uk -> Other"
    Given "Robert" got to the "Domestic - Great.gov.uk account" page via "The UK -> Great.gov.uk account and services support -> Your account on Great.gov.uk"

    When "Robert" chooses "Other" option

    Then "Robert" should be on the "Domestic - Short contact form (Tell us how we can help)" page


  @TT-758
  @greatgovuk-account
  @support
  Scenario: Domestic enquirers should be able to find answers to sought topic about "Your account on Great.gov.uk"
    Given "Robert" got to the "Domestic - Great.gov.uk account" page via "The UK -> Great.gov.uk account and services support -> Your account on Great.gov.uk"

    When "Robert" chooses any available option except "Other"

    Then "Robert" should be on the "Domestic - Great.gov.uk account - Dedicated Support Content" page


  @TT-758
  @exopps
  @support
  Scenario Outline: Exporters should be able to find answers to Export Opportunities related topic "<selected>"
    Given "Robert" got to the "Domestic - Export opportunities service" page via "The UK -> Great.gov.uk account and services support -> Export opportunities service"

    When "Robert" chooses "<selected>" option

    Then "Robert" should be on the "Domestic - <selected> - Dedicated Support Content" page

    Examples:
      | selected                                                    |
      | I haven't had a response from the opportunity I applied for |
      | My daily alerts are not relevant to me                      |


  @TT-758
  @zendesk
  @dev-only
  @captcha
  @account-support
  Scenario Outline: Domestic Enquirers should be able to contact Great Support team via "The UK -> Great.gov.uk account and services support -> Your account on Great.gov.uk -> <selected topic>"
    Given "Robert" got to the "Domestic - <selected topic> - Dedicated Support Content" page via "The UK -> Great.gov.uk account and services support -> Your account on Great.gov.uk -> <selected topic>"

    When "Robert" decides to "Submit an enquiry"
    And "Robert" is on the "Domestic - Short contact form (Tell us how we can help)" page
    And "Robert" fills out and submits the form

    Then "Robert" should be on the "Domestic - Thank you for your enquiry (<selected topic>)" page
    And a "zendesk" notification entitled "great.gov.uk contact form" should be sent to "Robert"

    Examples:
      | selected topic                                                 |
      | I have not received an email confirmation                      |

    @full
    Examples:
      | selected topic                                                 |
      | I have not received an email confirmation                      |
      | I need to reset my password                                    |
      | My Companies House login is not working                        |
      | I do not know where to enter my verification code              |
      | I have not received my letter containing the verification code |
      | I have not received a verification code                        |


  @TT-758
  @zendesk
  @dev-only
  @captcha
  @exopps
  Scenario Outline: Exporters should be to contact Export Opportunities team via Zendesk using "Short contact form" page accessed via "The UK -> Great.gov.uk account and services support -> Export opportunities service -> <selected topic>"
    Given "Robert" got to the "Domestic - <selected topic> - Dedicated Support Content" page via "The UK -> Great.gov.uk account and services support -> Export opportunities service -> <selected topic>"

    When "Robert" decides to "Submit an enquiry"
    And "Robert" is on the "Domestic - Short contact form (Tell us how we can help)" page
    And "Robert" fills out and submits the form

    Then "Robert" should be on the "Domestic - Thank you for your enquiry (<selected topic>) - Short Domestic Contact us" page
    And a "zendesk" notification entitled "great.gov.uk contact form" should be sent to "Robert"

    Examples:
      | selected topic                                              |
      | I haven't had a response from the opportunity I applied for |
      | My daily alerts are not relevant to me                      |


  # Choosing "Other" on the "Your account on Great.gov.uk" page takes us
  # directly to the short contact us form
  @TT-758
  @zendesk
  @dev-only
  @captcha
  @account-support
  Scenario Outline: Domestic Enquirers should be able to contact Great Support team via "The UK -> Great.gov.uk account and services support -> Your account on Great.gov.uk -> <selected topic>"
    Given "Robert" got to the "Domestic - Short contact form (Tell us how we can help)" page via "The UK -> Great.gov.uk account and services support -> Your account on Great.gov.uk -> <selected topic>"

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Domestic - Thank you for your enquiry (<selected topic>) - Short Domestic Contact us" page
    And a "zendesk" notification entitled "great.gov.uk contact form" should be sent to "Robert"

    Examples:
      | selected topic |
      | Other          |


  @TT-758
  @ukef
  Scenario: Exporters should be able to get to the UKEF Check your eligibility contact-us form
    Given "Robert" got to the "Domestic - What can we help you with? - Domestic Contact us" page via "The UK"

    When "Robert" chooses "UK Export Finance (UKEF)" option

    Then "Robert" should be on the "Domestic - Your details - UKEF Contact us" page


  # already partially covered by stories for TT-585
  @wip
  @dev-only
  @captcha
  @ukef
  Scenario: Exporters should be able to contact UKEF mailbox
    Given "Robert" got to the "Domestic - Your details - UKEF Contact us" page via "The UK -> UK Export Finance (UKEF)"

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Domestic - Thank you - UKEF Contact us" page
    # No confirmation email is sent to the user
    # TODO check if email is sent to dedicated mailbox
    And an email is submitted to "UKEF mailbox"


  @TT-758
  @investing-overseas
  @events
  @dso
  @short-form
  Scenario Outline: Domestic enquirers should get to the "Short contact us form" via "The UK -> <selected option>"
    Given "Robert" got to the "Domestic - What can we help you with? - Domestic Contact us" page via "The UK"

    When "Robert" chooses "<selected option>" option

    Then "Robert" should be on the "Domestic - Short contact form (<selected option>)" page

    Examples:
      | selected option                         |
      | Events                                  |
      | Defence and Security Organisation (DSO) |
      | Other                                   |


  @TT-758
  @CMS-506
  @eu-exit
  @feature-flagged
  Scenario: Exporters should be able to get to the "Domestic Brexit help short contact-us form"
    Given "Robert" got to the "Domestic - What can we help you with? - Domestic Contact us" page via "The UK"

    When "Robert" chooses "Brexit enquiries" option

    Then "Robert" should be on the "Domestic - Brexit help" page


  @TT-758
  @zendesk
  @CMS-506
  @dev-only
  @captcha
  @eu-exit
  @feature-flagged
  Scenario: Exporters should be able to contact "Brexit help mailbox"
    Given "Robert" got to the "Domestic - Brexit help" page via "The UK -> Brexit enquiries"

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Domestic - Brexit help - Thank you" page
    And a "zendesk" notification entitled "Brexit contact form" should be sent to "Robert"


  @TT-758
  @dev-only
  @captcha
  @short-form
  Scenario Outline: Exporters should be able to contact "<expected recipient>" using "Short contact form (<selected option>)" page accessed via "The UK -> <selected option>"
    Given "Robert" got to the "Domestic - Short contact form (<selected option>)" page via "The UK -> <selected option>"

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "Domestic - Thank you for your enquiry (<selected option>) - Short Domestic Contact us" page
    And "Robert" should receive "<appropriate>" confirmation email
    And an email notification about "Robert"'s enquiry should be send to "<expected recipient>"

    Examples:
      | selected option                         | appropriate                                                  | expected recipient |
      | Events                                  | Thank you for your Events enquiry                            | Events mailbox     |
      | Defence and Security Organisation (DSO) | Thank you for your Defence and Security Organisation enquiry | DSO mailbox        |
      | Other                                   | Thank you for your enquiry                                   | DIT Enquiry unit   |


  @dev-only
  @TT-758
  @international
  Scenario: International Enquirers should be able to see all expected contact options on the "International - What would you like to know more about?" page
    Given "Robert" visits the "Domestic - Contact us" page

    When "Robert" says that his business is "Outside the UK"

    Then "Robert" should be on the "Domestic - What would you like to know more about? - International Contact us" page
    And "Robert" should see following form choices
      | radio elements               |
      | Expanding to the UK          |
      | Investing capital in the UK |
      | Find a UK business partner   |
      | Brexit enquiries             |
      | Other                        |


  @stage-only
  @prod-only
  @TT-758
  @international
  Scenario: International Enquirers should be able to see all expected contact options on the "International - What would you like to know more about?" page
    Given "Robert" visits the "Domestic - Contact us" page

    When "Robert" says that his business is "Outside the UK"

    Then "Robert" should be on the "Domestic - What would you like to know more about? (staging) - International Contact us" page
    And "Robert" should see following form choices
      | radio elements               |
      | Investing in the UK          |
      | Find a UK business partner   |
      | Brexit enquiries             |
      | Other                        |


  @TT-758
  @international
  Scenario Outline: International Enquirers should be able to get to the "<expected>" form for "<selected>"
    Given "Robert" got to the "Domestic - What would you like to know more about? - International Contact us" page via "Outside the UK"

    When "Robert" chooses "<selected>" option

    Then "Robert" should be on the "<expected>" page

    @dev-only
    Examples:
      | selected                     | expected                                                |
      | Expanding to the UK          | Invest - Contact us                                     |
      | Investing capital in the UK  | International - Contact the Capital Investment team     |
      | Find a UK business partner   | International - Find a UK business partner - Contact us |
      | Brexit enquiries             | International - Brexit help                             |
      | Other                        | International - Contact us                              |


  @TT-758
  @stage-only
  @prod-only
  @international
  Scenario Outline: International Enquirers should be able to get to the "<expected>" form for "<selected>"
    Given "Robert" got to the "Domestic - What would you like to know more about? (staging) - International Contact us" page via "Outside the UK"

    When "Robert" chooses "<selected>" option

    Then "Robert" should be on the "<expected>" page

    Examples:
      | selected                   | expected                                                |
      | Investing in the UK        | Invest - Contact us                                     |
      | Find a UK business partner | International - Find a UK business partner - Contact us |
      | Brexit enquiries           | International - Brexit help                             |
      | Other                      | International - Contact us                              |


  @TT-758
  @going-back
  Scenario Outline: Enquirers should be able to navigate back to previous pages from "<path>" back to "<expected>" page
    Given "Robert" navigates via "<path>"

    When "Robert" decides to use "back" link

    Then "Robert" should be on the "<expected>" page

    Examples:
      | path                                                                                | expected                                                    |
      | The UK                                                                              | Domestic - Contact us                                       |
      | Outside the UK                                                                      | Domestic - Contact us                                       |
      | The UK -> Great.gov.uk account and services support                                 | Domestic - What can we help you with? - Domestic Contact us |
      | The UK -> Great.gov.uk account and services support -> Export opportunities service | Domestic - Great.gov.uk account and services support        |
      | The UK -> Great.gov.uk account and services support -> Your account on Great.gov.uk | Domestic - Great.gov.uk account and services support        |


  @TT-758
  @capital-investment
  @international
  Scenario: International Enquirers should be able to get to contact the Capital Investment team
    Given "Robert" got to the "International - Contact the Capital Investment team" page via "Outside the UK -> Investing capital in the UK"

    When "Robert" fills out and submits the form

    Then "Robert" should be on the "International - Thank you for contacting the Capital Investment team" page
    And "Robert" should receive "Thank you for your enquiry" confirmation email
    And "Robert" should see following sections
      | sections          |
      | Header            |
      | Breadcrumbs       |
      | Thank you message |
      | What's next       |
      | Error reporting   |
      | Footer            |

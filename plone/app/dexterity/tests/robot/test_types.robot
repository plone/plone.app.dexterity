*** Settings *****************************************************************

Resource  plone/app/robotframework/keywords.robot
Resource  plone/app/robotframework/saucelabs.robot
Resource  plone/app/robotframework/selenium.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run Keywords  Plone test setup
Test Teardown  Run keywords  Plone test teardown


*** Test cases ***************************************************************

Scenario: type title is normalized
  Given a logged in manager
   When adding a new content type
    and type title is  Boîte à outils
   Then type id should become  boite_a_outils


*** Keywords *****************************************************************

adding a new content type
  Go to  ${PLONE_URL}/@@dexterity-types
  Click Overlay Button  Add New Content Type…

type title is
  [Arguments]  ${title}
  Input text  form-widgets-title  ${title}

type id should become
  [Arguments]  ${id}
  Set Focus To Element  form-widgets-id
  Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-id  ${id}

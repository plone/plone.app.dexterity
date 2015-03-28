*** Settings *****************************************************************

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers


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
  Focus  form-widgets-id
  Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-id  ${id}

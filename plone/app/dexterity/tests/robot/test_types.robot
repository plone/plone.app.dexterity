*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Run keywords  Open test browser
Test Teardown  Close all browsers

*** Variables ***

*** Keywords ***

adding a new content type
    Enable autologin as  Manager
    Go to  ${PLONE_URL}/@@dexterity-types
    Click Overlay Button  Add New Content Type…

type title is
    [Arguments]  ${title}
    Input text  form-widgets-title  ${title}

type id should become
    [Arguments]  ${id}
    Focus  form-widgets-id
    Wait until keyword succeeds  10  1  Textfield Value Should Be  form-widgets-id  ${id}


*** Test cases ***

Scenario: type title is normalized
    When adding a new content type
     and type title is  Boîte à outils
    then type id should become  boite_a_outils

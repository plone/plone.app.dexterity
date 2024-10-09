*** Settings ***

Resource    plone/app/robotframework/browser.robot

Library    Remote    ${PLONE_URL}/RobotRemote

Test Setup    Run Keywords    Plone test setup
Test Teardown    Run keywords    Plone test teardown


*** Test cases ***

Scenario: type title is normalized
    Given a site owner
     When adding a new content type
      and type title is    Boîte à outils
     Then type id should become    boite_a_outils


*** Keywords ***

# Given

a site owner

    Enable autologin as    Manager

# When

adding a new content type

    Go to    ${PLONE_URL}/@@dexterity-types
    Click    "Add New Content Type…"

# Then

type title is
    [Arguments]    ${title}

    Fill text    //input[@id="form-widgets-title"]    ${title}

type id should become
    [Arguments]    ${id}

    Focus    id=form-widgets-id
    Get text    //input[@id="form-widgets-id"]    should be    ${id}
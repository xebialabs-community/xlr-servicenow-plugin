/**
 * Copyright 2018 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
package com.xebialabs.xlr.xlrelease.test;

import com.xebialabs.pages.*;
import com.xebialabs.specs.BaseTest;
import org.testng.annotations.*;

public class LoginTest extends BaseTest {

    @BeforeMethod
    public void testStartUp(){
        System.out.println("called before method");
        LoginPage.login("admin","admin");
    }

    @Test
    public void openConfigurationServiceNow(){
        MainMenu.clickMenu("Settings");
        SubMenu.clickSubMenu("Shared configuration");
        SharedConfigurationPage.openSharedConfiguration("ServiceNow: Server");
        SharedConfigurationPropertiesPage.checkSharedConfigurationHeader("ServiceNow");
    }

    @Test
    public void SaveConfiguration(){
        MainMenu.clickMenu("Settings");
        SubMenu.clickSubMenu("Shared configuration");
        SharedConfigurationPage.openSharedConfiguration("ServiceNow: Server");
        SharedConfigurationPropertiesPage.checkSharedConfigurationHeader("ServiceNow");
        SharedConfigurationPropertiesPage.setEditFieldBySequence(1,"ServiceNow Config 1");
        SharedConfigurationPropertiesPage.setEditFieldBySequence(2,"ServiceNow url");
        SharedConfigurationPropertiesPage.clickButtonByText("Save");
        SharedConfigurationPropertiesPage.isNewConfigurationSaved().isSharedConfigurationPageVisible("ServiceNow: Server");
    }

    @Test
    public void TestInvalidConfiguration(){
        MainMenu.clickMenu("Settings");
        SubMenu.clickSubMenu("Shared configuration");
        SharedConfigurationPage.openSharedConfiguration("ServiceNow: Server");
        SharedConfigurationPropertiesPage.checkSharedConfigurationHeader("ServiceNow");
        SharedConfigurationPropertiesPage.setEditFieldBySequence(1,"ServiceNow Config 2");
        SharedConfigurationPropertiesPage.setEditFieldBySequence(2,"ServiceNow Url");
        SharedConfigurationPropertiesPage.clickElementById("authenticationMethod"); // clicking the element so that select field will be visible on next step
        SharedConfigurationPropertiesPage.setOptionFromSelectFieldBySequence(1,"None");
        SharedConfigurationPropertiesPage.clickButtonByText("Test");
        SharedConfigurationPropertiesPage.checkConnectionStatusShouldContain("Can't connect");
    }

    @Test
    public void TestValidConfiguration(){
        MainMenu.clickMenu("Settings");
        SubMenu.clickSubMenu("Shared configuration");
        SharedConfigurationPage.openSharedConfiguration("ServiceNow: Server");
        SharedConfigurationPropertiesPage.checkSharedConfigurationHeader("ServiceNow");
        SharedConfigurationPropertiesPage.setEditFieldBySequence(1,"ServiceNow Config 3");
        SharedConfigurationPropertiesPage.setEditFieldBySequence(2, System.getenv("SERVICENOW_URL"));
        SharedConfigurationPropertiesPage.clickElementById("authenticationMethod"); // clicking the element so that select field will be visible on next step
        SharedConfigurationPropertiesPage.setOptionFromSelectFieldBySequence(1,"Basic");
        SharedConfigurationPropertiesPage.setEditFieldBySequence(7, System.getenv("SERVICENOW_USERNAME"));
        SharedConfigurationPropertiesPage.setEditFieldBySequence(8, System.getenv("SERVICENOW_PASSWORD"));
        SharedConfigurationPropertiesPage.clickButtonByText("Test");
        SharedConfigurationPropertiesPage.checkConnectionStatusShouldContain("ServiceNow: Server is available");
    }

    @AfterMethod
    public void logout(){
        System.out.println("called after method");
        MainMenu.logout();
    }
}
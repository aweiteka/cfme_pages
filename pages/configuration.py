'''
Created on Mar 5, 2013

@author: bcrochet
'''

# -*- coding: utf-8 -*-

from pages.base import Base
from selenium.webdriver.common.by import By

class Configuration(Base):
    @property
    def submenus(self):
        return {"configuration" : lambda: Configuration.MySettings,
                "ops" : lambda: Configuration.Configuration
                }
        
    def __init__(self,setup):
        Base.__init__(self, setup)
        # TODO: Add more initialization here
    
    class MySettings(Base):
        _page_title = "CloudForms Management Engine: Configuration"
        
        def __init__(self,setup):
            Base.__init__(self, setup)

    class Configuration(Base):
        _page_title = "CloudForms Management Engine: Configuration"
        _view_groups_link = (By.CSS_SELECTOR, "div[title='View Groups']")
        _add_new_group_button = (By.CSS_SELECTOR, "a[title='Add a new Group']")
        _role_description_field = (By.ID, "description")
        _ldap_lookup_checkbox= (By.ID, "lookup")
        _role_selector= (By.ID, "group_role")
        _add_button = (By.CSS_SELECTOR, "img[title='Add this Group']")
        # fields display only after _ldap_lookup_checkbox checked
        _ldap_user_field = (By.ID, "user")
        _ldap_admin_field = (By.ID, "user_id")
        _ldap_passwd_field = (By.ID, "password")
        # FIXME: find better way to access retrieve button
        _ldap_retrieve_button = (By.CSS_SELECTOR, "img[class='button formbutton']")
        # selector displays only after ldap user retrieved
        _ldap_group_selector = (By.ID, "ldap_groups_user")

        _edit_group_tags = (By.CSS_SELECTOR, "a[title='Edit Red Hat Tags for this Group']")
        _tag_category_selector = (By.ID, "tag_cat")
        _tag_value_selector = (By.ID, "tag_add")
        _save_tag_edits_button = (By.CSS_SELECTOR, "img[title='Save Changes']")

        def __init__(self,setup):
            Base.__init__(self, setup)

        @property
        def accordion(self):
            from pages.regions.accordion import Accordion
            from pages.regions.treeaccordionitem import TreeAccordionItem
            return Accordion(self.testsetup,TreeAccordionItem)

        @property
        def view_groups(self):
            return self.selenium.find_element(*self._view_groups_link)

        @property
        def add_group(self):
            return self.selenium.find_element(*self._add_new_group_button)

        @property
        def retrieve(self):
            return self.selenium.find_element(*self._ldap_retrieve_button)

        @property
        def add(self):
            return self.selenium.find_element(*self._add_button)

        @property
        def save_tag(self):
            return self.selenium.find_element(*self._save_tag_edits_button)

        @property
        def edit_tag(self):
            return self.selenium.find_element(*self._edit_group_tags)

        @property
        def ldap_lookup_checkbox(self):
            return self.selenium.find_element(*self._ldap_lookup_checkbox)

        def click_on_view_groups(self):
            self.view_groups.click()
            return Configuration.Configuration(self.testsetup)

        def click_on_group_detail(self, group):
            _group_detail = (By.CSS_SELECTOR, "td[title='%s']" % group)
            self.selenium.find_element(*_group_detail).click()
            self._wait_for_results_refresh()
            return Configuration.Configuration(self.testsetup)

        def click_on_edit_tags(self):
            self.edit_tag.click()
            self._wait_for_results_refresh()
            return Configuration.Configuration(self.testsetup)

        def select_tag(self, tag):
            self.select_dropdown(tag[0], *self._tag_category_selector)
            self._wait_for_results_refresh()
            self.select_dropdown(tag[1], *self._tag_value_selector)
            self._wait_for_results_refresh()
            return

        def click_on_add_group(self):
            self.add_group.click()
            return Configuration.Configuration(self.testsetup)

        def click_on_retrieve(self):
            self.retrieve.click()
            self._wait_for_results_refresh()
            return Configuration.Configuration(self.testsetup)

        def select_ldap_lookup(self):
            if not self.ldap_lookup_checkbox.is_selected():
                return self.ldap_lookup_checkbox.click()

        def lookup_ldap_group(self, user, ldap_admin, ldap_pass):
            self.selenium.find_element(*self._ldap_user_field).send_keys(user)
            self.selenium.find_element(*self._ldap_admin_field).send_keys(ldap_admin)
            self.selenium.find_element(*self._ldap_passwd_field).send_keys(ldap_pass)
            return self.click_on_retrieve()

        def click_on_add(self):
            self.add.click()
            return Configuration.Configuration(self.testsetup)

        def click_on_save_tag(self):
            self.save_tag.click()
            return Configuration.Configuration(self.testsetup)

        def create_local_group(self, group, role):
            self.click_on_view_groups()
            self._wait_for_results_refresh()
            self.click_on_add_group()
            self.selenium.find_element(*self._role_description_field).send_keys(group)
            self.select_dropdown(role, *self._role_selector)
            return self.click_on_add()

        def create_ldap_group(self, group, role, user, ldap_admin, ldap_pass):
            self.click_on_view_groups()
            self._wait_for_results_refresh()
            self.click_on_add_group()
            self.select_ldap_lookup()
            self.lookup_ldap_group(user, ldap_admin, ldap_pass)
            self.select_dropdown(group, *self._ldap_group_selector)
            self.select_dropdown(role, *self._role_selector)
            return self.click_on_add()

        # TODO: recommend moving tag management to region/tags.py
        def assign_group_tags(self, group, tag):
            self.click_on_view_groups()
            self._wait_for_results_refresh()
            self.click_on_group_detail(group)
            self.click_on_edit_tags()
            self.select_tag(tag)
            return self.click_on_save_tag()


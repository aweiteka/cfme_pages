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
        _save_edits_button = (By.CSS_SELECTOR, "img[title='Save Changes']")

        # Region C&U collection 
        _cu_collect_tab = (By.CSS_SELECTOR, "a[href='#settings_cu_collection']")
        _collect_all_clusters_checkbox = (By.ID, "all_clusters")
        _collect_all_datastores_checkbox = (By.ID, "all_storages")

        # database
        _database_tab = (By.CSS_SELECTOR, "a[href='#settings_database']")
        _database_selector= (By.ID, "production_dbtype")
        _database_host_field= (By.ID, "production_host")
        _validate_database_button = (By.CSS_SELECTOR, "img[title='Validate Database Configuration']")
        _save_database_button = (By.CSS_SELECTOR, "img[title='Save changes and restart the Server']")

        # zone
        _view_zones_link = (By.CSS_SELECTOR, "div[title='View Zones']")
        _create_new_zone_button = (By.CSS_SELECTOR, "a[title='Add a new zone']")
        _zone_name_field = (By.ID, "name")
        _zone_description_field = (By.ID, "description")
        _save_zone_button = (By.CSS_SELECTOR, "img[title='Add']")
        _server_zone_selector = (By.ID, "server_zone")

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
        def view_zones(self):
            return self.selenium.find_element(*self._view_zones_link)

        @property
        def add_group(self):
            return self.selenium.find_element(*self._add_new_group_button)

        @property
        def create_new_zone(self):
            return self.selenium.find_element(*self._create_new_zone_button)

        @property
        def save_zone(self):
            return self.selenium.find_element(*self._save_zone_button)

        @property
        def retrieve(self):
            return self.selenium.find_element(*self._ldap_retrieve_button)

        @property
        def add(self):
            return self.selenium.find_element(*self._add_button)

        @property
        def save(self):
            return self.selenium.find_element(*self._save_edits_button)

        @property
        def save_database(self):
            return self.selenium.find_element(*self._save_database_button)

        @property
        def validate(self):
            return self.selenium.find_element(*self._validate_database_button)

        @property
        def edit_tag(self):
            return self.selenium.find_element(*self._edit_group_tags)

        @property
        def ldap_lookup_checkbox(self):
            return self.selenium.find_element(*self._ldap_lookup_checkbox)

        @property
        def cu_collect_tab(self):
            return self.selenium.find_element(*self._cu_collect_tab)

        @property
        def database_tab(self):
            return self.selenium.find_element(*self._database_tab)

        @property
        def collect_all_clusters_checkbox(self):
            return self.selenium.find_element(*self._collect_all_clusters_checkbox)

        @property
        def collect_all_datastores_checkbox(self):
            return self.selenium.find_element(*self._collect_all_datastores_checkbox)

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

        def click_on_cu_collect_tab(self):
            self.cu_collect_tab.click()
            self._wait_for_results_refresh()
            return Configuration.Configuration(self.testsetup)

        def click_on_database_tab(self):
            self.database_tab.click()
            self._wait_for_results_refresh()
            return Configuration.Configuration(self.testsetup)

        def complete_database_form(self, external_cfme_vmdb):
            self.select_dropdown("External Database on another EVM Appliance", \
                *self._database_selector)
            self.selenium.find_element(*self._database_host_field).clear()
            self.selenium.find_element(*self._database_host_field).send_keys(external_cfme_vmdb)
            return Configuration.Configuration(self.testsetup)

        def complete_zone_form(self, name, desc):
            self.selenium.find_element(*self._zone_name_field).send_keys(name)
            self.selenium.find_element(*self._zone_description_field).send_keys(desc)
            return Configuration.Configuration(self.testsetup)

        def click_on_save_zone(self):
            self.save_zone.click()
            self._wait_for_results_refresh()
            return Configuration.Configuration(self.testsetup)

        def select_zone(self, zone):
            self.select_dropdown(zone, *self._server_zone_selector)
            return Configuration.Configuration(self.testsetup)
            
        def click_on_validate_database(self):
            self.validate.click()
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

        def click_on_save(self):
            self.save.click()
            self._wait_for_results_refresh()
            return Configuration.Configuration(self.testsetup)

        def toggle_collect_all_clusters(self, enable):
            if enable:
                if not self.collect_all_clusters_checkbox.is_selected():
                    return self.collect_all_clusters_checkbox.click()
            else:
                if self.collect_all_clusters_checkbox.is_selected():
                    return self.collect_all_clusters_checkbox.click()

        def toggle_collect_all_datastores(self, enable):
            if enable:
                if not self.collect_all_datastores_checkbox.is_selected():
                    return self.collect_all_datastores_checkbox.click()
            else:
                if self.collect_all_datastores_checkbox.is_selected():
                    return self.collect_all_datastores_checkbox.click()

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
            return self.click_on_save()

        def toggle_region_cu_collection(self, enable_clusters, enable_datastores):
            self.click_on_cu_collect_tab()
            self.toggle_collect_all_clusters(enable_clusters)
            self.toggle_collect_all_datastores(enable_datastores)
            return self.save.is_displayed()

        def save_changes(self):
            return self.click_on_save()

        def validate_external_cfme_vmdb(self, appliance, cfme_name, external_cfme_vmdb):
            appliance.click()
            self._wait_for_results_refresh()
            self.click_on_database_tab()
            self._wait_for_results_refresh()
            self.complete_database_form(external_cfme_vmdb)
            return self.click_on_validate_database()

        def save_database_and_restart(self):
            # assumes validate_external_cfme_vmdb() called
            self.save_database.click()
            self.handle_popup()
            self._wait_for_results_refresh()
            return Configuration.Configuration(self.testsetup)

        def create_zone(self, name, desc):
            self.view_zones.click()
            self._wait_for_results_refresh()
            self.create_new_zone.click()
            self._wait_for_results_refresh()
            self.complete_zone_form(name, desc)
            return self.click_on_save_zone()

        def select_zone(self, zone):
            self.select_dropdown(zone, *self._server_zone_selector)
            self._wait_for_results_refresh()
            return Configuration.Configuration(self.testsetup)


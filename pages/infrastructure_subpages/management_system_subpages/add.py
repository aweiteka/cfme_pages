'''
Created on May 31, 2013

@author: bcrochet
'''
from pages.base import Base
from selenium.webdriver.common.by import By

class ManagementSystemsAdd(Base):
    _page_title = 'CloudForms Management Engine: Management Systems'

    _management_system_add_button_locator = (
            By.CSS_SELECTOR,
            "img[alt='Add this Management System']")
    _management_system_credentials_verify_button_locator = (
            By.CSS_SELECTOR,
            "div#default_validate_buttons_on > ul#form_buttons > li > a > img")
    _management_system_credentials_verify_disabled_button_locator = (
            By.CSS_SELECTOR,
            "div#default_validate_buttons_off > ul#form_buttons > li > a > img")
    _management_system_cancel_button_locator = (
            By.CSS_SELECTOR, "img[title='Cancel']")
    _management_system_name_locator = (By.ID, "name")
    _management_system_hostname_locator = (By.ID, "hostname")
    _management_system_ipaddress_locator = (By.ID, "ipaddress")
    _management_system_type_locator = (By.ID, "server_emstype")
    _management_system_userid_locator = (By.ID, "default_userid")
    _management_system_password_locator = (By.ID, "default_password")
    _management_system_verify_password_locator = (By.ID, "default_verify")
    _management_system_cu_userid_locator = (By.ID, "metrics_userid")
    _management_system_cu_password_locator = (By.ID, "metrics_password")
    _management_system_cu_verify_locator = (By.ID, "metrics_verify")
    _server_zone_edit_field_locator = (By.ID, "server_zone")
    _default_credentials_button_locator = (
            By.CSS_SELECTOR, "div#auth_tabs > ul > li > a#ui-id-1")
    _metrics_credentials_button_locator = (
            By.CSS_SELECTOR, "div#auth_tabs > ul > li > a#ui-id-2")
    _management_system_api_port_locator = (
            By.ID, "port")

    @property
    def add_button(self):
        return self.get_element(*self._management_system_add_button_locator)

    @property
    def verify_button(self):
        return self.get_element(
                *self._management_system_credentials_verify_button_locator)

    @property
    def cancel_button(self):
        return self.get_element(
                *self._management_system_cancel_button_locator)

    @property
    def name(self):
        return self.get_element(*self._management_system_name_locator)

    @property
    def hostname(self):
        return self.get_element(*self._management_system_hostname_locator)

    @property
    def ipaddress(self):
        return self.get_element(*self._management_system_ipaddress_locator)

    @property
    def default_userid(self):
        return self.get_element(*self._management_system_userid_locator)

    @property
    def default_password(self):
        return self.get_element(*self._management_system_password_locator)

    @property
    def default_verify(self):
        return self.get_element(
                *self._management_system_verify_password_locator)

    @property
    def metrics_userid(self):
        return self.get_element(*self._management_system_cu_userid_locator)

    @property
    def metrics_password(self):
        return self.get_element(
                *self._management_system_cu_password_locator)

    @property
    def metrics_verify(self):
        return self.get_element(*self._management_system_cu_verify_locator)

    @property
    def api_port(self):
        return self.get_element(*self._management_system_api_port_locator)

    @property
    def server_zone(self):
        return self.get_element(*self._server_zone_edit_field_locator)

    def click_on_default_credentials(self):
        self.get_element(*self._default_credentials_button_locator).click()

    def click_on_metrics_credentials(self):
        self.get_element(*self._metrics_credentials_button_locator).click()

    def new_management_system_fill_data(
            self,
            name="test_name",
            hostname="test_hostname",
            ip_address="127.0.0.1",
            user_id="test_user",
            password="test_password"):
        self.name.send_keys(name)
        self.hostname.send_keys(hostname)
        self.ipaddress.send_keys(ip_address)
        self.default_userid.send_keys(user_id)
        self.default_password.send_keys(password)
        self.default_verify.send_keys(password)

    def _fill_management_system(self, management_system):
        for key, value in management_system.iteritems():
            # Special cases
            if "server_zone" in key:
                if self.server_zone.tag_name == "select":
                    self.select_dropdown(value)
            elif "cu_credentials" in key:
                credentials = self.testsetup.credentials[value]
                self.metrics_userid.clear()
                self.metrics_userid.send_keys(credentials['username'])
                self.metrics_password.clear()
                self.metrics_password.send_keys(credentials['password'])
                self.metrics_verify.clear()
                self.metrics_verify.send_keys(credentials['password'])
                continue
            elif "credentials" in key:
                credentials = self.testsetup.credentials[value]
                self.default_userid.clear()
                self.default_userid.send_keys(credentials['username'])
                self.default_password.clear()
                self.default_password.send_keys(credentials['password'])
                self.default_verify.clear()
                self.default_verify.send_keys(credentials['password'])
                continue
            else:
                # Only try to send keys if there is actually a property
                if hasattr(self, key):
                    attr = getattr(self, key)
                    attr.clear()
                    attr.send_keys(value)

    def add_vmware_management_system(self, management_system):
        self.select_management_system_type("VMware vCenter")
        self._fill_management_system(management_system)
        return self.click_on_add()

    def add_rhevm_management_system(self, management_system):
        self.select_management_system_type("Red Hat Enterprise Virtualization Manager")
        self._fill_management_system(management_system)
        return self.click_on_add()

    def add_management_system(self, management_system):
        if "virtualcenter" in management_system["type"]:
            return self.add_vmware_management_system(management_system)
        elif "rhevm" in management_system["type"]:
            return self.add_rhevm_management_system(management_system)
        raise Exception("Unknown management system type")

    def add_management_system_with_bad_credentials(self, management_system):
        if "virtualcenter" in management_system["type"]:
            self.select_management_system_type("VMware vCenter")
        elif "rhevm" in management_system["type"]:
            self.select_management_system_type("Red Hat Enterprise Virtualization Manager")
        self._fill_management_system(management_system)
        self._wait_for_visible_element(*self._management_system_credentials_verify_button_locator)
        self.click_on_credentials_verify()
        return self

    def select_management_system_type(self, management_system_type):
        self.select_dropdown(
                management_system_type,
                *self._management_system_type_locator)
        self._wait_for_results_refresh()
        return ManagementSystemsAdd(self.testsetup)

    def click_on_add(self):
        self.add_button.click()
        from pages.infrastructure_subpages.management_systems import ManagementSystems
        return ManagementSystems(self.testsetup)

    def click_on_credentials_verify(self):
        self.verify_button.click()
        self._wait_for_results_refresh()
        return ManagementSystemsAdd(self.testsetup)

    def click_on_cancel(self):
        self.cancel_button.click()
        from pages.infrastructure_subpages.management_systems import ManagementSystems
        return ManagementSystems(self.testsetup)


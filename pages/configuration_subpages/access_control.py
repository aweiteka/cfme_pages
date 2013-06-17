from pages.base import Base
from pages.regions.checkboxtree import CheckboxTree
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from pages.regions.taggable import Taggable
from selenium.webdriver.support.ui import WebDriverWait

class AccessControl(Base):
    _page_title = 'CloudForms Management Engine: Configuration'
    _roles_button = (By.CSS_SELECTOR, "div[title='View Roles']")
    _groups_button = (By.CSS_SELECTOR, "div[title='View Groups']")

    # ROLES
    def click_on_roles(self):
        self.selenium.find_element(*self._roles_button).click()
        self._wait_for_results_refresh()
        return AccessControl.Roles(self.testsetup)

    class Roles(Base):
        _page_title = 'CloudForms Management Engine: Configuration'
        _add_role_button = (By.CSS_SELECTOR, "a[title='Add a new Role']")

        def click_on_add_new(self):
            self.selenium.find_element(*self._add_role_button).click()
            self._wait_for_results_refresh()
            return AccessControl.NewRole(self.testsetup)

        def click_on_role(self, role_name):
            selector = "td[title='%s']" % role_name
            self.selenium.find_element_by_css_selector(selector).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowRole(self.testsetup)

    class NewRole(Base):
        _submit_role_button = (By.CSS_SELECTOR, "img[title='Add this Role']")
        _name_field = (By.CSS_SELECTOR, "input[name='name']")
        _access_restriction_field = (By.CSS_SELECTOR, "select[name='vm_restriction']")
        _product_features_tree = (By.CSS_SELECTOR, "#features_treebox")

        @property
        def product_features(self):
            return CheckboxTree(self.testsetup, self.selenium.find_element(*self._product_features_tree))

        def fill_name(self, name):
            return self.selenium.find_element(*self._name_field).send_keys(name)

        def save(self):
            # when editing an existing role, wait until "save" button shows up
            # after ajax validation
            self._wait_for_visible_element(*self._submit_role_button)
            self.selenium.find_element(*self._submit_role_button).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowRole(self.testsetup)

        def select_access_restriction(self, value):
            Select(self.selenium.find_element(*self._access_restriction_field)).select_by_value(value)

    class EditRole(NewRole):
        _name_field = (By.CSS_SELECTOR, "input[name='name']")
        _submit_role_button = (By.CSS_SELECTOR, "img[title='Save Changes']")

        def fill_name(self, name):
            field = self.selenium.find_element(*self._name_field)
            field.clear()
            field.send_keys(name)

    class ShowRole(Base):
        _edit_role_button = (By.CSS_SELECTOR, "a[title='Edit this Role']")
        _delete_role_button = (By.CSS_SELECTOR, "a[title='Delete this Role']")
        _role_name_label = (By.CSS_SELECTOR, ".style1 tr:nth-child(1) td:nth-child(2)")
        _product_features_tree = (By.CSS_SELECTOR, "#features_treebox")

        def click_on_edit(self):
            self.selenium.find_element(*self._edit_role_button).click()
            self._wait_for_results_refresh()
            return AccessControl.EditRole(self.testsetup)

        def click_on_delete(self):
            self.selenium.find_element(*self._delete_role_button).click()
            self.handle_popup()
            self._wait_for_results_refresh()
            return AccessControl.Roles(self.testsetup)

        @property
        def role_name(self):
            return self.selenium.find_element(*self._role_name_label).text.strip()
        @property
        def product_features(self):
            return CheckboxTree(self.testsetup, self.selenium.find_element(*self._product_features_tree))

        def traverse_rbac_tree(self, parent=None, depth=3):
            """Repackage product_features tree so it's available after loading
               another page
            """
            if parent is None:
                parent = CheckboxTree(self.testsetup, self.selenium.find_element(*self._product_features_tree)).find_node_by_name("Everything")
            else:
                parent.twisty.expand()
            rbac_node = RBAC_Node(parent)
            if depth > 0:
                for child in parent.children:
                    # move selenium along when no children, avoid 10-sec delay
                    self.selenium.implicitly_wait(0)
                    rbac_node.children.append(self.traverse_rbac_tree(parent=child, depth=depth-1))
     
            return rbac_node

    # GROUPS
    def click_on_groups(self):
        self.selenium.find_element(*self._groups_button).click()
        self._wait_for_results_refresh()
        return AccessControl.Groups(self.testsetup)

    class Groups(Base):
        _page_title = 'CloudForms Management Engine: Configuration'
        _add_group_button = (By.CSS_SELECTOR, "a[title='Add a new Group']")

        def click_on_add_new(self):
            self.selenium.find_element(*self._add_group_button).click()
            self._wait_for_results_refresh()
            return AccessControl.NewGroup(self.testsetup)

        def click_on_group(self, group_name):
            selector = "td[title='%s']" % group_name
            self.selenium.find_element_by_css_selector(selector).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowGroup(self.testsetup)

    class NewGroup(Base):
        _submit_group_button = (By.CSS_SELECTOR, "img[title='Add this Group']")
        _group_description_field = (By.ID, "description")
        _role_selector= (By.ID, "group_role")
        _company_tags_tree = (By.CSS_SELECTOR, "#myco_treebox")
        _hosts_clusters_tree = (By.CSS_SELECTOR, "#hac_treebox")
        _vms_templates_tree = (By.CSS_SELECTOR, "#vat_treebox")

        @property
        def company_tags(self):
            return CheckboxTree(self.testsetup, self.selenium.find_element(*self._company_tags_tree))

        @property
        def hosts_clusters(self):
            return CheckboxTree(self.testsetup, self.selenium.find_element(*self._hosts_clusters_tree))

        @property
        def vms_templates(self):
            return CheckboxTree(self.testsetup, self.selenium.find_element(*self._vms_templates_tree))

        def fill_info(self, description, role):
            self.selenium.find_element(*self._group_description_field).send_keys(description)
            return self.select_dropdown(role, *self._role_selector)

        def save(self):
            # when editing an existing group, wait until "save" button shows up
            # after ajax validation
            self._wait_for_visible_element(*self._submit_group_button)
            self.selenium.find_element(*self._submit_group_button).click()
            self._wait_for_results_refresh()
            return AccessControl.ShowGroup(self.testsetup)

    class EditGroup(NewGroup):
        _group_description_field = (By.ID, "description")
        _role_selector= (By.ID, "group_role")
        _submit_group_button = (By.CSS_SELECTOR, "img[title='Save Changes']")

        def fill_info(self, description, role):
            field = self.selenium.find_element(*self._group_description_field)
            field.clear()
            field.send_keys(description)
            return self.select_dropdown(role, *self._role_selector)

    class ShowGroup(Base):
        _edit_group_button = (By.CSS_SELECTOR, "a[title='Edit this Group']")
        _delete_group_button = (By.CSS_SELECTOR, "a[title='Delete this Group']")
        _group_name_label = (By.CSS_SELECTOR, ".style1 tr:nth-child(1) td:nth-child(2)")
        _edit_tags_button = (By.CSS_SELECTOR, "li#tag > a")
        _role_locator = (By.CSS_SELECTOR, "tr[title='View this Role']")

        @property
        def role(self):
            return self.selenium.find_element(*self._role_locator)

        def click_on_role(self):
            self.role.click()
            self._wait_for_results_refresh()
            return AccessControl.ShowRole(self.testsetup)

        def click_on_edit(self):
            self.selenium.find_element(*self._edit_group_button).click()
            self._wait_for_results_refresh()
            return AccessControl.EditGroup(self.testsetup)

        def click_on_delete(self):
            self.selenium.find_element(*self._delete_group_button).click()
            self.handle_popup()
            self._wait_for_results_refresh()
            return AccessControl.Groups(self.testsetup)

        def click_on_edit_tags(self):
            self.selenium.find_element(*self._edit_tags_button).click()
            self._wait_for_results_refresh
            return AccessControl.TagGroup(self.testsetup)

        @property
        def group_name(self):
            return self.selenium.find_element(*self._group_name_label).text.strip()

    class TagGroup(ShowGroup, Taggable):
        @property
        def save(self):
            return self.save_tag_edits

        @property
        def cancel(self):
            return self.cancel_tag_edits

        @property
        def reset(self):
            return self.reset_tag_edits

# helper class to build product features (RBAC) tree
class RBAC_Node(object):

    def __init__(self, node):
        self.children = list()
        self._node = node
        self.name = self.translate_menu()
        # TODO: make these properties
        self.node_type = self.node_type()
        self.is_accordion = self.is_accordion()
        self.is_menu = self.is_menu()
        self.is_enabled = self.is_enabled()

    def translate_menu(self):
        '''translate RBAC tree string into menu string
        '''
        # all depths
        menu_map = {"Settings & Operations": "Configuration",
                    "Catalogs Explorer": "Catalogs",
                    # for submenus
                    "Import/Export": "Import / Export",
                    # for accordion
                    "Import / Export": "Import/Export"}
        return menu_map.get(self._node.name, self._node.name)


    def node_type(self):
        '''Return icon type: folder, view, operate, modify
        '''
        icon_map = {"feature_node.png": "node",
                    "feature_view.png": "view",
                    "feature_admin.png": "modify",
                    "feature_control.png": "operate"}
        _icon = self._node.node_icon_img
        return icon_map.get(_icon[_icon.rfind("/")+1:])

    def is_accordion(self):
        '''Test if node is accordion based on icon image and list of exclusions
        '''
        # at depth - 2
        not_accordion_items = ["All Services",
                               "Accordions",
                               "Template Access Rules",
                               "VM Access Rules"
                               ]
        if self.node_type == "node":
            if self._node.name not in not_accordion_items:
                return True

    def is_menu(self):
        '''Filter out RBAC items that aren't represented as menus
        '''
        # at depth (storage) and depth-1 (buttons)
        if self._node.name not in ["Storage", "Buttons"]:
            return True

    def is_enabled(self):
        '''check if menu is checked or checked_dim
        '''
        # all depths
        if self._node.is_checked or self._node.is_checked_dim:
            return True

    

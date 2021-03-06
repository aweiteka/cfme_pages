'''
Created on May 1, 2013

@author: bcrochet
'''
# -*- coding: utf-8 -*-

import pytest
import random
from unittestzero import Assert

@pytest.mark.nondestructive  # IGNORE:E1101
class TestProvisionVms:
    def test_provision_start(self, infra_vms_pg):
        Assert.true(infra_vms_pg.is_the_current_page)
        vmstart_pg = infra_vms_pg.click_on_provision_vms()

        for item in vmstart_pg.template_list.items:
            print item.name
            print item.operating_system
            print item.platform

        vm_pg = vmstart_pg.click_on_cancel()
        Assert.true(vm_pg.is_the_current_page)

    def __pick_random_template(self, vm_pg):
        number_of_templates = len(vm_pg.template_list.items)
        if not number_of_templates:
            raise IndexError("No templates defined")
        template = random.randint(0, number_of_templates - 1)
        vm_pg.template_list.items[template].click()

    def test_provision_continue(self, infra_vms_pg):
        Assert.true(infra_vms_pg.is_the_current_page)
        vmstart_pg = infra_vms_pg.click_on_provision_vms()
        self.__pick_random_template(vmstart_pg)
        prov_pg = vmstart_pg.click_on_continue()
        prov_pg.click_on_cancel()

    def test_provision_tabbuttons(self, infra_vms_pg):
        Assert.true(infra_vms_pg.is_the_current_page)
        vmstart_pg = infra_vms_pg.click_on_provision_vms()
        self.__pick_random_template(vmstart_pg)
        prov_pg = vmstart_pg.click_on_continue()
        from pages.services_subpages.provision_subpages.provision_request \
                import ProvisionRequest
        req_pg = prov_pg.tabbutton_region.current_tab
        Assert.equal(req_pg.__class__, ProvisionRequest,
                "Did not return ProvisionRequest")
        customize_pg = prov_pg.tabbutton_region.tabbutton_by_name(
                "Customize").click()
        from pages.services_subpages.provision_subpages.provision_customize \
                import ProvisionCustomize
        Assert.equal(customize_pg.__class__, ProvisionCustomize,
                "Did not return ProvisionCustomize")

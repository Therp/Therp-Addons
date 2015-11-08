# -*- coding: utf-8 -*-
"""Run branding company tests."""
##############################################################################
#
#    Copyright (C) 2015 Therp BV <http://therp.nl>.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.tests.common import TransactionCase

class TestBrandingCompany(TransactionCase):
    """Run branding company tests."""

    def setUp(self):
        super(TestBrandingCompany, self).setUp()
        # Create two branding companies
        branding_model = self.env['branding.company']
        self.jansen_branding = branding_model.create({
            'name': 'Jansen Company BV',
            'email': 'info@jansen.com',
            'rml_footer': 'Jansen for all your stuff',
        })
        self.pietersen_branding = branding_model.create({
            'name': 'Pietersen Company BV',
            'email': 'info@pietersen.com',
            'rml_footer': 'Pietersen ready to serve you',
        })
        # Get admin and Demo users, set Demo user, to use Jansen branding
        self.root_user = self.env.ref('base.user_root')
        self.root_user.branding_id = False
        self.demo_user = self.env.ref('base.user_demo')
        self.demo_user.branding_id = self.jansen_branding.id
        # Get ASUSTek and Agrolait partners, set Agrolait partner to use
        # Pietersen branding
        self.asustek_partner = self.env.ref('base.res_partner_1')
        self.asustek_partner.branding_id = False
        self.agrolait_partner = self.env.ref('base.res_partner_2')
        self.agrolait_partner.branding_id = self.pietersen_branding.id

    def test_branding_defaults(self):
        """Test basic methods on branding.company."""
        branding_model = self.env['branding.company']
        # Branding for demo user
        demo_branding = branding_model.get_user_branding(
            self.demo_user.id)
        self.assertEqual(
            self.jansen_branding.id, demo_branding.id,
            "Expected branding %d not equal to returned branding %d." %
            (self.jansen_branding.id, demo_branding.id)
        )
        # Admin user should not have branding
        self.assertFalse(
            branding_model.get_user_branding(self.root_user.id).id,
            "Got unexpected branding for Admin user."
        )
        # Branding for Agrolait partner
        agrolait_branding = branding_model.get_partner_branding(
            self.agrolait_partner.id)
        self.assertEqual(
            self.pietersen_branding.id, agrolait_branding.id,
            "Expected branding %d not equal to returned branding %d." %
            (self.pietersen_branding.id, agrolait_branding.id)
        )
        # ASUSTek partner should not have branding
        self.assertFalse(
            branding_model.get_partner_branding(
                self.asustek_partner.id).id,
            "Got unexpected branding for ASUSTek partner."
        )
        # Branding for Agrolait partner and demo user
        default_branding = branding_model.get_default_branding(
            self.agrolait_partner.id, self.demo_user.id)
        self.assertEqual(
            self.pietersen_branding.id, default_branding.id,
            "Expected branding %d not equal to returned branding %d." %
            (self.pietersen_branding.id, default_branding.id)
        )
        # No branding for ASUSTek partner and Admin user
        self.assertFalse(
            branding_model.get_default_branding(
                self.asustek_partner.id, self.root_user.id).id,
            "Got unexpected branding for ASUSTek partner and Admin user."
        )

    def test_sale_order(self):
        """Test branding on sale order."""
        # Models to use:
        so_model = self.env['sale.order']
        sol_model = self.env['sale.order.line']
        # Check wether default for user works:.
        so_defaults = so_model.sudo(
            self.demo_user
        ).default_get(['branding_id'])
        self.assertEqual(
            self.jansen_branding.id, so_defaults['branding_id'],
            "Expected branding %d not equal to returned branding %d." %
            (self.jansen_branding.id, so_defaults['branding_id'])
        )
        # Changing partner to Agrolait should give Pietersen branding:
        ret = so_model.sudo(
            self.demo_user
        ).onchange_partner_id(self.agrolait_partner.id)
        self.assertEqual(
            self.pietersen_branding.id, ret['value']['branding_id'],
            "Expected branding %d not equal to returned branding %d." %
            (self.pietersen_branding.id, ret['value']['branding_id'])
        )
        # Order line vals to use on all test orders
        pc_assemble_product = self.env.ref('product.product_product_3')
        sol_vals = sol_model.product_id_change(
            False, pc_assemble_product.id,
            partner_id=self.agrolait_partner.id,
        )['value']
        sol_vals['state'] = 'confirmed'
        sol_vals['product_id'] = pc_assemble_product.id
        # Check that a manual invoice for a sale order uses branding,
        # and an invoice after delivery also, by creating two sale orders.
        so_manual_vals = so_defaults.copy()
        so_manual_vals['partner_id'] = self.agrolait_partner.id
        so_manual_vals.update(ret['value'])
        # Create sales order already in manual state and invoice order
        so_manual_vals['order_policy'] = 'manual'
        so_manual_vals['state'] = 'manual'
        so_manual_vals['branding_id'] = self.jansen_branding.id
        so_manual = so_model.create(so_manual_vals)
        sol_vals['order_id'] = so_manual.id
        sol_model.create(sol_vals)
        so_manual.action_invoice_create()
        # We should have an invoice now...
        self.assertTrue(
            so_manual.invoice_ids,
            "No invoice created for manual policy sales order."
        )
        # ... and it should have jansen_branding
        self.assertEqual(
            self.jansen_branding.id, so_manual.invoice_ids.branding_id.id,
            "Expected branding %d not equal to invoice branding %d." %
            (self.jansen_branding.id, so_manual.invoice_ids.branding_id.id)
        )
        # Tried also to add a test with invoice created from shipping
        # but this failed due to strange intractions with delivery module.
        # This module adds a weight_uom_id as required field to stock_move
        # and stock_picking, resulting in a NULL value error.

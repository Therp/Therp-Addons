# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestTrpExternalUser(TransactionCase):
    def test_trp_external_user(self):
        external_user = self.env.ref("trp_external_user.user_external")
        # check some permissions
        with self.assertRaises(AccessError):
            self.env.ref("base.user_root").with_user(external_user).name
        self.assertEqual(
            self.env.ref("base.main_partner").name,
            self.env.ref("base.main_partner").with_user(external_user).name,
        )
        self.assertEqual(
            self.env.ref("base.res_partner_2").name,
            self.env.ref("base.res_partner_2").with_user(external_user).name,
        )
        self.assertEqual(
            external_user.name, external_user.with_user(external_user).name
        )
        # check flag
        self.assertTrue(external_user.is_external_user)
        self.assertFalse(self.env.ref("base.user_root").is_external_user)
        # check user creation
        test_user = self.env["res.users"].create(
            {"login": "some login", "name": "Some name"}
        )
        self.assertNotIn(self.env.ref("base.group_user"), test_user.groups_id)
        self.assertNotIn(
            self.env.ref("base.group_partner_manager"), test_user.groups_id
        )

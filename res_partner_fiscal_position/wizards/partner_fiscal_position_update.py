# -*- coding: utf-8 -*-
# © 2015 Therp BV (http://therp.nl).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import SUPERUSER_ID, _, api, fields, models


class PartnerFiscalPositionUpdate(models.TransientModel):
    """Add fiscal position to country."""
    _name = 'partner.fiscal.position.update'

    state = fields.Selection(
        selection=[
            ('specification', 'Specification'),
            ('done', 'Done'),
        ],
        default='specification',
        readonly=True,
    )
    all_partners = fields.Boolean(
        string='All partners',
        help="Set all partners, not only selected, to the fiscal position"
             " specified below. Processing will be done for the current"
             " company only!",
    )
    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Selected partners',
        readonly=True,
        help="Partners that will be updated.",
    )
    use_country = fields.Boolean(
        string='Fiscal position determined by country?',
        default=True,
        help="Use fiscal position from country for partner.",
    )
    override_current_position = fields.Boolean(
        string='Override current fiscal position in partner',
        default=True,
        help="Set fiscal position in partner, even when already specified.\n"
             "This might even clear an existing position, if an empty"
             " position is selected, or set according to country.",
    )
    ignore_company_country = fields.Boolean(
        string='Ignore partners in same country',
        default=True,
        help="Do not set fiscal positions for partners that are in the same"
             " country as the current company.\n"
             "This also ignores partners with no country set.",
    )
    property_account_position = fields.Many2one(
        comodel_name='account.fiscal.position',
        string="Fiscal Position",
        company_dependent=True,
        help="The fiscal position will determine"
             " taxes and the accounts used for the country,"
             " if not set specifically elsewere.",
    )
    result_message = fields.Text(
        string='Result of wizard processing',
        readonly=True,
    )

    @api.model
    def default_get(self, field_names):
        """Store selected partner ids, if any."""
        res = super(PartnerFiscalPositionUpdate, self).default_get(field_names)
        partner_ids = self._context.get('active_ids', False)
        if partner_ids:
            res['partner_ids'] = partner_ids
        else:
            res['all_partners'] = True
        return res

    def _add_result_message(self, message):
        """Add message separated by blank line to result message."""
        self.result_message = (
            (self.result_message and self.result_message + '\n\n' or '') +
            message
        )

    @api.multi
    def process_selection(self):
        """Set fiscal position selected on specified partners."""
        domain = []
        counter = 0
        if self.partner_ids and not self.all_partners:
            domain += [('id', 'in', self.partner_ids._ids)]
        if not self.override_current_position:
            domain += [('property_account_position', '=', False)]
        if self.ignore_company_country:
            user = self.env['res.users'].browse(self.env.uid)
            user_country = user.company_id.partner_id.country_id
            if user_country:
                domain += [
                    ('country_id', '!=', False),
                    ('country_id', '!=', user_country.id),
                ]
        # Prevent unneeded i/o and dummy updates by filtering out
        # records that already have the desired fiscal position:
        if self.use_country:
            domain += [
                '|',
                ('property_account_position', '=', False),
                ('property_account_position', '!=',
                 'country_id.property_account_position'
                ),
            ]
        else:
            domain += [
                '|',
                ('property_account_position', '=', False),
                ('property_account_position', '!=',
                 self.property_account_position.id
                ),
            ]
        # Also filter out records that use their parents accounting settings:
        domain += [
            '|',
            ('parent_id', '=', False),
            ('is_company', '=', True),
        ]
        for partner in self.env['res.partner'].search(domain):
            counter += 1
            if self.use_country:
                partner.property_account_position = (
                    partner.country_id.property_account_position)
            else:
                partner.property_account_position = (
                    self.property_account_position)
        if counter > 0:
            if self.use_country:
                self._add_result_message(
                    _("%d partners had their fiscal position set,"
                      " according to country."
                     ) % counter
                )
            else:
                self._add_result_message(
                    _("%d partners had their fiscal position set to %s.") %
                    (counter, self.property_account_position.display_name)
                )
        if (not self.all_partners and self.partner_ids and
                counter < len(self.partner_ids)):
            ignored = len(self.partner_ids) - counter
            self._add_result_message(
                _("%d partners were ignored because they did not meet the"
                  " selection criteria, or already had the right fiscal"
                  " position."
                 ) % ignored
            )
        if self.env.uid == SUPERUSER_ID:
            self._add_result_message(
                _("ADMIN INFO. Domain used to read parters was:\n%s") %
                str(domain)
            )
        self.state = 'done'
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': self._name,
            'res_id': self.id,
            'target': 'new',
        }

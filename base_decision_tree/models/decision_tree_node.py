# -*- coding: utf-8 -*-
# Copyright 2020 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class DecisionTreeNode(models.Model):
    _name = 'decision.tree.node'
    _description = 'A node in a decision tree'
    _order = 'sequence'

    name = fields.Char(required=True)
    description = fields.Html()
    sequence = fields.Integer()
    parent_id = fields.Many2one(
        'decision.tree.node', index=True, ondelete='cascade',
    )
    link_id = fields.Many2one(
        'decision.tree.node',
        help='This node will be replaced by the node (subtree) it links to',
    )
    branch_name = fields.Char()
    child_ids = fields.One2many('decision.tree.node', 'parent_id', 'Children')
    cheapo_html_rendering = fields.Html(
        compute='_compute_cheapo_html_rendering', sanitize=False,
    )

    @api.multi
    @api.depends('name', 'child_ids')
    def _compute_cheapo_html_rendering(self):
        for this in self:
            this.cheapo_html_rendering = self.env.ref(
                'base_decision_tree.qweb_decision_tree_node'
            ).render({'object': this})

    # TODO: constraints for circularity, self-referencing in links,
    #       either link or children
    #       mail.thread (or do we want this on document.page in the end? maybe)
    #       implement links

# Copyright (C) 2019, Patrick Wilson
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class FSMOrder(models.Model):
    _inherit = "fsm.order"

    opportunity_id = fields.Many2one("crm.lead", tracking=True)
    opportunity_customer_vat = fields.Char(
        related="opportunity_id.partner_id.vat", string="Customer VAT"
    )
    sales_person_id = fields.Many2one(
        related="opportunity_id.user_id", string="Salesperson"
    )

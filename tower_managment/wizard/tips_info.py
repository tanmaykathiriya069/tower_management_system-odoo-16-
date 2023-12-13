from odoo import fields,models
from datetime import datetime


class TipsInfoWizard(models.TransientModel):

    _name="tips.info"

    _description="Tips Info Wizard"

    name=fields.Char("Name")

    def confirm(self):
        print("Confirm button Press.. ")

        self.env['res.partner'].create({'name': self.name})

    




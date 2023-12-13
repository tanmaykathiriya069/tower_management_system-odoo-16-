from odoo import fields,models,api



class towersInfoWizard(models.TransientModel):

    _name="sale.info"
    _description="Tower Info Wizard"


    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")

    status_selection=fields.Selection([('draft','Quotation'),('sale','Sale Order'),('both','Both')],string='Status')

    

    def generate_report(self):
        print("Self.................")

        # res = self.env['sale.order'].search([('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date)])
        # for doc in res:
        #     print("Res..............",doc.name)
        state = []
        if self.status_selection == 'both':
            state.append('sale')
            state.append('draft')
        elif self.status_selection:
            state.append(self.status_selection)
        data = {
            'start_date':self.start_date,
            'end_date':self.end_date,
            # 'res': res
            'state':state,    
        }

        
        # data['res'] = res

        return self.env.ref('tower_managment.action_order_report').report_action(self,data=data)
    
class SaleReport(models.AbstractModel):
    _name = 'report.tower_managment.order_report'
    _description = "Order Report Abstract Model"

    @api.model
    def _get_report_values(self, docids, data=None):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        status = data.get('state')
        
        docs = self.env['sale.order'].search([('create_date', '>=', start_date), ('create_date', '<=', end_date),('state','in',status)])
        return {
            'docs': docs
        }
        
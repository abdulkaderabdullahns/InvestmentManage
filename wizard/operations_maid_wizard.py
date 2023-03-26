from datetime import  datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import datetime


class OperationsMaidWizard(models.TransientModel):
    _name = 'operations_maid.report.wizard'

    from_date = fields.Date('Till Day', default=fields.Date.today())
    # fin_type = fields.Selection(
    #     [("Agricultural Finance", "Agricultural Finance"), ("Animal Finance", "FemAnimal Financeale"),
    #     ("Microfinance", "Microfinance"), ("other", "Other")])

    # section_id = fields.Many2one("bank.section", string="Section ", ondelete="cascade")
    # activity_id = fields.Many2one("bank.activity", string="Activity ", ondelete="cascade")
    # formula_id = fields.Many2one("bank.formula", string="Formula ", ondelete="cascade")

    @api.constrains('from_date')
    def _check_date(self):
        if self.from_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))
   
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'from_date': fields.Date.from_string(self.from_date),
                # 'fin_type':self.fin_type,
                # 'section_id':self.section_id,
                # 'activity_id':self.activity_id,
                # 'formula_id':self.formula_id,
            },
        }
        return self.env.ref('bank.operations_maid_report').report_action(self, data=data)

class OperationsMaidReport(models.AbstractModel):
    _name = 'report.bank.operations_maid_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        
        from_date = data['form']['from_date']
        # fin_type = data['form']['fin_type']
        # section_id = data['form']['section_id']
        # activity_id = data['form']['activity_id']
        # formula_id = data['form']['formula_id']
        docs = self.env['bank.transaction_installments'].search([('req_date', '>=', from_date)])

        # domain = [('req_date', '<=', to_date),('fin_type', '=', fin_type)]
        # section_id_temp = 'no'
        # activity_id_temp = 'no'
        # formula_id_temp = 'no'

        # if section_id:
        #     domain.append(('section_id', '=', section_id))
        #     section_id_temp = self.env['bank.finance_request'].search([('id', '=', 'section_id')])
        #     section_id_temp = section_id_temp.name

        # if activity_id:
        #     domain.append(('activity_id', '=', activity_id))
        #     activity_id_temp = activity_id_temp

        # if formula_id:
        #     domain.append(('formula_id', '=', formula_id))
        #     formula_id_temp = formula_id_temp

        # docs = self.env['bank.finance_request'].search(domain)

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],

            
            'from_date': from_date,
            # 'fin_type': fin_type,
            # 'section_id': section_id_temp,
            # 'activity_id': activity_id_temp,
            # 'formula_id':formula_id_temp,

            'docs': docs,
        }


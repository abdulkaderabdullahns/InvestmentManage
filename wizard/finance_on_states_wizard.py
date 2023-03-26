from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import datetime

class FinanceOnStatesReportWizard(models.TransientModel):
    _name = 'finance_on_states.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())
    to_date = fields.Date('To', default=fields.Date.today())

    @api.constrains('from_date')
    def _check_date_from(self):
        if self.from_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

    @api.constrains('to_date')
    def _check_date_to(self):
        if self.to_date < datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))


    def get_state_data(self, from_date, to_date):
        lines = []
        finance_request_data =self.env['bank.finance_request'].search([])
        state_list =finance_request_data.mapped('states_id')

        
        total_state_amount = sum(finance_request_data.mapped('amount_cert'))
        self.env['bank.states'].search([]).write({"state_share": 0})

        for state in state_list:
            state_amount = sum(finance_request_data.filtered(lambda p: p.states_id == state).mapped('amount_cert'))
            state_share = round((state_amount / total_state_amount) * 100, 2)

            lines.append({
                'state': state.states_id,
                'state_amount': state_amount,
                'state_share': state_share,
            })
            state.state_share = state_share

        return lines

    def get_report(self):
        state_data = self.get_state_data(self.from_date, self.to_date)
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'data': state_data,

            
            }
        
        return self.env.ref('bank.finance_on_states_report').report_action(self, data=data)

    def get_chart(self):
        state_data = self.get_state_data(self.from_date, self.to_date)
        action = {
            'view_mode': 'graph',
            'res_model': 'bank.states',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'name': _('Finance On States In Period From: {} To: {}'.format(self.from_date, self.to_date)),
        }
        return action 

class FinanceOnStatesReport(models.AbstractModel):
    _name = 'report.bank.finance_on_states_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'docs': data.get('data'),
            'from_date': data.get('from_date'),
            'to_date': data.get('to_date'),
        }


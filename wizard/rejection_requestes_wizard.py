from odoo import models, fields, api
from datetime import  datetime
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import datetime

class RejectionRequestReportWizard(models.TransientModel):
    _name = 'rejection_requestes.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())
    to_date = fields.Date('To', default=fields.Date.today())

    state = fields.Selection(selection=([
        # ('accept', 'Accept'),
        ('cancel', 'Cancel'),
    ]), string='Status',tracking=True)

    @api.constrains('from_date')
    def _check_date_from(self):
        if self.from_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

    @api.constrains('to_date')
    def _check_date_to(self):
        if self.to_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

    # by = fields.Selection(selection=([
    #     ('fin_type', 'Finance Type'),
    #     ('number', 'Animal'),
    #     ('nbati', 'Nbati'),
    #
    #     ('number_id', 'Activity'),
    #     ('for_number', 'Formula'),
    #     ]),string='by_select',tracking=True)
    #
    # number = fields.Many2one("bank.section", string="Section")


    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'from_date': fields.Date.from_string(self.from_date),
                'to_date': fields.Date.from_string(self.to_date),
                'state': self.state,
                # 'by': self.by,
                # 'number': self.number.id,
            },
        }

        return self.env.ref('bank.rejection_requestes_report').report_action(self, data=data)


class RejectionRequestReport(models.AbstractModel):
    _name = 'report.bank.rejection_requestes_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        state = data['form']['state']
        # by = data['form']['by']
        # number = data['form']['number']
        #
        # if number:
        #
        #      docs = self.env['bank.finance_request'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date),
        #                                                 ('number','=',number)])
        if state:
            docs = self.env['bank.finance_request'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date),
                                                   ('state','=',state)])

        else:
            docs = self.env['bank.finance_request'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date)])

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],

            'from_date': from_date,
            'to_date': to_date,
            'state': state,
            # 'by':by,

            'docs': docs,
        }

# class FinanceRequestReportWizard(models.TransientModel):
#     _name = 'finance_request.report.wizard'

#     from_date = fields.Date('From', default=fields.Date.today())
#     to_date = fields.Date('To', default=fields.Date.today())
#     state = fields.Selection(selection=[
#         ('accept', 'Accept'),
#         ('cancel', 'cancelled'),
#     ], string='Status', tracking=True)
#     def get_report(self):
#         data = {
#             'ids': self.ids,
#             'model': self._name,
#             'form': {
#                 'from_date': fields.Date.from_string(self.from_date),
#                 'to_date': fields.Date.from_string(self.to_date),
#                 'state': fields.Selection(self.state),
#             },
#         }
#         return self.env.ref('bank.finance_request_report').report_action(self, data=data)

# class FinanceRequestReport(models.AbstractModel):
#     _name = 'report.bank.finance_request_template'

#     @api.model
#     def _get_report_values(self, docids, data=None):
#         from_date = data['form']['from_date']
#         to_date = data['form']['to_date']

#         docs = self.env['bank.finance_request'].search([('req_date', '>=', from_date), ('req_date', '<=', to_date)])

#         return {
#             'doc_ids': data['ids'],
#             'doc_model': data['model'],

#             'from_date': from_date,
#             'to_date': to_date,
#             'docs': docs,
#         }


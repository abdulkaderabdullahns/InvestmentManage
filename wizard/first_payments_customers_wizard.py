from odoo import models, fields, api


class FirstpaymentscustomerstypeReportWizard(models.TransientModel):
    _name = 'first_payments_customers.report.wizard'

    from_date = fields.Date('From', default=fields.Date.today())
    to_date = fields.Date('To', default=fields.Date.today())

    fin_type = fields.Selection(
        [("Agricultural Finance", "تمويل الزراعي"), ("Animal Finance", "FemAnimal Financeale"),
         ("Microfinance", "Microfinance"), ("other", "Other")], defualt="Agricultural Finance", string="Finance Type",
        Tracking=True)

    name_section = fields.Many2one("bank.section",string='Section')
    name_activity = fields.Many2one("bank.activity", string="Activity ")
    for_number = fields.Many2one("bank.formula", string="Formula ")


    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'from_date': fields.Date.from_string(self.from_date),
                'to_date': fields.Date.from_string(self.to_date),
                'fin_type':self.fin_type,
                'name_section': self.name_section.id,
                'name_activity': self.name_activity.id,
                'for_number': self.for_number.id,

                # 'state': self.state,
                # 'by': self.by,
                # 'number': self.number.id,
            },
        }

        return self.env.ref('bank.first_payments_customers_report').report_action(self, data=data)


class FirstpaymentscustomerstypeReport(models.AbstractModel):
    _name = 'report.bank.first_payments_customers_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        from_date = data['form']['from_date']
        to_date = data['form']['to_date']
        fin_type = data['form']['fin_type']
        name_section = data['form']['name_section']
        name_activity = data['form']['name_activity']
        for_number = data['form']['for_number']

        # state = data['form']['state']
        # by = data['form']['by']
        # number = data['form']['number']
        #


        if fin_type:
            docs = self.env['bank.first_payments_customers'].search(
                [('request_date', '>=', from_date), ('request_date', '<=', to_date),
                 ('fin_type', '=', fin_type)])

        if name_section:
             docs = self.env['bank.first_payments_customers'].search([('request_date', '>=', from_date), ('request_date', '<=', to_date),
                                                        ('name_section','=',name_section)])
        if name_activity:
            docs = self.env['bank.first_payments_customers'].search([('request_date', '>=', from_date), ('request_date', '<=', to_date),
                                                   ('name_activity','=',name_activity)])
        if for_number:
            docs = self.env['bank.first_payments_customers'].search([('request_date', '>=', from_date), ('request_date', '<=', to_date),
                                                   ('for_number','=',for_number)])


        # # if:
        # docs = self.env['bank.first_payments_customers'].search([('request_date', '>=', from_date), ('request_date', '<=', to_date),
        #                                                 ('fin_type', '=', fin_type)])

        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],

            'from_date': from_date,
            'to_date': to_date,
            'fin_type':fin_type,
            'name_section': name_section,
            'name_activity': name_activity,
            'for_number': for_number,
            # 'state': state,
            # 'by':by,

            'docs': docs,
        }

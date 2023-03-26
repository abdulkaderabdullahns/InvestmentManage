from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import re
import datetime


# from datetime import date


#
# 
# Create Reverenced Models
# 
# 

# Create Model States

class Imags(models.Model):
    _name = "bank.imag"

    image = fields.Image(string="Image")


class States(models.Model):
    _name = "bank.states"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "states_id"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    # numer = fields.Integer(string="State Number", required="1")
    states_id = fields.Char(string="State ", Tracking="1")
    state_share = fields.Float()

    # localities_num = fields.Many2one("bank.localities", "Localities", ondelete="cascade")
    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('states.sequence.code') or 'New'
        return super(States, self).create(vals)

    @api.constrains('states_id')
    def check_number(self):
        states = self.env['bank.states'].search([('id', '!=', self.id), ('states_id', '=', self.states_id)])
        if states:
            raise ValidationError(("State nume must be unique!"))

    @api.constrains('states_id')
    def check_name(self):
        for i in self.states_id:
            if i.isdigit():
                raise ValidationError(("State name must be name!"))


# Create Model Localities

class Localities(models.Model):
    _name = "bank.localities"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "localities_id"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))

    localities_id = fields.Char(string="Name", required="1", Tracking=True)
    states_id = fields.Many2one("bank.states", "State ", ondelete="cascade", Tracking=True)
    locality_share = fields.Float()

    @api.constrains('name')
    def check_name(self):
        for i in self.name:
            if i.isdigit():
                raise ValidationError(("Localities name must be name!"))

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('localities.sequence.code') or 'New'
        return super(Localities, self).create(vals)

    @api.constrains('localities_id')
    def check_number(self):
        localities = self.env['bank.localities'].search(
            [('id', '!=', self.id), ('localities_id', '=', self.localities_id)])
        if localities:
            raise ValidationError(("Locality number must be unique!"))


# Create Model Job

class Job(models.Model):
    _name = "bank.job"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name_job"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    # number = fields.Integer(string="Job Number", required=1)
    name_job = fields.Char(string="Job", required="1", Tracking=True)

    @api.constrains('name_job')
    def check_name(self):
        for i in self.name_job:
            if i.isdigit():
                raise ValidationError(_("job name must be name!"))

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('job.sequence.code') or 'New'
        return super(Job, self).create(vals)

    @api.constrains('name_job')
    def check_number(self):
        jobs = self.env['bank.job'].search([('id', '!=', self.id), ('name_job', '=', self.name_job)])
        if jobs:
            raise ValidationError(("Job name must be unique!"))


# Create Model Customers

class Customers(models.Model):
    _name = "bank.customers"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    image = fields.Image(string="Image", Tracking=True)
    customer_id = fields.Char(string="Customer Number", Tracking=True)
    email = fields.Char(string="Email")
    name = fields.Char(string="Customers Name", Tracking=True)
    # phone = fields.Integer(string="Phone")
    phones = fields.Char(string="Phone", Tracking=True)
    Gender = fields.Selection([("male", "Male"), ("female", "Female"), ("other", "Other")], defualt="Male",
                              Tracking=True)
    birth = fields.Date("Birth Date", Tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    address = fields.Text("Address", Tracking=True)
    job_id = fields.Many2one("bank.job", string="Job ", ondelete="cascade", Tracking=True)
    social_state = fields.Selection(
        [("single", "Single"), ("married", "Married"), ("married", "Married"), ("absolute", "Absolute"),
         ("unmarried", "Unarried")], default='single', Tracking=True)
    states_id = fields.Many2one("bank.states", string="State ", ondelete="cascade", Tracking=True)
    localities_id = fields.Many2one("bank.localities", string="Localities ", ondelete="cascade", Tracking=True)

    # @api.constrains('email')
    # def _check_email(self):
    #     for customers in self:
    #         if customers.email and not tools.email_re.match(customers.email):
    #             raise ValidationError('Invalid Email Address!')

    @api.depends('birth')
    def _compute_age(self):
        today = date.today()
        for customers in self:
            if customers.birth:
                birth = fields.Date.from_string(customers.birth)
                customers.age = today.year - birth.year
            else:
                customers.age = 0

    _sql_constraints = [
        ('age_constraint', 'CHECK(age >= 18)', 'Age must be greater than or equal to 18.')

    ]

    @api.constrains('age')
    def _check_date(self):
        if self.age < 18:
            raise ValidationError(_('Do not enter a date greater than todays date'))

    # def action_submit(self):
    #
    #     body = ('<strong>You have new penalty<br/>click here to view it: </strong>')
    #     body += '<a href=# data-oe-model=employee.penalty data-oe-id=%d>%s</a>' % (self.id, self.employee_id.name)
    #     if self.employee_id.work_email and self.employee_id.address_home_id:
    #         mail_details = {
    #             'subject': "{} Penalty".format(self.employee_id.name),
    #             'body': body,
    #             'partner_ids': [self.employee_id.address_home_id.id],
    #             'message_type': 'email',
    #             'email_to': self.employee_id.work_email or False
    #         }
    #         self.message_post(**mail_details)
    #     self.state = 'waiting_approval'
    #
    # @api.returns('mail.message', lambda value: value.id)
    # def message_post(self, **kwargs):
    #     return super(EmployeePenalty, self.with_context(
    #         mail_post_autofollow=self.env.context.get('mail_post_autofollow', True))).message_post(**kwargs)

    @api.constrains('name')
    def check_name(self):
        for i in self.name:
            if i.isdigit():
                raise ValidationError(_("name name must be name!"))

    @api.constrains('phones')
    def _check_number_field_length(self):
        for record in self:
            if record.phones and len(str(record.phones)) != 10:
                raise models.ValidationError('Number Phone must be a 10-digit integer.')

    @ api.constrains('customer_id')
    def _check_number_field_length_customer_id(self):
        for record in self:
            if record.customer_id and len(str(record.customer_id)) != 10:
                raise models.ValidationError(' Customer Id must be a 10-digit integer.')

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('customers.sequence.code') or 'New'
        return super(Customers, self).create(vals)

    @api.constrains('customer_id')
    def check_customer_id(self):
        customers = self.env['bank.customers'].search([('id', '!=', self.id), ('customer_id', '=', self.customer_id)])
        if customers:
            raise ValidationError(("Customer number must be unique!"))

    @api.onchange('states_id')
    def _get_locality(self):
        locality_list = []

        localities = self.env['bank.localities'].search([('states_id', '=', self.states_id.id)])

        if localities:

            for locality in localities:
                locality_list.append(locality.id)
        return {'domain': {'localities_id': [('id', 'in', locality_list)]},
                'value': {'locality_id': localities[0].id if len(localities) > 0 else None}}


# Create Model Section

class Section(models.Model):
    _name = "bank.section"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name_section"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    name_section = fields.Char(string="Section Name", Tracking=True)
    section_share = fields.Float()

    # activity_id = fields.One2many('bank.activity', 'section_id', string="activity_id")
    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('section.sequence.code') or 'New'
        return super(Section, self).create(vals)

    @api.constrains('name')
    def check_number(self):
        sections = self.env['bank.section'].search([('id', '!=', self.id), ('name', '=', self.name)])
        if sections:
            raise ValidationError(("Section name must be unique!"))


# Create Model Activity

class Activity(models.Model):
    _name = "bank.activity"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name_activity"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    name_activity = fields.Char(string="Activity Name", Tracking=True)
    name_section = fields.Many2one('bank.section', string='section')

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('activity.sequence.code') or 'New'
        return super(Activity, self).create(vals)

    @api.constrains('name_activity')
    def check_number(self):
        activity = self.env['bank.activity'].search([('id', '!=', self.id), ('name_activity', '=', self.name_activity)])
        if activity:
            raise ValidationError(("Activity name must be unique!"))


# Create Model Formula

class Formula(models.Model):
    _name = "bank.formula"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name_formula"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    name_formula = fields.Char(string="Formula Name", Tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('formula.sequence.code') or 'New'
        return super(Formula, self).create(vals)

    @api.constrains('name_formula')
    def check_number(self):
        formulas = self.env['bank.formula'].search([('id', '!=', self.id), ('name_formula', '=', self.name_formula)])
        if formulas:
            raise ValidationError(("Formula name must be unique!"))


# Create Model Gurantee

class Gurantee(models.Model):
    _name = "bank.gurantee"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name_gurantee"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    name_gurantee = fields.Char(string="Gurantee Name", Tracking=True)
    color = fields.Integer('Color Index')

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('gurantee.sequence.code') or 'New'
        return super(Gurantee, self).create(vals)

    @api.constrains('name_gurantee')
    def check_number(self):
        gurantee = self.env['bank.gurantee'].search([('id', '!=', self.id), ('name_gurantee', '=', self.name_gurantee)])
        if gurantee:
            raise ValidationError(("gurantee name must be unique!"))


# Create Model Rejection_Reasons

class Rejection_Reasons(models.Model):
    _name = "bank.rejection_reasons"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _rec_name = "name_rejection_reasons"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    name_rejection_reasons = fields.Char(string="Rejection_Reasons Name", Tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('rejection_reasons.sequence.code') or 'New'
        return super(Rejection_Reasons, self).create(vals)

    @api.constrains('name_rejection_reasons')
    def check_number(self):
        rejection_reasons = self.env['bank.rejection_reasons'].search(
            [('id', '!=', self.id), ('name_rejection_reasons', '=', self.name_rejection_reasons)])
        if rejection_reasons:
            raise ValidationError(("Rejection reasons name must be unique!"))


# Create Model Stumbling_Reasons

class Stumbling_Reasons(models.Model):
    _name = "bank.stumbling_reasons"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name_stumbling_reasons"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    name_stumbling_reasons = fields.Char(string="Stumbling_Reasons Name", Tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('stumbling_reasons.sequence.code') or 'New'
        return super(Stumbling_Reasons, self).create(vals)

    @api.constrains('name_stumbling_reasons')
    def check_number(self):
        stumbling_reasons = self.env['bank.stumbling_reasons'].search(
            [('id', '!=', self.id), ('name_stumbling_reasons', '=', self.name_stumbling_reasons)])
        if stumbling_reasons:
            raise ValidationError(("Stumbling reasons name must be unique!"))


# Create Model Judges

class Judges(models.Model):
    _name = "bank.judges"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name_judges"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    name_judges = fields.Char(string="Judge Name", Tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('judges.sequence.code') or 'New'
        return super(Judges, self).create(vals)

    @api.constrains('name_judges')
    def check_number(self):
        judges = self.env['bank.judges'].search(
            [('id', '!=', self.id), ('name_judges', '=', self.name_judges)])
        if judges:
            raise ValidationError(("Judges name must be unique!"))


# Create Model Court

class Courts(models.Model):
    _name = "bank.courts"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name_courts"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    name_courts = fields.Char(string="Court Name", Tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('courts.sequence.code') or 'New'
        return super(Courts, self).create(vals)

    @api.constrains('name_courts')
    def courts(self):
        courts = self.env['bank.courts'].search(
            [('id', '!=', self.id), ('name_courts', '=', self.name_courts)])
        if courts:
            raise ValidationError(("Courts name must be unique!"))


# Create Transaction Models

# Create Model Job_detalls

class Job_detalls(models.Model):
    _name = "bank.job_detalls"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "customer_id"

    sequence = fields.Char("Sequence", default='New', copy=False)
    customer_id = fields.Many2one("bank.customers", "Customer id", ondelete="cascade", Tracking=True)
    job_date = fields.Date(string="Job Date", default=fields.Date.today(), Tracking=True)
    job_id = fields.Many2one("bank.job", "Job id", ondelete="cascade", Tracking=True)


# Create Model Social_State

class Social_State(models.Model):
    _name = "bank.social_state"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    sequence = fields.Char("Sequence", default='New', copy=False)
    customer_id = fields.Many2one("bank.customers", "Customer id", ondelete="cascade", Tracking=True)
    state_date = fields.Date(string="State Date", default=fields.Date.today(), Tracking=True)
    social_state = fields.Selection(
        [("single", "Single"), ("married", "Married"), ("married", "Married"), ("absolute", "Absolute"),
         ("unmarried", "Unarried")], default='Single', Tracking=True)


# Create Model Finance_Request


class Finance_Request(models.Model):
    _name = "bank.finance_request"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "requer_num"

    # name = fields.Char(string="Name")
    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    requer_num = fields.Char(string="Request Id", Tracking=True, readonly=True)
    req_date = fields.Date(required=1, string="Request Date", default=fields.Date.today(), Tracking=True)
    customer_id = fields.Many2one("bank.customers", string="Customer Number", required='1', Tracking=True)
    customer_image = fields.Image(string="Image", related='customer_id.image', Tracking=True)
    customer_name = fields.Char(string=" Name", related='customer_id.name', Tracking=True)
    customer_phone = fields.Char(string="Phone ", related='customer_id.phones', Tracking=True)
    states_id = fields.Many2one("bank.states", string="State", related='customer_id.states_id', ondelete="cascade",
                                Tracking=True)
    localities_id = fields.Many2one("bank.localities", string="Localities ", ondelete="cascade", Tracking=True)

    fin_type = fields.Selection(
        [("Agricultural Finance", "تمويل الزراعي"), ("Animal Finance", " تمويل حيواني "),
         ("Microfinance", "تمويل اصغر")], string="Finance Type",
        Tracking=True)
    name_section = fields.Many2one("bank.section", string="Section ", required='1', Tracking=True)
    name_activity = fields.Many2one("bank.activity", string="Activity ", required='1', Tracking=True)
    for_number = fields.Many2one("bank.formula", string="Formula ", required='1', Tracking=True)
    req_amount = fields.Float(string="Request Amount", required='1', default=1, Tracking=True)
    Gurantee_ids = fields.Many2many("bank.gurantee", string="Gurantee ", required='1', Tracking=True)
    reason = fields.Many2one("bank.rejection_reasons", "Rejection Reasons ", Tracking=True)
    amount_cert = fields.Float(string="Amount Certified", Tracking=True)
    date_certified = fields.Date(string=" Certified Date", Tracking=True, default=fields.Date.today())
    total_amount = fields.Float(compute='compute_amount')
    state = fields.Selection(selection=[
        ('accept', 'Accept'),
        ('cancel', 'Decline'),
        ('draft', 'Draft'),
    ], string='Status', default='draft', readonly=True, copy=False, tracking=True)
    finance_share = fields.Float()

    # def compute_random(self):
    #     x = str(datetime.now().year+math.random())
    #     return x

    # @api.constrains('requer_num')
    # def _check_number_field_length_requer_num(self):
    #     for record in self:
    #         if record.requer_num and len(str(record.requer_num)) >= 5:
    #             raise models.ValidationError('Number field must be a 5-digit integer.')

    def compute_amount(self):
        for rece in self:
            if not rece.amount_cert:
                rece.total_amount = 0.0
            else:
                rece.total_amount += rece.amount_cert

    @api.constrains('date_certified')
    def _check_date(self):
        if self.date_certified > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

        elif self.date_certified < datetime.date.today():
            raise ValidationError(_('Do not enter a date less than todays date'))

    @api.onchange('states_id')
    def compute_amount_cert(self, vals):
        sum = 0
        record_search = self.env['bank.finance_request'].search([('states_id', '=', self.states_id)])
        for rec in record_search:
            sum += rec.amount_cert
        return sum

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('finance_request.sequence.code') or 'New'
        if vals.get('requer_num', 'New') == 'New':
            vals['requer_num'] = self.env['ir.sequence'].next_by_code('Requestnumber.code') or 'New'
        return super(Finance_Request, self).create(vals)

    @api.constrains('amount_cert')
    def get_amount_cert(self):
        if self.amount_cert > self.req_amount:
            raise ValidationError('{self.amount_cert} Must Be Less Than {self.req_amount}')

    @api.constrains('req_amount')
    def check_req_amount(self):
        if self.req_amount < 0.00:
            raise ValidationError("xxxxxxx")
        elif self.req_amount == 0.0:
            raise ValidationError("xxxxxxx")

    def action_accept(self):
        return self.write({'state': 'accept'})

    def action_draft(self):
        return self.write({'state': 'draft'})

    def action_cancel(self):
        return self.write({'state': 'cancel'})

    @api.constrains('req_date')
    def _check_date(self):
        if self.req_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

        elif self.req_date < datetime.date.today():
            raise ValidationError(_('Do not enter a date less than todays date'))

    @api.constrains('date_certified')
    def _check_date_date_certified(self):
        if self.date_certified > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

        elif self.date_certified < datetime.date.today():
            raise ValidationError(_('Do not enter a date less than todays date'))

    @api.constrains('requer_num')
    def check_number(self):
        finance_Request = self.env['bank.finance_request'].search(
            [('id', '!=', self.id), ('requer_num', '=', self.requer_num)])
        if finance_Request:
            raise ValidationError(("requer number number must be unique!"))

    @api.onchange('name_section')
    def _get_activity(self):
        activity_list = []

        activitys = self.env['bank.activity'].search([('name_section', '=', self.name_section.id)])

        if activitys:
            for ax in activitys:
                activity_list.append(ax.id)
        return {'domain': {'name_activity': [('id', 'in', activity_list)]},
                'value': {'name_activity': activitys[0].id if len(activitys) > 0 else None}}


# Create Model First_Payments_Customers

class First_Payments_Customers(models.Model):
    _name = "bank.first_payments_customers"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "number"
    _sql_constraints = [('name_unique', 'unique(number)', 'hgsbcavchvhsa')]

    def get_domain(self):
        requset = []
        record = self.env["bank.finance_request"].search([('state', '=', 'accept')])
        for rec in record:
            requset.append(rec.id)
        return [('id', 'in', requset)]

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    number = fields.Many2one("bank.finance_request", string="Request id", domain=get_domain, ondelete="cascade",
                             required='1', Tracking=True)
    request_date = fields.Date(related='number.req_date', string="Request Date", tracking=True, Tracking=True)
    customer_id = fields.Many2one('bank.customers', related='number.customer_id')
    customer_name = fields.Char(string=" Name", related='customer_id.name')

    advance_amount = fields.Float(string="Advance Amount", required='1', Tracking=True)
    amount_cert = fields.Float(related='number.amount_cert', string="Amount Certified", Tracking=True)
    rem_amount = fields.Float(compute='_compute_amount', string="Remaining Amount", Tracking=True)
    advance_date = fields.Date(string="Advance Date", default=fields.Date.today(), Tracking=True)
    fin_type = fields.Selection(related='number.fin_type')
    name_section = fields.Many2one('bank.section', related='number.name_section')
    name_activity = fields.Many2one('bank.activity', related='number.name_activity')
    for_number = fields.Many2one('bank.formula', related='number.for_number')

    # @api.constrains('requer_num')
    # def check_number(self):
    #     finance_Request = self.env['bank.first_payments_customers'].search(
    #         [('id', '!=', self.id), ('number', '=', self.number)])
    #     if finance_Request:
    #         raise ValidationError(("requer number number must be unique!"))

    #
    # @api.constrains('number')
    # def create(self):
    #     finance_Request = self.env['bank.first_payments_customers'].search(
    #         [('id', '!=', self.id), ('number', '=', self.number)])
    #     if finance_Request:
    #         raise ValidationError(("requer number number must be unique!"))

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('first_payments_customers.sequence.code') or 'New'
        return super(First_Payments_Customers, self).create(vals)

    @api.model
    def create(self, vals):
        if vals.get('number', 'New') == 'New':
            vals['number'] = self.env['ir.number']
        return super(First_Payments_Customers, self).create(vals)
        raise ValidationError(_('Do not enter a date less than todays date'))

    @api.constrains('advance_amount')
    def get_amount_cert(self):
        if self.advance_amount > self.amount_cert:
            raise ValidationError('{self.advance_amount} Must Be Less Than {self.amount_cert}')

    @api.depends('advance_amount', 'amount_cert')
    def _compute_amount(self):
        for rec in self:
            rec.rem_amount = (rec.amount_cert - rec.advance_amount)

    @api.constrains('advance_date')
    def _check_date(self):
        if self.advance_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

        elif self.advance_date < datetime.date.today():
            raise ValidationError(_('Do not enter a date less than todays date'))


# Create Model Transaction_installments

class Transaction_installments(models.Model):
    _name = "bank.transaction_installments"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "requer_num"
    _sql_constraints = [('name_unique', 'unique(requer_num)', 'hgsbcavchvhsa')]

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'), Tracking=True)
    requer_num = fields.Many2one("bank.first_payments_customers", "Request Id", ondelete="cascade",
                                 required=1, Tracking=True)
    req_date = fields.Date(related='requer_num.request_date', required=1, string="Request Date", Tracking=True)
    installment = fields.Integer(string="No Of Installments", default=1, help="Number of installments", Tracking=True)
    payment_date = fields.Date(string="Installment Start Date", default=fields.Date.today(), help="Date of the paymemt",
                               Tracking=True)
    install_ids = fields.One2many('bank.installments', 'requer_ids', string='install_ids', Tracking=True)
    install_num = fields.Integer(related='install_ids.install_num', )
    pre_date = fields.Date(related='install_ids.pre_date')
    install_amount = fields.Float(related='install_ids.install_amount')
    # first_rem = fields.Many2one("bank.first_payments_customers")
    amount = fields.Float(string='Amount', related='requer_num.rem_amount', Tracking=True)
    filter_date = fields.Date(string='Cleared Date')
    fin_type = fields.Selection(related='requer_num.fin_type')
    name_section = fields.Many2one('bank.section', related='requer_num.name_section')
    name_activity = fields.Many2one('bank.activity', related='requer_num.name_activity')
    for_number = fields.Many2one('bank.formula', related='requer_num.for_number')
    sum_paid_amount = fields.Float(compute="_compute_paid_and_remaining_amount", store=True)
    sum_remaining_amount = fields.Float(compute="_compute_paid_and_remaining_amount", store=True)

    @api.constrains('payment_date')
    def _check_dateyy(self):
        if self.payment_date < datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

    @api.depends("install_ids", "install_ids.paid")
    def _compute_paid_and_remaining_amount(self):
        sum_paid_amount = 0
        sum_remaining_amount = 0
        for rec in self:
            for install in rec.install_ids:
                if install.paid:
                    sum_paid_amount = (sum_paid_amount + install.install_amount)
                else:
                    sum_remaining_amount = (sum_remaining_amount + install.install_amount)

        rec.sum_paid_amount = sum_paid_amount
        rec.sum_remaining_amount = sum_remaining_amount

    # amount = fields.Float(related='first_rem.rem_amount', string='Amount')

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('transaction_installments.sequence.code') or 'New'
        return super(Transaction_installments, self).create(vals)

    def compute_installment(self):
        """This automatically create the installment the company need to pay to
        insurance company based on payment start date and the no of installments.
            """
        finance_Request = self.env['bank.transaction_installments'].search(
            [('id', '!=', self.id), ('requer_num', '=', self.requer_num.id)])
        if finance_Request:
            raise ValidationError(("requer number number must be unique!"))
        else:
            for transaction in self:
                transaction.install_ids.unlink()
                install_num = 1
                date_start = transaction.payment_date
                amount = transaction.amount / transaction.installment
                for i in range(1, transaction.installment + 1):
                    self.env['bank.installments'].create({
                        'pre_date': date_start,
                        'install_num': install_num,
                        'install_amount': amount,
                        'requer_ids': transaction.id})
                    date_start = date_start + relativedelta(months=1)
                    install_num += 1
            return True


# Create Model Installments_payments
class Installments(models.Model):
    _name = "bank.installments"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "install_num"

    install_num = fields.Integer(required=1, string="Install Number", Tracking=True)
    pre_date = fields.Date(string="Previous Date", default=fields.Date.today(), required=1, Tracking=True)
    install_amount = fields.Float(string="Install Amount", required=1, Tracking=True)
    paid_amount = fields.Float(string="Paid Amount")
    remaining_amount = fields.Float(string="Remaining  Amount", compute="_get_remaining_amount", Tracking=True)
    paid = fields.Boolean(string="Paid", Tracking=True)
    requer_ids = fields.Many2one('bank.transaction_installments', Tracking=True)
    # sum_paid_amount = fields.Float(, string="sum_paid_amount", Tracking=True)
    # sum_remaining_amount = fields.Float(string="sum_remaining_amount", compute="_compute_sum_remaining_amoun")

    requerid = fields.Many2one('bank.first_payments_customers', )
    customer_id = fields.Many2one('bank.customers', related='requerid.customer_id')
    customer_name = fields.Char(related='requerid.customer_name')
    fin_type = fields.Selection(related='requerid.fin_type')
    name_section = fields.Many2one('bank.section', related='requerid.name_section')
    name_activity = fields.Many2one('bank.activity', related='requerid.name_activity')
    for_number = fields.Many2one('bank.formula', related='requerid.for_number')

    # @api.model
    # def create(self, vals):
    #     if vals.get('sequence', 'New') == 'New':
    #         vals['sequence'] = self.env['ir.sequence'].next_by_code('installmentss_payments.sequence.code') or 'New'
    #     return super(Installments, self).create(vals)

    def _compute_sum_remaining_amoun(self):
        for rec in self:
            rec.sum_remaining_amount = (rec.remaining_amount + rec.remaining_amount)

    def _compute_paid_amount(self):
        for rec in self:
            rec.sum_paid_amount = (rec.paid_amount + rec.paid_amount)

    def _get_remaining_amount(self):
        for rec in self:
            rec.remaining_amount = rec.install_amount - rec.paid_amount

    # @api.constrains('install_num')
    # def check_number(self):
    #     installmentss = self.env["bank.transaction_installments"].search(
    #         [('install_ids', '=', self.id), ('install_ids.install_num', '=', self.install_num)])
    #     if installmentss:
    #         raise ValidationError(("requer number number must be unique!"))


class Installments_payments(models.Model):
    _name = "bank.installments_payments"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "requer_ids"

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'), Tracking=True)
    requer_ids = fields.Many2one("bank.transaction_installments", "Request Id", required=1, Tracking=True)
    req_date = fields.Date(related='requer_ids.req_date', string="Request Date", Tracking=True)
    install_num = fields.Many2one('bank.installments', string="Install Number", Tracking=True)
    amout_install = fields.Float(related='install_num.install_amount', string="Installment Amount ", Tracking=True)
    pay_date = fields.Date(related='install_num.pre_date')
    pay_amount = fields.Float()
    rem_amount = fields.Float(related='install_num.remaining_amount', string="Remaining Amount", Tracking=True)
    # pay_date = fields.Date(string="pay date")
    #############
    # install_num = fields.Integer(required=1, string="Install Number", Tracking=True)
    # pre_date = fields.Date(string="Previous Date", default=fields.Date.today(), required=1, Tracking=True)
    # install_amount = fields.Float(string="Install Amount", required=1, Tracking=True)
    #

    ##########
    customer_id = fields.Many2one('bank.customers', related='install_num.customer_id')
    customer_name = fields.Char(related='install_num.customer_name')
    fin_type = fields.Selection(related='install_num.fin_type')
    name_section = fields.Many2one('bank.section', related='install_num.name_section')
    name_activity = fields.Many2one('bank.activity', related='install_num.name_activity')
    for_number = fields.Many2one('bank.formula', related='install_num.for_number')

    @api.constrains("pay_amount")
    def check_pay_amount(self):
        for rec in self:
            if rec.pay_amount > rec.amout_install:
                raise ValidationError("The pay amount must pay under the installment amount")

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('installments_payments.sequence.code') or 'New'
        return super(Installments_payments, self).create(vals)

    @api.model
    def create(self, vals):
        res = super(Installments_payments, self).create(vals)
        if res:
            res.install_num.paid_amount += res.pay_amount
            if res.install_num.install_amount == res.install_num.paid_amount:
                res.install_num.paid = True

        return res

    # @api.depends('amout_install', 'pay_amount')
    # def _compute_amount(self):
    #     for rec in self:
    #         rec.rem_amount = (rec.amout_install - rec.pay_amount)

    @api.onchange('requer_ids')
    def _get_payments(self):
        payments_list = []
        if self.requer_ids:
            paymentsInstallment = self.env['bank.installments'].search(
                [('requer_ids', '=', self.requer_ids.id), ('paid', '=', False)])
            # raise ValidationError(paymentsInstallment)

            if paymentsInstallment:
                for payments in paymentsInstallment:
                    payments_list.append(payments.id)
            return {'domain': {'install_num': [('id', 'in', payments_list)]},
                    'value': {'install_num': paymentsInstallment[0].id if len(paymentsInstallment) > 0 else None}}


# Create Model Stumbling

class Stumbling(models.Model):
    _name = "bank.stumbling"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "requer_number"
    _sql_constraints = [('name_unique', 'unique(requer_number,req_date)', 'hgsbcavchvhsa')]

    def get_domain(self):
        requset = []
        record = self.env["bank.stumbling"].search([('state', '=', 'accept')])
        for rec in record:
            requset.append(rec.id)
        return [('id', 'in', requset)]

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'), Tracking=True)
    requer_number = fields.Many2one("bank.finance_request", "Request Id", required=1, Tracking=True)
    req_date = fields.Date(related='requer_number.req_date', string="Request Date", Tracking=True)
    stumb_amount = fields.Float(string="Stumbling Amount", required=1, Tracking=True)
    stumb_num = fields.Many2one("bank.stumbling_reasons", "Stumbling Reasons ", required=1, Tracking=True)
    amount_cert = fields.Float(related='requer_number.amount_cert', )

    @api.constrains('stumb_amount','amount_cert')
    def check_req_amounttt(self):
        if self.amount_cert <= self.stumb_amount:
            raise ValidationError("invalid amount")


    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('stumbling.sequence.code') or 'New'
        return super(Stumbling, self).create(vals)

    def action_stumbling(self):
        context = {}
        context.update({'requer_numb': self.requer_number.id})
        return {
            'name': 'test',
            'type': "ir.actions.act_window",
            'res_model': 'bank.transmit_to_low_mangement',
            'view_mode': 'form',
            'context': context,
        }


# Create Model Transmit_To_Low_Mangement

class Transmit_To_Low_Mangement(models.Model):
    _name = "bank.transmit_to_low_mangement"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "requer_numb"
    _sql_constraints = [('name_unique', 'unique(requer_numb,tran_date)', 'hgsbcavchvhsa')]

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    requer_numb = fields.Many2one("bank.stumbling", "Request Id", required=1, Tracking=True)
    req_date = fields.Date(related='requer_numb.req_date', string="Request Date", Tracking=True)
    tran_date = fields.Date(string="Transmit Date", default=fields.Date.today(), required=1, Tracking=True)
    amount_stumbling = fields.Float(related='requer_numb.stumb_amount', Tracking=True)

    def action_Reschedule(self):
        context = {}
        context.update({'requer_num': self.requer_numb.id})
        return {
            'name': 'test',
            'type': "ir.actions.act_window",
            'res_model': 'bank.rescheduled',
            'view_mode': 'form',
            'context': context,
        }

    def action_transmit_to_court(self):
        context = {}
        context.update({'requer_num': self.requer_numb.id})
        return {
            'name': 'test',
            'type': "ir.actions.act_window",
            'res_model': 'bank.transmit_to_court',
            'view_mode': 'form',
            'context': context,
        }

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('transmit_to_low_mangement.sequence.code') or 'New'
        return super(Transmit_To_Low_Mangement, self).create(vals)

    @api.constrains('req_date')
    def _check_date(self):
        if self.tran_date > datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))


# Create Model Reschedule

class Reschedule(models.Model):
    _name = "bank.rescheduled"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "requer_num"
    _sql_constraints = [('name_unique', 'unique(requer_num,rescheduled_date)', 'hgsbcavchvhsa')]

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    # requer_num = fields.Many2one("bank.transmit_to_low_mangement", "Request Id", required=1)
    requer_num = fields.Many2one("bank.transmit_to_low_mangement", "Request Id", required=1)
    req_date = fields.Date(related='requer_num.req_date', required=1, string="Request Date")
    rescheduled_date = fields.Date(string="Date Rescheduled")
    amount_stumbling = fields.Many2one("bank.stumbling")
    amount_rescheduled = fields.Float(related='requer_num.amount_stumbling', string="Amount Rescheduled")
    install_reschedule_number = fields.One2many("bank.reschedule_installd", 'install_reschedule_numbbers',
                                                string='install_reschedule_number')

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('rescheduled.sequence.code') or 'New'
        return super(Reschedule, self).create(vals)


class RescheduleInstall(models.Model):
    _name = "bank.reschedule_installd"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherit = 'mail.thread'

    def get_domain(self):
        inst = []
        record = self.env["bank.stumbling"].search([('requer_number', '=', 'requer_number')])
        for rec in record:
            requset.append(rec.id)
        return [('id', 'in', inst)]

    # install_num = fields.Integer("Install Number", required=1)
    install_num = fields.Integer("Install Number", required=1, Tracking=True)
    pay_date = fields.Date(string="Old Pay Date", Tracking=True)
    new_pre_date = fields.Date(string="New Pay Date", required=1, Tracking=True)
    amount = fields.Float(string="Amount", required=1, Tracking=True)
    install_reschedule_numbbers = fields.Many2one("bank.rescheduled", Tracking=True)


# Create Model Transmit_To_Court

class Transmit_To_Court(models.Model):
    _name = "bank.transmit_to_court"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "requer_num"
    _sql_constraints = [('name_unique', 'unique(requer_num,tran_to_court_date)', 'hgsbcavchvhsa')]

    sequence = fields.Char("Sequence", copy=False, index=True, default=lambda self: _('New'))
    requer_num = fields.Many2one("bank.rescheduled", string="Request Id", required=1, Tracking=True)
    req_date = fields.Date(related='requer_num.req_date', string="Request Date", Tracking=True)
    tran_to_court_date = fields.Date(string="Transmit To Court Date", Tracking=True)
    cout_numb = fields.Many2one("bank.courts", string="Courts", required=1, Tracking=True)
    judg_number = fields.Many2one("bank.judges", string="Judges ", required=1, Tracking=True)
    court_deci = fields.Char(string="Court Decision", required=1, Tracking=True)
    file = fields.Binary(string="Court Decision file", Tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('transmit_to_court.code') or 'New'
        return super(Transmit_To_Court, self).create(vals)

    @api.constrains('tran_to_court_date')
    def _check_dateco(self):
        if self.tran_to_court_date <= datetime.date.today():
            raise ValidationError(_('Do not enter a date greater than todays date'))

    # class Imagman(models.Model):
    #     _name = "bank.Imag"
    #
    #     Imagm = fields.Image()

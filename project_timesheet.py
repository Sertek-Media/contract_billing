import time
import datetime
from openerp.osv import fields, osv
from openerp import pooler
from openerp import tools
from openerp.tools.translate import _
from openerp.addons.project import project
from openerp.addons.project_timesheet.project_timesheet import project_work

class project_work_class(osv.osv):    
    
    _inherit = 'project.task.work'
    _description  = 'Adding the task billing functionality'
    
    def create_analytic_entries_custom(self, cr, uid, vals, context):
        """Create the hr analytic timesheet from project task work"""
        timesheet_obj = self.pool['hr.analytic.timesheet']
        task_obj = self.pool['project.task']

        vals_line = {}
        timeline_id = False
        acc_id = False

        task_obj = task_obj.browse(cr, uid, vals['task_id'], context=context)
        if task_obj.type_billing.id == 1 or task_obj.type_billing.id == 2 :
            result = self.get_user_related_details(cr, uid, vals.get('user_id', uid))
            vals_line['name'] = '%s[%s]: %s' % (tools.ustr(task_obj.name), task_obj.sequence1,tools.ustr(vals['name'] or '/'))
            vals_line['user_id'] = vals['user_id']
            vals_line['product_id'] = result['product_id']
            if vals.get('date'):
                timestamp = datetime.datetime.strptime(vals['date'], tools.DEFAULT_SERVER_DATETIME_FORMAT)
                ts = fields.datetime.context_timestamp(cr, uid, timestamp, context)
                vals_line['date'] = ts.strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
    
            # Calculate quantity based on employee's product's uom
            vals_line['unit_amount'] = vals['hours']
    
            default_uom = self.pool['res.users'].browse(cr, uid, uid, context=context).company_id.project_time_mode_id.id
            if result['product_uom_id'] != default_uom:
                vals_line['unit_amount'] = self.pool['product.uom']._compute_qty(cr, uid, default_uom, vals['hours'], result['product_uom_id'])
            acc_id = task_obj.project_id and task_obj.project_id.analytic_account_id.id or acc_id
            if acc_id:
                vals_line['account_id'] = acc_id
                res = timesheet_obj.on_change_account_id(cr, uid, False, acc_id)
                if res.get('value'):
                    vals_line.update(res['value'])
                vals_line['general_account_id'] = result['general_account_id']
                vals_line['journal_id'] = result['journal_id']
                vals_line['amount'] = 0.0
                vals_line['product_uom_id'] = result['product_uom_id']
                amount = vals_line['unit_amount']
                prod_id = vals_line['product_id']
                unit = False
                vals_line.update({'is_fixed':True,'to_invoice':False}) # this is a conditional field
                timeline_id = timesheet_obj.create(cr, uid, vals=vals_line, context=context)
    
                # Compute based on pricetype
                amount_unit = timesheet_obj.on_change_unit_amount(cr, uid, timeline_id,
                    prod_id, amount, False, unit, vals_line['journal_id'], context=context)
                if amount_unit and 'amount' in amount_unit.get('value',{}):
                    updv = { 'amount': 0.0 }
                    timesheet_obj.write(cr, uid, [timeline_id], updv, context=context)
                vals['hr_analytic_timesheet_id'] = timeline_id
                return timeline_id
        else:
            result = self.get_user_related_details(cr, uid, vals.get('user_id', uid))
            vals_line['name'] = '%s[%s]: %s' % (tools.ustr(task_obj.name), tools.ustr(task_obj.sequence1),tools.ustr(vals['name'] or '/'))
            vals_line['user_id'] = vals['user_id']
            vals_line['product_id'] = result['product_id']
            if vals.get('date'):
                timestamp = datetime.datetime.now()
#                 timestamp = datetime.datetime.strptime(vals['date'], tools.DEFAULT_SERVER_DATETIME_FORMAT)
                ts = fields.datetime.context_timestamp(cr, uid, timestamp, context)
                vals_line['date'] = ts.strftime(tools.DEFAULT_SERVER_DATE_FORMAT)
    
            # Calculate quantity based on employee's product's uom
            vals_line['unit_amount'] = vals['hours']
    
            default_uom = self.pool['res.users'].browse(cr, uid, uid, context=context).company_id.project_time_mode_id.id
            if result['product_uom_id'] != default_uom:
                vals_line['unit_amount'] = self.pool['product.uom']._compute_qty(cr, uid, default_uom, vals['hours'], result['product_uom_id'])
            acc_id = task_obj.project_id and task_obj.project_id.analytic_account_id.id or acc_id
            if acc_id:
                vals_line['account_id'] = acc_id
                res = timesheet_obj.on_change_account_id(cr, uid, False, acc_id)
                if res.get('value'):
                    vals_line.update(res['value'])
                vals_line['general_account_id'] = result['general_account_id']
                vals_line['journal_id'] = result['journal_id']
                vals_line['amount'] = 0.0
                vals_line['product_uom_id'] = result['product_uom_id']
                amount = vals_line['unit_amount']
                prod_id = vals_line['product_id']
                unit = False
                timeline_id = timesheet_obj.create(cr, uid, vals=vals_line, context=context)
                # Compute based on pricetype
                amount_unit = timesheet_obj.on_change_unit_amount(cr, uid, timeline_id,
                    prod_id, amount, False, unit, vals_line['journal_id'], context=context)
                if amount_unit and 'amount' in amount_unit.get('value',{}):
                    updv = { 'amount': amount_unit['value']['amount'] }
                    timesheet_obj.write(cr, uid, [timeline_id], updv, context=context)
            return timeline_id            
            
    project_work._create_analytic_entries = create_analytic_entries_custom
    

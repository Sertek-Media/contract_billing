import time
import datetime
from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import date
from xml.etree.ElementTree import _namespaces

class project_issue(osv.osv):    
    
    _inherit = 'project.issue'
    _description  = 'Adding the Issue billing functionality'
    
    def timer_state_stop(self,cr,uid,id,context=None):
        if context==None: context = {}
        user_start = super(project_issue,self).timer_state_stop(cr,uid,id,context=context)
        if user_start:
            type_billing = user_start.get('type_billing',False)
            project_id = user_start.get('project_id',False)
            analytic_account_id = user_start.get('analytic_account_id',False)
            timesheet_obj = self.pool.get('hr.analytic.timesheet')
            result= self.pool.get('project.task.work').get_user_related_details(cr, uid, user_start.get('user_start',1)[0])
            vals_line = {}
            vals_line['name'] = context.get('desc','Issue Work Summary')  
            vals_line['user_id'] = user_start.get('user_start',1)[0]
            vals_line['product_id'] = result['product_id']
            vals_line['date'] = date.today()
            vals_line['unit_amount'] = user_start.get('difference_time_float',0)
            default_uom = self.pool.get('res.users').browse(cr, uid, uid).company_id.project_time_mode_id.id
            if project_id:
                analytic_account_id_project  = self.pool.get('project.project').browse(cr,uid,project_id,context).analytic_account_id.id 
                if analytic_account_id_project:
                    vals_line['account_id'] = analytic_account_id_project
                elif analytic_account_id:
                    vals_line['account_id'] = analytic_account_id
                else:
                    raise osv.except_osv(_('Error !'), _('Please define a analytic account on the issue '))
            elif analytic_account_id:
                vals_line['account_id'] = analytic_account_id
            else:
                raise osv.except_osv(_('Error !'), _('Please define a analytic account on the issue '))
            
            vals_line['general_account_id'] = result['general_account_id']
            vals_line['journal_id'] = result['journal_id']
            vals_line['product_uom_id'] = result['product_uom_id']
            amount = vals_line['unit_amount']
            prod_id = vals_line['product_id']
            unit = False
            vals_line['issue_id'] = id[0]
            
            if not type_billing or type_billing[0] == 1 or type_billing[0] == 2:
                vals_line['is_fixed'] = True
                vals_line['to_invoice'] = False
                vals_line['amount'] = 0.0
                timesheet_obj = self.pool.get('hr.analytic.timesheet')
                timeline_id = timeline_id = timesheet_obj.create(cr, uid, vals=vals_line, context=context)
                amount_unit = timesheet_obj.on_change_unit_amount(cr, uid, timeline_id,
                        prod_id, amount, False, unit, vals_line['journal_id'], context=context)
                if amount_unit and 'amount' in amount_unit.get('value',{}):
                    updv = { 'amount': 0.0 }
                    timesheet_obj.write(cr, uid, [timeline_id], updv, context=context)
            else :
                vals_line['is_fixed'] =False
                view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'hr_timesheet_invoice', 'timesheet_invoice_factor1')
                vals_line['to_invoice'] = view_ref[1]
                timesheet_obj = self.pool.get('hr.analytic.timesheet')
                timeline_id = timeline_id = timesheet_obj.create(cr, uid, vals=vals_line, context=context)
                amount_unit = timesheet_obj.on_change_unit_amount(cr, uid, timeline_id,
                        prod_id, amount, False, unit, vals_line['journal_id'], context=context)
                if amount_unit and 'amount' in amount_unit.get('value',{}):
                    updv = { 'amount': amount_unit['value']['amount'] }
                    timesheet_obj.write(cr, uid, [timeline_id], updv, context=context)
        return True
    
    def set_value(self,timesheet_ids,type_billing):
        if type_billing == 1 or type_billing == 2:
            for i in timesheet_ids:
                if i[0] == 0:
                    if type(i[2]) == type({}):
                        i[2].update({'is_fixed':True})
        return timesheet_ids
    
    def create(self,cr,uid,vals,context=None):
        if vals.get('timesheet_ids',False):
            timesheet_ids = self.set_value(vals.get('timesheet_ids',[]),vals.get('type_billing','none'))
            vals.update({'timesheet_ids':timesheet_ids})
        return super(project_issue,self).create(cr,uid,vals,context=context)
    
    def write(self,cr,uid,ids,vals,context=None):
        if vals.get('timesheet_ids',False):
            if vals.get('type_billing'):
                timesheet_ids = self.set_value(vals.get('timesheet_ids',[]),vals.get('type_billing','none'))
            else:
                type_billing = self.read(cr,uid,ids[0],['type_billing'],context)
                timesheet_ids = self.set_value(vals.get('timesheet_ids',[]),type_billing.get('type_billing',False))
            vals.update({'timesheet_ids':timesheet_ids})
        return super(project_issue,self).write(cr,uid,ids,vals,context)

    def onchange_sales_order(self,cr,uid,id,context=None):
        return {'value':{'sale_order_id':False}}
        
    _defaults = {
                 'is_fix_invoice':'no',
                 }

    _columns = {
                'type_billing':fields.many2one('type.task','Task Type'),
                'is_fix_invoice':fields.selection([('no','To be Invoiced'),('yes','Invoiced')],"Invoiceable"),
#                 'type_billing':fields.selection([('none','No Charge'),('fixed','Fixed Invoicing'),('variable','Time Invoicing')],'Task Type'),
                'sale_order_id':fields.many2one('sale.order','Sale Order Associated'),
                }

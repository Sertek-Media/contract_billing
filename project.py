from openerp.osv import fields, osv
from datetime import date
from threading import Thread
try:
    from openerp.addons.project_management import project as project_management
except:
    print "The project management module is not present"
    
class type_task(osv.osv):
    _name  = "type.task"
    _description = "Type of task"

    def name_search(self, cr, user, name='', args=None, operator='ilike', context=None, limit=100):
        dict = {}
        if context.get('project_id',False):
            try:
                project_brw = self.pool.get('project.project').browse(cr,user,context.get('project_id',False),context)
                if project_brw.analytic_account_id:
                    dict.update({'fix':project_brw.analytic_account_id.fix_price_invoices,
                                    'variable':project_brw.analytic_account_id.invoice_on_timesheets,
                                    'cancel':False
                                    }) 
                else :
                    dict.update({
                                    'cancel':True
                                })
            except:
                dict.update({'cancel':True})        
            if dict.get('cancel',False):
                return super(type_task,self).name_search(cr, user, name='', args=None, operator='ilike', context=None, limit=100)
            else:
                list = []
                list = super(type_task,self).name_search(cr, user, name='', args=None, operator='ilike', context=None, limit=100)
                if dict.get('variable',False) and dict.get('fix'):
                    return list
                elif not dict.get('variable',False) and dict.get('fix'):
                    list.pop(2)
                    return list
                elif not dict.get('fix') and dict.get('variable',False) :
                    list.pop(1)
                    return list
                elif not(dict.get('variable',False) and dict.get('fix')):
                    list.pop(1)
                    list.pop(1)
                    return list
                else:
                    return list
            
        return super(type_task,self).name_search(cr, user, name='', args=None, operator='ilike', context=None, limit=100)
    
    _columns = {
                'name':fields.char('Name'),
                }

class task(osv.osv):
    _inherit = 'project.task'
    _description = 'Fixed or variable task'

            
    def onchange_selection(self,cr,uid,id,project_id,context={}):
        context.update({'project_id':project_id})
        return {'value':{'type_billing':False}}
    
    def onchange_sales_order(self,cr,uid,id,context=None):
        return {'value':{'sale_order_id':False}}
    
    _defaults = {
                 'is_fix_invoice':'no',
                 }
    _columns = {
                    'type_billing':fields.many2one('type.task','Task Type'),
                    'is_fix_invoice':fields.selection([('no','To be Invoiced'),('yes','Invoiced')],'Is Invoiced'),
    #                     'type_billing':fields.selection([('none','No Charge'),('fixed','Fixed Invoicing'),('variable','Time Invoicing')],'Task Type'),
                   'sale_order_id':fields.many2one('sale.order','Sale Order Associated')
                }
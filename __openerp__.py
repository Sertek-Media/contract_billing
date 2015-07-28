# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name' : 'Project Task Issue Billing',
    'version' : '1.1',
    'author' : 'Intellerist',
    'category' : 'contract',
    'description' : """
Contact Billing

1.The project_management module is supposed to be installed before installing this module
    - The reason is the method action_close() of the class  project_task is over ride in project_management and then back again in this module
    - Hence the functionality of both the module is preserved
2.  Also depends on project_issue_sheet but not put into dependencies so that the module does not get uninstalled if the other module is uninstalled     
    """,
    'website': 'www.intellerist.com',
    'images' : [],
    'depends' : ['base','sale','hr_timesheet','project_timesheet','project','analytic','account_analytic_analysis','project_issue_sheet'],
    
    'data': ['project_view.xml','project_issue_view.xml','views/contract_billing.xml',
            'contract_billing_view.xml','wizard/fixed_invoice_wizard.xml','account_analytic_line_view.xml','contract_billing_data.xml'
            ],
    
    'demo': [],
    
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

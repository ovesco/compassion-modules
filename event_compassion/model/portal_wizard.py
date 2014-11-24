# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    The licence is in the file __openerp__.py
#
##############################################################################

from openerp.osv import osv


class portal_wizard(osv.osv_memory):
    """ This class creates analytic accounts for new portal users."""

    _inherit = 'portal.wizard'

    def action_apply(self, cr, uid, ids, context=None):
        res = super(portal_wizard, self).action_apply(cr, uid, ids, context)
        wizard = self.browse(cr, uid, ids[0], context)
        for user in wizard.user_ids:
            user_ids = self.pool.get('res.users').search(
                cr, uid, [('name', '=', user.partner_id.name)],
                context=context)
            partner_name = user.partner_id.name
            
            analytics_obj = self.pool.get('account.analytic.account')
            acc_ids = analytics_obj.search(
                cr, uid, [('name', '=', partner_name)], context=context)
            if not acc_ids and user_ids:
                acode = self.pool.get('ir.sequence').get(cr, uid, 'AASEQ')
                parent_id = analytics_obj.search(
                    cr, uid, [('name', '=', 'Partners')],
                    context=context)[0]
                analytics_obj.create(cr, uid, {
                    'name': partner_name,
                    'type': 'normal',
                    'code': acode,
                    'parent_id': parent_id,
                    'manager_id': user_ids[0],
                })
        return res

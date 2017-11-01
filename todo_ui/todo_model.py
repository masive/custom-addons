# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Tag(models.Model):
    _name = 'todo.task.tag'
    name = fields.Char('Name', size=40, translate=True)


class Stage(models.Model):
    _name = 'todo.task.stage'
    _order = 'sequence, name'
    #String fields:
    name = fields.Char('Name', size=40)
    desc = fields.Text('Description')
    state = fields.Selection(
        [('draft', 'New'),
         ('open', 'Started'),
         ('done', 'Closed')], 'State')
    docs = fields.Html('Documentation')
    # Numeric fields:
    sequence = fields.Integer('Sequence')
    perc_complete = fields.Float('% Complete', (3, 2))
    # Date fields:
    date_effective = fields.Date('Effective Date')
    date_changed = fields.Datetime('Last Change')
    # Other fields:
    fold = fields.Boolean('Folded?')
    image = fields.Binary('Image')


class TodoTask(models.Model):
    _inherit = 'todo.task'
    stage_id = fields.Many2one('todo.task.stage', 'Stage')
    tag_ids = fields.Many2many('todo.task.tag', string='Tags')
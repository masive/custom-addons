# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Tag(models.Model):
    _name = 'todo.task.tag'
    _parent_store = True
    # _parent_name = 'parent_id'
    name = fields.Char('Name')
    parent_id = fields.Many2one('todo.task.tag', 'Parent Tag', ondelete='restrict')
    parent_left = fields.Integer('Parent Left', index=True)
    parent_right = fields.Integer('Parent Right', index=True)


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
    stage_fold = fields.Boolean(string='Stage Folded?',
                                compute='_compute_stage_fold',
                                store=True,
                                search='_search_stage_fold',
                                inverse='_write_stage_fold')
    stage_state = fields.Selection(related='stage_id.state', string='Stage State')
    refers_to = fields.Reference(
        [('res.user', 'User'), ('res.partner', 'Partner')],
        'Refers to')
    effort_estimate = fields.Integer('Effort Estimate')

    @api.one
    @api.depends('stage_id.fold')
    def _compute_stage_fold(self):
        self.stage_fold = self.stage_id.fold

    def _search_stage_fold(self, operator, value):
        return [('stage_id.fold', operator, value)]

    def _write_stage_fold(self):
        self.stage_id.fold = self.stage_fold

    _sql_constraints = [
        ('todo_task_name_uniq',
         'UNIQUE (name, user_id, active)',
         'Task title must be unique!')]

    @api.one
    @api.constrains('name')
    def _check_name_size(self):
        if len(self.name) < 5:
            raise ValueError('Must have 5 chars!')

    @api.one
    def compute_user_todo_count(self):
        self.user_todo_count = self.search_count([('user_id', '=', self.user_id.ids)])

    user_todo_count = fields.Integer('User To-Do Count', compute='compute_user_todo_count')
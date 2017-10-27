{
    'name': 'To-Do Application',
    'description': 'Manage your personal Task with this module.',
    'author': 'Daniel Reis',
    'data': ['views/todo_view.xml',
             'security/ir.model.access.csv',
             'security/todo_access_rules.xml',],
    'depends': ['mail'],
    'application': True,
}
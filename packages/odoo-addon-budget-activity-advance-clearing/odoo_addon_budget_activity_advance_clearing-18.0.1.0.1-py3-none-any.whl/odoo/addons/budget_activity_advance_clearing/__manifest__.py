# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Budget Activity - Advance/Clearing",
    "version": "18.0.1.0.1",
    "category": "Accounting",
    "license": "AGPL-3",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/ecosoft-odoo/budgeting",
    "depends": [
        "budget_activity_expense",
        "budget_control_advance_clearing",
    ],
    "data": [
        "data/budget_advance_data.xml",
        "views/hr_expense_view.xml",
        "views/advance_budget_move.xml",
    ],
    "installable": True,
    "auto_install": True,
    "maintainers": ["Saran440"],
    "development_status": "Alpha",
}

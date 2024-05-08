from . import __version__ as app_version  # noqa: F401

app_name = "time_and_expense"
app_title = "Time And Expense"
app_publisher = "CherryRoad Technologies"
app_description = "Time and Expense"
app_email = "support@cherryroad.com"
app_license = "Proprietary"
required_apps = ["frappe/erpnext", "frappe/hrms"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/time_and_expense/css/time_and_expense.css"
app_include_js = [
	"time_and_expense.bundle.js",
]

# include js, css files in header of web template
web_include_css = "/assets/time_and_expense/css/web.css"
# web_include_js = "/assets/time_and_expense/js/time_and_expense.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "time_and_expense/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Employee": "public/js/custom/employee_custom.js",
	"Expense Claim": "public/js/custom/expense_claim_custom.js",
	"Project": "public/js/custom/project_custom.js",
	"Purchase Invoice": "public/js/custom/purchase_invoice_custom.js",
	"Sales Invoice": "public/js/custom/sales_invoice_custom.js",
	"Timesheet": "public/js/custom/timesheet_custom.js",
}

doctype_list_js = {
	"Expense Claim": "public/js/custom/expense_claim_list.js",
	"Timesheet": "public/js/custom/timesheet_list.js",
}

fixtures = [
	{
		"dt": "Workflow",
		"filters": [
			[
				"name",
				"in",
				[
					"Expense Claim Workflow",
					"Timesheet Approval Flow",
				],
			]
		],
	},
	"Workflow State",
	"Workflow Action Master",
	{
		"dt": "Email Template",
		"filters": [["name", "in", ["Pending Approval", "Rejected Approval"]]],
	},
]
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "time_and_expense.utils.jinja_methods",
# 	"filters": "time_and_expense.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "time_and_expense.install.before_install"
after_install = "time_and_expense.install.after_install"
after_migrate = "time_and_expense.customize.load_customizations"

# Uninstallation
# ------------

# before_uninstall = "time_and_expense.uninstall.before_uninstall"
# after_uninstall = "time_and_expense.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "time_and_expense.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Employee": "time_and_expense.permissions.employee_permission_query_conditions",
	"Timesheet": "time_and_expense.permissions.timesheet_permission_query_conditions",
	"Expense Claim": "time_and_expense.permissions.expense_claim_permission_query_conditions",
}
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

standard_queries = {
	"Timesheet": "time_and_expense.overrides.timesheet.timesheet_query",
}

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Project": "time_and_expense.overrides.project.TimeAndExpenseProject",
	"Task": "time_and_expense.overrides.task.TimeAndExpenseTask",
	"Timesheet": "time_and_expense.overrides.timesheet.TimeAndExpenseTimesheet",
	"Employee Checkin": "time_and_expense.overrides.employee_checkin.TimeAndExpenseEmployeeCheckin",
	"Expense Claim": "time_and_expense.overrides.expense_claim.TimeAndExpenseExpenseClaim",
	"Expense Claim Type": "time_and_expense.overrides.expense_claim_type.TimeAndExpenseExpenseClaimType",
	"Purchase Invoice": "time_and_expense.overrides.purchase_invoice.TimeAndExpensePurchaseInvoice",
	"Sales Invoice": "time_and_expense.overrides.sales_invoice.TimeAndExpenseSalesInvoice",
	"Activity Type": "time_and_expense.overrides.activity_type.TimeAndExpenseActivityType",
	"Employee": "time_and_expense.overrides.employee.TimeAndExpenseEmployee",
}

extend_bootinfo = "time_and_expense.boot.boot_session"

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Timesheet": {
		"validate": [
			"time_and_expense.overrides.timesheet.check_auto_approval",
		],
	},
	"User": {
		"validate": [
			"time_and_expense.permissions.set_up_employee_role_profile",
			"time_and_expense.overrides.user.cache_user_timezone",
		]
	},
	"Company": {
		"validate": [
			"time_and_expense.time_and_expense.doctype.time_and_expense_settings.time_and_expense_settings.create_time_and_expense_settings",
		],
		"after_insert": [
			"time_and_expense.time_and_expense.doctype.time_and_expense_settings.time_and_expense_settings.create_time_and_expense_settings",
		],
	},
	"Employee Checkin": {
		"on_update": ["time_and_expense.overrides.employee_checkin.update_tags"],
		"after_insert": ["time_and_expense.overrides.employee_checkin.create_employee_checkin_duration"],
		"validate": ["time_and_expense.overrides.employee_checkin.create_employee_checkin_duration"],
	},
	"Task": {
		"validate": ["time_and_expense.overrides.task.set_is_group_if_has_dependent_tasks"],
	},
}

# Scheduled Tasks
# ---------------


scheduler_events = {
	"cron": {
		"30	8	*	*	*": [
			"time_and_expense.overrides.expense_claim.send_approval_email",
			"time_and_expense.overrides.timesheet.send_reminder_email",
		]
	},
	# 	"all": [
	# 		"time_and_expense.tasks.all"
	# 	],
	# 	"daily": [
	# 		"time_and_expense.tasks.daily"
	# 	],
	"hourly": ["time_and_expense.overrides.employee_checkin.automatic_checkout"],
	# 	"weekly": [
	# 		"time_and_expense.tasks.weekly"
	# 	],
	# 	"monthly": [
	# 		"time_and_expense.tasks.monthly"
	# 	],
}

# Testing
# -------

# before_tests = "time_and_expense.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "time_and_expense.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "time_and_expense.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["time_and_expense.utils.before_request"]
# after_request = ["time_and_expense.utils.after_request"]

# Job Events
# ----------
# before_job = ["time_and_expense.utils.before_job"]
# after_job = ["time_and_expense.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"time_and_expense.auth.validate"
# ]

app_name = "restaurant1"
app_title = "Restaurant1"
app_publisher = "Hilda Chepkirui"
app_description = "Simple restaurant management system."
app_email = "baraiywohilda181@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/restaurant1/css/restaurant1.css"
# app_include_js = "/assets/restaurant1/js/restaurant1.js"

# include js, css files in header of web template
# web_include_css = "/assets/restaurant1/css/restaurant1.css"
# web_include_js = "/assets/restaurant1/js/restaurant1.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "restaurant1/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "restaurant1/public/icons.svg"

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
# 	"methods": "restaurant1.utils.jinja_methods",
# 	"filters": "restaurant1.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "restaurant1.install.before_install"
# after_install = "restaurant1.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "restaurant1.uninstall.before_uninstall"
# after_uninstall = "restaurant1.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "restaurant1.utils.before_app_install"
# after_app_install = "restaurant1.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "restaurant1.utils.before_app_uninstall"
# after_app_uninstall = "restaurant1.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "restaurant1.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"restaurant1.tasks.all"
# 	],
# 	"daily": [
# 		"restaurant1.tasks.daily"
# 	],
# 	"hourly": [
# 		"restaurant1.tasks.hourly"
# 	],
# 	"weekly": [
# 		"restaurant1.tasks.weekly"
# 	],
# 	"monthly": [
# 		"restaurant1.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "restaurant1.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "restaurant1.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "restaurant1.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["restaurant1.utils.before_request"]
# after_request = ["restaurant1.utils.after_request"]

# Job Events
# ----------
# before_job = ["restaurant1.utils.before_job"]
# after_job = ["restaurant1.utils.after_job"]

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
# 	"restaurant1.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Whitelist the method to be called via API
from frappe import whitelist

@whitelist()
def create_or_update_invoice(order):
    # Your function implementation here
    pass

# Add the function to the __all__ list
__all__ = [
    # other methods...
    'create_or_update_invoice',
]


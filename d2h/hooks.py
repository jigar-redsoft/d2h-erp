app_name = "d2h"
app_title = "D2H"
app_publisher = "ashish"
app_description = "d2h"
app_email = "ashish.barvaliya@redsoftware.in"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/d2h/css/d2h.css"
# app_include_js = "/assets/d2h/js/d2h.js"

# include js, css files in header of web template
# web_include_css = "/assets/d2h/css/d2h.css"
# web_include_js = "/assets/d2h/js/d2h.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "d2h/public/scss/website"

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
# app_include_icons = "d2h/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "d2h.utils.jinja_methods",
#	"filters": "d2h.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "d2h.install.before_install"
# after_install = "d2h.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "d2h.uninstall.before_uninstall"
# after_uninstall = "d2h.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "d2h.utils.before_app_install"
# after_app_install = "d2h.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "d2h.utils.before_app_uninstall"
# after_app_uninstall = "d2h.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "d2h.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"d2h.tasks.all"
#	],
#	"daily": [
#		"d2h.tasks.daily"
#	],
#	"hourly": [
#		"d2h.tasks.hourly"
#	],
#	"weekly": [
#		"d2h.tasks.weekly"
#	],
#	"monthly": [
#		"d2h.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "d2h.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "d2h.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "d2h.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["d2h.utils.before_request"]
# after_request = ["d2h.utils.after_request"]

# Job Events
# ----------
# before_job = ["d2h.utils.before_job"]
# after_job = ["d2h.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

fixtures = [
    {
        "doctype": "Client Script",
    },
    {
        "dt": "Custom Field",
    }
]

doc_events = {
    "Purchase Receipt": {
        "before_save": "d2h.overrides.purchase_receipt_before_save",
        "on_submit": "d2h.overrides.on_submit_purchase_receipt"
    },
    "Delivery Note": {
        "before_save": "d2h.overrides.delivery_note_before_save",
    },
    "*": {
        "before_print": "d2h.api.before_print",
    }
}

app_include_js = "/assets/d2h/js/form.js"

doctype_js = {"Purchase Receipt" : "public/js/purchase_receipt.js", "Purchase Order" : "public/js/purchase_order.js", "Delivery Note" : "public/js/delivery_note.js"}
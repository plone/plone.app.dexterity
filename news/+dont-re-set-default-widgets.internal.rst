Do not re-define the same widgets where there are already default widgets.

The `Datetime` fields for `effective` and `expires` in the `IPublication`
behavior do not need to re-define the `DatetimeFieldWidget` widget. It is
already set in plone.app.z3cform. Leaving it out here allows to override the
widget in custom code.

[thet]

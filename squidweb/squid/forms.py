from django import forms

from squidweb.squid.fields import ColorField, RangeField, Base64FileField
from squidnet import squidprotocol as sp

def message_form_factory(message):
    form_name = ('%s_%s' % (message.device.name, message.name)).title()
    attrs = {}
    for argument in message.arguments:
        attrs[argument.name] = field_factory[argument.argtype.clssquidtype()](
            argument.name, '', argument.default and argument.default.value or '',
            argument.argtype)
    attrs['description'] = message.desc
    attrs['name'] = message.name
    attrs['messageobj'] = message

    def create_squid_args(self):
        arg_types = dict((a.name, a.argtype) for a in self.messageobj.arguments)
        arguments = {}
        for key, value in self.cleaned_data.items():
            arguments[key] = arg_types[key](value)
        return arguments

    attrs['create_squid_args'] = create_squid_args

    return type(str(form_name), (forms.Form,), attrs)


# A mapping between the argument types and their respective field output
field_factory = {
    'boolean': lambda name, desc, default, _: forms.BooleanField(help_text=desc, initial=default),
    'color':   lambda name, desc, default, _: ColorField(help_text=desc, initial=default),
    'integer': lambda name, desc, default, _: forms.IntegerField(help_text=desc, initial=default),
    'range':   lambda name, desc, default, _: RangeField(help_text=desc, initial=default),
    'string':  lambda name, desc, default, _: forms.CharField(help_text=desc, initial=default),
    'base64file': lambda name, desc, default, _: Base64FileField(help_text=desc),
    'enum': lambda name, desc, default, argtype: forms.ChoiceField(help_text=desc, initial=default, choices=[(x, x) for x in argtype.choices]),
    }

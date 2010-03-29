from django import forms

from squidweb.squid.fields import ColorField
from squidnet import squidprotocol as sp

def message_form_factory(message):
    form_name = ('%s_%s' % (message.device.name, message.name)).title()
    attrs = {}
    for argument in message.arguments:
        attrs[argument.name] = field_factory[argument.argtype.argtype](
            argument.name, '')
    attrs['description'] = message.desc
    attrs['name'] = message.name
    attrs['messageobj'] = message

    def create_squid_args(self):
        arg_types = dict((a.name, a.argtype) for a in self.messageobj.arguments)
        arguments = {}
        for key, value in self.cleaned_data.items():
            arguments[key] = sp.SquidValue(arg_types[key], value)
        return arguments

    attrs['create_squid_args'] = create_squid_args

    return type(form_name, (forms.Form,), attrs)


# A mapping between the argument types and their respective field output
field_factory = {
    'boolean': lambda name, desc: forms.BooleanField(help_text=desc),
    'color':   lambda name, desc: ColorField(help_text=desc),
    'integer': lambda name, desc: forms.IntegerField(help_text=desc),
    'range':   lambda name, desc: forms.FloatField(help_text=desc, min_value=0, max_value=1),
    'string':  lambda name, desc: forms.CharField(help_text=desc),
    }

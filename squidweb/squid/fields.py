from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.forms.util import ValidationError
import re

__all__ = ('ColorField',)

color_re = re.compile('^[0-9A-F]{6}$', re.I)

class ColorWidget(forms.Widget):
    class Media:
        js = (settings.MEDIA_URL + "js/jquery.js",
              settings.MEDIA_URL + "js/farbtastic.js",
              settings.MEDIA_URL + "js/colorpicker.js",
              )
        css = {
            'all': (settings.MEDIA_URL + 'css/farbtastic.css',),
            }

    def render(self, name, value, attrs=None):
        data = {'name': name.title(), 'value': value or '#0000FF'}
        if attrs:
            data.update(attrs)
        data['id'] = name.lower()
        return render_to_string('widget/color.html', data)


class ColorField(forms.CharField):
    widget = ColorWidget

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 10
        super(ColorField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(ColorField, self).clean(value)
        value = value.strip().lstrip('#')
        if not color_re.match(value):
            raise ValidationError("A valid hex color code required")
        colors = [int(value[i:i+2], 16)
                  for i in (0, 2, 4)]
        return colors


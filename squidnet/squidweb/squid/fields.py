from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.forms.util import ValidationError

import Image
import cStringIO as StringIO

import re

__all__ = ('ColorField', 'RangeField','Base64FileField')

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

class RangeWidget(forms.Widget):
    class Media:
        js = (settings.MEDIA_URL + 'js/jquery.js',
              settings.MEDIA_URL + 'js/jquery-ui.js',
              )
        css = {
            'all': (settings.MEDIA_URL + 'css/ui-lightness/jquery-ui-1.8.custom.css',),
            }

    def render(self, name, value, attrs=None):
        data = {'name': name.title(), 'value': value or 0}
        if getattr(self, 'attrs', None):
            data.update(self.attrs)
        if attrs:
            data.update(attrs)
        data.setdefault('width', '300px')
        data['id'] = name.lower()
        return render_to_string('widget/range.html', data)

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


class RangeField(forms.FloatField):
    widget = RangeWidget

    def __init__(self, *args, **kwargs):
        self.min_value = kwargs.setdefault('min_value', 0)
        self.max_value = kwargs.setdefault('max_value', 1)
        self.width = kwargs.pop('width', '300px')
        return super(RangeField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        attrs = super(RangeField, self).widget_attrs(widget)
        attrs['width'] = self.width
        attrs['min_value'] = self.min_value
        attrs['max_value'] = self.max_value
        return attrs

class Base64FileField(forms.FileField):
    def clean(self, value, initial):
        
        if value.size < (16 << 10):
            return value.read().encode('base64')
        else:
            im = Image.open(value)
            im.thumbnail((320, 240))
            c = StringIO.StringIO()
            im.save(c, "JPEG")
            c.seek(0)
            return c.read().encode('base64')

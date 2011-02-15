from django import forms

class _BaseForm(object):
    def clean(self):
        cleaned_data = super(_BaseForm, self).clean()
        for field in cleaned_data:
            if isinstance(cleaned_data[field], basestring):
                cleaned_data[field] = \
                  cleaned_data[field].replace('\r\n','\n').strip()

        return cleaned_data

class BaseModelForm(_BaseForm, forms.ModelForm):
    pass

class BaseForm(_BaseForm, forms.Form):
    pass


class VisibleHiddenInput(forms.widgets.TextInput):
    input_type = 'hidden'
    def __init__(self, text, *args, **kwargs):
        super(VisibleHiddenInput, self).__init__(*args, **kwargs)
        self.text = text

    def render(self, name, value, attrs=None):
        output = super(VisibleHiddenInput, self).render(name, value, attrs) + self.text
        return output


class DatePickerMixIn(object):

    def prepare_datefields(self):
        for field in self.fields:
            if isinstance(self.fields[field], forms.fields.DateField):
                self.fields[field].widget.format = '%A, %d %B, %Y'
                self.fields[field].input_formats = ['%A, %d %B, %Y']
                self.fields[field].widget.attrs.update(
                  {'class':'datepicker'}
                )
            elif isinstance(self.fields[field], forms.fields.DateTimeField):
                self.fields[field].widget.format = '%A, %d %B, %Y %H:%M'
                self.fields[field].input_formats = ['%A, %d %B, %Y %H:%M']
                self.fields[field].widget.attrs.update(
                  {'class':'datetimepicker', 'size': '29'}
                )

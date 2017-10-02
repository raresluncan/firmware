""" All the widget objects for creating necesary fields.Holds classes of \
    widgets for:
    -TextAreaField, SelextField, FileField, PasswordField, RadioField
     SubmitField """

from wtforms.widgets import PasswordInput, TextArea, FileInput, HTMLString, \
    Select, html_params, SubmitInput, ListWidget


class WidgetTextArea(TextArea):
    """ a widget to create the text area.Can give extra porperties to construct:
        - _class : adds a class to the TextArea (String)
        - maxlength: add a maxlength property to TextArea (Int/String)
        - rows/cols adds rows and colls properties (Int/String) """
    def __init__(self, **kwargs):
        super(WidgetTextArea, self).__init__()
        self.properties = {
            'class': kwargs.get('_class', 'add-user --input-new-user'),
            'placeholder': kwargs.get('placeholder', 'Enter your info'),
            'onfocus': kwargs.get('onfocus', "this.placeholder = ''"),
            'onblur': kwargs.get('onblur', "this.placeholder = 'Enter your info\
                                 '"),
        }
        if kwargs.get('_class', None) is not None:
            self.properties['class'] = kwargs.get('_class', 'default-class')
        if kwargs.get('maxlength', None) is not None:
            self.properties['maxlength'] = str(kwargs['maxlength'])
        if kwargs.get('rows', None) is  not None:
            self.properties['rows'] = str(kwargs.get('rows', "20"))
        if kwargs.get('cols', None) is  not None:
            self.properties['cols'] = str(kwargs.get('cols', "80"))
        if kwargs.get('id', None) is  not None:
            self.properties['id'] = str(kwargs.get('id', "no-id"))

    def __call__(self, field, **kwargs):
        self.properties['placeholder'] = "Enter " + field.label.text
        self.properties['onblur'] = "this.placeholder = 'Enter " \
            + field.label.text +"'"
        return super(WidgetTextArea, self).__call__(field, **self.properties)


class WidgetFile(FileInput):
    """ adds extra properties toa FileInput:
        - _class - adds a class """
    def __init__(self, **kwargs):
        super(WidgetFile, self).__init__()
        self.properties = {
            'class': kwargs.get('_class', 'file-upload')
        }
        if kwargs.get('id', None) is  not None:
            self.properties['id'] = str(kwargs.get('id', "no-id"))

    def __call__(self, field, **kwargs):
        return super(WidgetFile, self).__call__(field, **self.properties)


class WidgetPassword(PasswordInput):
    """ adds extra properties toa Password INPUT:
        - _class - adds a class (same as WidgetTextArea)"""
    def __init__(self, **kwargs):
        super(WidgetPassword, self).__init__()
        self.properties = {
            'class': kwargs.get('_class', 'add-user --input-new-user'),
            'placeholder': kwargs.get('placeholder', 'Enter your password'),
            'onfocus': kwargs.get('onfocus', "this.placeholder = ''"),
            'onblur': kwargs.get('onblur', "this.placeholder = 'Enter your password'")
        }

    def __call__(self, field, **kwargs):
        if field.label.text == "confirm password":
            self.properties['placeholder'] = "Confirm your password"
            self.properties['onblur'] = "Confirm your password"
        return super(WidgetPassword, self).__call__(field, **self.properties)


class WidgetSubmit(SubmitInput):
    """ adds extra properties to a SubmitInput:
        - _class: adds a class  """
    def __init__(self, **kwargs):
        super(WidgetSubmit, self).__init__()
        self.properties = {
            'class': kwargs.get('_class', 'add-user-submit-button')
        }
    def __call__(self, field, **kwargs):
        return super(WidgetSubmit, self).__call__(field, **self.properties)


class WidgetRadio(ListWidget):
    """ adds extra properties to a ListWidget
        - _class: adds a class """
    def __init__(self, **kwargs):
        super(WidgetRadio, self).__init__()
        self.properties = {
            'class': kwargs.get('_class', 'radio-buttons')
        }

    def __call__(self, field, **kwargs):
        return super(WidgetRadio, self).__call__(field, **self.properties)


class WidgetSelect(Select):
    """ adds extra properties to a Select:
        - disabeled: adds a disabled selected option (String) -> default:
                     -- select an option --"""
    def __init__(self, **kwargs):
        self.disabled = kwargs.get('disabled', '-- select an option --')
        super(WidgetSelect, self).__init__()


    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        html.append('<option disabled selected value>%s</option>' % self.disabled)
        for val, label, selected in field.iter_choices():
            html.append(self.render_option(val, label, selected))
        html.append('</select>')
        return HTMLString(''.join(html))

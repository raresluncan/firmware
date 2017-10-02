""" module containing the classes for form objects """

from wtforms import Form, validators
from wtforms.fields import FileField, TextAreaField, RadioField, SubmitField, \
    PasswordField, SelectField
from firmware.widgets import WidgetTextArea, WidgetPassword, WidgetRadio, \
    WidgetSubmit, WidgetFile, WidgetSelect
from firmware import repository


class AddUser(Form):
    """class used to create the add user form with its fields, validators and
        the validating messages in case of errors """
    username = TextAreaField(
        'username',
        [
            validators.InputRequired(message="Please enter a username"),
            validators.Length(min=2, max=20, message="Username must be \
                              2 and 20 characters")
        ],
        widget=WidgetTextArea(maxlength=20)
    )
    password = PasswordField(
        'password',
        [
            validators.InputRequired(message='Input add a password'),
            validators.DataRequired(message='Passwords must match, Data'),
            validators.EqualTo('confirm_password',
                               message='Passwords must match'),
            validators.Length(min=2, max=120, message='Password must be between\
                              2 and 120 characters')
        ],
        widget=WidgetPassword(maxlength=120)
    )
    confirm_password = PasswordField(
        'confirm_password',
        [
            validators.InputRequired(message='Please confirm your password!--inputccccc'),
        ],
        widget=WidgetPassword(maxlength=120)
    )
    email = TextAreaField(
        'email',
        [
            validators.InputRequired(message="Please enter an email adress"),
            validators.Email(message="Invalid email adress"),
            validators.Length(min=3, max=80, message="Email name must be at \
                              least 3 characters long")
        ],
        widget=WidgetTextArea(maxlength=80)
    )
    name = TextAreaField(
        'name',
        [
            validators.Length(min=2, max=100, message="Name must be at least 2 \
                              characters"),
            validators.optional()
        ],
        widget=WidgetTextArea(maxlength=100)
    )
    surname = TextAreaField(
        'surname',
        [
            validators.Length(min=2, max=100, message="Surname must be at \
                            least 2 characters"),
            validators.optional()
        ],
        widget=WidgetTextArea(maxlength=100)
    )
    contact = TextAreaField(
        'contact',
        [
            validators.Length(min=2, max=60, message="Contact must be at least \
                              2 characters"),
            validators.optional()
        ],
        widget=WidgetTextArea(maxlength=60)
    )
    gender = RadioField(
        'gender',
        widget=WidgetRadio(),
        choices=[('male', 'male'), ('female', 'female')], default='male'
    )
    privilege = RadioField(
        'privilege',
        widget=WidgetRadio(),
        choices=[('user', 'user'), ('admin', 'admin')], default='user'
    )
    avatar = FileField(
        'avatar',
        widget=WidgetFile(id="picture")
    )
    submit = SubmitField(
        'ADD USER',
        widget=WidgetSubmit()
    )


    def to_dict(self):
        """ returns the data in the form fields to a mutable dictionary
            format """
        return {
            'username': self.username.data,
            'password': self.password.data,
            'email': self.email.data,
            'name': self.name.data,
            'surname': self.surname.data,
            'contact': self.contact.data,
            'gender': self.gender.data,
            'privilege': self.privilege.data
        }


class AddCompany(Form):
    """ creates a form for adding a company.Constructor takes optional params:
        - categories - a Category model object mapped to sqlalchemy db
            with an id and domain attribute mapped to id and domain columns
            in the database.The id represents the value of, and the domain the text
            of, the option rendered in HTML <select>."""
    name = TextAreaField(
        'company name',
        [
            validators.InputRequired(message="Please enter a company name"),
            validators.Length(min=2, max=20, message="Name must be between \
                              2 and 20 characters")
        ],
        widget=WidgetTextArea(maxlength=20)
    )
    adress = TextAreaField(
        'adress',
        [
            validators.InputRequired(message="Please enter an adress"),
            validators.Length(min=5, max=120, message="Adress must be between \
                              2 and 120 characters")
        ],
        widget=WidgetTextArea(maxlength=120)
    )
    description = TextAreaField(
        'description',
        [
            validators.InputRequired(message="Please enter a description"),
            validators.Length(min=10, max=150, message="Description must be \
                              at least 10 and up to 150 characters long")
        ],
        widget=WidgetTextArea(maxlength=150)
    )
    category_id = SelectField(
        label='category',
        coerce=int,
        choices=[(a.id, a.domain) for a in repository.get_categories()],
        widget=WidgetSelect(disabled="--SELECT A CATEGORY--"),
        validators=[
            validators.Required(message="Please select a category")
        ]
    )
    details = TextAreaField(
        'details',
        [
            validators.InputRequired(message="Please add a few details"),
            validators.Length(min=1, max=2000, message="Details must be max. \
                              2000 characters long")
        ],
        widget=WidgetTextArea(maxlength=2000, rows=20, cols=80, _class="add-user \
                              --input-new-user details")
        )
    logo = FileField(
        'logo',
        widget=WidgetFile(id="picture")
    )
    submit = SubmitField(
        'ADD COMPANY',
        widget=WidgetSubmit()
    )


    def to_dict(self):
        """ returns the data in the form fields to a mutable dictionary
            format """
        return {
            'name': self.name.data,
            'adress': self.adress.data,
            'description': self.description.data,
            'details': self.details.data,
            'category_id': self.category_id.data,
            'logo': self.logo.data
            }


class LogIn(Form):
    """ Renders a login form containing a username field, password field and
        a submit button"""
    username = TextAreaField(
        'username',
        [
            validators.DataRequired(message="Please enter a username"),
            validators.Length(min=2, max=20, message="Username must be \
                              2 and 20 characters")
        ],
        widget=WidgetTextArea(maxlength=20, rows=0, cols=1)
    )
    password = PasswordField(
        'password',
        [
            validators.InputRequired(message='Please add a password'),
            validators.Length(min=2, max=120, message='Password must be between\
                              2 and 120 characters')
        ],
        widget=WidgetPassword(maxlength=120)
    )

    submit = SubmitField(
        'LOG IN',
        widget=WidgetSubmit()
    )


class AddReview(Form):
    """ Render a form used to add a review for a company """
    message = TextAreaField(
        'review',
        [
            validators.InputRequired(message="Please write a review"),
            validators.Length(min=2, max=2000, message="Review must be \
                              max. 2000 characters")
        ],
        widget=WidgetTextArea(maxlength=2000, rows=20, cols=80,
                              _class="review-field")
    )
    submit = SubmitField(
        'ADD REVIEW',
        widget=WidgetSubmit()
    )

    def to_dict(self):
        """ returns for data as a mutable dictionary """
        return {
            'message': self.message.data
        }

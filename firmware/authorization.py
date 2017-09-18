""" module for operations that need authorization """

def authorize_edit_company(session, company):
    """ function that verifies if the user in the current session has editing
        rights over the company """
    if (session['user'].get('username', 'no-user')
            != company.added_by_user.username):
        errors = dict()
        errors['not-owner'] = ("You are not the owner of this company. \
                               Only %s can edit this page!"
                               % (company.added_by_user.username))
        return errors

""" module containing functions unrelated to the main modules of the app
    used to execute specific tasks """

from werkzeug.datastructures import MultiDict


def dict_to_multidict(dictionary):
    """ transforms a dictionary, dict, to a MultiDict and returns the
        MultiDict """
    if not dictionary:
        return MultiDict()
    imd = MultiDict()
    for key, value in dictionary.items():
        imd.add(key, value)
    return imd

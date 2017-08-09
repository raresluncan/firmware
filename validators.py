import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

def validate_company(request_form, request_files):
    errors = dict()
    if(request_form['company_name'] == ""):
        errors['company_name'] = "Please add a name for your company!"
    if(request_form['company_adress'] == ""):
        errors['company_adress'] = "Please add an adress for your company!"
    if(request_form['company_description'] == ""):
        errors['company_description'] = "Please add a short description for \
        your company!"
    if request_form.get('select-category-list') == None:
        errors['select-category-list'] = 'Please select a category for your \
        company!'
    if(request_form['company_details'] == ""):
        errors['company_details'] = "Please add a few details about your \
        company!"
    return errors

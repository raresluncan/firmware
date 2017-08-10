import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

def validate_company(request_form, request_files):
    errors = dict()
    if(request_form['company_name'] == ""):
        errors['add-name'] = "Please add a name for your company!"
    if(request_form['company_adress'] == ""):
        errors['add-adress'] = "Please add an adress for your company!"
    if(request_form['company_description'] == ""):
        errors['add-description'] = "Please add a short description for \
        your company!"
    if request_form.get('select-category-list') == None:
        errors['add-category'] = 'Please select a category for your \
        company!'
    if(request_form['company_details'] == ""):
        errors['add-details'] = "Please add a few details about your \
        company!"
    return errors

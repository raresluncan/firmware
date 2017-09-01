import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import pdb


def validate_add_company(session):
    errors = dict()
    if not session.get('logged_in', None):
        errors['logged_in'] = "You must be logged in to add a company!"
        return errors
    if session.get('privilege', None) != 'admin':
        errors['not_admin'] = "Sorry, dear %s.Only admins can add companies.\
        Please upgrade to admin." % session.get('username', None)
    return errors


def validate_add_user(session):
    errors = dict()
    if not session.get('logged_in', None):
        errors['logged_in'] = "You must be logged in to add a user!"
        return errors
    if session.get('privilege', None) != 'admin':
        errors['not_admin'] = "Sorry, dear %s.Only admins can add users.\
        Please upgrade to admin." % session.get('username', None)
    return errors


def validate_company(company, company_files):
    errors = dict()
    if(company['company_name'] == ""):
        errors['add-name'] = "Please add a name for your company!"
    if(company['company_adress'] == ""):
        errors['add-adress'] = "Please add an adress for your company!"
    if(company['company_description'] == ""):
        errors['add-description'] = "Please add a short description for \
        your company!"
    if company.get('select-category-list') == None:
        errors['add-category'] = 'Please select a category for your \
        company!'
    if(company['company_details'] == ""):
        errors['add-details'] = "Please add a few details about your \
        company!"
    return errors


def validate_user(user, user_files):
    errors = dict()
    if user['username'] == "":
        errors['username'] = "Please add a username"
    if user['password'] == "":
        errors['password'] = "Please add a password"
    if user['confirm_password'] != user['password']:
        errors['confirm_password'] = "Passwords don't match"
    if user['confirm_password'] == "":
        errors['confirm_password'] = "Please confirm your password!"
    if user['email'] == "":
        errors['email'] = "Please enter an email!"
    return errors


def validate_login(login):
    errors = dict()
    if login['username-login'] == "":
        errors['username-login'] = "Please enter your username"
    if login['password-login'] == "":
        errors['password-login'] = "Please enter your password"
    return errors


def validate_review(review):
    errors = dict()
    if(review['enter-review'] == ""):
        errors['text'] = "Please write a review before submitting"
    return errors

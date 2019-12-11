from flask import Flask, render_template, session, redirect, url_for, escape, request
import sqlite3
import hashlib, os, binascii
from os import path

#---classes

class Pilgrim:
    def __init__(self, id, first_name, last_name, email, level, username):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.level = level
        self.username = username

class Level:
    def __init__(self, id, name, color, image, text, answer, date):
        self.id = id
        self.name = name
        self.color = color
        self.image = image
        self.text = text
        self.answer = answer
        self.date = date

#---functions without routing


def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

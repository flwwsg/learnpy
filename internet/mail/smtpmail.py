#!/usr/bin/python3

import smtplib, sys, email.utils, mailconfig

mailserver = mailconfig.smtpservername
From = input('From? ').strip()
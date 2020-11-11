# IMPORTS
import sys, os, json
import requests
import getpass
import inquirer
import datetime

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from pyfiglet import Figlet
from utils import *

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/methods")
from user import users, switch_me, switch_user
from friend import friends
from slot import slots
from invite import invites, slot_invites
from date import choice_date

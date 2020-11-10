# IMPORTS
import sys, os, json
import requests
import getpass
import inquirer

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from pyfiglet import Figlet
from utils import *

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, dir_path + "/methods")
from user import users, friends, slots, invites, switch_me, switch_user

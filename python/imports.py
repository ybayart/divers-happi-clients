# IMPORTS
import sys, os, json
import requests
import getpass
import inquirer
import datetime
import time
import sys
import websocket

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from pyfiglet import Figlet
from threading import Thread
from utils import *

#dir_path = os.path.dirname(os.path.realpath(__file__))
#sys.path.insert(0, dir_path + "/methods")
from methods import user
from methods import friend
from methods import slot
from methods import invite
from methods import date

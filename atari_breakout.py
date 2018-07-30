import sys
import os
username = os.environ['LOGNAME']
new_path = '/Users/' + username + '/Library/Python/3.6/lib/python/site-packages'
sys.path.insert(0, new_path)

import pygame
from pygame.locals import *

pygame.init()

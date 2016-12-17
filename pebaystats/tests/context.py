
import os, sys
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath('.') + '/pebaystats/tests/')
sys.path.insert(0, os.path.abspath('.') + '/tests/')
sys.path.insert(0, os.path.abspath('.') + '/../')

import pebaystats


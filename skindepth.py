__author__ = 'Chris'
'''Simple frontend to SkinDepth, currently runs the wxPython front end.
Should be trivial to expand to other front ends as they appear.'''
#TODO - think about other UI's, e.g. Pyjamas
from platform import wxSkinDepth
wxSkinDepth.main()
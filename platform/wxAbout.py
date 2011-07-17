'''wxAbout.py - Simple About This Program dialog box, based on code courtesy 
    http://zetcode.com/wxpython/dialogs/ '''

__author__ = 'Chris'
from platform import banelogo
import textwrap
import wx

def About():
    '''Displays a simple wxPython About dialog box'''
    raw_description = '  '.join([
        "Calculates the depth of attenuation or 'skin depth' of electromagnetic waves in conductive materials.",
        "Refer to the documenation for more background info."])
    description = textwrap.fill(raw_description, 75)

    raw_license = '  '.join([
        "Usage of this program is unexpected but governed by the BSD license.",
        "Please refer to the license.txt file for full details."
    ])
    license = textwrap.fill(raw_license, 75)
    with open('version.txt','r') as fid_ver:
        version = fid_ver.readline()

    info = wx.AboutDialogInfo()

    info.SetIcon(banelogo.getBaneIcon())
    info.SetName('SkinDepth')
    info.SetVersion(version)
    info.SetDescription(description)
    info.SetCopyright('(C) 2011 Chris Coughlin')
    info.SetWebSite('http://www.chriscoughlin.com')
    info.SetLicence(license)
    info.AddDeveloper('Chris Coughlin')
    info.AddDocWriter('Chris Coughlin')
    wx.AboutBox(info)
'''wxSkinDepth.py- Defines the wxPython UI for SkinDepth'''

import sys
try:
    import wx
except ImportError as err:
    # Handle errors with importing wxPython, e.g.
    # on OS X Python defaults to 64-bit but the wxPython lib is 32-bit.
    import textwrap
    print("Unable to import wxPython, error was:\n\t{0}\n".format(err.message))
    info_str = '''Please ensure that wxPython has been installed.  OS X users-Python is '''\
        '''usually compiled as a 64-bit application but wxPython is by default 32-bit.  '''\
        '''To temporarily run in 32-bit mode use "arch -i386 python skindepth.py"'''
    print(textwrap.fill(info_str))
    sys.exit(1)
import os
import os.path
import webbrowser
from platform import wxMatWindow
from platform import wxAbout
from platform import SkinDepthController
from material import constants

__author__ = 'Chris'

class wxUI(wx.Frame):
    '''A simple wxFrame for the SkinDepth program.'''
    def __init__(self, parent=None):
        self.parent = parent
        wx.Frame.__init__(self, id=-1, name='', parent=None, title='SkinDepth')
        self.init_menubar()
        self.init_components()
        self.init_db()

    def init_db(self, dbname=":memory:"):
        '''Initializes the application's SQLite database.  Defaults to
        in-memory database if dbname is unspecified.'''
        self.dbname = dbname
        self.controller = SkinDepthController.SkinDepthController(self.dbname)
        self.controller.open()
        self.refresh_materials()

    def refresh_materials(self):
        '''Updates the list of materials after a change to the database'''
        if self.materials_list is not None:
            self.materials_list.Set(self.controller.fetchlist())

    def init_menubar(self):
        '''Sets up the main window's menu bar'''
        self.menubar = wx.MenuBar()

        # File Menu
        self.file_mnu = wx.Menu()
        self.file_mnu.Append(100, "&Open Materials File...\tCTRL+O",
            "Open a materials file")
        self.Bind(wx.EVT_MENU, self.open, id=100)
        self.file_mnu.Append(101, "&Save Materials File\tCTRL+S",
            "Saves current materials file")
        self.Bind(wx.EVT_MENU, self.save, id=101)
        self.file_mnu.Append(102, "Save Materials &As...",
            "Saves current materials list to new file")
        self.Bind(wx.EVT_MENU, self.saveas, id=102)
        self.file_mnu.AppendSeparator()
        self.file_mnu.Append(103, "Import Materials File...",
            "Adds the unique materials from another file into the current file")
        self.Bind(wx.EVT_MENU, self.importdb, id=103)
        self.file_mnu.Append(104, "Import Text File...",
            "Imports a materials file exported from SkinDepth")
        self.Bind(wx.EVT_MENU, self.importmats, id=104)
        self.file_mnu.Append(105, "Export As Text File...",
            "Exports the materials as a SQL script")
        self.Bind(wx.EVT_MENU, self.exportmats, id=105)

        self.file_mnu.AppendSeparator()
        self.file_mnu.Append(106, "Get Updated Materials Database...", "Fetches updates from the website")
        self.Bind(wx.EVT_MENU, self.remote_update, id = 106)
        self.file_mnu.AppendSeparator()
        
        self.file_mnu.Append(111, "E&xit SkinDepth\tALT+F4", "Exit The Program")
        self.Bind(wx.EVT_MENU, self.quit, id=111)
        self.menubar.Append(self.file_mnu, "&File")

        # Operations Menu - add/edit/delete materials
        self.ops_mnu = wx.Menu()
        self.ops_mnu.Append(210, "Add A Material\tCTRL-+", "Adds a material to the database")
        self.Bind(wx.EVT_MENU, self.add_mat, id=210)
        self.ops_mnu.Append(220, "Remove A Material\tCTRL--", "Removes a material from the database")
        self.Bind(wx.EVT_MENU, self.delete_mat, id=220)
        self.menubar.Append(self.ops_mnu, "&Operations")

        # Help Menu
        self.help_mnu = wx.Menu()
        self.help_mnu.Append(400, "Introduction To SkinDepth")
        self.Bind(wx.EVT_MENU, self.show_intro, id=400)
        self.help_mnu.Append(420, "About This Program", "About SkinDepth")
        self.Bind(wx.EVT_MENU, self.about, id=420)
        self.menubar.Append(self.help_mnu, "&Help")
        self.SetMenuBar(self.menubar)

    def init_components(self):
        '''Sets up the controls for the wx UI'''
        self.Bind(wx.EVT_CLOSE, self.quit)
        # Layout:  one main panel w. a list of materials and controls underneath
        self.main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        # self.materials_list : listbox of available SkinDepth materials
        self.materials_lbl = wx.StaticText(self.main_panel, wx.ID_ANY, u"Available Materials:",
            wx.DefaultPosition,wx.DefaultSize, 0)
        self.materials_list = wx.ListBox(self.main_panel, wx.ID_ANY, name="Available Materials")
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.matlist_dclick, self.materials_list)

        # Single vertical BoxSizer to contain materials list
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer.Add(self.materials_lbl, 0, wx.ALL|wx.EXPAND, 5)
        self.panel_sizer.Add(self.materials_list, 1, wx.ALL|wx.EXPAND, 5)

        
        # Layout the skin depth and frequency controls in two
        # horizontal BoxSizers.  Each control consists of a text control
        # for user entry and a combo box to set units (plus labels), and a recalculation button.

        # Define how to allocate space to the various controls on resize-
        # labels unimportant, comboboxes kind of important, text controls
        # very important.
        
        lbl_proportion = 0
        tc_proportion = 1
        cb_proportion = 0.2
        self.sdparams_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.freqparams_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Controls for excitation frequency
        self.freq_lbl = wx.StaticText(self.main_panel, wx.ID_ANY, u"Frequency:",
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.freq_tc = wx.TextCtrl(self.main_panel, wx.ID_ANY, u"",
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.freq_units_choices = [u'mHz', u'Hz', u'kHz', u'MHz', u'GHz']
        self.freq_units_cb = wx.ComboBox(self.main_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize,
            self.freq_units_choices, wx.CB_READONLY)
        self.freq_units_cb.Select(1)
        self.Bind(wx.EVT_COMBOBOX, self.freq_units_cb_changed, self.freq_units_cb)
        self.sd_recalc_btn = wx.Button(self.main_panel, wx.ID_ANY, u"Calculate Skin Depth", wx.DefaultPosition,
            wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.sdbtn_click, self.sd_recalc_btn)
        self.freqparams_sizer.Add(self.freq_lbl, lbl_proportion, wx.ALL|wx.EXPAND, 5)
        self.freqparams_sizer.Add(self.freq_tc, tc_proportion, wx.ALL|wx.EXPAND, 5)
        self.freqparams_sizer.Add(self.freq_units_cb, cb_proportion, wx.ALL|wx.EXPAND, 5)
        self.freqparams_sizer.Add(self.sd_recalc_btn, cb_proportion, wx.ALL|wx.EXPAND, 5)
        self.panel_sizer.Add(self.freqparams_sizer, 0.25, wx.ALL|wx.EXPAND, 0)

        # Controls for skin depth
        self.sd_lbl = wx.StaticText(self.main_panel, wx.ID_ANY, u"Skin Depth:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.sd_tc = wx.TextCtrl(self.main_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.sd_units_choices = [u'mm', u'm', u'inches', u'feet']
        self.sd_units_cb = wx.ComboBox(self.main_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize,
            self.sd_units_choices, wx.CB_READONLY)
        self.sd_units_cb.Select(0)
        self.Bind(wx.EVT_COMBOBOX, self.sd_units_cb_changed, self.sd_units_cb)
        self.freq_recalc_btn = wx.Button(self.main_panel, wx.ID_ANY, u"Calculate Frequency", wx.DefaultPosition,
            wx.DefaultSize, 0)
        self.Bind(wx.EVT_BUTTON, self.freqbtn_click, self.freq_recalc_btn)
        self.sdparams_sizer.Add(self.sd_lbl, lbl_proportion, wx.ALL|wx.EXPAND, 5)
        self.sdparams_sizer.Add(self.sd_tc, tc_proportion, wx.ALL|wx.EXPAND, 5)
        self.sdparams_sizer.Add(self.sd_units_cb, cb_proportion, wx.ALL|wx.EXPAND, 5)
        self.sdparams_sizer.Add(self.freq_recalc_btn, cb_proportion, wx.ALL|wx.EXPAND, 5)
        self.panel_sizer.Add(self.sdparams_sizer, 0.25, wx.ALL|wx.EXPAND, 0)

        self.main_panel.SetSizer(self.panel_sizer)
        self.main_sizer.Add(self.main_panel, 1, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(self.main_sizer)
        self.main_panel.SetSizer(self.panel_sizer)
        self.CreateStatusBar()
        self.SetStatusText("SkinDepth Copyright (C) 2011 Chris Coughlin")
        self.Layout()

    def about(self, evt):
        '''Shows the About Dialog'''
        wxAbout.About()

    def show_intro(self, evt):
        '''Shows the brief Introduction in the user's default web browser'''

        # Build the path to the documentation folder - start by checking if
        # we were run directly.
        base_path = sys.path[0]
        if base_path == '':
            # Running interactively, try using current directory instead
            base_path = os.getcwd()
        intro_url = os.path.join(base_path, "docs", "skindepth.html")
        if os.path.exists(intro_url):
            webbrowser.open(intro_url, new=2, autoraise=True)

    def quit(self, evt):
        '''Confirm exit program'''
        dlg = wx.MessageDialog(self, 'Are you sure you want to quit?', 'Exit SkinDepth?',
            wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        confirm_exit = dlg.ShowModal()
        dlg.Destroy()
        if confirm_exit == wx.ID_OK:
            self.Destroy()

    def open(self, evt):
        '''Opens an existing materials file and sets the materials list'''
        dlg = wx.FileDialog(self, message='Choose File To Open', defaultDir=os.getcwd(), defaultFile='', style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            try:
                self.init_db(dlg.GetPath())
            except Exception as err:
                msg = 'SkinDepth was unable to read this materials file, error was:\n\n{0}'.format(err.message)
                errdlg = wx.MessageDialog(self, caption='Unable To Read File',
                    message=msg, style=wx.OK|wx.ICON_ERROR)
                errdlg.ShowModal()
                errdlg.Destroy()
                self.init_db()

    def save(self, evt):
        '''Saves the current materials list.  If no file is currently in use,
        prompts for filename.'''
        if self.dbname == ":memory:":
            self.saveas(evt)
        else:
            self.controller.update()

    def saveas(self, evt):
        '''Saves the current database to another file'''
        dlg = wx.FileDialog(self, message='Choose Destination File', defaultDir=os.getcwd(), defaultFile='',
            style=wx.SAVE|wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.controller.savecopy(dlg.GetPath())

    def importdb(self, evt):
        '''Imports another SQLite3 database into the current, adding only unique materials.'''
        dlg = wx.FileDialog(self, message='Choose File To Import', defaultDir=os.getcwd(), defaultFile='',
            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            try:
                self.controller.importdb(dlg.GetPath())
                self.refresh_materials()
            except Exception as err:
                msg = 'SkinDepth was unable to import the selected file, error was:\n\n{0}'.format(err.message)
                dlg = wx.MessageDialog(self, caption='Unable To Import File',
                    message=msg, style=wx.OK|wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()

    def importmats(self, evt):
        '''Imports a materials database previously exported as a SQL script text file.'''
        dlg = wx.FileDialog(self, message='Choose File To Import', defaultDir=os.getcwd(), defaultFile='',
            style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            try:
                self.controller.importsql(dlg.GetPath())
                self.refresh_materials()
            except Exception as err:
                msg = 'SkinDepth was unable to import the selected file, error was:\n\n{0}'.format(err.message)
                dlg = wx.MessageDialog(self, caption='Unable To Import File',
                    message=msg, style=wx.OK|wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()

    def exportmats(self, evt):
        '''Exports the materials database to a SQL script'''
        dlg = wx.FileDialog(self, message='Choose Destination File', defaultDir=os.getcwd(), defaultFile='',
            style=wx.SAVE|wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            self.controller.exportsql(dlg.GetPath())

    def matlist_dclick(self, evt):
        '''Handles double-clicks in the materials list - edits the currently
        selected material.'''
        self.add_material(self.materials_list.GetStringSelection())

    def remote_update(self, evt):
        '''Handles the remote update event'''
        progress_dlg = wx.ProgressDialog(title='Retrieving Updates', message='Fetching updates, please wait...')
        progress_dlg.Pulse()
        wx.MilliSleep(350)
        try:
            materials_added = self.controller.import_remotedb()
            progress_dlg.UpdatePulse()
            self.refresh_materials()
            progress_dlg.Update(value=75, newmsg="Found {0} materials, importing...".format(materials_added))
            wx.MilliSleep(750)
        except Exception as err:
            msg = 'Unable to update materials file, error was:\n\n{0}'.format(err.message)
            err_dlg = wx.MessageDialog(self, caption='Unable To Fetch Updates', message=msg, style=wx.OK|wx.ICON_ERROR)
            err_dlg.ShowModal()
            err_dlg.Destroy()
        finally:
            progress_dlg.Update(value = 100)
            progress_dlg.Destroy()

    def add_mat(self, evt):
        '''Handles the Add Material Event'''
        self.add_material()

    def add_material(self, materialname=None):
        '''Pops up a new dialog to add or revise an existing material to the database.'''
        dlg = wxMatWindow.wxMatWindow(self)
        if materialname is not None:
            matdict = self.controller.fetch(materialname)
            dlg.set_material(matname=matdict["name"], matiacs=matdict["iacs"], matmu=matdict["mu_r"],
                matnotes=matdict["notes"])
        if dlg.ShowModal() == wx.ID_OK:
            edited_material = dlg.get_material()
            if edited_material["name"] != "":
                self.controller.add(edited_material)
                self.refresh_materials()
        dlg.Destroy()

    def delete_mat(self, evt):
        '''Handles the Delete Material event'''
        self.delete_material()

    def delete_material(self):
        '''Removes a material from the list on confirmation'''
        materialname = self.materials_list.GetStringSelection()
        if materialname != '':
            dlg = wx.MessageDialog(self, 
                'Are you sure you want to delete %s from the materials list?' % (materialname), 
                'Remove %s?' % (materialname), wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_OK:
                self.controller.remove(materialname)
                self.refresh_materials()
            else:
                dlg.Destroy()

    def sd_units_cb_changed(self, evt):
        '''Skin depth units changed'''
        self.calc_skindepth()

    def freq_units_cb_changed(self, evt):
        '''Skin depth units changed'''
        self.calc_frequency()

    def freqbtn_click(self, evt):
        '''Clicked Calculate Frequency'''
        self.calc_frequency()

    def calc_skindepth(self):
        '''Calculates the excitation frequency and updates the corresponding text control'''
        materialname = self.materials_list.GetStringSelection()
        if materialname != '':
            try:
                freq = float(self.freq_tc.GetValue()) * self.get_frequnits_factor()
                skindepth = round(self.controller.calcdelta(materialname, freq) / self.get_deltaunits_factor(), 3)
                self.sd_tc.SetValue(str(skindepth))
            except ValueError:
                '''Couldn't convert the frequency text control contents to a float, skip and swallow'''
                return
        else:
            dlg = wx.MessageDialog(self, caption='No Material Selected',
                message='Please select a material for calculating\nskin depth.', style=wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def get_frequnits_factor(self):
        '''Returns the unit conversion factor for the frequency
        based on the value of the units combo box'''
        multipliers = [1e-3, 1, 1e3, 1e6, 1e9]
        return multipliers[self.freq_units_cb.GetSelection()]

    def get_deltaunits_factor(self):
        '''Returns the unit conversion factor for the skin depth
        based on the value of the units combo box'''
        inches_per_metre = constants.MillimetresPerInch * 1e-3
        multipliers = [1e-3, 1, inches_per_metre, 12.0*inches_per_metre]
        return multipliers[self.sd_units_cb.GetSelection()]

    def sdbtn_click(self, evt):
        '''Clicked the Calculate Skin Depth button'''
        self.calc_skindepth()

    def calc_frequency(self):
        '''Calculates the skin depth and updates the corresponding text control'''
        materialname = self.materials_list.GetStringSelection()
        if materialname != '':
            try:
                skindepth = float(self.sd_tc.GetValue())*self.get_deltaunits_factor()
                # Display excitation frequency result in currently selected units'''
                new_freq = round(self.controller.calcfrequency(materialname, skindepth) / self.get_frequnits_factor(),
                    3)
                self.freq_tc.SetValue(str(new_freq))
            except ValueError:
                # Couldn't convert entry in skin depth text control to float, ignore
                return
        else:
            dlg = wx.MessageDialog(self, caption='No Material Selected',
                message='Please select a material for calculating\nexcitation frequency.', style=wx.OK|wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

def main():
    '''Main entry point of the program - creates and runs the wxPython UI'''
    app = wx.App()
    ui = wxUI()
    ui.Show(True)
    app.MainLoop()

if __name__ == "__main__":
    main()
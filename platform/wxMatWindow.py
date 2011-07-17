'''wxMatWindow.py - Defines the window to revise/create materials in SkinDepth's wxPython UI'''

__author__ = 'Chris'
import wx

class wxMatWindow(wx.Dialog):
    '''Creates a window to revise and create Materials in SkinDepth's wxPython frontend'''
    lbl_proportion = 0
    tc_proportion = 1
    cb_proportion = 0.2
    sizer_flags = wx.ALL|wx.EXPAND
    widget_margin = 5

    def __init__(self, parent, id=wx.ID_ANY, title="Add/Edit Material", size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE,):
        wx.Dialog.__init__(self, parent, id, title, pos, size, style)
        self.init_components()

    def init_components(self):
        '''Creates the UI of the dialog'''

        # Layout:  one main panel w. a list of materials and controls underneath
        self.main_panel = wx.Panel(self)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel_sizer = wx.FlexGridSizer(cols=2)
        self.panel_sizer.AddGrowableCol(1, 1)
        self.matname_lbl = wx.StaticText(self.main_panel, wx.ID_ANY, u"Material Name:", wx.DefaultPosition, 
            wx.DefaultSize, 0)
        self.matname_tc = wx.TextCtrl(self.main_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.panel_sizer.Add(self.matname_lbl, self.lbl_proportion, self.sizer_flags, self.widget_margin)
        self.panel_sizer.Add(self.matname_tc, self.tc_proportion, self.sizer_flags, self.widget_margin)

        
        self.matiacs_lbl = wx.StaticText(self.main_panel, wx.ID_ANY, u"Electrical Conductivity (%IACS):", 
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.matiacs_tc = wx.TextCtrl(self.main_panel, wx.ID_ANY, u"", wx.DefaultPosition, wx.DefaultSize, 0)
        self.panel_sizer.Add(self.matiacs_lbl, self.lbl_proportion, self.sizer_flags, self.widget_margin)
        self.panel_sizer.Add(self.matiacs_tc, self.tc_proportion, self.sizer_flags, self.widget_margin)

        self.matmu_lbl = wx.StaticText(self.main_panel, wx.ID_ANY, u"Relative Magnetic Permeability:",
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.matmu_tc = wx.TextCtrl(self.main_panel, wx.ID_ANY, u"",
                                   wx.DefaultPosition, wx.DefaultSize,0)
        self.panel_sizer.Add(self.matmu_lbl, self.lbl_proportion, self.sizer_flags, self.widget_margin)
        self.panel_sizer.Add(self.matmu_tc, self.tc_proportion, self.sizer_flags, self.widget_margin)

        self.matnotes_lbl = wx.StaticText(self.main_panel, wx.ID_ANY, u"Notes:",
            wx.DefaultPosition, wx.DefaultSize, 0)
        self.matnotes_tc = wx.TextCtrl(self.main_panel, wx.ID_ANY, u"", wx.DefaultPosition, size=wx.Size(320, 75),
            style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
        self.panel_sizer.Add(self.matnotes_lbl, self.lbl_proportion, self.sizer_flags, self.widget_margin)
        self.panel_sizer.Add(self.matnotes_tc, self.tc_proportion, self.sizer_flags, self.widget_margin)

        self.btn_sizer = wx.StdDialogButtonSizer()
        self.ok_btn = wx.Button(self, wx.ID_OK)
        self.btn_sizer.AddButton(self.ok_btn)
        self.cancel_btn = wx.Button(self, wx.ID_CANCEL)
        self.btn_sizer.AddButton(self.cancel_btn)
        self.btn_sizer.Realize()

        self.main_panel.SetSizer(self.panel_sizer)
        self.main_sizer.Add(self.main_panel, 1, self.sizer_flags, self.widget_margin)
        self.main_sizer.Add(self.btn_sizer, 0, self.sizer_flags, self.widget_margin)
        self.SetSizer(self.main_sizer)
        self.main_sizer.Fit(self)

    def set_material(self, matname, matiacs, matmu, matnotes):
        '''Sets the widget contents to the specified Material properties.'''
        self.matname_tc.SetValue(matname)
        self.matiacs_tc.SetValue(str(matiacs))
        self.matmu_tc.SetValue(str(matmu))
        self.matnotes_tc.SetValue(matnotes)

    def get_material(self):
        '''Returns a dict of the current Material properties.'''
        try:
            iacs =  float(self.matiacs_tc.GetValue())
        except ValueError:
            iacs = 0.0
        try:
            mu_r = float(self.matmu_tc.GetValue())
        except ValueError:
            mu_r = 1.0
        material = {"name":self.matname_tc.GetValue(),
                    "notes":self.matnotes_tc.GetValue(),
                    "iacs":iacs,
                    "mu_r":mu_r}
        return material
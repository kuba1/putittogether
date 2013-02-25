#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.5 on Mon Feb 18 21:33:16 2013

import wx
import engine
import sqlite3

# begin wxGlade: extracode
# end wxGlade


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.mainFrame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        self.load = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "&Load", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.load)
        self.restart = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "&Restart", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.restart)
        self.play = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "&Play", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.play)
        self.quit = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "&Quit", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.quit)
        self.mainFrame_menubar.Append(wxglade_tmp_menu, "&File")
        self.SetMenuBar(self.mainFrame_menubar)
        # Menu Bar end
        
        # Tool Bar
        self.mainFrame_toolbar = wx.ToolBar(self, -1)
        self.SetToolBar(self.mainFrame_toolbar)
        self.load_tool = self.mainFrame_toolbar.AddLabelTool(wx.NewId(), "Load",\
                wx.BitmapFromImage(wx.Image('glyphicons_144_folder_open.png', wx.BITMAP_TYPE_PNG)),\
                wx.BitmapFromImage(wx.Image('glyphicons_144_folder_open.png', wx.BITMAP_TYPE_PNG)),\
                wx.ITEM_NORMAL, "", "")
        self.restart_tool = self.mainFrame_toolbar.AddLabelTool(wx.NewId(), "Restart",\
                wx.BitmapFromImage(wx.Image('glyphicons_081_refresh.png', wx.BITMAP_TYPE_PNG)),\
                wx.BitmapFromImage(wx.Image('glyphicons_081_refresh.png', wx.BITMAP_TYPE_PNG)),\
                wx.ITEM_NORMAL, "", "")
        self.mainFrame_toolbar.AddSeparator()
        self.presentation_tool = self.mainFrame_toolbar.AddLabelTool(wx.NewId(), "Presentation",\
                wx.BitmapFromImage(wx.Image('glyphicons_008_film.png', wx.BITMAP_TYPE_PNG)),\
                wx.BitmapFromImage(wx.Image('glyphicons_008_film.png', wx.BITMAP_TYPE_PNG)),\
                wx.ITEM_NORMAL, "", "")
        self.mainFrame_toolbar.AddControl(wx.ComboBox(self.mainFrame_toolbar))
        self.play_tool = self.mainFrame_toolbar.AddLabelTool(wx.NewId(), "Play",\
                wx.BitmapFromImage(wx.Image('glyphicons_173_play.png', wx.BITMAP_TYPE_PNG)),\
                wx.BitmapFromImage(wx.Image('glyphicons_173_play.png', wx.BITMAP_TYPE_PNG)),\
                wx.ITEM_NORMAL, "", "")
        # Tool Bar end
        self.mainFrame_statusbar = self.CreateStatusBar(1, 0)
        self.puzzle = engine.PuzzleFrame(self)

        self.__set_properties()
        self.__do_layout()

        self.timer = wx.Timer(self)

        self.Bind(wx.EVT_MENU, self.menuLoad, self.load)
        self.Bind(wx.EVT_MENU, self.menuRestart, self.restart)
        self.Bind(wx.EVT_MENU, self.menuPlay, self.play)
        self.Bind(wx.EVT_MENU, self.menuQuit, self.quit)
        self.Bind(wx.EVT_TOOL, self.menuLoad, self.load_tool)
        self.Bind(wx.EVT_TOOL, self.menuRestart, self.restart_tool)
        self.Bind(wx.EVT_TOOL, self.menuPlay, self.play_tool)
        self.Bind(wx.EVT_TOOL, self.menuPresentation, self.presentation_tool)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)

        self.timer.Start(1000.0 / 30.0)
        # end wxGlade

        self.path = None

    def Update(self, e):
        self.puzzle.Update()

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("PutItTogether")
        self.mainFrame_toolbar.SetToolBitmapSize((16, 15))
        self.mainFrame_toolbar.Realize()
        self.mainFrame_statusbar.SetStatusWidths([-1])
        # statusbar fields
        mainFrame_statusbar_fields = ["mainFrame_statusbar"]
        for i in range(len(mainFrame_statusbar_fields)):
            self.mainFrame_statusbar.SetStatusText(mainFrame_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.puzzle, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
        # end wxGlade

    def menuLoad(self, event):  # wxGlade: MainFrame.<event_handler>
        wldcrd = 'ALL (*.*)|*.*|BMP (*.bmp)|*.bmp|JPG (*.jpg)|*.jpg|PNG (*.png)|*.png'
        dialog = wx.FileDialog(self, style=wx.FD_OPEN, wildcard=wldcrd)
        dialog.ShowModal()
        self.path = dialog.GetPath()
        if self.path and wx.Image.CanRead(self.path):
            self.puzzle.LoadPuzzle(self.path)
        else:
            pass
            #w = wx.MessageDialog(self, self.db[9][0], self.db[7][0], wx.OK)
            #w.ShowModal()

    def menuRestart(self, event):  # wxGlade: MainFrame.<event_handler>
        if self.path and wx.Image.CanRead(self.path):
            self.puzzle.LoadPuzzle(self.path)
        else:
            pass

    def menuPlay(self, event):
        print "Event handler `menuPlay' not implemented!"

    def menuPresentation(self, event):
        print "Event handler `menuPresentation' not implemented!"

    def menuQuit(self, event):
        self.Close()

class PresentationFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)

# end of class MainFrame
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    mainFrame = MainFrame(None, -1, "")
    app.SetTopWindow(mainFrame)
    mainFrame.Show()
    app.MainLoop()

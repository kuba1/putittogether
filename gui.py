#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.5 on Mon Feb 18 21:33:16 2013

import os
import wx
import engine
import frames
import sqlite3
from sqlite3 import OperationalError

# begin wxGlade: extracode
# end wxGlade


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        self._check_db()

        self._captions = {}
        self._read_captions()
        print(self._captions)

        # Menu Bar
        self._mainFrame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        self._load = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), self._captions['_load'], "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self._load)
        self._restart = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), self._captions['_restart'], "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self._restart)
        self._stop = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), self._captions['_stop'], "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self._stop)
        self._play = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), self._captions['_play'], "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self._play)
        self._quit = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), self._captions['_quit'], "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self._quit)
        self._mainFrame_menubar.Append(wxglade_tmp_menu, self._captions['wxglade_tmp_menu']) 
        self.SetMenuBar(self._mainFrame_menubar)
        # Menu Bar end
        
        # Tool Bar
        self._mainFrame_toolbar = wx.ToolBar(self, -1)
        self.SetToolBar(self._mainFrame_toolbar)
        self._load_tool = self._mainFrame_toolbar.AddLabelTool(wx.NewId(), "Load",\
                wx.BitmapFromImage(wx.Image('glyphicons_144_folder_open.png', wx.BITMAP_TYPE_PNG)),\
                wx.BitmapFromImage(wx.Image('glyphicons_144_folder_open.png', wx.BITMAP_TYPE_PNG)),\
                wx.ITEM_NORMAL, self._captions['_load_tool_shortHelp'], "")
        self._restart_tool = self._mainFrame_toolbar.AddLabelTool(wx.NewId(), "Restart",\
                wx.BitmapFromImage(wx.Image('glyphicons_081_refresh.png', wx.BITMAP_TYPE_PNG)),\
                wx.BitmapFromImage(wx.Image('glyphicons_081_refresh.png', wx.BITMAP_TYPE_PNG)),\
                wx.ITEM_NORMAL, self._captions['_restart_tool_shortHelp'], "")
        self._mainFrame_toolbar.AddSeparator()
        self._presentations_box = wx.ComboBox(self._mainFrame_toolbar)
        self._combo_tool = self._mainFrame_toolbar.AddControl(self._presentations_box)
        self._presentation_tool = self._mainFrame_toolbar.AddLabelTool(wx.NewId(), "Presentation",\
                wx.BitmapFromImage(wx.Image('glyphicons_008_film.png', wx.BITMAP_TYPE_PNG)),\
                wx.BitmapFromImage(wx.Image('glyphicons_008_film.png', wx.BITMAP_TYPE_PNG)),\
                wx.ITEM_NORMAL, self._captions['_presentation_tool_shortHelp'], "")
        self._stop_tool = self._mainFrame_toolbar.AddLabelTool(wx.NewId(), "Stop",\
                wx.BitmapFromImage(wx.Image('glyphicons_175_stop.png', wx.BITMAP_TYPE_PNG)),\
                wx.BitmapFromImage(wx.Image('glyphicons_175_stop.png', wx.BITMAP_TYPE_PNG)),\
                wx.ITEM_NORMAL, self._captions['_stop_tool_shortHelp'], "")
        self._play_tool = self._mainFrame_toolbar.AddLabelTool(wx.NewId(), "Play",\
                wx.BitmapFromImage(wx.Image('glyphicons_173_play.png', wx.BITMAP_TYPE_PNG)),\
                wx.BitmapFromImage(wx.Image('glyphicons_173_play.png', wx.BITMAP_TYPE_PNG)),\
                wx.ITEM_NORMAL, self._captions['_play_tool_shortHelp'], "")
        # Tool Bar end
        self._mainFrame_statusbar = self.CreateStatusBar(1, 0)
        self._puzzle = engine.PuzzleFrame(self)

        self.__set_properties()
        self.__do_layout()

        self._timer = wx.Timer(self)

        self.Bind(wx.EVT_MENU, self._menu_load, self._load)
        self.Bind(wx.EVT_MENU, self._menu_restart, self._restart)
        self.Bind(wx.EVT_MENU, self._menu_play, self._play)
        self.Bind(wx.EVT_MENU, self._menu_stop, self._stop)
        self.Bind(wx.EVT_MENU, self._menu_quit, self._quit)
        self.Bind(wx.EVT_TOOL, self._menu_load, self._load_tool)
        self.Bind(wx.EVT_TOOL, self._menu_restart, self._restart_tool)
        self.Bind(wx.EVT_TOOL, self._menu_play, self._play_tool)
        self.Bind(wx.EVT_TOOL, self._menu_stop, self._stop_tool)
        self.Bind(wx.EVT_TOOL, self._menu_presentation, self._presentation_tool)
        self.Bind(wx.EVT_TIMER, self._update, self._timer)

        self._timer.Start(1000.0 / 30.0)
        # end wxGlade

        self._path = None
        self._get_presentations()

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("PutItTogether")
        self._mainFrame_toolbar.SetToolBitmapSize((16, 15))
        self._mainFrame_toolbar.Realize()
        self._mainFrame_statusbar.SetStatusWidths([-1])
        # statusbar fields
        mainFrame_statusbar_fields = ["mainFrame_statusbar"]
        for i in range(len(mainFrame_statusbar_fields)):
            self._mainFrame_statusbar.SetStatusText(mainFrame_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self._puzzle, 1, wx.EXPAND, 0)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Layout()
        # end wxGlade

    def _update(self, e):
        self._puzzle.update()

    def _menu_load(self, event):  # wxGlade: MainFrame.<event_handler>
        wldcrd = 'ALL (*.*)|*.*|BMP (*.bmp)|*.bmp|JPG (*.jpg)|*.jpg|PNG (*.png)|*.png'
        dialog = wx.FileDialog(self, style=wx.FD_OPEN, wildcard=wldcrd)
        dialog.ShowModal()
        path = dialog.GetPath()
        if path and wx.Image.CanRead(path):
            self._path = path
            self._puzzle.load_puzzle(self._path)
        else:
            w = wx.MessageDialog(self, self._captions['file_load_error'], self._captions['error_title'], wx.OK)
            w.ShowModal()

    def _menu_restart(self, event):  # wxGlade: MainFrame.<event_handler>
        if self._path and wx.Image.CanRead(self._path):
            self._puzzle.load_puzzle(self._path)

    def _menu_play(self, event):
        print "Event handler `menuPlay' not implemented!"

    def _menu_stop(self, event):
        print "Event handler `menuStop' not implemented!"

    def _menu_presentation(self, event):
        frames_frame = frames.FramesDialog(self, captions=self._captions)
        frames_frame.ShowModal()

    def _menu_quit(self, event):
        self.Close()

    def _read_captions(self):
        try:
            co = sqlite3.connect('data.db')
            cu = co.cursor()
            cu.execute('SELECT c.key, c.value FROM captions c INNER JOIN languages l\
                    ON c.language_id = l.id\
                    WHERE l.name = (SELECT value FROM settings WHERE key = "language")'
            )
            captions = cu.fetchall()
        except Exception as e:
            w = wx.MessageDialog(self, 'Database read error. This shouldn\'t have happened unless the database has been damaged!\n\nBlad odczytu z bazy danych. To nie powinno sie zdarzyc chyba ze baza danych zostala uszkodzona!\n\n' + str(e), 'Serious error! / Powazny blad!', wx.OK)
            w.ShowModal()
            exit()
        else:
            for (name, value) in captions:
                self._captions[name] = value
        finally:
            cu.close()
            co.close()

    def _get_presentations(self):
        co = sqlite3.connect('data.db')
        cu = co.cursor()
        try:
            cu.execute('SELECT * FROM presentations')
            presentations = cu.fetchall()
        except:
            raise
        else:
            for p in presentations:
                self._presentations_box.Append(p[1], p[0])
            self._presentations_box.SetSelection(0)
        finally:
            cu.close()
            co.close()

    def _add_presentation(self, name):
        co = sqlite3.connect('data.db')
        cu = co.cursor()
        try:
            cu.execute('INSERT INTO presentations VALUES ("' + str(self._presentations_box.GetCount()) + '", "'\
                    + name + '")')
            co.commit()
        except:
            #TODO: show error dialog
            raise
        else:
            #TODO: change id from autoincrement into combobox index and it should
            # take care of the id bullshit
            self._presentations_box.Append(name)
        finally:
            cu.close()
            co.close()

    def _update_presentation(self, idv, name):
        co = sqlite3.connect('data.db')
        cu = co.cursor()
        try:
            cu.execute('UPDATE presentations SET name = "' + name + '" WHERE id = ' + str(idv))
            co.commit()
        except:
            raise
        else:
            pass
        finally:
            cu.close()
            co.close()

    def _get_frames(self, pres_id):
        co = sqlite3.connect('data.db')
        cu = co.cursor()
        try:
            cu.execute('UPDATE presentation SET name = "' + name + '" WHERE id = ' + str(idv))
            co.commit()
        except:
            raise
        else:
            pass
        finally:
            cu.close()
            co.close()

    def _add_frame(self, pres_id, data):
        pass

    def _check_db(self):
        if os.path.isfile('data.db'):
            return
        else:
            w = wx.MessageDialog(self, 'Cannot find database. Empty database will be created!\n\nNie mozna znalezc bazy danych. Zostanie stworzona pusta baza danych!', 'Serious error! / Powazny blad!', wx.OK)
            w.ShowModal()

        try:
            co = sqlite3.connect('data.db')
            f = open('recreate.sql', 'r')
            co.executescript(f.read())
            f.close()
            co.commit()
        except Exception as e:
            w = wx.MessageDialog(self, 'Database creation error. This shouldn\'t have happened unless the database engine on the system is not working properly!\n\nBlad przy tworzeniu bazy danych. To nie powinno sie zdarzyc chyba ze silnik bazodanowy w systemie nie dziala poprawnie!\n\n' + str(e), 'Serious error! / Powazny blad!', wx.OK)
            w.ShowModal()
            exit()
        finally:
            co.close()

# end of class MainFrame
if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    mainFrame = MainFrame(None, -1, "")
    app.SetTopWindow(mainFrame)
    mainFrame.Show()
    app.MainLoop()

import sys

import wx.adv
import wx
import os
import lua_extracting
import json_util as util
import background

VERSION = 'v.1.2.2'

TRAY_TOOLTIP = 'L.O.C.K.E.D'
TRAY_ICON = 'imgs/icon.png'
SAVE_FILE = 'save_file.json'
BACKGROUND_IMG = 'imgs/vulpera.jpg'


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


window_size = (1000, 700)


class MainWindow(wx.Frame):
    data = {}
    data_list = []
    savedPath = ''
    savedPlayer = ''
    name = "main"

    def __init__(self):
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            wx.MessageBox("Another instance is running", "ERROR")
            return
        wx.Frame.__init__(self, None, wx.ID_ANY, 'L.O.C.K.E.D' + ' (' + VERSION + ')',
                          pos=(100, 100), size=window_size)
        wx.Window.SetMinSize(self, size=window_size)
        wx.Window.SetMaxSize(self, size=window_size)

        # =============BACKGROUND STUFF=============
        img = wx.Image(BACKGROUND_IMG)
        img = img.Scale(window_size[0], window_size[1], wx.IMAGE_QUALITY_HIGH)
        self.BgBitmap = wx.Bitmap(img)

        self.Bind(wx.EVT_ERASE_BACKGROUND, self.on_erase_background)

        self.button1 = wx.Button(self, id=-1, label='Save info and search for characters',
                                 pos=(10, 120), size=(200, 30))

        self.button1.Bind(wx.EVT_BUTTON, self.find_characters)

        font = wx.Font(14, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        self.top_label = wx.StaticText(self, pos=(10, 15), label="Select your WoW directory:")
        self.top_label.SetBackgroundColour('white')
        self.top_label.SetFont(font)

        self.dirPicker = wx.DirPickerCtrl(self, size=(500, -1),  pos=(10, 40), message="select WoW directory")
        self.dirPicker.TextCtrl.SetSize((400, -1))
        self.dirPicker.PickerCtrl.SetPosition((410, 0))

        self.check_label = wx.StaticText(self, pos=(10, 160), label="Chars found in WoW directory:")
        self.check_label.SetBackgroundColour('white')
        self.check_label.SetFont(font)

        self.checkList = wx.CheckListBox(self, size=(300, 250), pos=(10, 190))
        # Load saved path from json and make default
        self.savedPath = util.load_path(SAVE_FILE)
        if self.savedPath != "":
            self.dirPicker.SetPath(self.savedPath)

        self.player_name = wx.TextCtrl(self, id=-1, size=(140, -1), pos=(10, 80))
        self.player_name.SetHint("Player name")
        self.savedPlayer = util.load_player(SAVE_FILE)
        if self.savedPlayer != '':
            self.player_name.SetValue(self.savedPlayer)

        self.button2 = wx.Button(self, id=-1, label='Save selected chars',
                                 pos=(10, 450), size=(150, 30))

        self.button2.Bind(wx.EVT_BUTTON, self.save_selected)

        tracked_chars = util.load_tracked_characters(SAVE_FILE)

        self.track_label = wx.StaticText(self, pos=(650, 160), label="Currently tracked chars:")
        self.track_label.SetBackgroundColour('white')
        self.track_label.SetFont(font)

        self.track_list = wx.ListBox(self, size=(300, 250), pos=(650, 190), choices=tracked_chars)

        self.Raise()
        self.Show(True)

    def on_erase_background(self, event):
        EraseDC = event.GetDC()
        if EraseDC is None:
            EraseDC = wx.ClientDC(self)

        memory_dc = wx.MemoryDC()
        memory_dc.SelectObject(self.BgBitmap)
        EraseDC.Blit(0, 0, self.BgBitmap.GetWidth(),
                     self.BgBitmap.GetHeight(), memory_dc, 0, 0)
        memory_dc.SelectObject(wx.NullBitmap)

    def find_characters(self, event):
        # for each account in wow folder, find locked_out file and parse to extracting.
        folder_path = self.dirPicker.GetPath()

        # save path
        util.save_path(folder_path, SAVE_FILE)
        # save player name
        player = self.player_name.GetValue()
        util.save_player(player, SAVE_FILE)

        folder_path = os.path.join(folder_path, "_retail_", "WTF", "Account")
        locked_out_paths = []

        for dir in os.walk(folder_path):
            locked_out_file = os.path.join(folder_path, dir[0], "SavedVariables", "AB_Locked.lua")
            if os.path.exists(locked_out_file):
                locked_out_paths.append(locked_out_file)

        info_strings = []
        key_results = set()  # set of keys
        for path in locked_out_paths:
            for res in lua_extracting.extractkeys(path):
                key_results.add(res)  # since its a set it auto check for duplicate entries

        for key_tuple in key_results:
            self.data[key_tuple[0]] = key_tuple
            info_strings.append(key_tuple[0] + ": " + key_tuple[1] + " +" + str(key_tuple[2]))

        self.data_list = list(self.data.values())
        self.checkList.Set(info_strings)

    def save_selected(self, event):
        # find selected from self.dirPicker.
        items = self.checkList.GetCheckedItems()
        to_be_saved = []
        for item in items:
            to_be_saved.append(self.data_list[item][0])
        # save in lua file.
        chars_deleted = util.save_chars(to_be_saved, SAVE_FILE)
        background.save_keys_to_db()
        wx.MessageBox("Updated your tracked characters! \n \nRemoved the following chars: \n"
                      + '\n'.join(chars_deleted) + '\n' +
                      '\nStarted tracking: \n'
                      + '\n'.join(to_be_saved),
                      "Changes")
        self.track_list.Set(to_be_saved)


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        self.name = "LOCKED TASKBAR"
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            wx.MessageBox("Another instance is running", "ERROR")
            sys.exit(0)
            return
        self.frame = frame
        super(TaskBarIcon, self).__init__()
        self.set_icon(TRAY_ICON)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.show)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Open', self.show)
        menu.AppendSeparator()
        create_menu_item(menu, 'Close program', self.on_exit)
        return menu

    def set_icon(self, path):
        icon = wx.Icon(path)
        self.SetIcon(icon, TRAY_TOOLTIP)

    def show(self, event):
        # open new window!
        MainWindow()

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class App(wx.App):
    def OnInit(self):
        frame = wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True


def main():
    app = App(False)
    if not util.save_file_exist_with_path(SAVE_FILE):
        MainWindow()
    app.MainLoop()


if __name__ == '__main__':
    main()
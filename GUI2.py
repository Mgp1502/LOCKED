import threading

import wx.adv
import wx
import os
import lua_extracting
import json_util as util

TRAY_TOOLTIP = 'L.O.C.K.E.D'
TRAY_ICON = 'icon.png'
save_file = 'save_file.json'


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class mainWindow(wx.Frame):
    info_strings = []
    data = []
    savedPath = ''
    name = "main"

    def __init__(self):
        self.instance = wx.SingleInstanceChecker(self.name)
        if self.instance.IsAnotherRunning():
            wx.MessageBox("Another instance is running", "ERROR")
            return
        wx.Frame.__init__(self, None, wx.ID_ANY, 'L.O.C.K.E.D',
                          pos=(100, 100), size=(680, 550))

        self.button1 = wx.Button(self, id=-1, label='Find characters',
                                 pos=(10, 80), size=(100, 30))

        self.button1.Bind(wx.EVT_BUTTON, self.find_characters)

        self.track_label = wx.StaticText(self, pos=(10, 20), label="Select your WoW directory:")
        self.dirPicker = wx.DirPickerCtrl(self,  pos=(10, 40), message="select WoW directory")

        self.check_label = wx.StaticText(self, pos=(10, 120), label="Chars found in WoW directory:")
        self.checkList = wx.CheckListBox(self, size=(200, 250), pos=(10, 150), choices=self.info_strings)
        # Load saved path from json and make default
        self.savedPath = util.load_path(save_file)
        if self.savedPath != "":
            self.dirPicker.SetPath(self.savedPath)

        self.button2 = wx.Button(self, id=-1, label='Save selected chars',
                                 pos=(10, 410), size=(150, 30))

        self.button2.Bind(wx.EVT_BUTTON, self.save_selected)

        tracked_chars = util.load_chars(save_file)

        self.track_label = wx.StaticText(self, pos=(350, 120), label="Currently tracked chars:")
        self.track_list = wx.ListBox(self, size=(200, 250), pos=(350, 150), choices=tracked_chars)

        self.Raise()
        self.Show(True)


    def find_characters(self, event):
        self.checkList.Destroy()
        # for each account in wow folder, find locked_out file and parse to extracting.
        folder_path = self.dirPicker.GetPath()

        # TODO save path in json file,
        util.save_path(folder_path, save_file)
        folder_path = os.path.join(folder_path, "_retail_", "WTF", "Account")

        locked_out_paths = []

        for dir in os.walk(folder_path):
            if dir[0] == "SavedVariables":
                continue
            else:
                locked_out_file = os.path.join(folder_path, dir[0], "SavedVariables", "LockedOut.lua")
                if os.path.exists(locked_out_file):
                    locked_out_paths.append(locked_out_file)

        self.info_strings = []
        self.data = []
        for path in locked_out_paths:
            #TODO check for no duplicates of entries
            self.data = self.data + lua_extracting.extract(path)
            for entry in self.data:
                self.info_strings.append(entry[0] + ": " + entry[1] + " +" + str(entry[2]))

        self.checkList = wx.CheckListBox(self, pos=(10, 150), size=(200, 250), choices=self.info_strings)
        print(self.dirPicker.GetPath())

    def save_selected(self, event):
        # find selected from self.dirPicker.
        items = self.checkList.GetCheckedItems()
        to_be_saved = []
        for item in items:
            to_be_saved.append(self.data[item][0])
        # save in lua file.
        util.save_chars(to_be_saved, save_file)
        wx.MessageBox("Updated your tracked characters!", "Updated")
        self.track_list.Destroy()
        self.track_list = wx.ListBox(self, size=(200, 250), pos=(350, 150), choices=to_be_saved)


class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
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
        mainWindow()

    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
        self.frame.Close()


class App(wx.App):
    def OnInit(self):
        frame=wx.Frame(None)
        self.SetTopWindow(frame)
        TaskBarIcon(frame)
        return True


def main():
    app = App(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
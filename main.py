# ------------------------------------------------------------
# mediaLocker.py
#
# Author: Mike Driscoll
# Contact: mike@pythonlibrary.org
#
# This program demonstrates how to work with a SQLite database
# using wxPython and SqlAlchemy. It is also an example of MVC
# concepts and how to put together a fully working wxPython
# application.
# ------------------------------------------------------------

import addModRecord
import commonDlgs
from controller import Controller
import wx
from ObjectListView import ObjectListView, ColumnDefn
from model import SaleOrder

########################################################################
class ButtonPanel(wx.Panel):

  def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)

        addRecordBtn = wx.Button(self, label="Add")
        addRecordBtn.Bind(wx.EVT_BUTTON, parent.onAddRecord)
        btnSizer.Add(addRecordBtn, 0, wx.ALL, 5)
        
        editRecordBtn = wx.Button(self, label="Edit")
        editRecordBtn.Bind(wx.EVT_BUTTON, parent.onEditRecord)
        btnSizer.Add(editRecordBtn, 0, wx.ALL, 5)
        
        deleteRecordBtn = wx.Button(self, label="Delete")
        deleteRecordBtn.Bind(wx.EVT_BUTTON, parent.onDelete)
        btnSizer.Add(deleteRecordBtn, 0, wx.ALL, 5)
        
        showAllBtn = wx.Button(self, label="Show All")
        showAllBtn.Bind(wx.EVT_BUTTON, parent.onShowAllRecord)
        btnSizer.Add(showAllBtn, 0, wx.ALL, 5)

        self.SetSizer(btnSizer)
         
        
########################################################################
class SearchPanel(wx.Panel):

  def __init__(self, parent):

        wx.Panel.__init__(self, parent)

        # create the search related widgets
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD) 
        searchSizer = wx.BoxSizer(wx.HORIZONTAL)
        cat = ["Author", "Title", "ISBN", "Publisher"]
        searchByLbl = wx.StaticText(self, label="Search By:")
        searchByLbl.SetFont(font)
        searchSizer.Add(searchByLbl, 0, wx.ALL, 5)
        
        self.categories = wx.ComboBox(self, value="Author", choices=cat)
        searchSizer.Add(self.categories, 0, wx.ALL, 5)
        
        self.search = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.search.Bind(wx.EVT_TEXT_ENTER, parent.onSearch)
        searchSizer.Add(self.search, 0, wx.ALL, 5)
       
        self.SetSizer(searchSizer) 
    
########################################################################
class ListViewPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        self.controller=Controller(SaleOrder,"sqlite:///odoo.db")
        controller=self.controller

        wx.Panel.__init__(self, parent)
        try:
            self.olvResults = controller.getAllRecords()
        except:
            self.olvResults = []
       
      
        #Panels 
        search_panel=SearchPanel(self)
        button_panel=ButtonPanel(self)
 
        #ListView
        self.olvResultsOlv = ObjectListView(self, style=wx.LC_REPORT
                                                        |wx.SUNKEN_BORDER)
        self.olvResultsOlv.SetEmptyListMsg("No Records Found")
        self.setRows()
        
        #Organize the shit   
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(search_panel)
        mainSizer.Add(self.olvResultsOlv, 1, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(button_panel, 0, wx.CENTER)
        self.SetSizer(mainSizer)
        
    #----------------------------------------------------------------------
    def onAddRecord(self, event):
        """
        Add a record to the database
        """
        dlg = addModRecord.AddModRecDialog()
        dlg.ShowModal()
        dlg.Destroy()
        self.showAllRecords()
        
    #----------------------------------------------------------------------
    def onEditRecord(self, event):
        """
        Edit a record
        """
        selectedRow = self.olvResultsOlv.GetSelectedObject()
        if selectedRow == None:
            commonDlgs.showMessageDlg("No row selected!", "Error")
            return
        dlg = addModRecord.AddModRecDialog(selectedRow, title="Modify",
                                           addRecord=False)
        dlg.ShowModal()
        dlg.Destroy()
        self.showAllRecords()
        
    #----------------------------------------------------------------------
    def onDelete(self, event):
        """
        Delete a record
        """
        selectedRow = self.olvResultsOlv.GetSelectedObject()
        if selectedRow == None:
            commonDlgs.showMessageDlg("No row selected!", "Error")
            return
        self.controller.deleteRecord(selectedRow.id)
        self.showAllRecords()
        
    #----------------------------------------------------------------------
    def onSearch(self, event):
        """
        Searches database based on the user's filter choice and keyword
        """
        filterChoice = self.categories.GetValue()
        keyword = self.search.GetValue()
        print "%s %s" % (filterChoice, keyword)
        self.olvResults = self.controller.searchRecords(filterChoice, keyword)
        self.setRows()
        
    #----------------------------------------------------------------------
    def onShowAllRecord(self, event):
        """
        Updates the record list to show all of them
        """
        self.showAllRecords()
        
    #----------------------------------------------------------------------
    def setRows(self):
        column_defs=[]
        #TODO: mudar para Table_Class.formato
        for column_def in self.olvResults[0].formato:
          column_defs.append(ColumnDefn(column_def["label"],
                                        column_def["align"],
                                        column_def["size"],
                                        column_def["field"]))
        self.olvResultsOlv.SetColumns(column_defs)
        self.olvResultsOlv.SetObjects(self.olvResults)
        
    #----------------------------------------------------------------------
    def showAllRecords(self):
        """
        Show all records in the object list view control
        """
        self.olvResults = self.controller.getAllRecords()
        self.setRows()
        
########################################################################
class GridFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Vendas Grings",
                          size=(800, 600))
        panel = ListViewPanel(self)
        
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = GridFrame()
    app.MainLoop()

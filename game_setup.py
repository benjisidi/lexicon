import wx

APP_EXIT = 1

class SetupScreen(wx.Frame):

	def __init__(self, *args, **kwargs):
		super(SetupScreen, self).__init__(*args, **kwargs)

		self.InitUI()

	def InitUI(self):
		panel = wx.Panel(self)
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		quit = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
		quit.SetBitmap(wx.Bitmap('exit.png'))
		fileMenu.AppendItem(quit)
		self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)
		menubar.Append(fileMenu, '&File')

		font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Quicksand_Book')
		titlefont = wx.Font(28, wx.DEFAULT, wx.NORMAL, wx.NORMAL, True, 'Quicksand_Bold')
		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		titleString = wx.StaticText(panel, label='Game Setup')
		titleString.SetFont(titlefont)
		hbox1.Add(titleString, proportion=1)
		vbox.Add(hbox1, flag=wx.CENTER)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		#hbox2.Add(st2, proportion=1)
		panel.SetSizer(vbox) 
		vbox.Fit(self)
		self.SetMenuBar(menubar)
		self.SetSize((800, 600))
		self.SetTitle('Lexicon; Game Setup')
		self.Centre()
		self.Show(True)

	def OnQuit(self, e):
		self.Close()

def main():
	win = wx.App()
	SetupScreen(None)
	win.MainLoop()

if __name__ == '__main__':
	main()
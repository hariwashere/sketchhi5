
import cStringIO

import urllib2
import urllib
import simplejson
import wx

class Panel1(wx.Panel):

    def __init__(self, parent, id):
        # create the panel
        wx.Panel.__init__(self, parent, id)
        self.btn = wx.Button(self, label="Search", pos=(400, 505))
        self.btn.Bind(wx.EVT_BUTTON, self.buttonClick)
        self.control = wx.TextCtrl(self, size=(350, 30), pos=(20, 500))


    def buttonClick(self, event):
 
        search_string = self.control.GetValue()
        url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+search_string+'&userip=INSERT-USER-IP')
        request = urllib2.Request(url, None, {'Referer': 'google.com'})
        response = urllib2.urlopen(request)

        results = simplejson.load(response)
        image_url = urllib2.urlopen(results['responseData']['results'][1]['unescapedUrl'])

        stream = cStringIO.StringIO(image_url.read())
        bmp = wx.BitmapFromImage(wx.ImageFromStream(stream))
        wx.StaticBitmap(self, -1, bmp, (5, 5), (450, 480))

wx.InitAllImageHandlers()
app = wx.PySimpleApp()
frame1 = wx.Frame(None, -1, "Sketch-hi-5", size = (480, 570))
Panel1(frame1,-1)
frame1.Show(1)
app.MainLoop()
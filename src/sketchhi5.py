
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
        #search_string = 'blah'
        search_string = self.control.GetValue()
        url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q='+search_string+'&userip=INSERT-USER-IP')
        # pick a .jpg file you have in the working folder
        request = urllib2.Request(url, None, {'Referer': 'google.com'})
        response = urllib2.urlopen(request)

        # Process the JSON string.
        results = simplejson.load(response)
        urllib.urlretrieve(results['responseData']['results'][1]['unescapedUrl'], "blah.png")
        imageFile = 'blah.png'
        data = open(imageFile, "rb").read()
        # convert to a data stream
        stream = cStringIO.StringIO(data)
        # convert to a bitmap
        bmp = wx.BitmapFromImage(wx.ImageFromStream(stream))
        # show the bitmap, (5, 5) are upper left corner coordinates
        wx.StaticBitmap(self, -1, bmp, (5, 5), (450, 480))
#url = ('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=blah&userip=INSERT-USER-IP')

app = wx.PySimpleApp()
# create a window/frame, no parent, -1 is default ID
# increase the size of the frame for larger images
frame1 = wx.Frame(None, -1, "Sketch-hi-5", size = (480, 570))

#btn = wx.Button(window, label = 'Hello')
# call the derived class
Panel1(frame1,-1)
frame1.Show(1)
app.MainLoop()
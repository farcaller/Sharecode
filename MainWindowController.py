#
#  MainWindowController.py
#  Sharecode
#
#  Created by Farcaller on 20.10.09.
#  Copyright (c) 2009 Hack&Dev Team. All rights reserved.
#

from Foundation import *
from objc import *
from AppKit import *

class MainWindowController(NSObject):
    snippetScrollView = IBOutlet()
    snippetTextView = IBOutlet()
    
    def awakeFromNib(self):
        bigSize = NSMakeSize(1e+308, 1e+308) # TODO: FLT_MAX        
        self.snippetScrollView.setHasHorizontalScroller_(YES)
        self.snippetTextView.setHorizontallyResizable_(YES)
        self.snippetTextView.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
        self.snippetTextView.textContainer().setContainerSize_(bigSize)
        self.snippetTextView.textContainer().setWidthTracksTextView_(NO)

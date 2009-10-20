#
#  main.py
#  Sharecode
#
#  Created by Farcaller on 19.10.09.
#  Copyright Hack&Dev Team 2009. All rights reserved.
#

#import modules required by application
import objc, Foundation, AppKit, CoreData, sys

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
sys.path.append(Foundation.NSBundle.mainBundle().resourcePath()+'/support')
import Sharecode_AppDelegate, AddSnippetController, Snippet, MainWindowController

# pass control to AppKit
AppHelper.runEventLoop()

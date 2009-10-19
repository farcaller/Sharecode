#
#  AddSnippetController.py
#  Sharecode
#
#  Created by Farcaller on 19.10.09.
#  Copyright (c) 2009 Hack&Dev Team. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet
from Foundation import *
from AppKit import *
from pygments.lexers import guess_lexer

class AddSnippetController(NSObject):
    window = IBOutlet()
    titleField = IBOutlet()
    langField = IBOutlet()
    snippetField = IBOutlet()
    delegate = IBOutlet()
    
    def showForWindow(self, win, txt=''):
        self.titleField.setStringValue_('')
        self.langField.setStringValue_('')
        self.snippetField.setStringValue_(txt)
        NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            self.window, win, self, 'didEndSheet:returnCode:contextInfo:', None)
    
    def saveSnippet(self, title, language, code):
        ctx = self.delegate.managedObjectContext()
        mo = NSEntityDescription.insertNewObjectForEntityForName_inManagedObjectContext_('Snippet', ctx)
        mo.setValue_forKey_(title, 'title')
        mo.setValue_forKey_(language, 'language')
        mo.setValue_forKey_(code, 'code')
        res = ctx.save_(None)
        print res
    
    @objc.selectorFor(NSApplication.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_)
    def didEndSheet_returnCode_contextInfo_(self, sheet, returnCode, contextInfo):
        sheet.orderOut_(self)
    
    @IBAction
    def AddAction_(self, sender):
        if self.langField.stringValue() == '':
            lex = guess_lexer(self.snippetField.stringValue())
            if lex:
                self.langField.setStringValue_(lex.aliases[0])
        else:
            NSApp.endSheet_(sender.window())
            self.saveSnippet(self.titleField.stringValue(), self.langField.stringValue(), self.snippetField.stringValue())
    
    @IBAction
    def CancelAction_(self, sender):
        NSApp.endSheet_(sender.window())

#
#  AddSnippetController.py
#  Sharecode
#
#  Created by Farcaller on 19.10.09.
#  Copyright (c) 2009 Hack&Dev Team. All rights reserved.
#

from objc import YES, NO, IBAction, IBOutlet, signature
from Foundation import *
from AppKit import *
from pygments.lexers import guess_lexer

class AddSnippetController(NSObject):
    window = IBOutlet()
    titleField = IBOutlet()
    langField = IBOutlet()
    snippetField = IBOutlet()
    tagsField = IBOutlet()
    delegate = IBOutlet()
    
    def showForWindow(self, win, txt=''):
        self.titleField.setStringValue_('')
        self.langField.setStringValue_('')
        self.tagsField.setStringValue_('')
        self.snippetField.setStringValue_(txt)
        NSApp.beginSheet_modalForWindow_modalDelegate_didEndSelector_contextInfo_(
            self.window, win, self, 'didEndSheet:returnCode:contextInfo:', None)
    
    @signature("v@:@@i^i")
    def tokenField_completionsForSubstring_indexOfToken_indexOfSelectedItem_(self, field, subs, idx, idxSel):
        ctx = self.delegate.managedObjectContext()
        frq = NSFetchRequest.alloc().init()
        frq.setEntity_(NSEntityDescription.entityForName_inManagedObjectContext_('Tag', ctx))
        frq.setPredicate_(NSPredicate.predicateWithFormat_('name beginswith %@', subs))
        res, err = ctx.executeFetchRequest_error_(frq, None)
        l = []
        for t in res:
            l.append(t.name())
        if err == None:
            return (l, 0)
        else:
            return ([], -1)
    
    @signature("v@:@@")
    def tokenField_representedObjectForEditingString_(self, field, s):
        ctx = self.delegate.managedObjectContext()
        frq = NSFetchRequest.alloc().init()
        frq.setEntity_(NSEntityDescription.entityForName_inManagedObjectContext_('Tag', ctx))
        frq.setPredicate_(NSPredicate.predicateWithFormat_('name == %@', s))
        res, err = ctx.executeFetchRequest_error_(frq, None)
        print "repo:",res,err
        if err == None:
            if len(res) > 1:
                print "ZOMG! Duptags?!", res
                return res[0]
            elif len(res) == 1:
                return res[0]
        return None
    
    @signature("v@:@@")
    def tokenField_displayStringForRepresentedObject_(self, field, obj):
        if obj.isKindOfClass_(NSManagedObject):
            return obj.name()
        else:
            return unicode(obj)
    
    def detokenize(self, mo):
        tok = self.tagsField.objectValue()
        for t in tok:
            if t.isKindOfClass_(NSManagedObject):
                mo.addTagsObject_(t)
                t.addSnippetsObject_(mo)
            else:
                ctx = self.delegate.managedObjectContext()
                tg = NSEntityDescription.insertNewObjectForEntityForName_inManagedObjectContext_('Tag', ctx)
                tg.setName_(t)
                mo.addTagsObject_(tg)
                tg.addSnippetsObject_(mo)
    
    def saveSnippet(self, title, language, code):
        ctx = self.delegate.managedObjectContext()
        mo = NSEntityDescription.insertNewObjectForEntityForName_inManagedObjectContext_('Snippet', ctx)
        mo.setTitle_(title)
        mo.setLanguage_(language)
        mo.setCode_(code)
        self.detokenize(mo)
        res = ctx.save_(None)
        print "ctx save:",res
    
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

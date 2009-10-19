#
#  Snippet.py
#  Sharecode
#
#  Created by Farcaller on 19.10.09.
#  Copyright (c) 2009 Hack&Dev Team. All rights reserved.
#

from Foundation import *
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import RtfFormatter

class Snippet(NSManagedObject):
    def prettyCode(self):
        print "want prettified for",self.language()
        lexer = get_lexer_by_name(self.language(), stripall=True)
        print "lexer:",lexer
        formatter = RtfFormatter()
        result = highlight(self.code(), lexer, formatter)
        b = NSString.stringWithString_(result).UTF8String()
        d = NSData.alloc().initWithBytes_length_(b, len(b))
        rtf = NSAttributedString.alloc().initWithRTF_documentAttributes_(d, None)
        return rtf[0]

#!/usr/bin/python
#
# lscs.py
#
# Lists Xcode 4 Code Snippets.
#
# Example:
# ./lscs.py
#
# Copyright 2012 Kirby Turner
#
# Version 1.0
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import sys
import getopt

def show(filename, dict):
    title = dict['IDECodeSnippetTitle']
    if 'IDECodeSnippetSummary' in dict:
        summary = dict['IDECodeSnippetSummary']
    else:
        summary = ''
    shortcut = dict['IDECodeSnippetCompletionPrefix']
    print 'File: ' + filename
    print 'Title: ' + title
    print 'Shortcut: ' + shortcut
    print summary
    print '====='

def showAsMarkdown(filename, dict):
    title = dict['IDECodeSnippetTitle']
    if 'IDECodeSnippetSummary' in dict:
        summary = dict['IDECodeSnippetSummary']
    else:
        summary = ''
    shortcut = dict['IDECodeSnippetCompletionPrefix']
    snippet = dict['IDECodeSnippetContents']
    scope = dict['IDECodeSnippetCompletionScopes']

    print '## ' + title
    print '**Shortcut**: ' + shortcut + '  '

    url = 'http://github.com/kirbyt/Xcode4CodeSnippets/blob/master/' + filename
    print '**File**: [' + filename + '](' + url +')  '

    scopeText = '**Scope**: '
    for s in scope:
        scopeText = scopeText + s + ' '
    scopeText = scopeText + ' '
    print scopeText

    print '**Summary**: ' + summary + '  '
    print ''
    for line in snippet.split('\n'):
        print '    ' + line + '  '
    print ''

def main():
    format = None
    opts, args = getopt.getopt(sys.argv[1:], 'f:', ['format='])
    for o, a in opts:
        if o in ('-f', '--format'):
            format = a

    codeSnippets = [];

    path = os.path.expanduser('~/Library/Developer/Xcode/UserData/CodeSnippets')
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('codesnippet'):
                from AppKit import NSDictionary
                snippetDict = NSDictionary.dictionaryWithContentsOfFile_(os.path.join(path, filename))
                # objDict = NSDictionary.dictionaryWithObjectsAndKeys_(filename,'filename',snippetDict,'snippet')
                codeSnippets.append({'filename':filename,'snippet':snippetDict});

    sortedCodeSnippets = sorted(codeSnippets, key=lambda k: k['snippet']['IDECodeSnippetTitle'].lower())
    for objDict in sortedCodeSnippets:
      filename = objDict['filename']
      dict = objDict['snippet']
      if format == 'markdown':
          showAsMarkdown(filename, dict)
      else:
          show(filename, dict)

if __name__ == '__main__':
  sys.exit(main())

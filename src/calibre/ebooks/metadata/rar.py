#!/usr/bin/env  python
__license__   = 'GPL v3'
__copyright__ = '2009, Kovid Goyal kovid@kovidgoyal.net'
__docformat__ = 'restructuredtext en'

'''
Read metadata from RAR archives
'''

import os
from cStringIO import StringIO
from calibre.ptempfile import PersistentTemporaryFile
from calibre.libunrar import extract_member, names

def get_metadata(stream):
    path = getattr(stream, 'name', False)
    if not path:
        pt = PersistentTemporaryFile('_rar-meta.rar')
        pt.write(stream.read())
        pt.close()
        path = pt.name
    path = os.path.abspath(path)
    file_names = list(names(path))
    for f in file_names:
        stream_type = os.path.splitext(f)[1].lower()
        if stream_type:
            stream_type = stream_type[1:]
            if stream_type in ('lit', 'opf', 'prc', 'mobi', 'fb2', 'epub',
                               'rb', 'imp', 'pdf', 'lrf'):
                data = extract_member(path, match=None, name=f)[1]
                stream = StringIO(data)
                from calibre.ebooks.metadata.meta import get_metadata
                return get_metadata(stream, stream_type)
    raise ValueError('No ebook found in RAR archive') 
        


#!/usr/bin/env python
"""FetchFile.py: Fetches a remote file if not already local"""

import urllib2
import shutil
import os.path

__author__ = "Chris Coughlin"
__copyright__ = "Copyright 2011, Chris Coughlin"
__credits__ = ['Chris Coughlin']
__license__ = "BSD"
__version__ = "06.01.2011"
__maintainer__ = "Chris Coughlin"
__email__ = "chriscoughlin@gmail.com"
__status__ = "Prototype"

class FetchFile(object):
    ''' Simple wrapper to urllib2 to retrieve a remote file.  Defaults to not overwriting destination file if found.
    '''
    def __init__(self, url, overwrite = False, dst=None):
        ''' Fetches the remote file url, writing to dst (defaults to the basename of the url file, e.g. index.html).
        If overwrite is False (default), if the local file exists it won't be overwritten.'''
        self.url = url
        self.overwrite = overwrite
        if dst is None:
            self.destination = os.path.basename(self.url)
        else:
            self.destination = dst

    def fetch(self, timeout=10):
        '''Retrieves the remote file, with a timeout of 10s by default.  Aborts retrieval if destination file
        already exists or self.overwrite is False. '''
        if not os.path.exists(self.destination) or self.overwrite:
            try:
                remote_file = urllib2.urlopen(self.url, timeout = timeout)
                with open(self.destination, "wb") as local_file:
                    shutil.copyfileobj(remote_file, local_file)
            except urllib2.URLError:
                '''Unable to retrieve the file'''
                raise
# -*- coding: utf-8 -*-

# This file is part of PyBOSSA.
#
# PyBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBOSSA.  If not, see <http://www.gnu.org/licenses/>.

import requests
from urllib import quote

try:
    import settings
except:
    print "There should be a settings.py file with the API-KEY for freesound"

def get_sounds(keyword):
    url = "http://www.freesound.org/api/sounds/search/"
    payload = {'q':keyword, 'api_key': settings.APIKEY,
               'f': 'type:ogg'
               }
    api_key =  {'api_key': settings.APIKEY}
    res = requests.get(url, params=payload)
    data = res.json()
    for s in data['sounds']:
        clip_url = '%s/%s.%s' % (settings.PUBLIC_DROPBOX_URL, s['id'], s['type'])
        #freesound_url = "%sdownload/%s__%s" % (s['url'], s['id'],  quote(s['original_filename']))
        freesound_url = s["serve"] + "?api_key=" + settings.APIKEY
        r = requests.get(s['serve'], params=api_key, stream=True)
        # Uncomment for writing the file
        #if r.status_code == 200:
        #    file_name = "%s/%s.%s" % (settings.DROPBOX_FOLDER, s['id'], s['type'])
        #    with open(file_name, 'wb') as f:
        #        for chunk in r.iter_content():
        #            f.write(chunk)
        s['dropbox_url'] = clip_url
        s['freesound_url'] = freesound_url
    return data['sounds']

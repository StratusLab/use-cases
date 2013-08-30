#
# Copyright (c) 2013, Centre National de la Recherche Scientifique (CNRS)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import requests
import unittest



map_view2 = {"views":
              {"by_runningvms":
               {"map":
                '''function (doc, meta) {
                     if (meta.id.indexOf("Accounting") == 0 && doc.state == "running")
                        {
                                emit(doc.uuid, null);
                        }
                   }'''
                },
               }
              }



map_view = {"views":
              {"by_id":
               {"map":
                '''function (doc, meta) {
                     if (meta.id.indexOf("Accounting") == 0)
                        {
                                emit(meta.id, null);
                        }
                   }'''
                },
               }
              }




class testConsolidationPublish(unittest.TestCase):

    def setUp(self):
        self.create_view('dev_byid', map_view)
        self.create_view('dev_byuuid',map_view2)

    def tearDown(self):
        pass

    def create_view(self, design_doc,mapview,host='localhost',bucket='default'):
        """
        Create view using REST API calls
        """
        view_url='http://%s:8092/%s/_design/%s' % (host,bucket,design_doc)
        print "view_url=", view_url
        data=json.dumps(mapview)
        headers = {'content-type': 'application/json'}
        r = requests.put(view_url, data=data, headers=headers)
        print r.text


    def delete_view(self, design_doc,host='localhost',bucket='default'):
        """
        Delete view using REST API calls
        """
        view_url='http://%s:8092/%s/_design/%s' % (self.host,self.bucket,self.design_doc)
        headers = {'content-type': 'application/json'}
        r = requests.delete(view_url, headers=headers)
        print r.text




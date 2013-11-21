#!/usr/bin/env python
"""
This work is made available under the Apache License, Version 2.0.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""
import unittest
import bufldiff

class BuflDiffUnitTest(unittest.TestCase):
  def setUp(self):
    pass

  def testNext(self):
    feature = bufldiff.Buflfeature("bufldiff.py")
    [feature.next() for i in range(0, 20)]    
    self.assertNotEqual(0, feature.next())
    feature.close()

  def testGetFeatures(self):
    diff = bufldiff.Buflfeature("bufldiff.py")
    diff.getFeatures(self.callback)
    diff.close()

  def callback(self, feature): 
    self.assertNotEqual(None, feature)    
  
  def testDiff(self):
    diff = bufldiff.Bufldiff()
    diff.diff("bufldiff.py", "bufldiff.py")    
    for value in diff.result:
      self.assertNotEqual(-1, value)

if __name__ == '__main__':
  unittest.main()
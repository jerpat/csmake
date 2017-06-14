# <copyright>
# (c) Copyright 2017 Hewlett Packard Enterprise Development LP
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# </copyright>
import unittest
from example import example
from subdir.another_test_example import subdir_test_example


class test_example(unittest.TestCase):
    def setUp(self):
        self.options = self.csmake_test.options
        self.log = self.csmake_test.log

    def test_example_pass(self):
        e = example()
        self.assertEqual(e.myfunc(), 5)

    def test_example_fail(self):
        e = example()
        self.assertEqual(e.myfunc(), 4)

    def test_example_useoption(self):
        e = subdir_test_example()
        self.assertEqual(str(e.myfunc()), self.options['option-answer'])


    def test_another_example(self):
        e = another_example()
        self.assertEqual(str(e.do()), 3)


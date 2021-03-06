#
# Copyright (C) 2016 Shang Yuanchun <idealities@gmail.com>
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# drummer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with drummer. If not, write to:
#   The Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor
#   Boston, MA  02110-1301, USA.
#
#


"""Common functions for Drummer :("""

import pkg_resources

def get_version():
    """
    Returns the version of drummer from the python egg metadata

    :returns: the version of drummer

    """
    try:
        return pkg_resources.require("drummer")[0].version
    except:
        return "dev"


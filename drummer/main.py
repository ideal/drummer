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
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.
#
#


"""Main starting point for Drummer.  Contains the main() entry point."""

import os, sys
import signal
from   optparse import OptionParser

import drummer.log

# Skip i18n currently
import __builtin__
__builtin__.__dict__["_"] = lambda x: x

def version_callback(option, opt_str, value, parser):
    print(os.path.basename(sys.argv[0]) + ": " + drummer.common.get_version())
    sys.exit(0)

def start_drummer():
    """Entry point for drummer script"""
    import drummer.common

    # Setup the argument parser
    parser = OptionParser(usage="%prog [options]")
    parser.add_option("-v", "--version", action="callback",
                      callback=version_callback,
                      help=_("Show program's version number and exit"))
    parser.add_option("-l", "--logfile", dest="logfile",
                      help=_("Set the logfile location"),
                      action="store", type="str")
    parser.add_option("-L", "--loglevel", dest="loglevel",
                      help=_("Set the log level: none, info, warning, error, "
                             "critical, debug"),
                      action="store", type="str")
    parser.add_option("-q", "--quiet", dest="quiet",
                      help=_("Sets the log level to 'none', this is the same as `-L none`"),
                      action="store_true", default=False)
    parser.add_option("-r", "--rotate-logs", dest="rotate_logs",
                      help=_("Rotate logfiles."),
                      action="store_true", default=False)

    # Get the options and args from the OptionParser
    (options, args) = parser.parse_args()

    if options.quiet:
        options.loglevel = "none"
    if not options.loglevel:
        options.loglevel = "info"

    logfile_mode = 'w'
    if options.rotate_logs:
        logfile_mode = 'a'

    if not options.logfile:
        options.logfile = '/dev/null'

    # Setup the logger
    try:
        # Try to make the logfile's directory if it doesn't exist
        os.makedirs(os.path.abspath(os.path.dirname(options.logfile)))
    except:
        pass

    # Setup the logger
    if os.path.isfile(options.logfile):
        logfile_mode = 'a'
    drummer.log.setupLogger(level=options.loglevel,
                           filename=options.logfile,
                           filemode=logfile_mode)

    drummer.log.addStreamHandler(level=options.loglevel)

    import logging
    log = logging.getLogger(__name__)

    try:
        log.info("Start drummer...")
        from drummer.benchmark import Benchmark
        benchmark = Benchmark(options, args)
        benchmark.start()
    except Exception as e:
        log.exception(e)
        sys.exit(1)
    log.info("Finished drummer")


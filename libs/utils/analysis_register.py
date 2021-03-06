# SPDX-License-Identifier: Apache-2.0
#
# Copyright (C) 2015, ARM Limited and contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

""" Helper module for registering Analysis classes methods """

import os
import sys

from glob import glob
from inspect import isclass
from importlib import import_module

from analysis_module import AnalysisModule

# Configure logging
import logging


class AnalysisRegister(object):
    """
    Define list of supported Analysis Classes.

    :param trace: input Trace object
    :type trace: :mod:`libs.utils.Trace`
    """

    def __init__(self, trace):

        # Add workloads dir to system path
        analysis_dir = os.path.dirname(os.path.abspath(__file__))
        analysis_dir = os.path.join(analysis_dir, 'analysis')
        logging.debug('%14s - Analysis: %s', 'Analysis', analysis_dir)

        sys.path.insert(0, analysis_dir)
        logging.debug('%14s - Syspath: %s', 'Analysis', format(sys.path))

        logging.info("Registering trace analysis modules:")
        for filepath in glob(os.path.join(analysis_dir, '*.py')):
            filename = os.path.splitext(os.path.basename(filepath))[0]

            # Ignore __init__ files
            if filename.startswith('__'):
                continue

            logging.debug('%14s - Filename: %s', 'Analysis', filename)

            # Import the module for inspection
            module = import_module(filename)
            for member in dir(module):
                # Ignore the base class
                if member == 'AnalysisModule':
                    continue
                handler = getattr(module, member)
                if handler and isclass(handler) and \
                   issubclass(handler, AnalysisModule):
                    module_name = module.__name__.replace('_analysis', '')
                    setattr(self, module_name, handler(trace))
                    logging.info("   %s", module_name)

# vim :set tabstop=4 shiftwidth=4 expandtab

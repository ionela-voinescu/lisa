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

class Screen(object):
    """
    Set of utility functions to control an Android Screen
    """

    @staticmethod
    def set_orientation(target, auto=True, portrait=None):
        """
        Set screen orientation mode
        """
        acc_mode = 1 if auto else 0
        # Force manual orientation of portrait specified
        if portrait is not None:
            acc_mode = 0
            target.logger.info("Force manual orientation")
        if acc_mode == 0:
            usr_mode = 0 if portrait else 1
            usr_mode_str = 'PORTRAIT' if portrait else 'LANDSCAPE'
            target.logger.info('Set orientation: %s', usr_mode_str)
        else:
            usr_mode = 0
            target.logger.info('Set orientation: AUTO')

        if acc_mode == 0:
            target.execute('content insert '\
                           '--uri content://settings/system '\
                           '--bind name:s:accelerometer_rotation '\
                           '--bind value:i:{}'.format(acc_mode))
            target.execute('content insert '\
                           '--uri content://settings/system '\
                           '--bind name:s:user_rotation '\
                           '--bind value:i:{}'.format(usr_mode))
        else:
            # Force PORTRAIT mode when activation AUTO rotation
            target.execute('content insert '\
                           '--uri content://settings/system '\
                           '--bind name:s:user_rotation '\
                           '--bind value:i:{}'.format(usr_mode))
            target.execute('content insert '\
                           '--uri content://settings/system '\
                           '--bind name:s:accelerometer_rotation '\
                           '--bind value:i:{}'.format(acc_mode))

    @staticmethod
    def set_brightness(target, auto=True, percent=None):
        """
        Set screen brightness percentage
        """
        bri_mode = 1 if auto else 0
        # Force manual brightness if a percent specified
        if percent:
            bri_mode = 0
        target.execute('content insert '\
                       '--uri content://settings/system '\
                       '--bind name:s:screen_brightness_mode '\
                       '--bind value:i:{}'.format(bri_mode))
        if bri_mode == 0:
            if percent<0 or percent>100:
                msg = "Screen brightness {} out of range (0,100)"\
                      .format(percent)
                raise ValueError(msg)
            value = 255 * percent / 100
            target.execute('content insert '\
                           '--uri content://settings/system '\
                           '--bind name:s:screen_brightness '\
                           '--bind value:i:{}'.format(value))
            target.logger.info('Set brightness: %d%%', percent)
        else:
            target.logger.info('Set brightness: AUTO')

    @staticmethod
    def set_dim(target, auto=True):
        """
        Set screen dimming mode
        """
        dim_mode = 1 if auto else 0
        dim_mode_str = 'ON' if auto else 'OFF'
        target.execute('content insert '\
                       '--uri content://settings/system '\
                       '--bind name:s:dim_screen '\
                       '--bind value:i:{}'.format(dim_mode))
        target.logger.info('Dim screen mode: %s', dim_mode_str)

    @staticmethod
    def set_timeout(target, seconds=30):
        """
        Set screen off timeout in seconds
        """
        if seconds<0:
            msg = "Screen timeout {}: cannot be negative".format(seconds)
            raise ValueError(msg)
        value = seconds * 1000
        target.execute('content insert '\
                       '--uri content://settings/system '\
                       '--bind name:s:screen_off_timeout '\
                       '--bind value:i:{}'.format(value))
        target.logger.info('Screen timeout: %d [s]', seconds)

    @staticmethod
    def set_defaults(target):
        """
        Reset screen settings to a reasonable default
        """
        Screen.set_orientation(target)
        Screen.set_brightness(target)
        Screen.set_dim(target)
        Screen.set_timeout(target)

# vim :set tabstop=4 shiftwidth=4 expandtab

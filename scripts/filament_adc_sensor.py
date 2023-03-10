# Filament Adc Sensor Module
#
# Copyright (C) 2021 Ette
#
# This file may be distributed under the terms of the GNU GPLv3 license.
import logging
from . import filament_switch_sensor

SAMPLE_TIME = 0.001
SAMPLE_COUNT = 8
REPORT_TIME = 0.100

class AdcFilamentSensor:
    def __init__(self, config):
        # Read config
        printer = config.get_printer()
        # Get printer objects
        self.reactor = printer.get_reactor()
        self.runout_helper = filament_switch_sensor.RunoutHelper(config)
        self.get_status = self.runout_helper.get_status
        ppins = config.get_printer().lookup_object('pins')
        self.mcu_adc = ppins.setup_pin('adc', config.get('adc_pin'))
        self.mcu_adc.setup_minmax(SAMPLE_TIME, SAMPLE_COUNT)
        self.mcu_adc.setup_adc_callback(REPORT_TIME, self.adc_callback)
        self.adc_threshold = config.getfloat(
                'adc_threshold', 0.5, above=0.)
        query_adc = config.get_printer().load_object(config, 'query_adc')
        query_adc.register_adc(config.get_name(), self.mcu_adc)
    def adc_callback(self, read_time, read_value):
        sensor_state = self.get_sensor_state(read_value)
        self.runout_helper.note_filament_present(sensor_state)
    def get_sensor_state(self, read_value):
        return self.adc_threshold > read_value

def load_config_prefix(config):
    return AdcFilamentSensor(config)

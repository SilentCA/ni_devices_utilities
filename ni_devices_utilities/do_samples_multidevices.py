import nidaqmx
# include setting options
import nidaqmx.constants
# write data to nidaqmx task (task_out_stream)
import nidaqmx.stream_writers

import numpy as np
import time


##--------- Create and configure NI task -----------------
# Create a NI Task
task = nidaqmx.Task()
# Add digital output port to task virtual channel
task.do_channels.add_do_chan("/cDAQ9189-1EFE359Mod3/port0")
task.do_channels.add_do_chan("/cDAQ9189-1EFE359Mod4/port0")
# Set sample timing type
# `ON_DEMAND` generate a sample on each write operation.
# task.timing.samp_timing_type = nidaqmx.constants.SampleTimingType.ON_DEMAND
task.timing.samp_timing_type = nidaqmx.constants.SampleTimingType.SAMPLE_CLOCK
# Set sample rate
task.timing.samp_clk_rate = 1e3
# Set sample mode
task.timing.samp_quant_samp_mode = nidaqmx.constants.AcquisitionType.CONTINUOUS
# Set number of samples to generate or buffer size
task.timing.samp_quant_samp_per_chan = 1000

##--------  Write data to task ---------------------------
# Create a multichannel writer
writer = nidaqmx.stream_writers.DigitalMultiChannelWriter(task.out_stream)
# Auto start
writer.auto_start = True
# Data to be writen
# Each row corresponds to a channel in the task.
# The order of the channels in the array correspond to the order
# the channels added to the task.
data = np.array([[0xFF,0x00,0xFF],[0x00,0xFF,0x00]], np.uint8)
writer.write_many_sample_port_byte(data)

# Wait write to end
# task.wait_until_done(timeout=30)
# continuous generate data for 10 second
time.sleep(10)

##------------ Close task ------------------------------
# Clears the task, aborting the task and releasing any resources the task 
# reserved.
task.stop()
task.close()

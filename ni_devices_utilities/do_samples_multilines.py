import nidaqmx
# include setting options
import nidaqmx.constants
# write data to nidaqmx task (task_out_stream)
import nidaqmx.stream_writers

import numpy as np


##--------- Create and configure NI task -----------------
# Create a NI Task
task = nidaqmx.Task()
# Add digital output port to task virtual channel
task.do_channels.add_do_chan("/cDAQ1DIOM/port0")
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
# Create a stream writer
writer = nidaqmx.stream_writers.DigitalSingleChannelWriter(task.out_stream)
# Auto start
writer.auto_start = True
# Data to be writen
data = np.array([0xFF,0x1F,0x23]*100, np.uint8)
writer.write_many_sample_port_byte(data)
# Wait write to end
task.wait_until_done(timeout=30)

##------------ Close task ------------------------------
# Clears the task, aborting the task and releasing any resources the task 
# reserved.
task.close()

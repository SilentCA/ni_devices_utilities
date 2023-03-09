"""Main module."""
import nidaqmx
# include setting options
import nidaqmx.constants
# read data from nidaqmx task (task_in_stream)
import nidaqmx.stream_readers

import numpy as np
import matplotlib.pyplot as plt


##--------- Create and configure NI task -----------------
# Create a NI Task
task = nidaqmx.Task()
# Add analog input channel to task
task.ai_channels.add_ai_voltage_chan("cDAQ1AIM/ai0")
# Sample rate must be set before accessing to other configurations.
# Set sample rate.
task.timing.samp_clk_rate = 3e4
# Other way to set sample rate, etc.
task.timing.cfg_samp_clk_timing(
        rate=3e4, sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
        samps_per_chan=30000)

# Read 100 samples from channels
# read must after setting sample rate.
# task.read(100)

# Set start trigger: tigger source and tigger edge
task.triggers.start_trigger.cfg_dig_edge_start_trig('/cDAQ1DIOM/PFI0',
        trigger_edge=nidaqmx.constants.Edge.RISING)

##--------- Read data from task -------------------------
# Create a stream_readers for reading data from NI task
reader = nidaqmx.stream_readers.AnalogSingleChannelReader(task.in_stream)
# Preallocate a NumPy arrary of floating-point values to hold the samples
data = np.empty(30000, dtype=np.float64)
# Read data using stream_readers
# If `number_of_samples_per_channel` set to `-1`, the number of samples is
# determined by `task.timing.samp_quant_samp_per_chan` value and 
# `task.in_stream.read_all_avail_samp` setting.
# If the time of `timeout` in second elapse, the method returns an error and
# any samples read before timeout.
reader.read_many_sample(data, number_of_samples_per_channel=-1, timeout=10.0)
# Set reader to read specified number of samples and wait until requested
# samples have been generated.
# reader.read_many_sample(data, number_of_samples_per_channel=300000,
#    timeout=nidaqmx.constants.WAIT_INFINITELY)

##------------ Close task ------------------------------
# Clears the task, aborting the task and releasing any resources the task 
# reserved.
task.close()

# Plot data
x = np.linspace(0,1,30000)
fig, ax = plt.subplots()
ax.plot(x, data)
plt.show()

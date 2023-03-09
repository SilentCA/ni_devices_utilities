import nidaqmx
import nidaqmx.constants


##--------- Create and configure NI task -----------------
# Create a NI Task
task = nidaqmx.Task()
# Add digital output channel to task
task.do_channels.add_do_chan("/cDAQ1DIOM/port0/line0")
# Set sample timing type
# `ON_DEMAND` generate a sample on each write operation.
task.timing.samp_timing_type = nidaqmx.constants.SampleTimingType.ON_DEMAND

##--------  Write data to task ---------------------------
# Write a sample
task.write(True)
# Write a list of samples
task.write([True, False], auto_start=True)

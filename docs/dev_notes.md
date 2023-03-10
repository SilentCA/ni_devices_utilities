# 移植流程
- [ ] 分析原有代码，找出需要修改的部分，列出需要实现的接口
- [ ] 测试仪器控制功能，实现对应接口并进行测试
- [ ] 将新的仪器控制代码添加到原有的程序中

# TODO
- [ ] 在硬件上测试模拟输入的开始触发。

# 采集卡功能
- 设置采样时间、采样率和采样通道等参数
  `daqinstance,listener,databuf = daq.setparameters(self.meas_time, rate=self.rate, startchan=self.in_chan)`
- 开始一次采样，返回采样结果数组
  `data = daq.startonce(daqinstance,listener,databuf)`

# 仪器信息
- TTL：NI9401
- 采集卡：NI9239
- 底座：NI cDAQ-9185

# 注意事项
- NI9239的采样率不是在范围内的所有值都可以选取，应该是时钟的某些倍数。
- 从NI9239读取一定数量的数据完成前中途停止读取，可能会导致之后的读取操作会读取到
  上一次的数据。可能是因为上次的数据仍然在缓存中。
- NI-DAQmx仿真设备的触发立即开始。

# NI-DAQmx使用
- [文档](https://nidaqmx-python.readthedocs.io)
- 安装：`python -m pip install nidaqmx`

- 通过`nidaqmx.system.device`进行物理设备参数查看。
- 通过`nidaqmx.task`进行测量，虚拟通道参数查看和设置。
- 通过`nidaqmx.task.timing`进行定时相关的设置，如采样时钟、采样率、采样模式和采样时间。
- 通过`nidaqmx.task.channel`进行通道的测量类型、方式、单位、信号大小范围和通道类型。
- 通过`nidaqmx.task.triggers`进行触发参数设置。
- 使用`nidaqmx.stream_readers`读取`task`中通道的数据。

# nidaqmx.task
- `close()`: clears the task.
- `is_task_done()`: Queries the status of the task and indicates if it completed execution.
- `start()`: Transitions the task to the running state to begin the measurement or generation.
- `stop()`: Stops the task and returns it to the state the task was in before the DAQmx Start Task method ran or the DAQmx Write method ran with the autostart input set to TRUE.
- `ai_channels.add_ai_voltage_chan()`: Creates channel(s) to measure voltage.
- `do_channels.add_do_chan()`: Creates channel(s) to generate digital signals.

## nidaqmx.task.timing
- `cfg_samp_clk_timing()`：设置采样率、采样模式和采样数等。
- `samp_clk_rate`: Specifies the sampling rate in samples per channel per second. 
- `samp_quant_samp_mode`: Specifies if a task acquires or generates a finite number of samples or if it continuously acquires or generates samples.
- `samp_quant_samp_per_chan`: Specifies the number of samples to acquire or generate for each channel if samp_quant_samp_mode is AcquisitionType.FINITE. 
- `samp_timing_type`: Specifies the type of sample timing to use for the task.
  也可以用来设置数字输出时的输出模式，如`nidaqmx.constants.SampleTimingType.ON_DEMAND`
  用来在每次写入数据的时候产生一个输出样本。

## nidaqmx.task.ai_channel
- `ai_meas_type`: Indicates the measurement to take with the analog input channel.
- `ai_voltage_units`: Specifies the units to use to return voltage measurements from the channel.
- `ai_term_cfg`: Specifies the terminal configuration for the channel.
- `ai_max`: Specifies the maximum value you expect to measure.
- `ai_min`: Specifies the minimum value you expect to measure.

# nidaqmx.stream_readers
用来从NI-DAQmx task中读取数据
- class `AnalogSingleChannelReader`: Reads samples from an analog input channel in an NI-DAQmx task.
  - `read_many_sample()`: Reads one or more floating-point samples from a single analog input channel in a task.
  - `read_one_sample()`: Reads a single floating-point sample from a single analog input channel in a task.
  
# nidaqmx.task.start_trigger
Represents the start trigger configurations for a DAQmx task.
可以通过`task.triggers.start_trigger`访问一个task示例中的start trigger。
- `trig_type`: Specifies the type of trigger to use to start a task. eg. 
  nidaqmx.constants.TriggerType.DIGITAL_EDGE数字脉冲边缘触发。
- `dig_edge_edge`: Specifies on which edge of a digital pulse to start acquiring or generating samples.
- `dig_edge_src`: Specifies the name of a terminal where there is a digital signal to use as the source of the Start Trigger.
- `cfg_dig_edge_start_trig()`: Configures the task to start acquiring or generating samples on a rising or falling edge of a digital signal.

# 查看系统上可用的设备和设备的可用通道
通道名称示例
- 模拟输入端口名称：`cDAQ1AIM/ai0`
- 数字输出端口：`cDAQ1DIOM/port0`
- 数字输出线：`cDAQ1DIOM/port0/line0`

```python
# 访问本地DAQmx系统
system = nidaqmx.system.System.local()
# 可用设备列表
devices = system.devices
# 可用模拟输入通道
phys_chans = system.devices['Dev1'].ai_physical_chans
# 可用数字输出端口
phys_ports = system.devices['Dev2'].do_ports
# 可用数字输出线
phys_lines = system.devices['Dev2'].do_lines
```
# BusServoControl

## Project description 项目描述

BusServoControl is a Python library for precise control of bus-based servo motors using serial communication protocols.
BusServoControl 是一个通过串行通信协议精确控制总线舵机的 Python 库。

**Website:** https://github.com/LeurDeLis/BusServoControl

**Documentation:** https://github.com/LeurDeLis/BusServoControl/README.md

**Source code:** https://github.com/LeurDeLis/BusServoControl/BusServoControl

**Bug reports:** https://github.com/LeurDeLis/BusServoControl/issues

------

## Key Features 核心特性

- **Protocol Implementation**
  完整实现 `0x55 0x55` 帧头协议，支持 ID 范围 `0x00-0xFE`（最多 254 个舵机）
- **Precise Motion Control**
  支持角度范围 `0-1000`（对应 0-240°），运动时间 `0-30000ms`
- **Real-Time Monitoring**
  实时读取温度、电压、当前位置等状态信息
- **Safety Protection**
  支持角度限制、电压限制、温度保护
- **Offset Adjustment**
  支持临时偏差调整（断电不保存）和永久保存
- **Broadcast Support**
  支持广播指令（ID=254），避免总线冲突

## Example Usage 示例代码

```python
# 初始化串口和舵机控制器
my_serial = MySerial(port="COM6", baud_rate=115200)
my_servo = BusServoControl(my_serial)

# 控制舵机运动
my_servo.move_time_write(1, 1000, 2000)  # 1号舵机2000ms内移动到1000位置

# 读取当前角度
position = my_servo.read_current_position(1)

# 设置角度限制（安全保护）
my_servo.set_angle_limit(1, min_angle=100, max_angle=500)

# 调整并保存角度偏差
my_servo.angle_offset_adjust(1, offset=10)
my_servo.angle_offset_save(1)
```

## Protocol Specification 协议说明

|  协议头   |      舵机 ID       | 数据长度 | 指令值 | 校验值 |
| :-------: | :----------------: | :------: | :----: | :----: |
| 0x55 0x55 | 1 byte (0x00-0xFD) |  1 byte  |  可变  | 1 byte |

- **校验值计算:** `Checksum = ~(ID + Length + Cmd + Param1 + ... + ParamN)`
- **广播 ID:** `0xFE`（所有舵机接收指令，但不返回应答）
- **数据长度:** 等于参数总长度 + 3（帧头到校验和的总长度）

------

## Supported Functions 支持功能

1. **Motion Control**

   - `move_time_write()` : 即时运动控制
   - `move_time_wait_write()` : 预设运动参数
   - `move_start()` : 启动预设动作
   - `move_stop()` : 停止当前动作

   

2. **Parameter Configuration**

   - `set_servo_id()` : 修改舵机 ID
   - `set_angle_limit()` : 设置角度范围
   - `set_voltage_limit()` : 设置电压限制
   - `set_max_temperature()` : 设置最高温度

   

3. **Status Monitoring**

   - `read_current_position()` : 读取当前位置
   - `read_current_voltage()` : 读取输入电压
   - `read_current_temperature()` : 读取内部温度

------

## Installation 安装

```bash
pip install BusServoControl
```

------

## Protocol Specification 协议说明

| 协议头    | 舵机 ID            | 数据长度 | 指令值 | 校验值 |
| --------- | ------------------ | -------- | ------ | ------ |
| 0x55 0x55 | 1 byte (0x00-0xFD) | 1 byte   | 可变   | 1 byte |

- **校验值计算:** `Checksum = ~(ID + Length + Cmd + Param1 + ... + ParamN)`
- **广播 ID:** `0xFE`（所有舵机接收指令，但不返回应答）
- **数据长度:** 等于参数总长度 + 3（帧头到校验和的总长度）

## Code of Conduct 行为准则

我们承诺为所有贡献者和用户维护一个友好且包容的社区。请阅读我们的完整行为准则：
https://github.com/LeurDeLis/BusServoControl/blob/CODE_OF_CONDUCT.md

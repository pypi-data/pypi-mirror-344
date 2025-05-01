# -*- coding: UTF-8 -*-
"""
@Project : servo_control
@File    : BusServoControl.py
@IDE     : PyCharm 
@Author  : MFK
@Date    : 2025/4/29 下午3:33 
"""

"""
                            舵机控制协议格式
|——————————————————————————————————————————————————————————————————————|
|  Header   | Servo ID | Data Len   |  Cmd    |     Param    |   CRC   |
| 0x55 0x55 |  1 byte  |  1 byte    | 1 byte  | Prm1 … PrmN  |  1 byte |
|——————————————————————————————————————————————————————————————————————|
********************************协议讲解*********************************
帧头:     连续收到两个0x55,表示有数据包到达。
ID:      每个舵机都有一个ID号。ID号范围0~253, 转换为十六进制0x00~0xFD。
广播ID:   ID号254(0xFE)为广播ID,若控制器发出的ID号为254(0xFE)，所有的舵机均接收指令，但都不返回应答信息，(读取舵机ID号除外，具体说明参见下面指令介绍)以防总线冲突。
数据长度:  等于待发送的数据(包含本身一个字节)长度，即数据长度Length加3等于这一包指令的长度，从帧头到校验和。
指令:     控制舵机的各种指令，如位置、速度控制等。
参数:     除指令外需要补充的控制信息。
校验和:   校验和Checksum，计算方法如下: Checksum = ~ (ID + Length + Cmd+ Prm1 + ... PrmN)若括号内的计算和超出255,则取最低的一个字节，“~”表示取反。
"""

# 舵机指令集
SERVO_MOVE_TIME1WRITE = "01"  # 舵机移动指令值
SERVO_MOVE_TIME_READ = "02"  # 舵机角度读取指令值
SERVO_MOVE_TIME_WAIT_WRITE = "07"  # 设置目标角度和时间（不立即执行），需配合 SERVO_MOVE_START 使用
SERVO_MOVE_TIME_WAIT_READ = "08"  # 读取预设的目标角度和运动时间
SERVO_MOVE_START = "0B"  # 启动等待中的动作（配合 WRITE WAIT 使用）
SERVO_MOVE_STOP = "0C"  # 停止当前运动
SERVO_ID_WRITE = "0D"  # 写入舵机 ID（支持掉电保存）
SERVO_ID_READ = "0E"  # 读取当前舵机 ID
SERVO_ANGLE_OFFSET_ADJUST = "11"  # 调整角度偏差（立即生效，但不掉电保存）
SERVO_ANGLE_OFFSET_WRITE = "12"  # 保存当前角度偏差设置（支持掉电保存）
SERVO_ANGLE_OFFSET_READ = "13"  # 读取当前角度偏差值
SERVO_ANGLE_LIMIT_WRITE = "14"  # 设置舵机最小和最大转动角度限制（支持掉电保存）
SERVO_ANGLE_LIMIT_READ = "15"  # 读取当前角度限制设置
SERVO_VIN_LIMIT_WRITE = "16"  # 设置输入电压限制（超出范围时报警并卸载电机）
SERVO_VIN_LIMIT_READ = "17"  # 读取电压限制设置
SERVO_TEMP_MAX_LIMIT_WRITE = "18"  # 设置舵机内部最高允许温度（超温报警并卸载电机）
SERVO_TEMP_MAX_LIMIT_READ = "19"  # 读取舵机内部最高温度限制的值
SERVO_TEMP_READ = "1A"  # 读取当前舵机内部温度值
SERVO_VIN_READ = "1B"  # 读取当前输入电压值
SERVO_POS_READ = "1C"  # 读取当前实际角度位置值
SERVO_OR_MOTOR_MODE_WRITE = "1D"  # 设置舵机模式（位置控制/电机控制）及转动参数
SERVO_OR_MOTOR_MODE_READ = "1E"  # 读取当前舵机工作模式及相关参数
SERVO_LOAD_OR_UNLOAD_WRITE = "1F"  # 控制电机是否加载（0:卸载断电；1:加载输出力矩）
SERVO_LOAD_OR_UNLOAD_READ = "20"  # 读取当前电机加载状态
SERVO_LED_CTRL_WRITE = "21"  # 设置 LED 状态（0:常亮；1:常灭；支持掉电保存）
SERVO_LED_CTRL_READ = "22"  # 读取当前 LED 状态
SERVO_LED_ERROR_WRITE = "23"  # 设置哪些故障会触发 LED 报警闪烁（参见错误表）
SERVO_LED_ERROR_READ = "24"  # 读取当前故障报警设置
SERVO_DIS_READ = "30"  # 读取当前故障报警设置


def calculate_checksum(data_str):
    """
    校验和计算方法: 
    Checksum = ~(ID + Length + Cmd + Param1 + ... + ParamN) & 0xFF
    - 所有字节相加
    - 最终结果按位取反（取反后保留 8 位）
    """
    byte_list = bytes.fromhex(data_str)
    # print(byte_list)
    total = sum(byte_list)
    checksum = (~total) & 0xFF  # 按位取反并保留低8位
    return f"{checksum:02X}"


def split_hex(value):
    """
    将 16 进制数值的高八位和低八位分离。
    :param value: (str 或 int)输入值，可以是十六进制字符串或整数
    :return: string 调整后的数据低八位在前高八位在后
    """
    if isinstance(value, str):
        # 如果是字符串，尝试转换为整数
        value = int(value, 16)
    elif not isinstance(value, int):
        raise ValueError("输入值必须是字符串或整数。")
    low_byte = value & 0xFF  # 取低八位
    high_byte = (value >> 8) & 0xFF  # 取高八位
    return f"{low_byte:02X}{high_byte:02X}"


class BusServoControl:
    def __init__(self, _serial):
        """
        总线舵机控制类
        :param _serial: 控制舵机的实例化串口
        """
        self.__serial__ = _serial
        # 协议头 0x55 0x55
        self.__header = "5555"
        # 广播舵机ID：254  0xFE
        self.__broadcast_id = "FE"

    # ———————————————————————————————————————————————————————————————————————————————
    # 📖 数据协议相关
    # ———————————————————————————————————————————————————————————————————————————————

    def __build_55_packet(self, servo_id: str, cmd: str, param: str):
        """
        构建完整的指令包: 
        [0x55, 0x55, ID, Length, Cmd, Param1, ..., ParamN, Checksum]
        """
        data = bytes.fromhex(param)
        # print("+++++++++++++", data)
        length = f"{(len(data) + 3):02x}"
        # print("-------------", length)
        # print(type(servo_id), servo_id)
        checksum = calculate_checksum(servo_id + length + cmd + param)
        # print(checksum)
        # return self.__header + servo_id + length + cmd + param + checksum
        self.__serial__.sendmsg(self.__header + servo_id + length + cmd + param + checksum)

    def __convert_30_to_55_packet(self, addr, cmd, data):
        """
        30协议转换为55协议
        """
        pass

    # ———————————————————————————————————————————————————————————————————————————————
    # 🛠️ 舵机运动相关指令
    # ———————————————————————————————————————————————————————————————————————————————

    def move_time_write(self, servo_id, angle, time):
        """
        设置目标角度和时间并立即执行
        :param servo_id: 舵机ID (类型: int 或 str) (类型: int 或 str)
        :param angle: 角度 0~1000 (对应 0~240°)
        :param time: 时间 0~30000ms
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        param = split_hex(angle) + split_hex(time)
        self.__build_55_packet(servo_id, SERVO_MOVE_TIME1WRITE, param)

    def move_time_mutil_write(self, angle_time_list):
        """
        批量设置目标角度和时间并立即执行
        :param angle_time_list:
        :return:
        """
        pass

    def move_time_read(self, servo_id):
        """
        读取当前设置的目标角度和时间
        舵机会返回上条控制指令设置的目标角度和时间
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_MOVE_TIME_READ, "")

    def move_time_wait_write(self, servo_id, angle, time):
        """
        预设目标角度和时间，配合 move_start 使用
        :param servo_id: 舵机ID (类型: int 或 str)
        :param angle: 角度 0~1000 (对应 0~240°)
        :param time: 时间 0~30000ms
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        param = split_hex(angle) + split_hex(time)
        self.__build_55_packet(servo_id, SERVO_MOVE_TIME_WAIT_WRITE, param)

    def move_time_wait_read(self, servo_id):
        """
        读取预设的角度和时间
        # **************** 经测试, 该条指令暂无应答信息返回 ******************
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_MOVE_TIME_WAIT_READ, "")

    def move_start(self, servo_id):
        """
        启动等待中的动作
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        # 55 55 id 03 0B crc
        self.__build_55_packet(servo_id, SERVO_MOVE_START, "")

    def move_stop(self, servo_id):
        """
        停止当前动作
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        # 55 55 id 03 0C crc
        self.__build_55_packet(servo_id, SERVO_MOVE_STOP, "")

    # ———————————————————————————————————————————————————————————————————————————————
    # 🆔 舵机ID设置
    # ———————————————————————————————————————————————————————————————————————————————

    def set_servo_id(self, servo_id, new_id):
        """
        修改舵机ID，支持掉电保存
        :param servo_id: 目标舵机ID (类型: int 或 str)
        :param new_id: 新舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        if isinstance(new_id, int):
            # 如果是整数，尝试转换为整数字符串
            new_id = hex(new_id)[2:].zfill(2)
        # 55 55 servo_id 04 0D new_id crc
        self.__build_55_packet(servo_id, SERVO_ID_WRITE, new_id)

    def read_servo_id(self):
        """
        读取当前连接舵机ID
        使用广播ID进行查询
        """
        # 55 55 id 03 0C crc
        self.__build_55_packet(self.__broadcast_id, SERVO_ID_READ, "")

    # ———————————————————————————————————————————————————————————————————————————————
    # 📏 角度偏移量设置
    # ———————————————————————————————————————————————————————————————————————————————

    def angle_offset_adjust(self, servo_id, offset: int):
        """
        临时调整角度偏差（不掉电保存）
        :param servo_id: 舵机ID (类型: int 或 str)
        :param offset: (int) -125 ~ 125，代表 -30° ~ 30°
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        # 55 55 servo_id 04 11 offset crc
        offset = max(-125, min(125, offset))
        offset = (hex(offset & 0xFF)[2:] if offset < 0 else hex(offset)[2:]).zfill(2)
        self.__build_55_packet(servo_id, SERVO_ANGLE_OFFSET_ADJUST, offset)

    def angle_offset_save(self, servo_id):
        """
        保存当前角度偏移量设置（掉电保存）
        该函数与`angle_offset_adjust()`配合使用
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_ANGLE_OFFSET_WRITE, "")

    def read_angle_offset(self, servo_id):
        """
        读取当前角度偏移量
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_ANGLE_OFFSET_READ, "")

    # ———————————————————————————————————————————————————————————————————————————————
    # 🔒 角度限制设置
    # ———————————————————————————————————————————————————————————————————————————————

    def set_angle_limit(self, servo_id, min_angle: int, max_angle: int):
        """
        设置舵机转动角度范围（支持掉电保存）
        :param servo_id: 舵机ID (类型: int 或 str)
        :param min_angle: 最小角度(范围: 0~1000)
        :param max_angle: 最大角度(范围: 0~1000)
        """
        if min_angle >= max_angle:
            print("最小角度不能大于等于最大角度")
            return
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        param = split_hex(min_angle) + split_hex(max_angle)
        self.__build_55_packet(servo_id, SERVO_ANGLE_LIMIT_WRITE, param)

    def read_angle_limit(self, servo_id):
        """读取当前角度限制"""
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_ANGLE_LIMIT_READ, "")

    # ———————————————————————————————————————————————————————————————————————————————
    # ⚡️ 电压限制设置
    # ———————————————————————————————————————————————————————————————————————————————

    def set_voltage_limit(self, servo_id, min_volt, max_volt):
        """
        设置输入电压限制（单位: mV，4500~14000）
        :param servo_id: 舵机ID (类型: int 或 str)
        :param min_volt: 最小电压 (范围: 4500~14000)
        :param max_volt: 最大电压 (范围: 4500~14000)
        """
        if min_volt >= max_volt:
            print("最小角度不能大于等于最大角度")
            return
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        param = split_hex(min_volt) + split_hex(max_volt)
        self.__build_55_packet(servo_id, SERVO_VIN_LIMIT_WRITE, param)

    def read_voltage_limit(self, servo_id):
        """
        读取电压限制值
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_VIN_LIMIT_READ, "")

    # ———————————————————————————————————————————————————————————————————————————————
    # 🌡️ 温度限制设置
    # ———————————————————————————————————————————————————————————————————————————————

    def set_max_temperature(self, servo_id, temp):
        """
        设置舵机最高允许温度（50~100℃）
        :param servo_id: 舵机ID (类型: int 或 str)
        :param temp: 最高温度 (范围: 50~100)
        """
        if temp > 100:
            print("温度不能超过100℃")
            return
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        param = hex(temp)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_TEMP_MAX_LIMIT_WRITE, param)

    def read_max_temperature(self, servo_id):
        """
        读取当前最高温度限制
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_TEMP_MAX_LIMIT_READ, "")

    def read_current_temperature(self, servo_id):
        """
        读取当前舵机内部温度
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_TEMP_READ, "")

    def read_current_voltage(self, servo_id):
        """
        读取当前输入电压
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_VIN_READ, "")

    def read_current_position(self, servo_id):
        """
        读取当前角度位置
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_POS_READ, "")

    # ———————————————————————————————————————————————————————————————————————————————
    # ⚙️ 工作模式设置（位置/电机控制）
    # ———————————————————————————————————————————————————————————————————————————————

    def set_motor_mode(self, servo_id, mode: int, turn_mode: int, speed: int) -> None:
        """
        设置舵机工作模式（位置控制 / 电机控制）
        :param servo_id: 舵机ID (类型: int 或 str)
        :param mode: 工作模式，0=位置控制，1=电机控制
        :param turn_mode: 电机转向模式: 0=固定占空比(-1000~1000)
        :param speed: 控制速度或占空比值
        :return: None
        """
        if mode not in (0, 1):
            print("模式参数错误，请检查参数")
            return
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        param = ""
        if mode == 0:
            param = "00000000"
        elif mode == 1:
            # 参数范围校验
            if turn_mode == 0 and not (-1000 <= speed <= 1000):
                print("占空比参数错误，请检查参数")
                return
            if speed < 0:
                speed = speed & 0xFFFF
            # 格式化参数为 2 字节 HEX 字符串拼接（高位在前）
            param = f"{mode:02x}{turn_mode:02x}{split_hex(speed)}"  # 确保只取最后 4 个字符（兼容高位溢出）
            print(f"发送参数: {param}")
        self.__build_55_packet(servo_id, SERVO_OR_MOTOR_MODE_WRITE, param)

    def read_motor_mode(self, servo_id):
        """
        读取当前工作模式
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_OR_MOTOR_MODE_READ, "")

    # ———————————————————————————————————————————————————————————————————————————————
    # 💪 加载/卸载电机输出力矩
    # ———————————————————————————————————————————————————————————————————————————————

    def set_load_state(self, servo_id, state):
        """
        控制电机是否加载输出力矩
        :param servo_id: 舵机ID (类型: int 或 str)
        :param state: 0=卸载，1=加载 (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        if isinstance(state, int):
            # 如果是整数，尝试转换为整数字符串
            state = hex(state)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_LOAD_OR_UNLOAD_WRITE, state)

    def read_load_state(self, servo_id):
        """
        读取当前加载状态
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_LOAD_OR_UNLOAD_READ, "")

    # ———————————————————————————————————————————————————————————————————————————————
    # 🚨 LED 状态与错误提示
    # ———————————————————————————————————————————————————————————————————————————————

    def set_led_state(self, servo_id, state):
        """
        设置LED状态
        :param servo_id: 舵机ID (类型: int 或 str)
        :param state: 0=常亮，1=常灭
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_LED_CTRL_WRITE, "")

    def read_led_state(self, servo_id):
        """
        读取LED状态
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_LED_CTRL_READ, "")

    def set_error_led(self, servo_id, error_code):
        """
        设置哪些错误会触发LED闪烁报警
        :param servo_id: 舵机ID (类型: int 或 str)
        :param error_code: 0~7, 具体错误类型如下:
                        0: 没有报警, 1: 过温, 2: 过压, 3: 过温和过压,
                        4: 堵转, 5: 过温和堵转, 6: 过压和堵转, 7: 过温、过压和堵转
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_LED_ERROR_WRITE, "")

    def read_error_led(self, servo_id):
        """
        读取当前错误报警设置
        :param servo_id: 舵机ID (类型: int 或 str)
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_LED_ERROR_READ, "")

    # ———————————————————————————————————————————————————————————————————————————————
    # 🚗 转动距离
    # ———————————————————————————————————————————————————————————————————————————————

    def move_dis_read(self, servo_id):
        """
        读取当前转动距离
        :param servo_id: 舵机ID (类型: int 或 str)
        :return: None
        """
        if isinstance(servo_id, int):
            # 如果是整数，尝试转换为整数字符串
            servo_id = hex(servo_id)[2:].zfill(2)
        self.__build_55_packet(servo_id, SERVO_DIS_READ, "")

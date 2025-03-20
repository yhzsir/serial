#!/usr/bin/env python

import logging
from cyber.python.cyber_py3 import cyber
from modules.common_msgs.control_msgs import control_cmd_pb2

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("chassis_print")

def control_callback(control_msg):
    """
    当接收到 ControlCommand 消息时打印主要字段信息，
    根据你的 .proto 文件，这里主要关注 throttle、brake、steering_target、speed、acceleration 等字段。
    """
    logger.info("收到 ControlCommand 消息:")
    logger.info("  Throttle: %s", control_msg.throttle)
    logger.info("  Brake: %s", control_msg.brake)
    logger.info("  Steering Rate: %s", control_msg.steering_rate)
    logger.info("  Steering Target: %s", control_msg.steering_target)
    logger.info("  Parking Brake: %s", control_msg.parking_brake)
    logger.info("  Speed: %s", control_msg.speed)
    logger.info("  Acceleration: %s", control_msg.acceleration)
    # 根据需要打印其它字段，例如:
    # logger.info("  Engine On/Off: %s", control_msg.engine_on_off)
    # logger.info("  Trajectory Fraction: %s", control_msg.trajectory_fraction)

def main():
    cyber.init()
    node = cyber.Node("chassis_print_node")
    # 创建订阅者，订阅 "/apollo/control" 主题，并注册 control_callback 回调函数
    subscriber = node.create_reader("/apollo/control", control_cmd_pb2.ControlCommand, control_callback)
    logger.info("底盘程序已启动，等待接收 ControlCommand 消息...")
    cyber.spin(node)

if __name__ == '__main__':
    main()
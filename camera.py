from cyber_record.record import Record
from record_msg.parser import ImageParser
import os

record_file = "demo_3.5.record"
output_dir = "images"  # 输出目录
target_topic = "/apollo/sensor/camera/front_6mm/image"

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 初始化ImageParser，指定输出路径
image_parser = ImageParser(output_path=output_dir)  # 关键修正

with Record(record_file) as record:
    for topic, message, t in record.read_messages():
        if topic == target_topic:
            # 直接调用parse，无需手动保存
            image_parser.parse(message)  # 自动保存到output_path

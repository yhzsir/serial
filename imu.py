from cyber_record.record import Record
from google.protobuf.json_format import MessageToDict
import datetime

def extract_pose_to_txt(input_path, output_txt, target_topic):
    with open(output_txt, 'w') as f:
        with Record(input_path) as record:
            # 设置消息过滤条件
            for topic, msg, t in record.read_messages(topics=[target_topic]):
                # 转换时间戳格式（与OpenCalib格式对齐）
                timestamp = datetime.datetime.fromtimestamp(t/1e9).strftime("%Y-%m-%d-%H-%M-%S-%f")[:-3]
                
                # 解析姿态消息（示例以LocalizationEstimate消息类型为准）
                pose_data = MessageToDict(msg).get('pose', {})
                
                # 提取旋转矩阵（需根据实际消息结构调整）
                orientation = pose_data.get('orientation', {})
                qw = orientation.get('qw', 1.0)
                qx = orientation.get('qx', 0.0)
                qy = orientation.get('qy', 0.0)
                qz = orientation.get('qz', 0.0)
                
                # 转换为旋转矩阵（简化为伪代码）
                # 此处需添加四元数转旋转矩阵的实际计算逻辑
                rot_matrix = [
                    [qw**2 + qx**2 - qy**2 - qz**2, 2*(qx*qy - qw*qz), 2*(qx*qz + qw*qy)],
                    [2*(qx*qy + qw*qz), qw**2 - qx**2 + qy**2 - qz**2, 2*(qy*qz - qw*qx)],
                    [2*(qx*qz - qw*qy), 2*(qy*qz + qw*qx), qw**2 - qx**2 - qy**2 + qz**2]
                ]
                
                # 提取平移向量
                position = pose_data.get('position', {})
                x = position.get('x', 0.0)
                y = position.get('y', 0.0)
                z = position.get('z', 0.0)
                
                # 格式化写入文件（匹配OpenCalib格式）
                line = f"{timestamp} " + \
                       " ".join([f"{val:.9f}" for row in rot_matrix for val in row]) + \
                       f" {x:.9f} {y:.9f} {z:.9f}\n"
                f.write(line)

# 使用示例
extract_pose_to_txt(
    input_path='sensor_rgb.record',
    output_txt='pose_data.txt',
    target_topic='/apollo/localization/pose'
)

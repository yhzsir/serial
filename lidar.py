from cyber_record.record import Record
from record_msg.parser import PointCloudParser

def extract_pointcloud(record_file, output_dir, topic_filter="/apollo/sensor/velodyne64/compensator/PointCloud2", mode='ascii'):
    """
    从 record 文件中提取指定 topic 的点云数据，并生成 PCD 文件，
    点云数据包含 x, y, z, intensity 四个字段。

    参数:
      record_file: record 文件路径
      output_dir: 输出 PCD 文件存放目录
      topic_filter: 点云数据所在的 topic（默认为 "/apollo/sensor/velodyne64/compensator/PointCloud2"）
      mode: 输出文件模式，可选 'ascii'（默认）、'binary' 或 'binary_compressed'
    """
    # 实例化 PointCloudParser，需要传入输出目录
    pointcloud_parser = PointCloudParser(output_dir)
    record = Record(record_file)

    for topic, message, t in record.read_messages():
        if topic == topic_filter:
            # 调用解析函数，指定输出模式，默认是 'ascii'
            pointcloud_parser.parse(message, mode=mode)
            print("已处理 timestamp 为 {} 的消息，生成 PCD 文件至目录：{}".format(t, output_dir))

if __name__ == "__main__":
    # 修改为你实际的 record 文件路径、输出目录和 topic
    record_file = "sensor_rgb.record"       # 例如： "path/to/your_record_file.record"
    output_dir  = "."                        # 输出目录，这里设为当前目录
    topic_filter = "/apollo/sensor/velodyne64/compensator/PointCloud2"
    extract_pointcloud(record_file, output_dir, topic_filter, mode='ascii')

import mobiwusi
import os

# 设置API密钥
mobiwusi.set_api_key("test_api_key_123456")

# 设置目标URL
mobiwusi.set_target_url("http://api.dev.mobiwusi.com/p1.syncData/uploadFile")

# 示例图片路径
test_file_path = r"C:\Users\Administrator\Pictures\Saved Pictures\replicate-prediction-bcjy55vye1rga0cpc5g9zzvm64.png"

try:
    # 测试文件上传
    print("测试文件上传...")
    result = mobiwusi.upload_file(test_file_path, destination="test_server")
    print(f"上传结果: {result}")

finally:
    print("\n测试结束")
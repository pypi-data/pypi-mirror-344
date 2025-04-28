"""
同步记录模块 - 提供记录同步功能
"""
from typing import Optional, Dict, Any, List, Literal
from .auth import get_api_key,get_target_url
from .exceptions import SyncError
from pydantic import BaseModel, Field
from datetime import datetime
import requests

# Define coordinate object
class Coordinate(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: List[float]

# 定义扩展属性对象
class Extra(BaseModel):
    # 根据实际扩展字段定义
    pass

# 定义同步记录的主模型
class SyncRecordModel(BaseModel):
    id: str
    caption: Optional[str]
    create_time: datetime
    update_time: datetime
    path: str
    size: int
    hash: str
    file_format: str
    file_name: str
    cate: int
    coordinate: Coordinate
    from_type: int
    from_unique_id: Optional[str]
    extra: Optional[Extra]

class RecordSynchronizer:
    """记录同步器类"""
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}

    def sync(self, record_data: Dict[str, Any], target: Optional[str] = None, 
             api_key: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        # 获取API密钥
        key = get_api_key(api_key)
        # 检查目标URL
        target_url = get_target_url(kwargs.get("target_url"))
        try:
            # 使用Pydantic模型校验和转换数据
            record = SyncRecordModel(**record_data)
            # 发送POST请求到后端
            headers = {
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            }
            response = requests.post(
                target_url+"/p1.syncData/data",
                data=record.model_dump_json(),
                headers=headers
            )
            response.raise_for_status()
            result = response.json()
            return result
        except Exception as e:
            raise SyncError(f"记录同步失败: {str(e)}")

def sync_record(record_data: Dict[str, Any], target: Optional[str] = None, 
                api_key: Optional[str] = None, **kwargs) -> Dict[str, Any]:
    synchronizer = RecordSynchronizer()
    return synchronizer.sync(record_data, target, api_key, **kwargs)
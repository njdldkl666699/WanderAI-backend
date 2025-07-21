import json

from common.database import redis
from common.log import log
from model.vo import HotspotVO
from agent.model import Hotspot
from server.agent import HotspotAgent


async def get_hotspots(refresh: bool) -> list[HotspotVO]:
    """获取热门景点列表"""
    cache_key = "hotspots:list"
    cache_ttl = 3600  # 缓存1小时

    # 如果不需要刷新，则从Redis中读取
    if not refresh:
        # 检查Redis中是否已有热门景点数据
        cached_data = redis.get(cache_key)
        if cached_data:
            # 如果有，直接从Redis获取并反序列化
            try:
                # 将缓存数据反序列化为Hotspot JSON字符串列表
                hotspots_str: list[str] = json.loads(cached_data)  # type: ignore
                # 将字符串列表转换为Hotspot模型实例列表
                hotspots: list[Hotspot] = [
                    Hotspot.model_validate(hotspot) for hotspot in hotspots_str
                ]
                return [HotspotVO(**hotspot.model_dump()) for hotspot in hotspots]
            except (json.JSONDecodeError, TypeError) as e:
                # 如果反序列化失败，删除缓存并继续获取新数据
                log.warning(f"缓存数据反序列化失败: {e}, 删除缓存并重新获取数据")
                redis.delete(cache_key)

    # 如果没有，调用HotspotAgent获取热门景点数据
    hotspots_result = await HotspotAgent.get_hotspots()

    # 将结果转换为 HotspotVO 列表
    hotspot_vos = [HotspotVO(**hotspot.model_dump()) for hotspot in hotspots_result.data]

    # 将数据缓存到Redis中
    try:
        cache_data = [hotspot.model_dump() for hotspot in hotspots_result.data]
        redis.setex(cache_key, cache_ttl, json.dumps(cache_data, ensure_ascii=False))
    except Exception as e:
        # 缓存失败不影响正常功能，只记录错误
        log.warning(f"缓存热门景点数据失败: {e}")

    return hotspot_vos

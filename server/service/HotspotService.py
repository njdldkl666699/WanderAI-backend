from model.vo import HotspotVO
from server.agent.interface import HotspotAgent


async def get_hotspots() -> list[HotspotVO]:
    """获取热门景点列表"""
    # 调用 HotspotAgent 获取热门景点
    hotspots_result = await HotspotAgent.get_hotspots()

    # 将结果转换为 HotspotVO 列表
    hotspots = [HotspotVO(**hotspot.model_dump()) for hotspot in hotspots_result.data]

    return hotspots

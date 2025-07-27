from fastapi import APIRouter, Query

from wanderai.common.log import log
from wanderai.model.result import Result
from wanderai.server.service import HotspotService

router = APIRouter(prefix="/hotspot")


@router.get("/")
async def get_hotspot(refresh: bool = Query(default=False, description="是否刷新")):
    """获取热门景点推荐"""
    log.info("请求获取热门景点推荐")
    hotspots = await HotspotService.get_hotspots(refresh)
    return Result.success(hotspots)

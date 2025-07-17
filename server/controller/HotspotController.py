from server import app
from model.result import Result
from common.log import log
from server.service import HotspotService


router = app.APIRouter()


@router.get("/hotspot")
async def get_hotspot():
    """获取热门景点推荐"""
    log.info("请求获取热门景点推荐")
    hotspots = await HotspotService.get_hotspots()
    return Result.success(hotspots)

from typing import List, Literal

from pydantic import BaseModel, Field

from wanderai.model.vo import WeatherVO


class Hotspot(BaseModel):
    """热门景点模型"""

    name: str = Field(description="景点名称")
    description: str = Field(description="景点描述")
    image: str = Field(description="景点图片URL")


class HotspotsResult(BaseModel):
    """热门景点结果模型"""

    data: List[Hotspot] = Field(default_factory=list, description="热门景点列表")


class IntentResult(BaseModel):
    """意图识别结果"""

    type: Literal["plan", "chat"] = Field(description="意图类型")
    location: str = Field(default="", description="目的地名称")
    duration: int = Field(default=0, description="旅行天数")
    content: str = Field(default="", description="用户原始输入")


class Schedule(BaseModel):
    """每日行程安排"""

    day: int = Field(description="第几天的行程")
    attractions: List[str] = Field(default_factory=list, description="当天的景点列表")


class PlanResult(BaseModel):
    """旅行计划结果"""

    daily_schedules: List[Schedule] = Field(default_factory=list, description="每日行程安排列表")


class Route(BaseModel):
    """旅行路线"""

    origin: str = Field(description="起点景点名")
    destination: str = Field(description="终点景点名")
    transport: str = Field(description="交通方式")
    distance: str = Field(description="距离")
    duration: str = Field(description="持续时间")


class Attraction(BaseModel):
    """景点详细信息"""

    attraction: str = Field(description="景点名称")
    address: str = Field(description="地址信息")
    coordinates: str = Field(description="经纬度信息，格式为：经度, 纬度")
    introduction: str = Field(description="景点介绍")


class RemarkCards(BaseModel):
    """备注卡片信息"""

    trip_feature: str = Field(description="行程特色")
    arrangement_description: str = Field(description="安排说明")
    travel_suggestion: str = Field(description="行程建议")
    accommodation: str = Field(description="住宿推荐")
    food_recommendation: str = Field(description="美食推荐")


class ExecutorResult(BaseModel):
    """执行Agent结果"""

    day: int = Field(description="第几天的行程")
    routes: List[Route] = Field(default_factory=list, description="当天的路线列表")
    attraction_details: List[Attraction] = Field(
        default_factory=list, description="当天的景点详细信息"
    )
    remark_cards: RemarkCards = Field(description="备注卡片信息")


class Overview(BaseModel):
    """旅行计划总览"""

    duration: str = Field(description="总天数")
    attraction_count: int = Field(description="总景点数")
    total_distance: str = Field(description="总距离")


class SummaryResult(BaseModel):
    """旅行计划总结结果"""

    title: str = Field(description="旅行计划标题")
    overview: Overview = Field(description="旅行计划总览信息")


class AttractionStaticMap(BaseModel):
    """景点静态地图信息"""

    attraction: str = Field(description="景点名称")
    static_map_url: str = Field(description="景点静态地图URL")


class FinalOutput(BaseModel):
    """最终输出格式"""

    summary_result: SummaryResult = Field(description="旅行计划总结结果")
    daily_schedules: List[Schedule] = Field(default_factory=list, description="每日行程安排列表")
    executor_results: List[ExecutorResult] = Field(
        default_factory=list, description="每日详细行程计划列表"
    )
    attraction_maps: List[AttractionStaticMap] = Field(
        default_factory=list, description="景点静态地图信息列表"
    )
    weather_vo: WeatherVO | None = Field(description="天气VO")

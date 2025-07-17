from typing import Any, Literal, AsyncGenerator
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field


class Result(BaseModel):
    code: Literal[0, 1] = Field(default=1, description="状态码，1表示成功，0表示失败")
    msg: str = Field(default="success", description="状态信息")
    data: Any = Field(default=None, description="返回数据")

    @staticmethod
    def success(data: Any = None) -> "Result":
        return Result(code=1, msg="success", data=data)

    @staticmethod
    def error(msg: str = "error") -> "Result":
        return Result(code=0, msg=msg, data=None)


class StreamResult(BaseModel):
    """流式响应结果封装"""

    type: Literal["chat", "plan", "end", "error", "all"] = Field(description="数据类型")
    content: Any = Field(description="内容")

    def to_sse_format(self) -> str:
        """转换为 Server-Sent Events 格式"""
        return f"data: {self.model_dump_json()}\n\n"

    @staticmethod
    def create_streaming_response(
        generator: AsyncGenerator[str, None],
    ) -> StreamingResponse:
        """创建标准的流式响应"""
        return StreamingResponse(
            generator,
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # 禁用Nginx缓冲
            },
        )

    @staticmethod
    def chat(content: str) -> "StreamResult":
        """创建聊天消息"""
        return StreamResult(type="chat", content=content)

    @staticmethod
    def plan(content: str) -> "StreamResult":
        """创建计划消息"""
        return StreamResult(type="plan", content=content)

    @staticmethod
    def all(content: Any) -> "StreamResult":
        """创建计划最终消息"""
        return StreamResult(type="all", content=content)

    @staticmethod
    def end() -> "StreamResult":
        """创建结束标识"""
        return StreamResult(type="end", content="")

    @staticmethod
    def error(message: str) -> "StreamResult":
        """创建错误信息"""
        return StreamResult(type="error", content=message)

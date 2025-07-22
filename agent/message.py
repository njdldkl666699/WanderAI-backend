import json
from typing import Any
from langchain_core.messages import AIMessage, HumanMessage


class AIAudioMessage(AIMessage):
    """带有音频的AI消息"""

    def __init__(self, audio_url: str, text: str):
        super().__init__(
            [{"type": "audio_url", "audio_url": audio_url}, {"type": "text", "text": text}]
        )


class AIPlanMessage(AIMessage):
    """旅行计划AI消息"""

    def __init__(self, plan_result: dict[str, Any]):
        super().__init__([{"type": "text", "text": json.dumps(plan_result)}])


class HumanImageMessage(HumanMessage):
    """带有图片的人类消息"""

    def __init__(self, image_url: str, text: str | None):
        super().__init__(
            [
                {
                    "type": "image_url",
                    "image_url": image_url,
                },
                {"type": "text", "text": text},
            ]
        )

from dashscope.audio.tts import SpeechSynthesizer
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.state import CompiledStateGraph

from wanderai.agent.state import TravelGuideState, TravelPlanState
from wanderai.agent.workflow import travel_guide_workflow
from wanderai.common.properties import SPEECH_MODEL

travel_guide_graph = travel_guide_workflow.compile(
    checkpointer=InMemorySaver(), name="travel_guide"
)


async def get_or_create_state(
    travel_plan_graph: CompiledStateGraph[TravelPlanState, TravelPlanState, TravelPlanState],
    user_input: str,
    image_url: str,
    thread_id: str,
) -> TravelGuideState:
    """获取或创建初始状态，保持历史记忆"""
    # 获取最新的检查点状态
    state_snapshot = await travel_plan_graph.aget_state({"configurable": {"thread_id": thread_id}})

    if state_snapshot and state_snapshot.values:
        # 如果存在历史状态，更新用户输入
        existing_state = state_snapshot.values
        return TravelGuideState(
            user_input=user_input,
            image_url=image_url,
            visual_result=existing_state.get("visual_result", ""),
            text_result=existing_state.get("text_result", ""),
            messages=existing_state.get("messages", []),
        )

    # 如果不存在，创建新状态
    return TravelGuideState(
        user_input=user_input,
        image_url=image_url,
        visual_result="",
        text_result="",
        messages=[],
    )


def generate_audio_from_text(text: str) -> bytes:
    """从文本生成音频"""
    audio_result = SpeechSynthesizer.call(model=SPEECH_MODEL, text=text)
    return audio_result.get_audio_data()

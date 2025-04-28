import os
import json
import time
from collections import defaultdict, deque
from fastapi import APIRouter, HTTPException, Request

from linebot.v3.webhooks import MessageEvent, TextMessageContent
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple
from pathlib import Path
from botrun_flow_lang.langgraph_agents.agents.agent_runner import agent_runner
from botrun_flow_lang.langgraph_agents.agents.search_agent_graph import (
    SearchAgentGraph,
    DEFAULT_SEARCH_CONFIG,
)
from botrun_flow_lang.langgraph_agents.agents.checkpointer.firestore_checkpointer import (
    AsyncFirestoreCheckpointer,
)
import asyncio


def get_subsidy_api_system_prompt():
    current_dir = Path(__file__).parent
    return (current_dir / "subsidy_api_system_prompt.txt").read_text(encoding="utf-8")


def get_subsidy_bot_search_config(stream: bool = True) -> dict:
    return {
        **DEFAULT_SEARCH_CONFIG,
        "search_prompt": get_subsidy_api_system_prompt(),
        "related_prompt": "",
        "domain_filter": ["*.gov.tw", "-*.gov.cn"],
        "user_prompt_prefix": "你是台灣人，你不可以講中國用語也不可以用簡體中文，禁止！你的回答內容不要用Markdown格式。",
        "stream": stream,
    }


class LineBotBase(ABC):
    """LINE Bot 基礎類別，定義共用功能和介面

    此類別提供 LINE Bot 的基本功能，包含：
    1. Webhook 處理和驗證
    2. 訊息接收和回覆
    3. 定義訊息回覆邏輯介面
    4. 訊息頻率限制

    所有的 LINE Bot 實作都應該繼承此類別並實作 get_reply_text 方法。
    """
    
    # 訊息頻率限制設定
    RATE_LIMIT_WINDOW: int = 300 # 預設時間窗口為 5 分鐘 (300 秒)
    RATE_LIMIT_COUNT: int = 1 # 預設在時間窗口內允許的訊息數量

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # 用於追蹤正在處理訊息的使用者，避免同一使用者同時發送多條訊息造成處理衝突
        cls._processing_users = set()
        # 用於訊息頻率限制：追蹤每個使用者在時間窗口內發送的訊息時間戳記
        # 使用 defaultdict(deque) 結構確保：1) 只記錄有發送訊息的使用者 2) 高效管理時間窗口內的訊息
        cls._user_message_timestamps = defaultdict(deque)

    def __init__(self, channel_secret: str, channel_access_token: str):
        """初始化 LINE Bot 設定

        Args:
            channel_secret (str): LINE Channel Secret，用於驗證 webhook 請求
            channel_access_token (str): LINE Channel Access Token，用於發送訊息給使用者

        Raises:
            ValueError: 當 channel_secret 或 channel_access_token 為空時
        """
        # 放到要用的時候才 init，不然loading 會花時間
        from linebot.v3 import WebhookHandler
        from linebot.v3.messaging import Configuration

        if not channel_secret or not channel_access_token:
            raise ValueError("LINE Bot channel_secret 和 channel_access_token 不能為空")

        self.handler = WebhookHandler(channel_secret)
        self.configuration = Configuration(access_token=channel_access_token)

        # 註冊訊息處理函數到 LINE Bot SDK
        # 使用 lambda 避免 SDK 傳入多餘的 destination 參數，並用 asyncio.create_task 處理非同步函數
        # MessageEvent: 訊息事件
        # message=TextMessageContent: 指定處理文字訊息
        self.handler.add(MessageEvent, message=TextMessageContent)(
            lambda event: asyncio.create_task(self.handle_message(event))
        )

    def check_rate_limit(self, user_id: str) -> Tuple[bool, int]:
        """檢查使用者是否超過訊息頻率限制

        檢查使用者在指定時間窗口內發送的訊息數量是否超過限制。
        同時清理過期的時間戳記，以避免記憶體無限增長。

        Args:
            user_id (str): 使用者的 LINE ID

        Returns:
            Tuple[bool, int]: (是否超過限制, 需要等待的秒數)
            如果未超過限制，第二個值為 0
        """
        current_time = time.time()
        user_timestamps = type(self)._user_message_timestamps[user_id]
        
        # 清理過期的時間戳記（超過時間窗口的）
        while user_timestamps and current_time - user_timestamps[0] > type(self).RATE_LIMIT_WINDOW:
            user_timestamps.popleft()
        
        # 如果清理後沒有時間戳記，則從字典中移除該使用者的記錄
        if not user_timestamps:
            del type(self)._user_message_timestamps[user_id]
            # 如果使用者沒有有效的時間戳記，則直接添加新的時間戳記
            type(self)._user_message_timestamps[user_id].append(current_time)
            return False, 0
        
        # 檢查是否超過限制
        if len(user_timestamps) >= type(self).RATE_LIMIT_COUNT:
            # 計算需要等待的時間
            oldest_timestamp = user_timestamps[0]
            wait_time = int(type(self).RATE_LIMIT_WINDOW - (current_time - oldest_timestamp))
            return True, max(0, wait_time)
        
        # 未超過限制，添加當前時間戳記
        user_timestamps.append(current_time)
        return False, 0
        
    async def callback(self, request: Request) -> Dict[str, Any]:
        """處理來自 LINE Platform 的 webhook 回調請求

        驗證請求簽章並處理訊息事件。所有接收到的 webhook 內容都會被記錄。

        Args:
            request (Request): FastAPI 請求物件，包含 webhook 請求的內容

        Returns:
            Dict[str, Any]: 包含處理結果的回應，成功時回傳 {"success": True}

        Raises:
            HTTPException: 當請求簽章驗證失敗時，回傳 400 狀態碼
        """
        # 放到要用的時候才 init，不然loading 會花時間
        from linebot.v3.exceptions import InvalidSignatureError

        signature = request.headers.get("X-Line-Signature", "")
        body = await request.body()
        body_str = body.decode("utf-8")

        try:
            self.handler.handle(body_str, signature)
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="Invalid signature")

        body_json = json.loads(body_str)
        print("Received webhook:", json.dumps(body_json, indent=2, ensure_ascii=False))

        return {"success": True}

    async def handle_message(self, event: MessageEvent) -> None:
        """處理收到的文字訊息並發送回覆

        此方法會：
        1. 記錄收到的訊息和發送者資訊
        2. 檢查使用者是否超過訊息頻率限制
        3. 使用 get_reply_text 取得回覆內容
        4. 發送回覆訊息給使用者，如果訊息過長會分段發送

        Args:
            event (MessageEvent): LINE 訊息事件，包含訊息內容和發送者資訊
        """
        # 放到要用的時候才 init，不然loading 會花時間
        from linebot.v3.messaging import (
            ApiClient,
            MessagingApi,
            ReplyMessageRequest,
            TextMessage,
        )

        MAX_MESSAGE_LENGTH: int = 5000 # LINE 訊息長度限制
        user_id = event.source.user_id
        user_message = event.message.text
        
        # 檢查使用者是否正在處理訊息中
        if user_id in type(self)._processing_users:
            print(f"使用者 {user_id} 已有處理中的訊息，回覆等待提示")
            
            # 快速回覆提示訊息
            with ApiClient(self.configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                messages = [TextMessage(text="您的上一條訊息正在處理中，請稍候再發送新訊息")]
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=messages)
                )
            return
        
        # 檢查使用者是否超過訊息頻率限制
        is_rate_limited, wait_seconds = self.check_rate_limit(user_id)
        if is_rate_limited:
            print(f"使用者 {user_id} 超過訊息頻率限制，需等待 {wait_seconds} 秒")
            
            # 回覆頻率限制提示
            window_minutes = type(self).RATE_LIMIT_WINDOW // 60
            limit_count = type(self).RATE_LIMIT_COUNT
            wait_minutes = max(1, wait_seconds // 60)
            with ApiClient(self.configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                messages = [TextMessage(text=f"您發送訊息的頻率過高，{window_minutes}分鐘內最多可發送{limit_count}則訊息。請等待約 {wait_minutes} 分鐘後再試。")]
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=messages)
                )
            return
        
        # 標記使用者為處理中
        type(self)._processing_users.add(user_id)
        
        try:
            print(f"Received message from {user_id}: {user_message}")
            reply_text = await self.get_reply_text(user_message, user_id)

            print(f"Total response length: {len(reply_text)}")

            # 將長訊息分段，每段不超過 MAX_MESSAGE_LENGTH
            message_chunks = []
            remaining_text = reply_text

            while remaining_text:
                # 如果剩餘文字長度在限制內，直接加入並結束
                if len(remaining_text) <= MAX_MESSAGE_LENGTH:
                    message_chunks.append(remaining_text)
                    print(f"Last chunk length: {len(remaining_text)}")
                    break

                # 確保分段大小在限制內
                safe_length = min(
                    MAX_MESSAGE_LENGTH - 100, len(remaining_text)
                )  # 預留一些空間

                # 在安全長度內尋找最後一個完整句子
                chunk_end = safe_length
                for i in range(safe_length - 1, max(0, safe_length - 200), -1):
                    if remaining_text[i] in "。！？!?":
                        chunk_end = i + 1
                        break

                # 如果找不到適合的句子結尾，就用空格或換行符號來分割
                if chunk_end == safe_length:
                    for i in range(safe_length - 1, max(0, safe_length - 200), -1):
                        if remaining_text[i] in " \n":
                            chunk_end = i + 1
                            break
                    # 如果還是找不到合適的分割點，就直接在安全長度處截斷
                    if chunk_end == safe_length:
                        chunk_end = safe_length

                # 加入這一段文字
                current_chunk = remaining_text[:chunk_end]
                print(f"Current chunk length: {len(current_chunk)}")
                message_chunks.append(current_chunk)

                # 更新剩餘文字
                remaining_text = remaining_text[chunk_end:]

            print(f"Number of chunks: {len(message_chunks)}")
            for i, chunk in enumerate(message_chunks):
                print(f"Chunk {i} length: {len(chunk)}")

            # 使用 LINE Messaging API 發送回覆
            with ApiClient(self.configuration) as api_client:
                line_bot_api = MessagingApi(api_client)
                messages = [TextMessage(text=chunk) for chunk in message_chunks]
                line_bot_api.reply_message_with_http_info(
                    ReplyMessageRequest(reply_token=event.reply_token, messages=messages)
                )
        except Exception as e:
            print(f"處理使用者 {user_id} 訊息時發生錯誤: {str(e)}")
            # 出錯時仍回覆使用者
            try:
                with ApiClient(self.configuration) as api_client:
                    line_bot_api = MessagingApi(api_client)
                    error_message = "很抱歉，處理您的訊息時遇到問題，請稍後再試"
                    messages = [TextMessage(text=error_message)]
                    line_bot_api.reply_message_with_http_info(
                        ReplyMessageRequest(reply_token=event.reply_token, messages=messages)
                    )
            except Exception as reply_error:
                print(f"無法發送錯誤回覆: {str(reply_error)}")
        finally:
            # 無論處理成功或失敗，都從處理中集合移除使用者
            type(self)._processing_users.discard(user_id)
            print(f"使用者 {user_id} 的訊息處理完成")

    @abstractmethod
    async def get_reply_text(self, line_user_message: str, user_id: str) -> str:
        """根據收到的訊息決定回覆內容

        此方法需要被子類別實作，定義 bot 的回覆邏輯。

        Args:
            line_user_message (str): 使用者傳送的 LINE 訊息內容
            user_id (str): 使用者的 LINE ID，可用於個人化回覆或追蹤使用者狀態

        Returns:
            str: 要回覆給使用者的訊息內容
        """
        pass


# 建立 subsidy_line_bot 專用的 SearchAgentGraph 實例
class SubsidyLineBot(LineBotBase):
    """波津貼 LINE Bot 實作"""
    RATE_LIMIT_WINDOW = int(os.environ.get("SUBSIDY_LINEBOT_RATE_LIMIT_WINDOW", 600))
    RATE_LIMIT_COUNT = int(os.environ.get("SUBSIDY_LINEBOT_RATE_LIMIT_COUNT", 2))

    async def get_reply_text(self, line_user_message: str, user_id: str) -> str:
        """實作波津貼 LINE Bot 的回覆邏輯

        使用 agent_runner 處理使用者訊息並回傳回覆內容

        Args:
            line_user_message (str): 使用者傳送的 LINE 訊息內容
            user_id (str): 使用者的 LINE ID

        Returns:
            str: 回覆訊息
        """
        env_name = os.getenv("ENV_NAME", "botrun-flow-lang-dev")
        subsidy_line_bot_graph = SearchAgentGraph(
            memory=AsyncFirestoreCheckpointer(env_name=env_name)
        ).graph

        # 使用 agent_runner 處理訊息，使用 LINE user_id 作為對話追蹤識別碼
        full_response = ""
        async for event in agent_runner(
            user_id,
            {"messages": [line_user_message]},
            subsidy_line_bot_graph,
            extra_config=get_subsidy_bot_search_config(),
        ):
            full_response += event.chunk

        # 移除sonar-reasoning-pro模型的思考過程內容
        if "</think>" in full_response:
            full_response = full_response.split("</think>", 1)[1]

        return full_response


# 初始化 FastAPI 路由器，設定 API 路徑前綴
router = APIRouter(prefix="/line_bot")


# 初始化波津貼 LINE Bot 實例
def get_subsidy_bot():
    # 使用環境變數取得 LINE Bot 的驗證資訊
    return SubsidyLineBot(
        channel_secret=os.getenv("SUBSIDY_LINE_BOT_CHANNEL_SECRET"),
        channel_access_token=os.getenv("SUBSIDY_LINE_BOT_CHANNEL_ACCESS_TOKEN"),
    )


@router.post("/subsidy/webhook")
async def subsidy_webhook(request: Request):
    """波津貼Line bot的webhook endpoint"""
    return await get_subsidy_bot().callback(request)

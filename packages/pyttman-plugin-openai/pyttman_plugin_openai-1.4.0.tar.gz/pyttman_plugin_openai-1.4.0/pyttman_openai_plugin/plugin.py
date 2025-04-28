import json
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from itertools import zip_longest
from pathlib import Path
from typing import Callable
from zoneinfo import ZoneInfo
import tiktoken

import requests

import pyttman
from pyttman.core.containers import MessageMixin, Reply

from pyttman_base_plugin import PyttmanPlugin


@dataclass
class OpenAiRequestPayload:
    model: str
    system_prompt: str
    user_prompt: str
    temperature: float = None

    def as_json(self):
        output = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": self.user_prompt
                }
            ]
        }
        if self.temperature is not None:
            output["temperature"] = self.temperature
        return output

@dataclass
class RagMemoryBank:
    """
    The OpenAiRagMemoryBank is a dataclass that holds
    the conversation history with a user, and the
    memories that the AI should remember.

    Saving the RAG data can be defined by the user, building the app.
    They can provide callbacks for us to use when CRUD:ing memories.
    """
    file_path: Path | None = None
    memories: dict[str, list[str]] = field(default_factory=dict)
    callbacks: dict[str, Callable or None] = field(default_factory=dict)

    def __post_init__(self):
        self.callbacks = {
            "purge_all_memories": None,
            "purge_memories": None,
            "append_memory": None,
            "get_memories": None,
        }

    def _execute_callback(self, callback_name: str, **kwargs) -> any:
        """
        Execute a callback if it's defined.
        """
        try:
            if (callback := self.callbacks.get(callback_name)) is not None:
                response = callback(**kwargs)
                return True if response is None else response
        except Exception as e:
            pyttman.logger.log(level="error",
                               message=f"OpenAIPlugin: RagMemoryBank: "
                                       f"callback {callback_name} failed: {e}")
            pyttman.logger.log(traceback.format_exc())

    def _load_memories_from_file(self):
        """
        Load the memories source
        """
        if self.file_path is None:
            raise ValueError("OpenAIPlugin: RagMemoryBank: Using file storage "
                             "fallback failed. No file path defined for the "
                             "memory bank.")

        if not self.file_path.exists():
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            self.save_to_file()

        with open(self.file_path, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            self.memories = data["memories"]

    def _get_memory_from_file(self, key):
        """
        Fallback, unless user implements callback. Use file-based memories.
        """
        if not self.memories:
            self._load_memories_from_file()
        return self.memories.get(str(key), [])

    def _add_memory_to_file(self, key, memory):
        if not self.memories:
            self._load_memories_from_file()

        key = str(key)
        if self.memories.get(key) is None:
            self.memories[key] = [memory]
        else:
            self.memories[key].append(memory)
        self.save_to_file()

    def purge_all_memories(self):
        """
        Purge all memories.
        """
        if self._execute_callback("purge_all_memories") is not None:
            return
        self.memories.clear()

    def purge_memories(self, key: str):
        """
        Purge all memories for a given key.
        """
        if self._execute_callback("purge_memories", key=key) is not None:
            return
        self.memories[key] = []

    def get_memories(self,
                     key: str,
                     message: MessageMixin,
                     conversation_context: str = None
                     ) -> tuple[str] or list[str]:
        """
        Return the memories for a given key.
        """
        if (memories := self._execute_callback("get_memories",
                                               key=key,
                                               message_text=message.as_str(),
                                               conversation_context=conversation_context)
        ) is not None:
            if not isinstance(memories, (list, tuple)):
                raise ValueError("OpenAIPlugin: The memories callback must "
                                 "return a list or tuple.")
            return memories
        return self._get_memory_from_file(key)

    def add_memory(self, key: str, memory: str):
        """
        Append a memory to the memory bank.
        """
        if callback_return := self._execute_callback("add_memory", key=key, memory=memory):
            return callback_return
        self._add_memory_to_file(key, memory)

    def save_to_file(self):
        """
        Save the memories to a file.
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            data = self.as_json()
            f.write(json.dumps(data, indent=4))

    def as_json(self):
        return {"memories": self.memories}


class OpenAIPlugin(PyttmanPlugin):
    """
    The OpenAIPlugin offers seamless integrations with the OpenAI API.
    Use the plugin to define pre-prompts that can be used to pre- or post
    process your message in your Pyttman application.

    An example is to use a pre-defined system prompt to correct spelling
    mistakes before the message is passed to the intent matching system.

    Another example is to use the GPT as a post-processor, to generate
    a response based on the intent matched by the Pyttman application.

    Or - use the GPT to generate a response from scratch, when no intent
    matches the user's message. This would be a great way to combine the
    rule-based intent matching system with an AI model.

    The plugin supports RAG: conversational mode. When this is enabled, the
    plugin will keep a conversation history for each user in memory, and
    use this history to generate responses. This can be useful to keep
    the conversation flowing naturally, and to keep the context of the
    conversation intact. While recommended, it's important to note that
    the data is stored in memory, non-encrypted, and will be lost when
    the application is restarted.

    :param api_key: The OpenAI API key to use for the plugin.
    :param model: The model to use for the OpenAI API. For valid options,
        see OpenAI's API documentation.
    :param system_prompt: A system prompt to use for the OpenAI API. Set
        this to configure your app behavior.
    :param max_tokens: The maximum number of tokens to use for the OpenAI API.
    :param enable_conversations: Enable RAG: conversational mode. This will
        keep a conversation history for each user,
        greatly improving the experience for conversational applications.
        Disable for stateless apps.
    :param enable_memories: Enable memory making. This will allow the AI to
        remember details about the user, automatically.
        To define custom functions for CRUD operations with memory to use
        a database or other source, provide the callbacks for the plugin to use.
    :param max_conversation_length: The maximum length of the conversation
        history to keep in memory. When the conversation history exceeds this
        length, the memory is truncated oldest first, making for a seamless
        experience.
    :param allowed_intercepts: A list of PyttmanPluginIntercept enums that
        define when the plugin should be executed in the Pyttman application.
        Use these intercepts to align the system prompts you set, with
        the time of execution in the Pyttman application. For example,
        use PyttmanPluginIntercept.before_router to correct spelling mistakes
        or otherwise pre-process the message before it's sent on to the intents.
        In this case, the system prompt could be a spell-checker prompt,
        return the message to the user spell corrected and otherwise intact.
        Stack multiple plugins with different intercept points to create
        a powerful AI system.
    :param time_aware: Set to True if the plugin should be aware of the current
        datetime. If True, the system prompt will be prepended with the current
        datetime, making the AI aware of the time of day. This can really
        improve the experience since the AI can reason about when things
        occur, and you can introduce reasoning about future and past events
        with the AI.
    :param time_zone: The timezone to use for the time awareness. If not set,
        the system will use the system timezone.
    """

    conversation_prompt = ("You will get a copy of the conversation history "
                           "with this user so far. Your previous messages "
                           "are prefixed with 'You: '. Do not include this "
                           "'You: ' in your actual replies. Respond according "
                           "to the users' last message, naturally as if conversing "
                           "with a human, taking the history in the dialogue "
                           "you've already had. \n\n")

    detect_memory_prompt = ("You are a filtering layer in a multi-modal AI system. Your "
                            "only job is to decide if the user's latest message contains "
                            "a new, long-term memory worth storing. You must not respond, "
                            "explain, or analyze the content beyond this decision. If the "
                            "message contains something the user shares about their life, "
                            "routines, values, people, events, goals, preferences, or direct"
                            " orders to store something — and this is not already in memory "
                            "— and this information is likely to be useful in future "
                            "conversations, summarize it briefly in this format: "
                            "`[MEMORY]: <memory content>`. If none of this applies, "
                            "return exactly: `0` You have access to the current date and time."
                            " If the user mentions a relative time (like \"tomorrow\", \"next "
                            "week\", etc), convert it to an absolute date or datetime in the "
                            "memory string, formatted YYYY-MM-DD. If a time is also mentioned,"
                            "format using YYYY-MM-DD-hh:mm:ss. Do not use relative terms in stored memories. "
                            "Strict rules: - Do not store questions. - Do not store short-term "
                            "statements like how the user feels right now or what they are "
                            "about to do, unless it's clearly meaningful long-term. - Do not "
                            "store user curiosity or opinions unless they reveal something "
                            "personal or recurring. - Always store user requests to be "
                            "reminded of specific actions. These are treated as high-priority "
                            "memories. - Do not store duplicates or near-duplicates of "
                            "existing memories. - Do not guess or assume meaning. - Do not "
                            "elaborate. Store the memory in the same language as the message is written in. "
                            "You will mention what the memory is about, in form of tags. These tags "
                            "are topics that the memory is about, making it easier to categorize the memory "
                            "and to find other memories that are related to this one. Tags should be "
                            "short, 1-3 words, and should be separated by commas. Re-use tags in previous "
                            "memories which are similar to this one. Only output `[MEMORY]: <memory content> "
                            "<tags>` or `0`. You are not ChatGPT. You do not answer. "
                            "You only filter and summarize if needed. Current date time information: "
                            "{DATE_TIME_DATA}")

    long_term_memory_prompt = ("\nThese following data are your long term "
                               "memories with this user. Look at "
                               "the date time mentioned in the memory and evaluate "
                               "whether this memory has already happened or if it's "
                               "in the future. Use the datetime right now to think "
                               "with the datetime right now to think when this "
                               "memory happened - it might be in the past now, "
                               "compared to when the memory was created. "
                               "Be aware of how long ago it was "
                               "since whatever the memory was stored and use this "
                               "time difference when responding to the user. Oldest "
                               "memories are at the top, newest at the bottom. "
                               "memories:\n```\n{}\n```\n")
    def __init__(self,
                 api_key: str,
                 model: str,
                 system_prompt: str = None,
                 max_tokens: int = None,
                 enable_conversations: bool = False,
                 enable_memories: bool = False,
                 max_conversation_length: int = 32_000,
                 memory_updated_notice: str = None,
                 allowed_intercepts: list["PluginInterceptPoint"] = None,
                 time_aware: bool = False,
                 time_zone: ZoneInfo = None,
                 purge_all_memories_callback: callable or None = None,
                 purge_memories_callback: callable or None = None,
                 add_memory_callback: callable or None = None,
                 get_memories_callback: callable or None = None):

        if time_zone and not isinstance(time_zone, ZoneInfo):
            raise ValueError("OpenAIPlugin: time_zone must be a ZoneInfo object,"
                             " or None to use the system timezone.")
        super().__init__(allowed_intercepts)

        self.api_key = api_key
        self.model = model
        self.system_prompt = system_prompt
        self.session = requests.Session()
        self.url = "https://api.openai.com/v1/chat/completions"
        self.max_tokens = max_tokens
        self.api_key = api_key
        self.enable_conversations = enable_conversations
        self.max_conversation_length = max_conversation_length
        self.enable_memories = enable_memories
        self.memory_updated_notice = memory_updated_notice or "Memory updated."
        self.rag_memories_path: Path | None = None
        self.long_term_memory: RagMemoryBank | None = None
        self.time_aware = time_aware
        self.zone_info = time_zone
        self.conversation_rag = {}

        self._purge_all_memories_callback = purge_all_memories_callback
        self._purge_memories_callback = purge_memories_callback
        self._add_memory_callback = add_memory_callback
        self._get_memories_callback = get_memories_callback

        self.session.headers.update({"Content-Type": "application/json"})
        self.session.headers.update({"Accept-Type": "application/json"})
        self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        del self.api_key

    @property
    def time_awareness_prompt(self):
        now = datetime.now(tz=self.zone_info) if self.zone_info else datetime.now()
        weekday = now.strftime("%A")
        calendar_week = now.isocalendar().week
        time_prompt = (f"[{now.strftime('%Y-%m-%d %H:%M:%S')} - "
                       f"{weekday}, week number {calendar_week}]")
        return time_prompt

    def on_app_start(self):
        if (static_files_dir := self.app.settings.STATIC_FILES_DIR) is None:
            static_files_dir = Path(self.app.settings.APP_BASE_DIR / "static")
        self.rag_memories_path = static_files_dir / "rag_memories" / "memories.json"
        self.long_term_memory = RagMemoryBank(self.rag_memories_path)

        self.long_term_memory.callbacks["purge_all_memories"] = self._purge_all_memories_callback
        self.long_term_memory.callbacks["purge_memories"] = self._purge_memories_callback
        self.long_term_memory.callbacks["add_memory"] = self._add_memory_callback
        self.long_term_memory.callbacks["get_memories"] = self._get_memories_callback

        pyttman.logger.log("- [OpenAIPlugin]: Plugin started.")

    def update_conversation(self, message: MessageMixin):
        """
        Update the conversation history with the user's message.
        """
        if self.time_aware:
            message_content = f"{self.time_awareness_prompt}: {message.as_str()}"
        else:
            message_content = message.as_str()

        if self.conversation_rag.get(message.author.id) is None:
            self.conversation_rag[message.author.id] = {"user": [message_content], "ai": []}
        else:
            self.conversation_rag[message.author.id]["user"].append(message_content)

        while True:
            user_length = len("".join(self.conversation_rag[message.author.id]["user"]))
            ai_length = len("".join(self.conversation_rag[message.author.id]["ai"]))

            if user_length + ai_length > self.max_conversation_length:
                self.conversation_rag[message.author.id]["user"].pop(0)
                self.conversation_rag[message.author.id]["ai"].pop(0)
            else:
                break

    def get_conversation(self, message: MessageMixin, last: int = None) -> str:
        """
        Use RAG to prepend conversation history with this user to
        the outgoing llm request.

        The last x messages can be returned provided a number.
        """
        if not self.enable_conversations or not self.conversation_rag:
            return message.as_str()

        conversation = ""
        try:
            user_messages = self.conversation_rag[message.author.id]["user"]
            ai_messages = self.conversation_rag[message.author.id]["ai"]
        except KeyError:
            user_messages = [message.as_str()]
            ai_messages = []

        if last is not None:
            try:
                user_messages = user_messages[len(user_messages) - last:]
                ai_messages = ai_messages[len(ai_messages) - last:]
            except KeyError:
                # No history saved - return the message as is.
                return message.as_str()

        for user_message, ai_message in zip_longest(
            user_messages,
            ai_messages,
            fillvalue=""
        ):
            if user_message:
                conversation += f"User: {user_message}\n"
            if ai_message:
                conversation += f"You: {ai_message}\n"
        return conversation + f"User: {message.as_str()}\n"

    def prepare_payload(self,
                        message: MessageMixin,
                        conversation: str = None,
                        memories: list[str] = None) -> dict:
        """
        Prepare a payload towards OpenAI.
        """
        system_prompt = self.system_prompt
        if conversation:
            system_prompt = self.system_prompt + self.conversation_prompt
            pyttman.logger.log(f" - [OpenAIPlugin]: conversation size "
                               f"for user {message.author.id}: {len(conversation)}")
        else:
            conversation = message.as_str()

        if memories:
            system_prompt += self.long_term_memory_prompt.format("\n".join(memories))

        if self.time_aware:
            now = datetime.now(tz=self.zone_info) if self.zone_info else datetime.now()
            weekday = now.strftime("%A")
            calendar_week = now.strftime("%U")
            time_prompt = (f"The date time right now is {now.strftime('%Y-%m-%d %H:%M:%S')}."
                           f"It's a {weekday} in week {calendar_week}.")
            system_prompt = f"{time_prompt}\n{system_prompt}"

        payload = OpenAiRequestPayload(
            model=self.model,
            system_prompt=system_prompt,
            user_prompt=conversation).as_json()
        return payload

    def before_router(self, message: MessageMixin):
        """
        Executes before the router resolves the message to an intent.
        """
        conversation = self.get_conversation(message) if self.enable_conversations else None
        payload = self.prepare_payload(message=message, conversation=conversation)

        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens

        try:
            response = self.session.post(self.url, json=payload)
            response_content = response.json()["choices"][0]["message"]["content"]
            tokens_used = response.json()["usage"]["total_tokens"]
            pyttman.logger.log(f" - [OpenAIPlugin]: total tokens used: {tokens_used}")
            message.content = response_content
            return message
        except requests.exceptions.RequestException as e:
            pyttman.logger.log(level="error",
                               message=f"OpenAIPlugin: Request to "
                                       f"OpenAI API failed: {e}")
            return message

    def create_memory_if_applicable(self,
                                    message: MessageMixin,
                                    conversation: str = None,
                                    memories: list[str] = None) -> str or None:
        """
        Create a memory if the message is a memory making message.
        If time awareness is enabled, the memory will be prepended
        with the current date and time in the user-defined timezone
        or the system timezone as fallback.

        When the llm is prompted, the ten most recent memories
        are included as a context. This is to mitigate the risk of
        the model creating multiple memories of the same thing over
        and over again.
        """
        if conversation is None:
            conversation = message.as_str()

        if len(memories) > 100:
            memories = memories[-100:]
        memories_prompt = self.long_term_memory_prompt.format("\n".join(memories))
        memory_detect_prompt = self.detect_memory_prompt.format(
            DATE_TIME_DATA=self.time_awareness_prompt)

        system_prompt = f"{memories_prompt}\n{memory_detect_prompt}"
        payload = OpenAiRequestPayload(
            model=self.model,
            system_prompt=system_prompt,
            temperature=0.0,
            user_prompt=conversation).as_json()

        try:
            response = self.session.post(self.url, json=payload)
            memory = response.json()["choices"][0]["message"]["content"]
            if str(memory) == "0":
                return None
            if self.time_aware:
                memory = f"{self.time_awareness_prompt}: {memory}"
            print(f"Creating new memory: {memory}")
            return memory
        except requests.exceptions.RequestException as e:
            pyttman.logger.log(level="error",
                               message=f"OpenAIPlugin: Request to "
                                       f"OpenAI API failed: {e}")
            return None

    def no_intent_match(self, message: MessageMixin) -> Reply | None:
        """
        Hook. Executed when no intent matches the user's message.
        """
        if self.enable_conversations:
            conversation = self.get_conversation(message)
        else:
            conversation = message.as_str()

        if self.enable_memories:
            memories = self.long_term_memory.get_memories(
                key=message.author.id,
                message=message,
                conversation_context=conversation)
        else:
            memories = []

        if new_memory := self.create_memory_if_applicable(
                message,
                conversation,
                memories
        ):
            self.long_term_memory.add_memory(message.author.id, new_memory)

        error_response = Reply("I'm sorry, I couldn't generate a response for you.")
        payload = self.prepare_payload(message, conversation, memories)

        if self.enable_conversations:
            self.update_conversation(message)

        if self.max_tokens:
            payload["max_tokens"] = self.max_tokens

        try:
            response = self.session.post(self.url, json=payload)
        except requests.exceptions.RequestException as e:
            pyttman.logger.log(level="error",
                               message=f"OpenAIPlugin: Request to OpenAI API failed: {e}")
            return error_response

        if not response.ok:
            pyttman.logger.log(level="error",
                               message=f"OpenAIPlugin: Request to OpenAI "
                                       f"API failed: {response.text}")
            return error_response

        try:
            gpt_content = response.json()["choices"][0]["message"]["content"]
            ai_reply = f"{self.time_awareness_prompt}: {gpt_content}" if self.time_aware else gpt_content

            self.conversation_rag[message.author.id]["ai"].append(ai_reply)
            if new_memory:
                gpt_content = f"{self.memory_updated_notice}\n{gpt_content}"
            return Reply(gpt_content)
        except KeyError:
            pyttman.logger.log(level="error",
                               message="OpenAIPlugin: No response from OpenAI API.")
            return error_response

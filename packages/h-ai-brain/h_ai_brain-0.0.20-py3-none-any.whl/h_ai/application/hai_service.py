from h_message_bus import NatsPublisherAdapter

from ..domain.llm_config import LLMConfig
from ..infrastructure.llm.ollama.ollama_generate_repository import OllamaGenerateRepository


class HaiService:
    def __init__(self, nats_publisher_adapter: NatsPublisherAdapter, llm_config: LLMConfig):
        self.nats_publisher_adapter = nats_publisher_adapter
        self.llm_config = llm_config
        self.llm_generate_repository = OllamaGenerateRepository(
            self.llm_config.url,
            self.llm_config.model_name,
            temperature=self.llm_config.temperature,
            max_tokens=self.llm_config.max_tokens)

    def ask_question(self, question: str, system_prompt: str = None, max_tokens = None) -> str:
        return self.llm_generate_repository.generate(question, system_prompt, max_tokens)



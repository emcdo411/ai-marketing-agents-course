# anthropic_client.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv
from anthropic import Anthropic, APIError

# Load API key and settings from .env
load_dotenv()

DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-latest")

@dataclass
class ClaudeClient:
    api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    model: str = DEFAULT_MODEL

    def __post_init__(self):
        if not self.api_key:
            raise RuntimeError("ANTHROPIC_API_KEY not set")
        self.client = Anthropic(api_key=self.api_key)

    def json_call(self, system: str, user: str, max_tokens: int = 800):
        """Return Claude JSON-like content (string). Keep prompts schema-first."""
        try:
            msg = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
                temperature=0.2,
            )
            # Anthropic returns a list of content blocks
            return "".join([blk.text for blk in msg.content if hasattr(blk, "text")])
        except APIError as e:
            raise RuntimeError(f"Claude error: {e}") from e

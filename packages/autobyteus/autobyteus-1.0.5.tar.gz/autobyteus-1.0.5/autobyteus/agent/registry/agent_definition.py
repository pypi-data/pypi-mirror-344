import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class AgentDefinition:
    """
    Represents the static definition of an agent, containing its role, description,
    tools, optional system prompt, and optional initial user message.
    """
    def __init__(self,
                 role: str,
                 description: str,
                 tools: List[str],
                 system_prompt: Optional[str] = None,
                 initial_user_message: Optional[str] = None):
        """
        Initializes the AgentDefinition.

        Args:
            role: The unique role identifier of the agent (e.g., 'coordinator', 'worker').
            description: A human-readable description of the agent's purpose.
            tools: A list of tool names the agent can use.
            system_prompt: An optional system prompt to configure the LLM's behavior.
            initial_user_message: An optional initial user message to start the agent's conversation.

        Raises:
            ValueError: If role, description, or tools are invalid, or if system_prompt or
                        initial_user_message are not strings when provided.
        """
        if not role or not isinstance(role, str):
            raise ValueError("AgentDefinition requires a non-empty string 'role'.")
        if not description or not isinstance(description, str):
            raise ValueError(f"AgentDefinition '{role}' requires a non-empty string 'description'.")
        if not isinstance(tools, list) or not all(isinstance(t, str) and t for t in tools):
            raise ValueError(f"AgentDefinition '{role}' requires a non-empty list of tool name strings.")
        if system_prompt is not None and not isinstance(system_prompt, str):
            raise ValueError(f"AgentDefinition '{role}' system_prompt must be a string or None.")
        if initial_user_message is not None and not isinstance(initial_user_message, str):
            raise ValueError(f"AgentDefinition '{role}' initial_user_message must be a string or None.")

        self._role = role
        self._description = description
        self._tools = tools
        self._system_prompt = system_prompt
        self._initial_user_message = initial_user_message

        logger.debug(f"AgentDefinition created for role '{self.role}'.")

    @property
    def role(self) -> str:
        """The unique role identifier of the agent."""
        return self._role

    @property
    def description(self) -> str:
        """The human-readable description of the agent's purpose."""
        return self._description

    @property
    def tools(self) -> List[str]:
        """The list of tool names the agent can use."""
        return self._tools

    @property
    def system_prompt(self) -> Optional[str]:
        """The optional system prompt for the agent."""
        return self._system_prompt

    @property
    def initial_user_message(self) -> Optional[str]:
        """The optional initial user message for the agent."""
        return self._initial_user_message

    def __repr__(self) -> str:
        """Provides a developer-friendly string representation."""
        desc_repr = self.description
        if len(desc_repr) > 70:
            desc_repr = desc_repr[:67] + "..."
        # Remove newlines/tabs for cleaner logging
        desc_repr = desc_repr.replace('\n', '\\n').replace('\t', '\\t')
        return (f"AgentDefinition(role='{self.role}', description='{desc_repr}', "
                f"tools={self.tools}, system_prompt='{self.system_prompt}', "
                f"initial_user_message='{self.initial_user_message}')")

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation of the agent definition."""
        return {
            "role": self.role,
            "description": self.description,
            "tools": self.tools,
            "system_prompt": self.system_prompt,
            "initial_user_message": self.initial_user_message
        }

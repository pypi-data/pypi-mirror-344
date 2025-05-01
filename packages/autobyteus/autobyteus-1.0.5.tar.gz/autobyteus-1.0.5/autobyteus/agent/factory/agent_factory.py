# file: autobyteus/agent/factory/agent_factory.py
import logging
from autobyteus.agent.agent import Agent
from autobyteus.agent.group.group_aware_agent import GroupAwareAgent
from autobyteus.llm.llm_factory import LLMFactory
from autobyteus.tools.factory.tool_factory import ToolFactory
from autobyteus.prompt.prompt_builder import PromptBuilder
from autobyteus.llm.models import LLMModel
from typing import List, Union

logger = logging.getLogger(__name__)

class AgentFactory:
    """
    Factory class for creating different types of agents.

    This factory simplifies the creation of Agent instances by encapsulating
    the necessary dependencies and configurations.
    """
    def __init__(self,
                 role: str,
                 agent_type: str,
                 tool_factory: ToolFactory,
                 llm_factory: LLMFactory,
                 prompt_builder: PromptBuilder, # Agent requires prompt_builder or initial_user_message
                 llm_model: LLMModel,
                 tool_names: List[str]):
        """
        Initializes the AgentFactory.

        Args:
            role: The role the created agents will fulfill.
            agent_type: The type of agent to create ("standalone" or "group_aware").
            tool_factory: A factory to create tool instances.
            llm_factory: A factory to create LLM instances.
            prompt_builder: The PromptBuilder instance to configure the agent's system prompt.
            llm_model: The specific LLM model configuration to use.
            tool_names: A list of tool names the agent should be equipped with.
        """
        self.role = role
        self.agent_type = agent_type
        self.tool_factory = tool_factory
        self.llm_factory = llm_factory
        self.prompt_builder = prompt_builder
        self.llm_model = llm_model
        self.tool_names = tool_names
        logger.info(f"AgentFactory initialized for role '{role}' and type '{agent_type}'")

    def create_agent(self, agent_id: str) -> Union[Agent, GroupAwareAgent]:
        """
        Creates an agent instance based on the factory's configuration.

        Args:
            agent_id: The unique identifier for the agent being created.

        Returns:
            An instance of Agent or GroupAwareAgent.

        Raises:
            ValueError: If the configured agent_type is unsupported.
        """
        logger.info(f"Creating agent with id '{agent_id}' for role '{self.role}' and type '{self.agent_type}'")
        try:
            tools = [self.tool_factory.create_tool(name) for name in self.tool_names]
            logger.debug(f"Tools created for agent '{agent_id}': {[tool.get_name() for tool in tools]}")
        except Exception as e:
            logger.error(f"Error creating tools for agent '{agent_id}': {e}")
            raise ValueError(f"Failed to create tools for agent {agent_id}: {e}") from e

        try:
            llm = self.llm_factory.create_llm(self.llm_model)
            logger.debug(f"LLM instance created for agent '{agent_id}' using model '{self.llm_model.model_name}'")
        except Exception as e:
            logger.error(f"Error creating LLM for agent '{agent_id}': {e}")
            raise ValueError(f"Failed to create LLM for agent {agent_id}: {e}") from e

        agent_args = {
            "agent_id": agent_id,
            "role": self.role,
            "prompt_builder": self.prompt_builder,
            "llm": llm,
            "tools": tools
        }

        if self.agent_type == "standalone":
            logger.debug(f"Instantiating Agent with args: {agent_args}")
            return Agent(**agent_args)
        elif self.agent_type == "group_aware":
            logger.debug(f"Instantiating GroupAwareAgent with args: {agent_args}")
            return GroupAwareAgent(**agent_args)
        else:
            logger.error(f"Unsupported agent type specified in factory: {self.agent_type}")
            raise ValueError(f"Unsupported agent type: {self.agent_type}")


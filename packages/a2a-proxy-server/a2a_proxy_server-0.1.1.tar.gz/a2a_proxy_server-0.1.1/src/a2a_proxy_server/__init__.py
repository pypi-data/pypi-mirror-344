import logging
import click
import yaml
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from google_a2a.common.types import AgentSkill, AgentCapabilities, AgentCard
from a2a_proxy_server.server import A2AProxyServer
from a2a_proxy_server.task_manager import AgentTaskManager

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_agent_config(config_path: str) -> Dict[str, Any]:
    """Load agent configuration from a YAML file."""
    try:
        with open(config_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.error(f"Failed to load config from {config_path}: {e}")
        raise


def create_agent_card(
    config: Dict[str, Any], host: str, port: int
) -> tuple[AgentCard, str, Optional[Dict[str, Any]]]:
    """Create an AgentCard from a configuration dictionary."""
    agent_name = config.get("name", "Unnamed Agent")
    agent_id = agent_name.lower().replace(" ", "-")

    # Create skills
    skills = []
    for skill_config in config.get("skills", []):
        skill = AgentSkill(
            id=skill_config.get("id"),
            name=skill_config.get("name"),
            description=skill_config.get("description"),
            tags=skill_config.get("tags", []),
            examples=skill_config.get("examples", []),
            inputModes=["text"],
            outputModes=["text"],
        )
        skills.append(skill)

    # Create capabilities
    cap_config = config.get("capabilities", {})
    capabilities = AgentCapabilities(streaming=cap_config.get("streaming", False))

    # Create agent card
    agent_card = AgentCard(
        name=config.get("name", "Unnamed Agent"),
        description=config.get("description", ""),
        url=config.get("url", f"http://{host}:{port}/{agent_id}"),
        version=config.get("version", "0.1.0"),
        defaultInputModes=config.get("defaultInputModes", ["text"]),
        defaultOutputModes=config.get("defaultOutputModes", ["text"]),
        capabilities=capabilities,
        skills=skills,
    )

    # Get tool configurations if available
    tool_config = None
    if "mcpServers" in config:
        tool_config = {
            server["name"]: {
                "url": server["url"],
                "transport": server["transport"],
            }
            for server in config.get("mcpServers", [])
        }

    return agent_card, agent_id, tool_config


@click.command()
@click.option("--host", default="localhost", help="Host to run the server on")
@click.option("--port", default=10002, help="Port to run the server on")
@click.option(
    "--config", "-c", multiple=True, required=True, help="Path to agent config file(s)"
)
def main(host, port, config):
    """Start A2A proxy server with agents loaded from config files."""
    server = A2AProxyServer(host=host, port=port)

    # Load agent configs and register them
    for config_path in config:
        try:
            logger.info(f"Loading agent config from {config_path}")
            agent_config = load_agent_config(config_path)
            agent_card, agent_id, tool_config = create_agent_card(
                agent_config, host, port
            )

            # Create task manager with tool config if available
            task_manager = AgentTaskManager(
                tool_config=tool_config, prompt=agent_config.get("prompt")
            )

            # Register the agent
            server.register_agent(
                agent_id=agent_id, agent_card=agent_card, task_manager=task_manager
            )
            logger.info(
                f"Registered agent '{agent_card.name}' with ID: {agent_id}, URL: http://{host}:{port}/{agent_id}"
            )
        except Exception as e:
            logger.error(f"Failed to register agent from {config_path}: {e}")

    logger.info(f"Starting server on http://{host}:{port}")
    server.start()


if __name__ == "__main__":
    main()

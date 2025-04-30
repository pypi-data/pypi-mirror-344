import logging
import click
from ephor_cli.agent import Agent
from ephor_cli.types import AgentConfig
import yaml
import os
import sys
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from google_a2a.common.types import (
    AgentSkill as A2AAgentSkill,
    AgentCapabilities as A2AAgentCapabilities,
    AgentCard,
)
from ephor_cli.server import A2AProxyServer
from ephor_cli.task_manager import AgentTaskManager
from ephor_cli.service.server.server import ConversationServer
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from colorama import Fore, Style
import colorama
import importlib.resources
import pathlib

# Define version
__version__ = "0.2.1"

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_agent_config(config_path: str) -> AgentConfig:
    """Load agent configuration from a YAML file."""
    try:
        with open(config_path, "r") as file:
            config_dict = yaml.safe_load(file)
            return AgentConfig(**config_dict)
    except Exception as e:
        logger.error(f"Failed to load config from {config_path}: {e}")
        raise


def create_agent_card(
    config: AgentConfig, host: str, port: int
) -> tuple[AgentCard, str, Optional[Dict[str, Any]]]:
    """Create an AgentCard from a configuration dictionary."""
    agent_name = config.name
    agent_id = agent_name.lower().replace(" ", "-")

    # Create skills
    skills = []
    for skill_config in config.skills:
        skill = A2AAgentSkill(
            id=skill_config.id,
            name=skill_config.name,
            description=skill_config.description,
            tags=skill_config.tags,
            examples=skill_config.examples,
            inputModes=skill_config.inputModes,
            outputModes=skill_config.outputModes,
        )
        skills.append(skill)

    # Create capabilities
    capabilities = A2AAgentCapabilities(streaming=config.capabilities.streaming)

    # Create agent card
    agent_card = AgentCard(
        name=config.name,
        description=config.description,
        url=f"http://{host}:{port}/{agent_id}",
        version=config.version,
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=capabilities,
        skills=skills,
    )

    return agent_card, agent_id


@click.group()
def cli():
    """Ephor CLI for managing A2A proxy agents."""
    pass


@cli.command()
@click.option("--host", default="localhost", help="Host to run the server on")
@click.option("--port", default=10002, help="Port to run the server on")
@click.option(
    "--config", "-c", multiple=True, required=True, help="Path to agent config file(s)"
)
def up(host, port, config):
    """Start A2A compatible agents loaded from config files."""
    server = A2AProxyServer(host=host, port=port)

    # Load agent configs and register them
    for config_path in config:
        try:
            logger.info(f"Loading agent config from {config_path}")
            agent_config = load_agent_config(config_path)
            agent_card, agent_id = create_agent_card(agent_config, host, port)

            agent = Agent(
                prompt=agent_config.prompt,
                mcpServers=agent_config.mcpServers,
            )

            # Create task manager with tool config if available
            task_manager = AgentTaskManager(agent)

            # Register the agent
            server.register_agent(
                agent_id=agent_id, agent_card=agent_card, task_manager=task_manager
            )
            logger.info(
                f"Registered agent '{agent_card.name}' with ID: {agent_id}, URL: http://{host}:{port}/{agent_id}"
            )
            # Print colorful URL for better visibility
            click.echo(
                f"Agent '{agent_card.name}' available at: {Fore.CYAN}{Style.BRIGHT}http://{host}:{port}/{agent_id}{Style.RESET_ALL}"
            )
        except Exception as e:
            logger.error(f"Failed to register agent from {config_path}: {e}")

    logger.info(f"Starting server on http://{host}:{port}")
    click.echo(
        f"Server running at: {Fore.YELLOW}{Style.BRIGHT}http://{host}:{port}{Style.RESET_ALL}"
    )
    server.start()


@cli.command()
@click.option(
    "--output", "-o", default=None, help="Output file path for the agent config"
)
def create_agent(output):
    """Create a new agent configuration file by answering prompts."""
    try:
        colorama.init()
    except ImportError:
        # Fallback if colorama is not installed
        class DummyFore:
            def __getattr__(self, _):
                return ""

        class DummyStyle:
            def __getattr__(self, _):
                return ""

        global Fore, Style
        Fore = DummyFore()
        Style = DummyStyle()

    click.echo(
        f"{Fore.GREEN}===== Creating New Agent Configuration ====={Style.RESET_ALL}"
    )

    # Collect basic information
    name = click.prompt(f"{Fore.CYAN}Agent name{Style.RESET_ALL}")
    description = click.prompt(f"{Fore.CYAN}Agent description{Style.RESET_ALL}")
    version = click.prompt(
        f"{Fore.CYAN}Agent version{Style.RESET_ALL}", default="1.0.0"
    )

    # Capabilities
    streaming = click.confirm(
        f"{Fore.CYAN}Enable streaming capability?{Style.RESET_ALL}", default=True
    )

    # Skills
    skills = []
    click.echo(f"{Fore.YELLOW}Now let's define the agent's skills:{Style.RESET_ALL}")

    while True:
        if skills and not click.confirm(
            f"{Fore.YELLOW}Add another skill?{Style.RESET_ALL}", default=False
        ):
            break

        skill_id = click.prompt(f"{Fore.CYAN}Skill ID{Style.RESET_ALL}")
        skill_name = click.prompt(f"{Fore.CYAN}Skill name{Style.RESET_ALL}")
        skill_description = click.prompt(
            f"{Fore.CYAN}Skill description{Style.RESET_ALL}"
        )

        # Tags
        tags = []
        click.echo(f"{Fore.BLUE}Enter tags (empty line to finish):{Style.RESET_ALL}")
        while True:
            tag = click.prompt(f"{Fore.BLUE}Tag{Style.RESET_ALL}", default="")
            if not tag:
                break
            tags.append(tag)

        # Examples
        examples = []
        click.echo(
            f"{Fore.BLUE}Enter example queries (empty line to finish):{Style.RESET_ALL}"
        )
        while True:
            example = click.prompt(f"{Fore.BLUE}Example{Style.RESET_ALL}", default="")
            if not example:
                break
            examples.append(example)

        skill = {
            "id": skill_id,
            "name": skill_name,
            "description": skill_description,
            "tags": tags,
            "examples": examples,
            "inputModes": ["text"],
            "outputModes": ["text"],
        }

        skills.append(skill)

    # Prompt
    click.echo(f"{Fore.YELLOW}Enter the system prompt for your agent:{Style.RESET_ALL}")
    prompt = click.edit(text="You are an agent. Your job is to...\n")

    # MCP Servers
    mcp_servers = []
    if click.confirm(
        f"{Fore.YELLOW}Would you like to configure MCP servers?{Style.RESET_ALL}",
        default=False,
    ):
        while True:
            server_name = click.prompt(f"{Fore.CYAN}Server name{Style.RESET_ALL}")
            server_url = click.prompt(f"{Fore.CYAN}Server URL{Style.RESET_ALL}")
            server_transport = click.prompt(
                f"{Fore.CYAN}Transport type{Style.RESET_ALL}",
                type=click.Choice(["sse", "websocket", "http"], case_sensitive=False),
                default="sse",
            )

            mcp_servers.append(
                {"name": server_name, "url": server_url, "transport": server_transport}
            )

            if not click.confirm(
                f"{Fore.YELLOW}Add another MCP server?{Style.RESET_ALL}", default=False
            ):
                break

    # Create the config dictionary
    config = {
        "name": name,
        "description": description,
        "version": version,
        "capabilities": {"streaming": streaming},
        "skills": skills,
        "prompt": prompt,
    }

    if mcp_servers:
        config["mcpServers"] = mcp_servers

    # Determine output file path
    if not output:
        output = f"agent-{name.lower().replace(' ', '-')}.yml"
        if not output.endswith(".yml"):
            output += ".yml"

    # Save to file
    output_path = os.path.abspath(output)
    with open(output_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    click.echo(
        f"{Fore.GREEN}Agent configuration saved to: {output_path}{Style.RESET_ALL}"
    )


@cli.command()
@click.argument("name", required=True)
@click.option("--host", default="localhost", help="Host to run the server on")
@click.option("--port", default=10002, help="Port to run the server on")
def run_sample(name, host, port):
    """Run a sample agent by name. Looks for <name>.yml in configs folder."""
    try:
        # Get the package directory using importlib.resources
        pkg_path = pathlib.Path(importlib.resources.files("ephor_cli"))
        config_path = pkg_path / "configs" / f"{name}.yml"

        if not config_path.exists():
            logger.error(f"Sample agent config not found: {config_path}")
            click.echo(
                f"{Fore.RED}Error: Sample agent '{name}' not found in configs folder{Style.RESET_ALL}"
            )
            sys.exit(1)

        server = A2AProxyServer(host=host, port=port)

        logger.info(f"Loading sample agent config from {config_path}")
        agent_config = load_agent_config(str(config_path))
        agent_card, agent_id = create_agent_card(agent_config, host, port)

        agent = Agent(prompt=agent_config.prompt, mcpServers=agent_config.mcpServers)

        # Create task manager with tool config if available
        task_manager = AgentTaskManager(agent)

        # Register the agent
        server.register_agent(
            agent_id=agent_id, agent_card=agent_card, task_manager=task_manager
        )
        logger.info(
            f"Registered sample agent '{agent_card.name}' with ID: {agent_id}, URL: http://{host}:{port}/{agent_id}"
        )
        # Print colorful URL for better visibility
        click.echo(
            f"Agent '{agent_card.name}' available at: {Fore.CYAN}{Style.BRIGHT}http://{host}:{port}/{agent_id}{Style.RESET_ALL}"
        )
    except Exception as e:
        logger.error(f"Failed to register sample agent: {e}")
        click.echo(
            f"{Fore.RED}Error: Failed to register sample agent: {e}{Style.RESET_ALL}"
        )
        sys.exit(1)

    logger.info(f"Starting server on http://{host}:{port}")
    click.echo(
        f"Server running at: {Fore.YELLOW}{Style.BRIGHT}http://{host}:{port}{Style.RESET_ALL}"
    )
    server.start()


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to run the server on")
@click.option("--port", default=12000, help="Port to run the server on")
def start_conversation_server(host, port):
    """Start the Conversation Server for agent interactions."""
    click.echo(
        f"{Fore.GREEN}Starting Conversation Server on http://{host}:{port}{Style.RESET_ALL}"
    )

    # Create FastAPI app and router
    app = FastAPI()

    # Add CORS middleware to allow all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    router = APIRouter()

    # Initialize the conversation server with the router
    ConversationServer(router)

    # Include the router in the app
    app.include_router(router)

    # Start the server
    import uvicorn

    uvicorn.run(
        app,
        host=host,
        port=port,
        timeout_graceful_shutdown=0,
    )


@cli.command()
def version():
    """Print the current version of the Ephor CLI."""
    click.echo(f"Ephor CLI version: {__version__}")


def main():
    cli()


if __name__ == "__main__":
    main()

# A2A Proxy Server

A proxy server for Google's A2A (Agent-to-Agent) protocol.

## Installation

This package requires a two-step installation:

1. First, install the Google A2A package from GitHub:

   ```
   uv pip install git+https://github.com/djsamseng/A2A.git@prefixPythonPackage#subdirectory=samples/python
   ```

   or using pip:

   ```
   pip install git+https://github.com/djsamseng/A2A.git@prefixPythonPackage#subdirectory=samples/python
   ```

2. Then, install the a2a-proxy-server package:
   ```
   uv pip install a2a-proxy-server
   ```
   or using pip:
   ```
   pip install a2a-proxy-server
   ```

## Usage

The ephor-cli provides several commands:

```bash
# Show available commands
ephor-cli --help

# Start the A2A proxy server with agents
ephor-cli up --config path/to/agent-config.yml

# Create a new agent configuration file
ephor-cli create-agent --output my-agent.yml
```

### Starting the server

Before starting the A2A proxy server, make sure to set your ANTHROPIC_API_KEY environment variable:

```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

To start the A2A proxy server with one or more agent configurations:

```bash
ephor-cli up -c configs/sample-agent.yml -c configs/another-agent.yml
```

### Creating a new agent

The interactive agent creation wizard helps you configure a new agent:

```bash
ephor-cli create-agent -o configs/custom-agent.yml
```

This will guide you through creating a new agent configuration with colored prompts.

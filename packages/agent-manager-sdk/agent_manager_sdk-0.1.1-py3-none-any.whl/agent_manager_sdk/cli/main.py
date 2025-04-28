import datetime
import json
import os
import sys
import traceback
import uuid

import click
import requests
import yaml
from click import style

# --- Templates for server.py, requirements.txt, Dockerfile ---
TEMPLATE_SERVER_PY = """\
import logging
import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from agent_manager_sdk import (
    Account,
    Chat,
    User,
    Workflow,
    WorkflowNodeExecution,
    WorkflowRun,
    init_celery,
    init_db,
)

load_dotenv()
migrate = Migrate()

def initialize_extensions(app):
    db = init_db(app)
    migrate.init_app(app, db)
    init_celery(app)

def register_blueprints(app):
    from agent_manager_sdk.controllers.console import bp as console_app_bp
    app.register_blueprint(console_app_bp)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/dnd_game.db'
    app.config['SQLALCHEMY_BINDS'] = {
        'dnd_db': 'sqlite:///db/dnd_game.db',
    }
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', 6379)
    app.config.from_mapping(
        CELERY=dict(
            broker_url=f"redis://{redis_host}:{redis_port}/0",
            result_backend=f"redis://{redis_host}:{redis_port}/0",
            task_ignore_result=True
        )
    )
    CORS(app, allow_headers=['Content-Type', 'Authorization', 'ngrok-skip-browser-warning'],
         resources={r"/*": {"origins": "*"}},
         methods=['GET', 'PUT', 'POST', 'DELETE', 'OPTIONS', 'PATCH'])
    register_blueprints(app)
    initialize_extensions(app)
    return app

flask_app = create_app()

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
"""

TEMPLATE_REQUIREMENTS_TXT = """\
agent_manager_sdk
"""

TEMPLATE_DOCKERFILE = """\
FROM python:3.10-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ -r requirements.txt

EXPOSE 5000

CMD ["python", "server.py"]
"""

SAMPLE_WORKFLOW = {
    "workflow_id": "0",
    "user_id": "1",
    "workflow_name": "Content Generator",
    "description": "Generates a short content based on the input text",
    "graph": {
        "nodes": [
            {
                "id": "1",
                "type": "custom",
                "data": {
                    "type": "start",
                    "title": "Start",
                    "desc": "",
                    "variables": [
                        {
                            "variable": "text",
                            "type": "text-input",
                            "required": True
                        }
                    ]
                }
            },
            {
                "id": "2",
                "data": {
                    "type": "llm",
                    "title": "LLM",
                    "desc": "",
                    "system": "You are a helpful AI assistant.",
                    "user": "Create html code following the instructions: {text}",
                    "assistant": "",
                    "output_key": "html"
                }
            }
        ],
        "edges": [
            {
                "source": "1",
                "target": "2",
                "data": {
                    "sourceType": "start",
                    "targetType": "llm"
                }
            }
        ]
    },
    "output_keys": ["html"]
}

# --- CLI Setup ---
@click.group()
def cli():
    """Agent Package Manager (APM)"""
    pass

@cli.command()
def init():
    """Initialize a new workflow project"""
    project_dir = "apm"

    # 🎨 Pretty print initialization start
    click.echo(style("\n╔════════════════════════════════════════════╗", fg="green"))
    click.echo(style("║      Initializing Agent Package Manager     ║", fg="green"))
    click.echo(style("╚════════════════════════════════════════════╝\n", fg="green"))

    if os.path.exists(project_dir):
        click.echo(style(f"Project directory '{project_dir}' already exists! Aborting.\n", fg="red"))
        return

    # Step 1: Create project structure
    os.makedirs(project_dir)
    os.makedirs(os.path.join(project_dir, "db"), exist_ok=True)
    with open(os.path.join(project_dir, "server.py"), "w") as f:
        f.write(TEMPLATE_SERVER_PY)
    with open(os.path.join(project_dir, "requirements.txt"), "w") as f:
        f.write(TEMPLATE_REQUIREMENTS_TXT)
    with open(os.path.join(project_dir, "Dockerfile"), "w") as f:
        f.write(TEMPLATE_DOCKERFILE)

    # Step 2: Touch empty db file
    db_file = os.path.join(project_dir, "db", "dnd_game.db")
    open(db_file, "a").close()

    # Step 3: Run migrations
    click.echo(style("Running database migrations...\n", fg="yellow"))
    try:
        os.chdir("apm")  # move inside project folder
        sys.path.insert(0, os.getcwd())
        os.environ["FLASK_APP"] = "server.py"
        os.environ["FLASK_ENV"] = "development"
        
        from flask_migrate import init as flask_migrate_init
        from flask_migrate import migrate as flask_migrate_migrate
        from flask_migrate import upgrade as flask_migrate_upgrade

        from server import flask_app

        with flask_app.app_context():
            migrations_dir = os.path.join(os.getcwd(), "migrations")
            if not os.path.exists(migrations_dir):
                flask_migrate_init()

            flask_migrate_migrate()
            flask_migrate_upgrade()

        click.echo(style("\nDatabase migrations applied successfully.\n", fg="green"))

    except Exception as e:
        click.echo(style("\nMigration failed:", fg="red"))
        click.echo(traceback.format_exc())
        return

    # 🎨 Pretty print initialization complete
    click.echo(style("\n╔════════════════════════════════════════════╗", fg="green"))
    click.echo(style("║      Project initialized successfully!      ║", fg="green"))
    click.echo(style("╚════════════════════════════════════════════╝\n", fg="green"))

    click.echo(style(
        "You are ready to build and run agents!\n"
        "This project was created by:\n"
        "\n"
        "  Aum Javalgikar\n"
        "  Amey Chavan\n"
        "  Mahesh Kadam\n"
        "\n"
        "As part of their SPPU Final Year Project (2025)\n"
        "\n"
        "© 2025 Aum, Amey, Mahesh. All rights reserved.\n",
        fg="bright_green"
    ))

    click.echo(style(f"Project directory: ./{project_dir}\n", fg="cyan"))

@cli.command()
def init_agent():
    """Initialize a new agent"""
    click.echo(style("\n╔════════════════════════════════════╗", fg="green"))
    click.echo(style("║        Initializing New Agent       ║", fg="green"))
    click.echo(style("╚════════════════════════════════════╝\n", fg="green"))
    
    if not os.path.exists("server.py"):
        click.echo(style("Error: 'server.py' not found in the current directory. Please run this command from your project root.\n", fg="red"))
        return

    agent_name = click.prompt("Enter agent name", type=str)
    description = click.prompt("Enter agent description", type=str)
    created_by = click.prompt("Enter created by (your username)", type=str)

    agent_dir = os.path.join("agents", agent_name)

    if os.path.exists(agent_dir):
        click.echo(style(f"Agent directory '{agent_dir}' already exists! Aborting.\n", fg="red"))
        return

    os.makedirs(os.path.join(agent_dir, "workflows"), exist_ok=True)

    agent_metadata = {
        "name": agent_name,
        "description": description,
        "created_by": created_by,
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "workflows": []
    }
    
    sample_path = os.path.join(agent_dir, 'workflows/sample.json')
    
    with open(sample_path, 'w') as f:
        f.write(json.dumps(SAMPLE_WORKFLOW))

    agent_yaml_path = os.path.join(agent_dir, ".agent")
    with open(agent_yaml_path, "w") as f:
        import yaml
        yaml.dump(agent_metadata, f, default_flow_style=False)

    click.echo(style(f"\nAgent '{agent_name}' initialized successfully at '{agent_dir}'\n", fg="cyan"))

@cli.command()
@click.argument('agent_name')
def agent_sync(agent_name):
    """Sync local workflows with the server"""

    agent_dir = os.path.join("agents", agent_name)
    agent_file = os.path.join(agent_dir, ".agent")
    workflows_dir = os.path.join(agent_dir, "workflows")

    # Check if agent exists
    if not os.path.exists(agent_file):
        click.echo(style(f"Error: Agent '{agent_name}' does not exist.\n", fg="red"))
        return

    # Check if server.py is present
    if not os.path.exists("server.py"):
        click.echo(style("Error: 'server.py' not found in the current directory. Please run this command from your project root.\n", fg="red"))
        return

    # Load .agent file
    with open(agent_file, "r") as f:
        agent_data = yaml.safe_load(f)

    # Find all workflow files
    workflow_files = [f for f in os.listdir(workflows_dir) if f.endswith(".json")]
    if not workflow_files:
        click.echo(style(f"No workflows found to sync in '{workflows_dir}'.\n", fg="yellow"))
        return

    server_url = "http://localhost:5000/miniapps/workflow"

    for wf_filename in workflow_files:
        wf_path = os.path.join(workflows_dir, wf_filename)
        with open(wf_path, "r") as f:
            workflow_json = json.load(f)

        workflow_id = workflow_json.get("workflow_id")
        if not workflow_id:
            click.echo(style(f"Skipping '{wf_filename}' - No workflow_id found.\n", fg="yellow"))
            continue

        # Check if workflow already exists (try fetching it)
        try:
            r = requests.get(f"{server_url}/{workflow_id}")
            exists = r.status_code == 200
        except Exception as e:
            click.echo(style(f"Error contacting server for '{wf_filename}': {str(e)}\n", fg="red"))
            continue

        # Decide POST or PATCH
        if exists:
            try:
                r = requests.patch(f"{server_url}/{workflow_id}", json=workflow_json)
                if r.ok:
                    click.echo(style(f"Updated workflow: {wf_filename}", fg="green"))
                    workflow_entry = next((w for w in agent_data.get("workflows", []) if w["name"] == wf_filename), None)
                    if not workflow_entry:
                        # New workflow entry
                        agent_data.setdefault("workflows", []).append({
                            "name": wf_filename,
                            "last_synced": datetime.datetime.utcnow().isoformat() + "Z"
                        })
                    else:
                        # Existing entry, just update last_synced
                        workflow_entry["last_synced"] = datetime.datetime.utcnow().isoformat() + "Z"
                else:
                    click.echo(style(f"Failed to update: {wf_filename}", fg="red"))
            except Exception as e:
                click.echo(style(f"Error updating '{wf_filename}': {str(e)}\n", fg="red"))
        else:
            try:
                r = requests.post(server_url, json=workflow_json)
                if r.ok:
                    click.echo(style(f"Uploaded new workflow: {wf_filename}", fg="cyan"))
                    workflow_entry = next((w for w in agent_data.get("workflows", []) if w["name"] == wf_filename), None)
                    if not workflow_entry:
                        # New workflow entry
                        agent_data.setdefault("workflows", []).append({
                            "name": wf_filename,
                            "last_synced": datetime.datetime.utcnow().isoformat() + "Z"
                        })
                    else:
                        # Existing entry, just update last_synced
                        workflow_entry["last_synced"] = datetime.datetime.utcnow().isoformat() + "Z"
                else:
                    click.echo(style(f"Failed to upload: {wf_filename}", fg="red"))
            except Exception as e:
                click.echo(style(f"Error uploading '{wf_filename}': {str(e)}\n", fg="red"))
    with open(agent_file, "w") as f:
        yaml.dump(agent_data, f, default_flow_style=False)
    click.echo(style(f"\nSync completed for agent '{agent_name}'.\n", fg="bright_green"))

@cli.command()
@click.argument('agent_name')
@click.argument('workflow_name')
def agent_run(agent_name, workflow_name):
    """Run a workflow from an agent"""

    agent_dir = os.path.join("agents", agent_name)
    workflow_file = os.path.join(agent_dir, "workflows", f"{workflow_name}.json")

    # Check if agent and workflow exist
    if not os.path.exists(workflow_file):
        click.echo(style(f"Error: Workflow '{workflow_name}' not found for agent '{agent_name}'.\n", fg="red"))
        return

    # Check server.py
    if not os.path.exists("server.py"):
        click.echo(style("Error: 'server.py' not found in the current directory. Please run this command from your project root.\n", fg="red"))
        return

    # Load workflow JSON
    with open(workflow_file, "r") as f:
        workflow_json = json.load(f)

    workflow_id = workflow_json.get("workflow_id")
    if not workflow_id:
        click.echo(style(f"Error: No workflow_id found in '{workflow_name}'.\n", fg="red"))
        return

    # Find start node
    start_node = next((node for node in workflow_json.get("graph", {}).get("nodes", []) if node["data"].get("type") == "start"), None)
    if not start_node:
        click.echo(style(f"Error: No start node found in workflow.\n", fg="red"))
        return

    # Prompt for variables
    inputs = {}
    for var in start_node["data"].get("variables", []):
        var_name = var.get("variable")
        if var_name:
            value = click.prompt(f"Enter value for '{var_name}'", type=str)
            inputs[var_name] = value

    # Prepare payload
    payload = {
        "workflow_id": workflow_id,
        "user_id": "1",  # Hardcoded user_id for now; can be prompted later
        "inputs": inputs
    }

    # Send run request
    server_url = "http://localhost:5000/miniapps/workflow/run"
    try:
        r = requests.post(server_url, json=payload)
        if r.ok:
            click.echo(style("\nWorkflow Run Result:", fg="bright_green"))
            click.echo(json.dumps(r.json(), indent=2))
        else:
            click.echo(style(f"Workflow run failed: {r.text}", fg="red"))
    except Exception as e:
        click.echo(style(f"Error contacting server: {str(e)}\n", fg="red"))


@cli.command()
@click.argument('agent_name')
def publish(agent_name):
    """Publish an agent and its workflows to the central server"""

    agent_dir = os.path.join("agents", agent_name)
    agent_file = os.path.join(agent_dir, ".agent")
    workflows_dir = os.path.join(agent_dir, "workflows")

    # Validate agent exists
    if not os.path.exists(agent_file):
        click.echo(style(f"Error: Agent '{agent_name}' does not exist.\n", fg="red"))
        return

    if not os.path.exists(workflows_dir) or not os.listdir(workflows_dir):
        click.echo(style(f"Error: No workflows found in '{workflows_dir}'. Cannot publish empty agent.\n", fg="red"))
        return

    # Load agent metadata
    with open(agent_file, "r") as f:
        agent_data = yaml.safe_load(f)

    # Load workflows
    workflow_files = [f for f in os.listdir(workflows_dir) if f.endswith(".json")]
    workflows = []
    for wf_filename in workflow_files:
        wf_path = os.path.join(workflows_dir, wf_filename)
        with open(wf_path, "r") as f:
            workflow_data = json.load(f)
            workflow_data["workflow_id"] = f"{wf_filename.replace('.json', '')}_{str(uuid.uuid4())}"
            workflows.append(workflow_data)

    # Prepare upload payload
    payload = {
        "agent": {
            "name": agent_data.get("name"),
            "description": agent_data.get("description"),
            "created_by": agent_data.get("created_by"),
            "created_at": agent_data.get("created_at"),
            "version": agent_data.get("version", "v1.0")
        },
        "workflows": workflows
    }

    # Central server URL
    server_url = "https://funky-open-wahoo.ngrok-free.app/miniapps/agents"

    headers = {
        "Content-Type": "application/json"
    }

    try:
        r = requests.post(server_url, json=payload, headers=headers)
        if r.ok:
            response_data = r.json()
            click.echo(style("\nAgent published successfully!", fg="bright_green"))
            click.echo(f"Agent ID: {response_data.get('agent_id')}")
        else:
            click.echo(style(f"Failed to publish agent: {r.status_code} {r.text}", fg="red"))
    except Exception as e:
        click.echo(style(f"Error contacting central server: {str(e)}\n", fg="red"))

@cli.command()
@click.option('--agent_id', type=str, required=False, help='Filter by agent ID')
@click.option('--user_id', type=str, required=False, help='Filter by user ID')
def agents(agent_id, user_id):
    """Fetch and view all agents and workflows from the central server"""
    import pydoc

    import requests
    import yaml
    from tabulate import tabulate

    # Prepare request
    server_url = "https://funky-open-wahoo.ngrok-free.app/miniapps/agents"
    params = {}
    if agent_id:
        params['agent_id'] = agent_id
    if user_id:
        params['user_id'] = user_id

    headers = {
        "Content-Type": "application/json"
    }

    try:
        r = requests.get(server_url, params=params, headers=headers)
        if not r.ok:
            click.echo(style(f"Failed to fetch agents: {r.status_code} {r.text}", fg="red"))
            return
        response_data = r.json()
    except Exception as e:
        click.echo(style(f"Error contacting server: {str(e)}\n", fg="red"))
        return

    agents = response_data.get("agents", [])
    if not agents:
        click.echo(style("No agents found.\n", fg="yellow"))
        return

    # Build table
    table = []
    for agent in agents:
        table.append([
            agent.get("id", ""),
            agent.get("name", ""),
            agent.get("description", ""),
            agent.get("user_id", ""),
            agent.get("created_at", ""),
            len(agent.get("workflows", []))  # show number of workflows
        ])

    headers = ["Agent ID", "Name", "Description", "User ID", "Created At", "# Workflows"]
    formatted_table = tabulate(table, headers, tablefmt="grid")

    # Show in scrollable pager
    pydoc.pager(formatted_table)

@cli.command()
@click.argument('agent_id')
def pull(agent_id):
    """Pull an agent from the master registry and recreate locally"""

    # Fetch from server
    server_url = "https://funky-open-wahoo.ngrok-free.app/miniapps/agents"
    params = {"agent_id": agent_id}
    headers = {
        "Content-Type": "application/json"
    }

    try:
        r = requests.get(server_url, params=params, headers=headers)
        if not r.ok:
            click.echo(style(f"Failed to pull agent: {r.status_code} {r.text}", fg="red"))
            return
        response_data = r.json()
    except Exception as e:
        click.echo(style(f"Error contacting server: {str(e)}\n", fg="red"))
        return

    agents = response_data.get("agents", [])
    if not agents:
        click.echo(style(f"No agent found with ID '{agent_id}'\n", fg="yellow"))
        return

    agent = agents[0]  # Only one agent returned for agent_id

    # Build local directories
    agent_name = agent.get("name")
    agent_dir = os.path.join("agents", agent_name)
    workflows_dir = os.path.join(agent_dir, "workflows")

    if os.path.exists(agent_dir):
        click.echo(style(f"Agent directory '{agent_dir}' already exists! Aborting to avoid overwriting.\n", fg="red"))
        return

    os.makedirs(workflows_dir, exist_ok=True)

    # Save .agent YAML
    agent_metadata = {
        "name": agent.get("name"),
        "description": agent.get("description"),
        "created_by": agent.get("user_id"),
        "created_at": agent.get("created_at"),
        "version": agent.get("version", "v1.0"),
        "workflows": []
    }

    agent_yaml_path = os.path.join(agent_dir, ".agent")
    with open(agent_yaml_path, "w") as f:
        yaml.dump(agent_metadata, f, default_flow_style=False)

    # Save each workflow JSON
    for wf in agent.get("workflows", []):
        wf_filename = f"{wf.get("id").split("_")[0]}.json"
        wf_path = os.path.join(workflows_dir, wf_filename)

        wf_data = {
            "workflow_id": wf.get("id").split("_")[0],
            "user_id": agent.get("user_id"),
            "graph": wf.get("graph"),
            "output_keys": wf.get("output_keys"),
            "version": wf.get("version")
        }

        with open(wf_path, "w") as f:
            json.dump(wf_data, f, indent=2)

    click.echo(style(f"\nAgent '{agent_name}' pulled successfully and created at '{agent_dir}'", fg="bright_green"))
    click.echo(style(f"You can now run 'apm agent-sync {agent_name}' to add it to your local DB.\n", fg="cyan"))


if __name__ == "__main__":
    cli()

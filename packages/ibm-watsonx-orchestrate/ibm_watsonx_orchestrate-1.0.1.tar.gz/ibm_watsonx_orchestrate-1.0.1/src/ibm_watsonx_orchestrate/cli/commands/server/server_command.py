import logging
import sys
import subprocess
import tempfile
from pathlib import Path
import requests
import time
import os
import platform


import typer
import importlib.resources as resources
import jwt

from dotenv import dotenv_values, load_dotenv

from ibm_watsonx_orchestrate.client.agents.agent_client import AgentClient
from ibm_watsonx_orchestrate.client.analytics.llm.analytics_llm_client import AnalyticsLLMClient, AnalyticsLLMConfig, \
    AnalyticsLLMUpsertToolIdentifier
from ibm_watsonx_orchestrate.client.utils import instantiate_client, check_token_validity, is_local_dev

from ibm_watsonx_orchestrate.cli.commands.environment.environment_controller import _login, _decode_token
from ibm_watsonx_orchestrate.cli.config import PROTECTED_ENV_NAME, clear_protected_env_credentials_token, Config, \
    AUTH_CONFIG_FILE_FOLDER, AUTH_CONFIG_FILE, AUTH_MCSP_TOKEN_OPT, ENVIRONMENTS_SECTION_HEADER, ENV_WXO_URL_OPT, \
    CONTEXT_SECTION_HEADER, CONTEXT_ACTIVE_ENV_OPT, AUTH_SECTION_HEADER
from dotenv import dotenv_values, load_dotenv

logger = logging.getLogger(__name__)

server_app = typer.Typer(no_args_is_help=True)


def ensure_docker_installed() -> None:
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        logger.error("Unable to find an installed docker")
        sys.exit(1)

def ensure_docker_compose_installed() -> list:
    try:
        subprocess.run(["docker", "compose", "version"], check=True, capture_output=True)
        return ["docker", "compose"]
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    try:
        subprocess.run(["docker-compose", "version"], check=True, capture_output=True)
        return ["docker-compose"]
    except (FileNotFoundError, subprocess.CalledProcessError):
        typer.echo("Unable to find an installed docker-compose or docker compose")
        sys.exit(1)

def docker_login(iam_api_key: str, registry_url: str) -> None:
    logger.info(f"Logging into Docker registry: {registry_url} ...")
    result = subprocess.run(
        ["docker", "login", "-u", "iamapikey", "--password-stdin", registry_url],
        input=iam_api_key.encode("utf-8"),
        capture_output=True,
    )
    if result.returncode != 0:
        logger.error(f"Error logging into Docker:\n{result.stderr.decode('utf-8')}")
        sys.exit(1)
    logger.info("Successfully logged in to Docker.")


def get_compose_file() -> Path:
    with resources.as_file(
        resources.files("ibm_watsonx_orchestrate.docker").joinpath("compose-lite.yml")
    ) as compose_file:
        return compose_file


def get_default_env_file() -> Path:
    with resources.as_file(
        resources.files("ibm_watsonx_orchestrate.docker").joinpath("default.env")
    ) as env_file:
        return env_file


def read_env_file(env_path: Path|str) -> dict:
    return dotenv_values(str(env_path))

def merge_env(
    default_env_path: Path,
    user_env_path: Path | None
) -> dict:

    merged = dotenv_values(str(default_env_path))

    if user_env_path is not None:
        user_env = dotenv_values(str(user_env_path))
        merged.update(user_env)


    return merged


def apply_llm_api_key_defaults(env_dict: dict) -> None:
    llm_value = env_dict.get("WATSONX_APIKEY")
    if llm_value:
        env_dict.setdefault("ASSISTANT_LLM_API_KEY", llm_value)
        env_dict.setdefault("ASSISTANT_EMBEDDINGS_API_KEY", llm_value)
        env_dict.setdefault("ROUTING_LLM_API_KEY", llm_value)
        env_dict.setdefault("BAM_API_KEY", llm_value)
        env_dict.setdefault("WXAI_API_KEY", llm_value)
    space_value = env_dict.get("WATSONX_SPACE_ID")
    if space_value:
        env_dict.setdefault("ASSISTANT_LLM_SPACE_ID", space_value)
        env_dict.setdefault("ASSISTANT_EMBEDDINGS_SPACE_ID", space_value)
        env_dict.setdefault("ROUTING_LLM_SPACE_ID", space_value)

def write_merged_env_file(merged_env: dict) -> Path:
    tmp = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".env")
    with tmp:
        for key, val in merged_env.items():
            tmp.write(f"{key}={val}\n")
    return Path(tmp.name)


def get_dbtag_from_architecture(merged_env_dict: dict) -> str:
    """Detects system architecture and returns the corresponding DBTAG."""
    arch = platform.machine()

    arm64_tag = merged_env_dict.get("ARM64DBTAG")
    amd_tag = merged_env_dict.get("AMDDBTAG")

    if arch in ["aarch64", "arm64"]:
        return arm64_tag
    else:
        return amd_tag

def refresh_local_credentials() -> None:
    """
    Refresh the local credentials
    """
    clear_protected_env_credentials_token()
    _login(name=PROTECTED_ENV_NAME, apikey=None)



def run_compose_lite(final_env_file: Path, experimental_with_langfuse=False, with_flow_runtime=False) -> None:
    compose_path = get_compose_file()
    compose_command = ensure_docker_compose_installed()
    db_tag = read_env_file(final_env_file).get('DBTAG', None)
    logger.info(f"Detected architecture: {platform.machine()}, using DBTAG: {db_tag}")

    # Step 1: Start only the DB container
    db_command = compose_command + [
        "-f", str(compose_path),
        "--env-file", str(final_env_file),
        "up",
        "-d",
        "--remove-orphans",
        "wxo-server-db"
    ]

    logger.info("Starting database container...")
    result = subprocess.run(db_command, env=os.environ, capture_output=False)

    if result.returncode != 0:
        logger.error(f"Error starting DB container: {result.stderr}")
        sys.exit(1)

    logger.info("Database container started successfully. Now starting other services...")


    # Step 2: Start all remaining services (except DB)
    if experimental_with_langfuse:
        command = compose_command + [
            '--profile',
            'langfuse'
        ]
    else:
        command = compose_command

    # Check if we start the server with tempus-runtime.
    if with_flow_runtime:
        command += ['--profile', 'with-tempus-runtime']

    command += [
        "-f", str(compose_path),
        "--env-file", str(final_env_file),
        "up",
        "--scale",
        "ui=0",
        "-d",
        "--remove-orphans",
    ]

    logger.info("Starting docker-compose services...")
    result = subprocess.run(command, capture_output=False)

    if result.returncode == 0:
        logger.info("Services started successfully.")
        # Remove the temp file if successful
        if final_env_file.exists():
            final_env_file.unlink()
    else:
        error_message = result.stderr.decode('utf-8') if result.stderr else "Error occurred."
        logger.error(
            f"Error running docker-compose (temporary env file left at {final_env_file}):\n{error_message}"
        )
        sys.exit(1)

def wait_for_wxo_server_health_check(health_user, health_pass, timeout_seconds=90, interval_seconds=2):
    url = "http://localhost:4321/api/v1/auth/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': health_user,
        'password': health_pass
    }

    start_time = time.time()
    errormsg = None
    while time.time() - start_time <= timeout_seconds:
        try:
            response = requests.post(url, headers=headers, data=data)
            if 200 <= response.status_code < 300:
                return True
            else:
                logger.debug(f"Response code from healthcheck {response.status_code}")
        except requests.RequestException as e:
            errormsg = e
            #print(f"Request failed: {e}")

        time.sleep(interval_seconds)
    if errormsg:
        logger.error(f"Health check request failed: {errormsg}")
    return False

def wait_for_wxo_ui_health_check(timeout_seconds=45, interval_seconds=2):
    url = "http://localhost:3000/chat-lite"
    logger.info("Waiting for UI component to be initialized...")
    start_time = time.time()
    while time.time() - start_time <= timeout_seconds:
        try:
            response = requests.get(url)
            if 200 <= response.status_code < 300:
                return True
            else:
                pass
                #print(f"Response code from UI healthcheck {response.status_code}")
        except requests.RequestException as e:
            pass
            #print(f"Request failed for UI: {e}")

        time.sleep(interval_seconds)
    logger.info("UI component is initialized")
    return False

def run_compose_lite_ui(user_env_file: Path) -> bool:
    compose_path = get_compose_file()
    compose_command = ensure_docker_compose_installed()
    ensure_docker_installed()
    default_env_path = get_default_env_file()
    logger.debug(f"user env file: {user_env_file}")
    merged_env_dict = merge_env(
        default_env_path,
        user_env_file if user_env_file else None
    )

    _login(name=PROTECTED_ENV_NAME)
    auth_cfg = Config(AUTH_CONFIG_FILE_FOLDER, AUTH_CONFIG_FILE)
    existing_auth_config = auth_cfg.get(AUTH_SECTION_HEADER).get(PROTECTED_ENV_NAME, {})
    existing_token = existing_auth_config.get(AUTH_MCSP_TOKEN_OPT) if existing_auth_config else None
    token = jwt.decode(existing_token, options={"verify_signature": False})
    tenant_id = token.get('woTenantId', None)
    merged_env_dict['REACT_APP_TENANT_ID'] = tenant_id


    registry_url = merged_env_dict.get("REGISTRY_URL")
    if not registry_url:
        logger.error("Error: REGISTRY_URL is required in the environment file.")
        sys.exit(1)

    agent_client = instantiate_client(AgentClient)
    agents = agent_client.get()
    if not agents:
        logger.error("No agents found for the current environment. Please create an agent before starting the chat.")
        sys.exit(1)

    iam_api_key = merged_env_dict.get("DOCKER_IAM_KEY")
    if iam_api_key:
        docker_login(iam_api_key, registry_url)

    #These are to removed warning and not used in UI component
    if not 'WATSONX_SPACE_ID' in merged_env_dict:
        merged_env_dict['WATSONX_SPACE_ID']='X'
    if not 'WATSONX_APIKEY' in merged_env_dict:
        merged_env_dict['WATSONX_APIKEY']='X'
    apply_llm_api_key_defaults(merged_env_dict)

    final_env_file = write_merged_env_file(merged_env_dict)

    logger.info("Waiting for orchestrate server to be fully started and ready...")

    health_check_timeout = int(merged_env_dict["HEALTH_TIMEOUT"]) if "HEALTH_TIMEOUT" in merged_env_dict else 120
    is_successful_server_healthcheck = wait_for_wxo_server_health_check(merged_env_dict['WXO_USER'], merged_env_dict['WXO_PASS'], timeout_seconds=health_check_timeout)
    if not is_successful_server_healthcheck:
        logger.error("Healthcheck failed orchestrate server.  Make sure you start the server components with `orchestrate server start` before trying to start the chat UI")
        return False

    command = compose_command + [
        "-f", str(compose_path),
        "--env-file", str(final_env_file),
        "up",
        "ui",
        "-d",
        "--remove-orphans"
    ]

    logger.info(f"Starting docker-compose UI service...")
    result = subprocess.run(command, capture_output=False)

    if result.returncode == 0:
        logger.info("Chat UI Service started successfully.")
        # Remove the temp file if successful
        if final_env_file.exists():
            final_env_file.unlink()
    else:
        error_message = result.stderr.decode('utf-8') if result.stderr else "Error occurred."
        logger.error(
            f"Error running docker-compose (temporary env file left at {final_env_file}):\n{error_message}"
        )
        return False
    
    is_successful_ui_healthcheck = wait_for_wxo_ui_health_check()
    if not is_successful_ui_healthcheck:
        logger.error("The Chat UI service did not initialize within the expected time.  Check the logs for any errors.")

    return True

def run_compose_lite_down_ui(user_env_file: Path, is_reset: bool = False) -> None:
    compose_path = get_compose_file()
    compose_command = ensure_docker_compose_installed()


    ensure_docker_installed()
    default_env_path = get_default_env_file()
    merged_env_dict = merge_env(
        default_env_path,
        user_env_file
    )
    merged_env_dict['WATSONX_SPACE_ID']='X'
    merged_env_dict['WATSONX_APIKEY']='X'
    apply_llm_api_key_defaults(merged_env_dict)
    final_env_file = write_merged_env_file(merged_env_dict)

    command = compose_command + [
        "-f", str(compose_path),
        "--env-file", str(final_env_file),
        "down",
        "ui"
    ]

    if is_reset:
        command.append("--volumes")
        logger.info("Stopping docker-compose UI service and resetting volumes...")
    else:
        logger.info("Stopping docker-compose UI service...")

    result = subprocess.run(command, capture_output=False)

    if result.returncode == 0:
        logger.info("UI service stopped successfully.")
        # Remove the temp file if successful
        if final_env_file.exists():
            final_env_file.unlink()
    else:
        error_message = result.stderr.decode('utf-8') if result.stderr else "Error occurred."
        logger.error(
            f"Error running docker-compose (temporary env file left at {final_env_file}):\n{error_message}"
        )
        sys.exit(1)

def run_compose_lite_down(final_env_file: Path, is_reset: bool = False) -> None:
    compose_path = get_compose_file()
    compose_command = ensure_docker_compose_installed()

    command = compose_command + [
        '--profile', '*',
        "-f", str(compose_path),
        "--env-file", str(final_env_file),
        "down"
    ]

    if is_reset:
        command.append("--volumes")
        logger.info("Stopping docker-compose services and resetting volumes...")
    else:
        logger.info("Stopping docker-compose services...")

    result = subprocess.run(command, capture_output=False)

    if result.returncode == 0:
        logger.info("Services stopped successfully.")
        # Remove the temp file if successful
        if final_env_file.exists():
            final_env_file.unlink()
    else:
        error_message = result.stderr.decode('utf-8') if result.stderr else "Error occurred."
        logger.error(
            f"Error running docker-compose (temporary env file left at {final_env_file}):\n{error_message}"
        )
        sys.exit(1)


def run_compose_lite_logs(final_env_file: Path, is_reset: bool = False) -> None:
    compose_path = get_compose_file()
    compose_command = ensure_docker_compose_installed()

    command = compose_command + [
        "-f", str(compose_path),
        "--env-file", str(final_env_file),
        "logs",
        "-f"
    ]

    logger.info("Docker Logs...")

    result = subprocess.run(command, capture_output=False)

    if result.returncode == 0:
        logger.info("End of docker logs")
        # Remove the temp file if successful
        if final_env_file.exists():
            final_env_file.unlink()
    else:
        error_message = result.stderr.decode('utf-8') if result.stderr else "Error occurred."
        logger.error(
            f"Error running docker-compose (temporary env file left at {final_env_file}):\n{error_message}"
        )
        sys.exit(1)

@server_app.command(name="start")
def server_start(
    user_env_file: str = typer.Option(
        None,
        "--env-file", '-e',
        help="Path to a .env file that overrides default.env. Then environment variables override both."
    ),
    experimental_with_langfuse: bool = typer.Option(
        False,
        '--with-langfuse', '-l',
        help=''
    ),
    with_flow_runtime: bool = typer.Option(
        False,
        '--with-tempus-runtime', '-f',
        help='Option to start server with tempus-runtime.',
        hidden=True
    )
):
    if user_env_file and not Path(user_env_file).exists():
        logger.error(f"Error: The specified environment file '{user_env_file}' does not exist.")
        sys.exit(1)
    ensure_docker_installed()

    default_env_path = get_default_env_file()

    merged_env_dict = merge_env(
        default_env_path,
        Path(user_env_file) if user_env_file else None
    )

    merged_env_dict['DBTAG'] = get_dbtag_from_architecture(merged_env_dict=merged_env_dict)

    iam_api_key = merged_env_dict.get("DOCKER_IAM_KEY")
    if not iam_api_key:
        logger.error("Error: DOCKER_IAM_KEY is required in the environment file.")
        sys.exit(1)

    registry_url = merged_env_dict.get("REGISTRY_URL")
    if not registry_url:
        logger.error("Error: REGISTRY_URL is required in the environment file.")
        sys.exit(1)

    docker_login(iam_api_key, registry_url)

    apply_llm_api_key_defaults(merged_env_dict)


    final_env_file = write_merged_env_file(merged_env_dict)
    run_compose_lite(final_env_file=final_env_file, experimental_with_langfuse=experimental_with_langfuse, with_flow_runtime=with_flow_runtime)

    run_db_migration()

    logger.info("Waiting for orchestrate server to be fully initialized and ready...")

    health_check_timeout = int(merged_env_dict["HEALTH_TIMEOUT"]) if "HEALTH_TIMEOUT" in merged_env_dict else (7 * 60)
    is_successful_server_healthcheck = wait_for_wxo_server_health_check(merged_env_dict['WXO_USER'], merged_env_dict['WXO_PASS'], timeout_seconds=health_check_timeout)
    if is_successful_server_healthcheck:
        logger.info("Orchestrate services initialized successfully")
    else:
        logger.error(
            "The server did not successfully start within the given timeout. This is either an indication that something "
            f"went wrong, or that the server simply did not start within {health_check_timeout} seconds. Please check the logs with "
            "`orchestrate server logs`, or consider increasing the timeout by adding `HEALTH_TIMEOUT=number-of-seconds` "
            "to your env file."
        )
        exit(1)

    try:
        refresh_local_credentials()
    except:
        logger.warning("Failed to refresh local credentials, please run `orchestrate env activate local`")

    logger.info(f"You can run `orchestrate env activate local` to set your environment or `orchestrate chat start` to start the UI service and begin chatting.")

    if with_flow_runtime:
        logger.info(f"Starting with flow runtime")

@server_app.command(name="stop")
def server_stop(
    user_env_file: str = typer.Option(
        None,
        "--env-file", '-e',
        help="Path to a .env file that overrides default.env. Then environment variables override both."
    )
):
    ensure_docker_installed()
    default_env_path = get_default_env_file()
    merged_env_dict = merge_env(
        default_env_path,
        Path(user_env_file) if user_env_file else None
    )
    merged_env_dict['WATSONX_SPACE_ID']='X'
    merged_env_dict['WATSONX_APIKEY']='X'
    apply_llm_api_key_defaults(merged_env_dict)
    final_env_file = write_merged_env_file(merged_env_dict)
    run_compose_lite_down(final_env_file=final_env_file)

@server_app.command(name="reset")
def server_reset(
    user_env_file: str = typer.Option(
        None,
        "--env-file", '-e',
        help="Path to a .env file that overrides default.env. Then environment variables override both."
    )
):
    
    ensure_docker_installed()
    default_env_path = get_default_env_file()
    merged_env_dict = merge_env(
        default_env_path,
        Path(user_env_file) if user_env_file else None
    )
    merged_env_dict['WATSONX_SPACE_ID']='X'
    merged_env_dict['WATSONX_APIKEY']='X'
    apply_llm_api_key_defaults(merged_env_dict)
    final_env_file = write_merged_env_file(merged_env_dict)
    run_compose_lite_down(final_env_file=final_env_file, is_reset=True)

@server_app.command(name="logs")
def server_logs(
    user_env_file: str = typer.Option(
        None,
        "--env-file", '-e',
        help="Path to a .env file that overrides default.env. Then environment variables override both."
    )
):
    ensure_docker_installed()
    default_env_path = get_default_env_file()
    merged_env_dict = merge_env(
        default_env_path,
        Path(user_env_file) if user_env_file else None
    )
    merged_env_dict['WATSONX_SPACE_ID']='X'
    merged_env_dict['WATSONX_APIKEY']='X'
    apply_llm_api_key_defaults(merged_env_dict)
    final_env_file = write_merged_env_file(merged_env_dict)
    run_compose_lite_logs(final_env_file=final_env_file)

def run_db_migration() -> None:
    compose_path = get_compose_file()
    compose_command = ensure_docker_compose_installed()

    command = compose_command + [
        "-f", str(compose_path),
        "exec",
        "wxo-server-db",
        "bash",
        "-c",
        '''
        APPLIED_MIGRATIONS_FILE="/var/lib/postgresql/applied_migrations/applied_migrations.txt"
        touch "$APPLIED_MIGRATIONS_FILE"

        for file in /docker-entrypoint-initdb.d/*.sql; do
            filename=$(basename "$file")

            if grep -Fxq "$filename" "$APPLIED_MIGRATIONS_FILE"; then
                echo "Skipping already applied migration: $filename"
            else
                echo "Applying migration: $filename"
                if psql -U postgres -d postgres -q -f "$file" > /dev/null 2>&1; then
                    echo "$filename" >> "$APPLIED_MIGRATIONS_FILE"
                else
                    echo "Error applying $filename. Stopping migrations."
                    exit 1
                fi
            fi
        done
        '''
    ]

    logger.info("Running Database Migration...")
    result = subprocess.run(command, capture_output=False)

    if result.returncode == 0:
        logger.info("Migration ran successfully.")
    else:
        error_message = result.stderr.decode('utf-8') if result.stderr else "Error occurred."
        logger.error(
            f"Error running database migration):\n{error_message}"
        )
        sys.exit(1)

if __name__ == "__main__":
    server_app()

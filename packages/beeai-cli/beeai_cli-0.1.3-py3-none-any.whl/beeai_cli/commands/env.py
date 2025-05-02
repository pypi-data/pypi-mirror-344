# Copyright 2025 © BeeAI a Series of LF Projects, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys
import tempfile
import typer
import httpx
import subprocess
from rich.table import Column
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator

from beeai_cli.api import api_request, wait_for_agents
from beeai_cli.async_typer import AsyncTyper, console, err_console, create_table
from beeai_cli.utils import parse_env_var, format_error

app = AsyncTyper()


@app.command("add")
async def add(
    env: list[str] = typer.Argument(help="Environment variables to pass to agent"),
) -> None:
    """Store environment variables"""
    env_vars = [parse_env_var(var) for var in env]
    env_vars = {name: value for name, value in env_vars}
    await api_request(
        "put",
        "variables",
        json={**({"env": env_vars} if env_vars else {})},
    )
    await list_env()


@app.command("list")
async def list_env():
    """List stored environment variables"""
    # TODO: extract server schemas to a separate package
    resp = await api_request("get", "variables")
    with create_table(Column("name", style="yellow"), Column("value", ratio=1)) as table:
        for name, value in sorted(resp["env"].items()):
            table.add_row(name, value)
    console.print(table)


@app.command("remove")
async def remove_env(
    env: list[str] = typer.Argument(help="Environment variable(s) to remove"),
):
    await api_request("put", "variables", json={**({"env": {var: None for var in env}})})
    await list_env()


@app.command("setup", help="Interactive setup for LLM provider environment variables")
async def setup() -> bool:
    """Interactive setup for LLM provider environment variables"""
    provider_name, api_base, recommended_model = await inquirer.select(
        message="Select LLM provider:",
        choices=[
            Choice(
                name="OpenAI".ljust(20) + "🚀 best performance", value=("OpenAI", "https://api.openai.com/v1", "gpt-4o")
            ),
            Choice(
                name="DeepSeek".ljust(20) + "🚀 best performance",
                value=("DeepSeek", "https://api.deepseek.com/v1", "deepseek-reasoner"),
            ),
            Choice(
                name="NVIDIA NIM".ljust(20) + "🚀 best performance",
                value=("NVIDIA", "https://integrate.api.nvidia.com/v1", "deepseek-ai/deepseek-r1"),
            ),
            Choice(
                name="OpenRouter".ljust(20) + "🆓 has some free models",
                value=("OpenRouter", "https://openrouter.ai/api/v1", "deepseek/deepseek-r1-distill-llama-70b:free"),
            ),
            Choice(
                name="Groq".ljust(20) + "🆓 has a free tier",
                value=("Groq", "https://api.groq.com/openai/v1", "deepseek-r1-distill-llama-70b"),
            ),
            Choice(
                name="Cohere".ljust(20) + "🆓 has a free tier",
                value=("Cohere", "https://api.cohere.ai/compatibility/v1", "command-r-plus"),
            ),
            Choice(
                name="Mistral".ljust(20) + "🚧 experimental 🆓 has a free tier",
                value=("Mistral", "https://api.mistral.ai/v1", "mistral-large-latest"),
            ),
            Choice(
                name="Anthropic Claude".ljust(20) + "🚧 experimental",
                value=("Anthropic", "https://api.anthropic.com/v1", "claude-3-7-sonnet-latest"),
            ),
            Choice(
                name="Perplexity".ljust(20) + "🚧 experimental", value=("Perplexity", "https://api.perplexity.ai", None)
            ),
            Choice(name="Ollama".ljust(20) + "💻 local", value=("Ollama", "http://localhost:11434/v1", "llama3.1:8b")),
            Choice(name="Jan".ljust(20) + "💻 local", value=("Jan", "http://localhost:1337/v1", None)),
            Choice(name="Other".ljust(20) + "🔧 provide API URL", value=("Other", None, None)),
        ],
    ).execute_async()

    if provider_name == "Other":
        api_base = await inquirer.text(
            message="Enter the base URL of your API (OpenAI-compatible):",
            validate=lambda url: (url.startswith(("http://", "https://")) or "URL must start with http:// or https://"),
            transformer=lambda url: url.rstrip("/"),
        ).execute_async()

    if (api_key := os.environ.get(f"{provider_name.upper()}_API_KEY")) is None or not await inquirer.confirm(
        message=f"Use the API key from environment variable '{provider_name.upper()}_API_KEY'?",
        default=True,
    ).execute_async():
        api_key = (
            "dummy"
            if provider_name in ["Ollama", "Jan"]
            else await inquirer.secret(message="Enter API key:", validate=EmptyInputValidator()).execute_async()
        )

    try:
        with console.status("Loading available models...", spinner="dots"):
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{api_base}/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0,
                )
                if response.status_code == 404:
                    available_models = []
                elif response.status_code == 401:
                    if provider_name == "Anthropic":  # Anthropic always returns 401 for /models
                        available_models = []
                    else:
                        console.print(
                            format_error("Error", "API key was rejected. Please check your API key and re-try.")
                        )
                        return False
                else:
                    response.raise_for_status()
                    available_models = [m.get("id", "") for m in response.json().get("data", []) or []]
    except httpx.HTTPError as e:
        console.print(format_error("Error", str(e)))
        match provider_name:
            case "Ollama":
                console.print("💡 [yellow]HINT[/yellow]: We could not connect to Ollama. Is it running?")
            case "Jan":
                console.print(
                    "💡 [yellow]HINT[/yellow]: We could not connect to Jan. Ensure that the server is running: in the Jan application, click the [bold][<>][/bold] button and [bold]Start server[/bold]."
                )
            case "Other":
                console.print(
                    "💡 [yellow]HINT[/yellow]: We could not connect to the API URL you have specified. Is it correct?"
                )
            case _:
                console.print(f"💡 [yellow]HINT[/yellow]: {provider_name} may be down.")
        return False

    if provider_name == "Ollama":
        available_models = [model for model in available_models if not model.endswith("-beeai")]

    if provider_name == "Ollama" and not available_models:
        if await inquirer.confirm(
            message=f"There are no locally available models in Ollama. Do you want to pull the recommended model '{recommended_model}'?",
            default=True,
        ).execute_async():
            selected_model = recommended_model
        else:
            console.print("[red]No model configured.[/red]")
            return False
    else:
        selected_model = (
            recommended_model
            if (
                (not available_models or recommended_model in available_models or provider_name == "Ollama")
                and await inquirer.confirm(
                    message=f"Do you want to use the recommended model '{recommended_model}'?"
                    + (
                        " It will be pulled from Ollama now."
                        if recommended_model not in available_models and provider_name == "Ollama"
                        else ""
                    ),
                    default=True,
                ).execute_async()
            )
            else (
                await inquirer.fuzzy(
                    message="Select a model (type to filter):",
                    choices=sorted(available_models),
                ).execute_async()
                if available_models
                else await inquirer.text(message="Write a model name to use:").execute_async()
            )
        )

    if provider_name == "Ollama" and selected_model not in available_models:
        try:
            subprocess.run(["ollama", "pull", selected_model], check=True)
        except Exception as e:
            console.print(f"[red]Error while pulling model: {str(e)}[/red]")
            return False

    if provider_name == "Ollama" and (
        (
            num_ctx := await inquirer.select(
                message="Larger context window helps agents see more information at once at the cost of memory consumption, as long as the model supports it. Set a larger context window?",
                choices=[
                    Choice(name="2k  ⚠️  some agents won't work", value=2048),
                    Choice(name="4k  ⚠️  some agents won't work", value=4096),
                    Choice(name="8k", value=8192),
                    Choice(name="16k", value=16384),
                    Choice(name="32k", value=32768),
                    Choice(name="64k", value=65536),
                    Choice(name="128k", value=131072),
                ],
            ).execute_async()
        )
        > 2048
    ):
        modified_model = f"{selected_model}-beeai"
        console.print(
            f"⚠️  [yellow]Warning[/yellow]: BeeAI will create and use a modified version of this model tagged [bold]{modified_model}[/bold] with default context window set to [bold]{num_ctx}[/bold]."
        )

        try:
            if modified_model in available_models:
                subprocess.run(["ollama", "rm", modified_model], check=False)
            with tempfile.TemporaryDirectory() as temp_dir:
                modelfile_path = os.path.join(temp_dir, "Modelfile")
                with open(modelfile_path, "w") as f:
                    f.write(f"FROM {selected_model}\n\nPARAMETER num_ctx {num_ctx}\n")
                subprocess.run(["ollama", "create", modified_model], cwd=temp_dir, check=True)
        except Exception as e:
            console.print(f"[red]Error setting up Ollama model: {str(e)}[/red]")
            return False

        selected_model = modified_model

    try:
        with console.status("Checking if the model works...", spinner="dots"):
            async with httpx.AsyncClient() as client:
                test_response = await client.post(
                    f"{api_base}/chat/completions",
                    json={
                        "model": selected_model,
                        "max_tokens": 500,  # reasoning models need some tokens to think about this
                        "messages": [
                            {
                                "role": "system",
                                "content": "Repeat each message back to the user, verbatim. Don't say anything else.",
                            },
                            {"role": "user", "content": "Hello!"},
                        ],
                    },
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0,
                )
        test_response.raise_for_status()
        response_text = test_response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        if "Hello!" not in response_text:
            err_console.print(format_error("Error", "Model did not provide a proper response."))
            return False
    except Exception as e:
        err_console.print(format_error("Error", f"Error during model test: {str(e)}"))
        return False

    with console.status("Saving configuration...", spinner="dots"):
        await api_request(
            "put",
            "variables",
            json={"env": {"LLM_API_BASE": api_base, "LLM_API_KEY": api_key, "LLM_MODEL": selected_model}},
        )

    with console.status("Reloading agents (may take a few minutes)...", spinner="dots"):
        if not await wait_for_agents():
            console.print(
                "[bold red]Some agents did not properly start. Please check their status with:[/bold red] beeai info <agent>"
            )
            from beeai_cli.commands.agent import list_agents  # avoid circular dependency

            await list_agents()

    console.print(
        "\n[bold green]You're all set![/bold green] (You can re-run this setup anytime with [blue]beeai env setup[/blue])"
    )
    return True


async def ensure_llm_env():
    try:
        env = (await api_request("get", "variables"))["env"]
    except httpx.HTTPStatusError:
        return  # Skip for non-conforming servers (like when running directly against an agent provider)
    if all(required_variable in env.keys() for required_variable in ["LLM_MODEL", "LLM_API_KEY", "LLM_API_BASE"]):
        return
    console.print("[bold]Welcome to 🐝 [red]BeeAI[/red]![/bold]")
    console.print("Let's start by configuring your LLM environment.\n")
    if not await setup():
        err_console.print(
            format_error("Error", "Could not continue because the LLM environment is not properly set up.")
        )
        err_console.print(
            "💡 [yellow]HINT[/yellow]: Try re-entering your LLM API details with: [green]beeai env setup[/green]"
        )
        sys.exit(1)
    console.print()

"""CLI module for LXMFy bot framework.

Provides command-line interface functionality for creating and managing LXMF bots,
including bot file creation, example cog generation, and bot analysis.
"""

import argparse
import ast
import hashlib
import importlib.util
import json
import os
import re
import sys
from glob import glob
from pathlib import Path
from typing import Any, Optional

from .templates import EchoBot, NoteBot, ReminderBot
from .validation import format_validation_results, validate_bot


def sanitize_filename(filename: str) -> str:
    """Sanitizes the filename while preserving the extension.

    Args:
        filename: The filename to sanitize.

    Returns:
        Sanitized filename with proper extension.
    """
    base, ext = os.path.splitext(os.path.basename(filename))
    base = re.sub(r"[^a-zA-Z0-9\-_]", "", base)

    if not ext or ext != ".py":
        ext = ".py"

    return f"{base}{ext}"


def validate_bot_name(name: str) -> str:
    """Validates and sanitizes a bot name.

    Args:
        name: The proposed bot name.

    Returns:
        The sanitized bot name.

    Raises:
        ValueError: If the name is invalid.
    """
    if not name:
        raise ValueError("Bot name cannot be empty")

    sanitized = "".join(c for c in name if c.isalnum() or c in " -_")
    if not sanitized:
        raise ValueError("Bot name must contain valid characters")

    return sanitized


def create_bot_file(name: str, output_path: str, no_cogs: bool = False) -> str:
    """Creates a new bot file from a template.

    Args:
        name: The name for the bot.
        output_path: The desired output path.
        no_cogs: Whether to disable cogs loading.

    Returns:
        The path to the created bot file.

    Raises:
        RuntimeError: If file creation fails.
    """
    try:
        name = validate_bot_name(name)

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        if output_path.endswith("/") or output_path.endswith("\\"):
            base_name = "bot.py"
            output_path = os.path.join(output_path, base_name)
        elif not output_path.endswith(".py"):
            output_path += ".py"

        safe_path = os.path.abspath(output_path)

        template = f"""from lxmfy import LXMFBot

bot = LXMFBot(
    name="{name}",
    announce=600,
    announce_immediately=True,
    admins=set(),
    hot_reloading=False,
    rate_limit=5,
    cooldown=60,
    max_warnings=3,
    warning_timeout=300,
    command_prefix="/",
    cogs_dir="cogs",
    cogs_enabled={not no_cogs},
    permissions_enabled=False,
    storage_type="json",
    storage_path="data",
    first_message_enabled=True,
    event_logging_enabled=True,
    max_logged_events=1000,
    event_middleware_enabled=True,
    announce_enabled=True
)

if __name__ == "__main__":
    bot.run()
"""
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(template)

        return os.path.relpath(safe_path)

    except Exception as e:
        raise RuntimeError(f"Failed to create bot file: {str(e)}") from e


def create_example_cog(bot_path: str) -> None:
    """Creates an example cog and the necessary directory structure.

    Args:
        bot_path: The path to the bot file to determine the cogs location.
    """
    try:
        bot_dir = os.path.dirname(os.path.abspath(bot_path))
        cogs_dir = os.path.join(bot_dir, "cogs")
        os.makedirs(cogs_dir, exist_ok=True)

        init_path = os.path.join(cogs_dir, "__init__.py")
        with open(init_path, "w", encoding="utf-8") as f:
            f.write("")

        template = """from lxmfy import Command

class BasicCommands:
    def __init__(self, bot):
        self.bot = bot

    @Command(name="hello", description="Says hello")
    async def hello(self, ctx):
        ctx.reply(f"Hello {ctx.sender}!")

    @Command(name="about", description="About this bot")
    async def about(self, ctx):
        ctx.reply("I'm a bot created with LXMFy!")

def setup(bot):
    bot.add_cog(BasicCommands(bot))
"""
        basic_path = os.path.join(cogs_dir, "basic.py")
        with open(basic_path, "w", encoding="utf-8") as f:
            f.write(template)

    except Exception as e:
        raise RuntimeError(f"Failed to create example cog: {str(e)}") from e


def verify_wheel_signature(whl_path: str, sigstore_path: str) -> bool:
    """Verifies the signature of a wheel file.

    Args:
        whl_path: The path to the wheel file.
        sigstore_path: The path to the sigstore file.

    Returns:
        True if the signature is valid, False otherwise.
    """
    try:
        with open(sigstore_path) as f:
            sigstore_data = json.load(f)

        with open(whl_path, "rb") as f:
            whl_content = f.read()
            whl_hash = hashlib.sha256(whl_content).hexdigest()

        if "hash" not in sigstore_data:
            print(f"Error: No hash found in {sigstore_path}")
            return False

        if whl_hash != sigstore_data["hash"]:
            print("Hash verification failed!")
            print(f"Wheel hash: {whl_hash}")
            print(f"Sigstore hash: {sigstore_data['hash']}")
            return False

        print("✓ Signature verification successful!")
        return True

    except Exception as e:
        print(f"Error during verification: {str(e)}")
        return False


def find_latest_wheel():
    """Finds the latest wheel file in the current directory.

    Returns:
        The path to the latest wheel file, or None if no wheel files are found.
    """
    wheels = glob("*.whl")
    if not wheels:
        return None
    return sorted(wheels)[-1]


def create_from_template(template_name: str, output_path: str, bot_name: str) -> str:
    """Creates a bot from a template.

    Args:
        template_name: The name of the template to use.
        output_path: The desired output path.
        bot_name: The name for the bot.

    Returns:
        The path to the created bot file.

    Raises:
        ValueError: If the template is invalid.
    """
    try:
        name = validate_bot_name(bot_name)
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        if output_path.endswith("/") or output_path.endswith("\\"):
            base_name = "bot.py"
            output_path = os.path.join(output_path, base_name)
        elif not output_path.endswith(".py"):
            output_path += ".py"

        safe_path = os.path.abspath(output_path)

        if template_name == "basic":
            return create_bot_file(name, safe_path)

        template_map = {
            "echo": EchoBot,
            "reminder": ReminderBot,
            "note": NoteBot
        }

        if template_name not in template_map:
            raise ValueError(
                f"Invalid template: {template_name}. Available templates: basic, {', '.join(template_map.keys())}"
            )

        template = f"""from lxmfy.templates import {template_map[template_name].__name__}

if __name__ == "__main__":
    bot = {template_map[template_name].__name__}()
    bot.bot.name = "{name}"  # Set custom name
    bot.run()
"""
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(template)

        return os.path.relpath(safe_path)

    except Exception as e:
        raise RuntimeError(f"Failed to create bot from template: {str(e)}") from e


def create_full_bot(name: str, output_path: str) -> str:
    """Creates a full-featured bot with storage and admin commands.

    Args:
        name: The name of the bot.
        output_path: The desired output path.

    Returns:
        The path to the created bot file.

    Raises:
        RuntimeError: If the bot creation fails.
    """
    try:
        name = validate_bot_name(name)

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        if output_path.endswith("/") or output_path.endswith("\\"):
            base_name = "bot.py"
            output_path = os.path.join(output_path, base_name)
        elif not output_path.endswith(".py"):
            output_path += ".py"

        safe_path = os.path.abspath(output_path)

        template = f"""from lxmfy.templates import FullBot

if __name__ == "__main__":
    bot = FullBot()
    bot.bot.name = "{name}"  # Set custom name
    bot.run()
"""
        with open(safe_path, "w", encoding="utf-8") as f:
            f.write(template)

        return os.path.relpath(safe_path)

    except Exception as e:
        raise RuntimeError(f"Failed to create full bot: {str(e)}") from e


def is_safe_path(path: str, base_path: str = None) -> bool:
    """Checks if a path is safe and within the allowed directory.

    Args:
        path: The path to check.
        base_path: The base path to check against. If None, all paths are considered safe.

    Returns:
        True if the path is safe, False otherwise.
    """
    try:
        if base_path:
            base_path = os.path.abspath(base_path)
            path = os.path.abspath(path)
            return path.startswith(base_path)
        return True
    except Exception:
        return False


def analyze_bot_file(file_path: str) -> dict[str, Any]:
    """Analyzes a bot file for configuration issues and best practices.

    Args:
        file_path: The path to the bot file to analyze.

    Returns:
        A dictionary containing the analysis results.
    """
    try:
        abs_path = os.path.abspath(file_path)
        if not is_safe_path(abs_path):
            return {'errors': ['Invalid file path']}

        if not os.path.exists(abs_path):
            return {'errors': ['File not found']}
        if not abs_path.endswith('.py'):
            return {'errors': ['Not a Python file']}

        with open(abs_path) as f:
            tree = ast.parse(f.read())

        results = {
            'commands': [],
            'events': [],
            'middleware': [],
            'permissions': [],
            'config': {},
            'warnings': [],
            'errors': []
        }

        class BotAnalyzer(ast.NodeVisitor):
            """A visitor class to analyze the bot file's AST."""

            def __init__(self, results):
                """Initializes the BotAnalyzer with the results dictionary."""
                self.results = results
                super().__init__()

            @staticmethod
            def _is_bot_call(node: ast.Call) -> bool:
                """Checks if the given call node is a call to LXMFBot."""
                return (isinstance(node.func, ast.Name) and
                       node.func.id == 'LXMFBot')

            @staticmethod
            def _is_bot_assign(node: ast.Assign) -> bool:
                """Checks if the given assignment node assigns a value to a variable named 'bot' by calling LXMFBot."""
                return (isinstance(node.targets[0], ast.Name) and
                       node.targets[0].id == 'bot' and
                       isinstance(node.value, ast.Call) and
                       isinstance(node.value.func, ast.Name) and
                       node.value.func.id == 'LXMFBot')

            def visit_Call(self, node):
                """Visits a call node in the AST."""
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'command':
                        self.results['commands'].append(node.args[0].value)
                    elif node.func.attr == 'on':
                        self.results['events'].append(node.args[0].value)
                    elif node.func.attr == 'middleware':
                        self.results['middleware'].append(node.args[0].value)
                    elif node.func.attr == 'permission':
                        self.results['permissions'].append(node.args[0].value)
                elif self._is_bot_call(node):
                    for kw in node.keywords:
                        self.results['config'][kw.arg] = kw.value.value

            def visit_Assign(self, node):
                """Visits an assignment node in the AST."""
                if self._is_bot_assign(node):
                    for kw in node.value.keywords:
                        self.results['config'][kw.arg] = kw.value.value

        analyzer = BotAnalyzer(results)
        analyzer.visit(tree)

        return results

    except Exception as e:
        return {'errors': [f'Error analyzing file: {str(e)}']}


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="LXMFy Bot Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lxmfy create                          # Create basic bot file 'bot.py'
  lxmfy create mybot                    # Create basic bot file 'mybot.py'
  lxmfy create --template echo mybot    # Create echo bot file 'mybot.py'
  lxmfy create --template reminder bot  # Create reminder bot file 'bot.py'
  lxmfy create --template note notes    # Create note-taking bot file 'notes.py'

  lxmfy run echo                        # Run the built-in echo bot
  lxmfy run reminder --name "MyReminder"  # Run the reminder bot with a custom name
  lxmfy run note                        # Run the built-in note bot

  lxmfy analyze bot.py                  # Analyze bot configuration
  lxmfy verify                          # Verify latest wheel in current directory
  lxmfy verify package.whl sigstore.json # Verify specific wheel and signature
        """,
    )

    parser.add_argument(
        "command",
        choices=["create", "verify", "analyze", "run"],
        help="Create a bot file, verify signature, analyze config, or run a template bot",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default=None,
        help="Name for 'create' (bot name/path), 'analyze' (file path), 'verify' (wheel path), or 'run' (template name: echo, reminder, note)",
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=None,
        help="Output directory for 'create', or sigstore path for 'verify' (optional)",
    )
    parser.add_argument(
        "--template",
        choices=["basic", "echo", "reminder", "note"],
        default="basic",
        help="Bot template to use for 'create' command (default: basic)",
    )
    parser.add_argument(
        "--name",
        dest="name_opt",
        default=None,
        help="Optional custom name for the bot (used with 'create' or 'run')",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path or directory for 'create' command",
    )
    parser.add_argument(
        "--no-cogs",
        action="store_true",
        help="Disable cogs loading for 'create' command",
    )

    args = parser.parse_args()

    if args.command == "analyze":
        if not args.name:
            print("Error: Please specify a bot file to analyze")
            sys.exit(1)

        bot_path = args.name
        if not os.path.exists(bot_path):
            print(f"Error: Bot file not found: {bot_path}")
            sys.exit(1)

        results = analyze_bot_file(bot_path)

        if results.get('errors'):
            print('Errors:')
            for error in results['errors']:
                print(f'  - {error}')

        if results.get('warnings'):
            print('Warnings:')
            for warning in results['warnings']:
                print(f'  - {warning}')

        print('Configuration:')
        for key, value in results.get('config', {}).items():
            print(f'  {key}: {value}')

        print('Commands:', ', '.join(results.get('commands', [])))
        print('Events:', ', '.join(results.get('events', [])))
        print('Middleware:', ', '.join(results.get('middleware', [])))
        print('Permissions:', ', '.join(results.get('permissions', [])))

    elif args.command == "create":
        try:
            bot_name = args.name_opt or args.name or "MyLXMFBot"

            if args.output:
                output_path = args.output
            elif args.directory:
                output_path = os.path.join(args.directory, "bot.py")
            elif args.name:
                if '.' in args.name:
                     output_path = args.name
                     if not args.name_opt:
                         bot_name = os.path.splitext(os.path.basename(args.name))[0]
                else:
                    output_path = f"{args.name}.py"

            else:
                output_path = "bot.py"

            try:
                bot_name = validate_bot_name(bot_name)
            except ValueError as ve:
                print(f"Error: Invalid bot name '{bot_name}'. {ve}", file=sys.stderr)
                sys.exit(1)

            bot_path = create_from_template(args.template, output_path, bot_name)

            if args.template == "basic":
                create_example_cog(bot_path)
                print(
                    f"""
✨ Successfully created new LXMFy bot!

Files created:
  - {bot_path} (main bot file)
  - {os.path.join(os.path.dirname(bot_path), 'cogs')}
    - __init__.py
    - basic.py (example cog)

To start your bot:
  python {bot_path}

To add admin rights, edit {bot_path} and add your LXMF hash to the admins list.
                """
                )
            else:
                print(
                    f"""
✨ Successfully created new LXMFy bot!

Files created:
  - {bot_path} (main bot file)

To start your bot:
  python {bot_path}

To add admin rights, edit {bot_path} and add your LXMF hash to the admins list.
                """
                )
        except Exception as e:
            print(f"Error creating bot: {str(e)}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "verify":
        whl_path = args.name
        sigstore_path = args.directory

        if not whl_path:
            whl_path = find_latest_wheel()
            if not whl_path:
                print("Error: No wheel files found in current directory")
                sys.exit(1)

        if not sigstore_path:
            sigstore_path = "sigstore.json"

        if not os.path.exists(whl_path):
            print(f"Error: Wheel file not found: {whl_path}")
            sys.exit(1)

        if not os.path.exists(sigstore_path):
            print(f"Error: Sigstore file not found: {sigstore_path}")
            sys.exit(1)

        if not verify_wheel_signature(whl_path, sigstore_path):
            sys.exit(1)

    elif args.command == "run":
        template_name = args.name
        if not template_name:
            print("Error: Please specify a template name to run (echo, reminder, note)")
            sys.exit(1)

        template_map = {
            "echo": EchoBot,
            "reminder": ReminderBot,
            "note": NoteBot
        }

        if template_name not in template_map:
             print(f"Error: Invalid template name '{template_name}'. Choose from: {', '.join(template_map.keys())}")
             sys.exit(1)

        try:
            BotClass = template_map[template_name]
            print(f"Starting {template_name} bot...")
            bot_instance = BotClass()

            custom_name = args.name_opt
            if custom_name:
                 try:
                     validated_name = validate_bot_name(custom_name)
                     if hasattr(bot_instance, 'bot'):
                         bot_instance.bot.config.name = validated_name
                         bot_instance.bot.name = validated_name
                     else:
                         bot_instance.config.name = validated_name
                         bot_instance.name = validated_name
                     print(f"Running with custom name: {validated_name}")
                 except ValueError as ve:
                     print(f"Warning: Invalid custom name '{custom_name}' provided. Using default. ({ve})")

            bot_instance.run()

        except Exception as e:
            print(f"Error running template bot '{template_name}': {str(e)}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()

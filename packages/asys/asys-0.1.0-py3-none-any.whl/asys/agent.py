"""
LMSYS Agent - A Python SDK for interacting with the Claude CLI tool.
"""

import os
import json
import subprocess
from typing import Optional, Dict, List, Union, Any


class Agent:
    """
    A class to interact with the Claude CLI tool.

    This class provides a simple interface to run Claude with various
    prompts and configuration options.
    """

    def __init__(self, working_dir: Optional[str] = None, allowed_tools: Optional[List[str]] = None):
        """
        Initialize a Claude Agent.

        Args:
            working_dir: The working directory for Claude to use. Defaults to current directory.
            allowed_tools: List of tools to allow Claude to use. Defaults to ["Edit", "Bash", "Write"].
        """
        self.working_dir = working_dir or os.getcwd()
        self.allowed_tools = allowed_tools or [
            "Bash",
            "Edit",
            "View",
            "GlobTool",
            "GrepTool",
            "LSTool",
            "BatchTool",
            "AgentTool",
            "WebFetchTool",
            "Write",
        ]

    def run(self, prompt: str, stream: bool = False, output_format: Optional[str] = None,
            additional_args: Optional[Dict[str, Any]] = None, auto_print: bool = True) -> Union[str, subprocess.Popen, List[str]]:
        """
        Run Claude with the specified prompt.

        Args:
            prompt: The prompt to send to Claude.
            stream: If True, handles streaming output either automatically or by returning a process.
            output_format: Optional output format (e.g., "stream-json").
            additional_args: Additional arguments to pass to the Claude CLI.
            auto_print: If True and stream=True, automatically prints output and returns collected lines.
                       If False and stream=True, returns the subprocess.Popen object for manual streaming.

        Returns:
            If stream=False: Returns the complete output as a string.
            If stream=True and auto_print=False: Returns a subprocess.Popen object for manual streaming.
            If stream=True and auto_print=True: Automatically prints output and returns collected lines as a list.
        """
        # Prepare the command
        cmd = ["claude", "-p", prompt]

        # Add allowed tools
        if self.allowed_tools:
            cmd.append("--allowedTools")
            cmd.extend(self.allowed_tools)

        # Add output format if specified
        if output_format:
            cmd.extend(["--output-format", output_format])
        elif stream:
            # Default to stream-json if streaming and no format specified
            cmd.extend(["--output-format", "stream-json"])

        # Add any additional arguments
        if additional_args:
            for key, value in additional_args.items():
                if value is True:
                    cmd.append(f"--{key}")
                elif value is not False and value is not None:
                    cmd.extend([f"--{key}", str(value)])

        # If streaming is requested
        if stream:
            # Start the process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
                cwd=self.working_dir
            )

            # If auto_print is False, return the process for manual streaming
            if not auto_print:
                return process

            # If auto_print is True, handle streaming automatically
            lines = []
            try:
                for line in process.stdout:
                    print(line, end="")
                    lines.append(line.rstrip())

                # Wait for process to complete
                return_code = process.wait()
                if return_code != 0:
                    stderr = process.stderr.read()
                    print(f"Error (code {return_code}): {stderr}", file=os.sys.stderr)

                return lines
            except KeyboardInterrupt:
                # Handle user interruption gracefully
                process.terminate()
                print("\nStreaming interrupted by user")
                return lines

        # For non-streaming, run the command and return the output
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                cwd=self.working_dir
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = f"Error executing Claude (code {e.returncode}): {e.stderr}"
            raise RuntimeError(error_msg)

    def run_with_tools(self, prompt: str, tools: List[str], stream: bool = False,
                      auto_print: bool = True) -> Union[str, subprocess.Popen, List[str]]:
        """
        Run Claude with specific allowed tools.

        Args:
            prompt: The prompt to send to Claude.
            tools: List of tools to allow Claude to use.
            stream: If True, handles streaming output.
            auto_print: If True and stream=True, automatically prints output.

        Returns:
            If stream=False: Returns the complete output as a string.
            If stream=True and auto_print=False: Returns a subprocess.Popen object.
            If stream=True and auto_print=True: Automatically prints output and returns collected lines.
        """
        # Save original tools, set the new ones, run, then restore
        original_tools = self.allowed_tools
        self.allowed_tools = tools

        try:
            return self.run(prompt, stream=stream, auto_print=auto_print)
        finally:
            self.allowed_tools = original_tools
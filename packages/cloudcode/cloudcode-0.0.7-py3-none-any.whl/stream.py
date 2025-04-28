import os
import threading
from typing import Any, Dict, List, Optional, Callable, Union
import json

from aider.io import InputOutput

class StreamingInputOutput(InputOutput):
    def __init__(self, callback=None, **kwargs):
        super().__init__(**kwargs)
        self.callback = callback
        self.running_shell_command = False
        self.current_command = None

    def tool_output(self, *messages, log_only=False, bold=False):
        super().tool_output(*messages, log_only=log_only, bold=bold)
        if self.callback:
            for message in messages:
                self.callback({"type": "output", "content": message})

                # Extract current command from "Running" messages
                if self.running_shell_command and not self.current_command and message.startswith("Running "):
                    self.current_command = message[8:]
                    self.callback({"type": "command", "command": self.current_command})

    def tool_warning(self, message="", strip=True):
        super().tool_warning(message, strip)
        if self.callback and message:
            self.callback({"type": "warning", "content": message})

    def tool_error(self, message="", strip=True):
        super().tool_error(message, strip)
        if self.callback and message:
            self.callback({"type": "error", "content": message})

    def confirm_ask(
        self,
        question,
        default="y",
        subject=None,
        explicit_yes_required=False,
        group=None,
        allow_never=False,
    ):
        if self.callback:
            # Send a question event
            self.callback({
                "type": "question",
                "question": question,
                "subject": subject,
                "default": default
            })
            # In streaming mode with callback, we auto-confirm by default
            return True

        # Default behavior without callback
        return super().confirm_ask(
            question, default, subject, explicit_yes_required, group, allow_never
        )

    def reset_state(self):
        self.running_shell_command = False
        self.current_command = None


class StreamJsonCollector:
    """
    Collects streaming updates and organizes them into structured JSON.
    """

    def __init__(self):
        self.updates = []
        self.final_result = None
        self.edited_files = []
        self.final_content = None

    def handle_update(self, update):
        """Collect updates for JSON output."""
        self.updates.append(update)

        # If this is the final response, save it
        if update.get("type") == "response" and update.get("finished", False):
            self.final_content = update.get("content", "")
            if "edited_files" in update:
                self.edited_files = update.get("edited_files", [])

    def get_result(self, result, working_dir):
        """
        Generate a complete result object with all updates and file contents.

        Args:
            result: The result object from the SDK code() method
            working_dir: Working directory where files are located

        Returns:
            A dictionary with complete result information
        """
        # Collect file contents
        file_contents = {}
        for file_path in self.edited_files:
            full_path = os.path.join(working_dir, file_path)
            if os.path.exists(full_path):
                try:
                    with open(full_path, "r") as f:
                        file_contents[file_path] = f.read()
                except Exception as e:
                    file_contents[file_path] = f"Error reading file: {str(e)}"

        # Create the complete result
        output = {
            "success": result.get("success", False),
            "updates": self.updates,
            "final_response": self.final_content,
            "edited_files": self.edited_files,
            "file_contents": file_contents,
            "cost": result.get("cost"),  # Just use the cost from the result, which is already marked up
            "credits_remaining": result.get("credits_remaining")
        }

        return output


class Stream:
    """
    Enhanced streaming interface for Aider SDK.

    This class provides a simple way to use the Aider SDK with streaming
    callbacks for real-time updates during AI coding operations.
    """

    def __init__(
        self,
        working_dir: str,
        model: str = "gpt-4.1-nano",
        editor_model: Optional[str] = None,
        use_git: bool = False,
        api_key: Optional[str] = None,
        api_keys: Optional[Dict[str, str]] = None,
        architect_mode: bool = False,
        weak_model: Optional[str] = None,
        session_id: Optional[str] = None,
        max_reflections: int = 3
    ):
        """
        Initialize the Stream enhanced SDK.

        Args:
            working_dir: Path to the directory where operations will occur
            model: The AI model to use for coding tasks
            editor_model: Optional separate model for editing operations
            use_git: Whether to use git for tracking changes
            api_key: LMSYS API key for authentication
            api_keys: Dictionary of API keys for various providers
            architect_mode: Whether to use architect mode (planner + editor workflow)
            weak_model: Optional planner model to use in architect mode
            session_id: Optional session ID for tracking usage across API calls
            max_reflections: Maximum number of reflections allowed per conversation
        """
        # Import here to avoid circular imports
        from cloudcode import Local

        # Create the Local SDK instance
        self.sdk = Local(
            working_dir=working_dir,
            model=model,
            editor_model=editor_model,
            use_git=use_git,
            api_key=api_key,
            api_keys=api_keys,
            architect_mode=architect_mode,
            weak_model=weak_model,
            session_id=session_id,
            max_reflections=max_reflections
        )

    def code(
        self,
        prompt: str,
        editable_files: List[str],
        readonly_files: List[str] = None,
        context_folders: List[str] = None,
        max_reflections: int = None,
        callback: Callable = None
    ) -> Dict[str, Any]:
        """
        Run an AI coding task with streaming updates to a callback.

        Args:
            prompt: Natural language instruction for the AI coding task
            editable_files: List of files that can be modified by the AI
            readonly_files: List of files that can be read but not modified
            context_folders: List of folder paths to recursively add as context
            max_reflections: Maximum number of reflections allowed for this task
            callback: Function to receive real-time updates

        Returns:
            Result dictionary with task information
        """
        if not callback:
            raise ValueError("A callback function is required for streaming")

        return self.sdk.code(
            prompt=prompt,
            editable_files=editable_files,
            readonly_files=readonly_files,
            context_folders=context_folders,
            max_reflections=max_reflections,
            stream=True,
            callback=callback
        )

    def code_json(
        self,
        prompt: str,
        editable_files: List[str],
        readonly_files: List[str] = None,
        context_folders: List[str] = None,
        max_reflections: int = None,
        pretty: bool = False
    ) -> str:
        """
        Run an AI coding task and return the result as a JSON string.

        This is a convenience method that streams the updates internally
        and returns a complete JSON document when finished, rather than
        streaming updates to a callback.

        Args:
            prompt: Natural language instruction for the AI coding task
            editable_files: List of files that can be modified by the AI
            readonly_files: List of files that can be read but not modified
            context_folders: List of folder paths to recursively add as context
            max_reflections: Maximum number of reflections allowed for this task
            pretty: Whether to format the JSON output with indentation

        Returns:
            A JSON string containing all updates and the final result
        """
        # Create a collector to gather all updates
        collector = StreamJsonCollector()

        # Run the code method with the collector's callback
        result = self.code(
            prompt=prompt,
            editable_files=editable_files,
            readonly_files=readonly_files,
            context_folders=context_folders,
            max_reflections=max_reflections,
            callback=collector.handle_update
        )

        # Get the complete result
        complete_result = collector.get_result(result, self.sdk.working_dir)

        # Return as JSON string
        if pretty:
            return json.dumps(complete_result, indent=2)
        else:
            return json.dumps(complete_result)

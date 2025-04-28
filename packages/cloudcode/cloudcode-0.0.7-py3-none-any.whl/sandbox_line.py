import asyncio
from e2b import AsyncSandbox
from typing import List, Optional, Tuple, Dict, Any

class SandboxLineSDK:
    """
    A simple wrapper around E2B SDK specifically for line-based file operations.
    Provides easy methods to read and write files by line ranges.
    """

    def __init__(self, api_key: Optional[str] = None, sandbox_id: Optional[str] = None):
        """
        Initialize the SandboxLineSDK.

        Args:
            api_key: E2B API key (optional, uses env var E2B_API_KEY if not provided)
            sandbox_id: Connect to existing sandbox if provided
        """
        self.api_key = api_key
        self.sandbox_id = sandbox_id
        self.sandbox = None

    async def connect(self) -> None:
        """
        Connect to an existing sandbox or create a new one.
        """
        if self.sandbox_id:
            self.sandbox = await AsyncSandbox.connect(self.sandbox_id, api_key=self.api_key)
        else:
            self.sandbox = await AsyncSandbox.create(api_key=self.api_key)
            self.sandbox_id = self.sandbox.sandbox_id

    async def read_lines(self, file_path: str, start_line: int = 1, end_line: Optional[int] = None) -> List[str]:
        """
        Read lines from a file within the specified range.

        Args:
            file_path: Path to the file in the sandbox
            start_line: First line to read (1-indexed)
            end_line: Last line to read (inclusive, 1-indexed)

        Returns:
            List of strings representing the lines in the specified range
        """
        if not self.sandbox:
            raise RuntimeError("Sandbox not connected. Call connect() first.")

        if start_line < 1:
            raise ValueError("start_line must be >= 1")

        # Read the entire file content
        content = await self.sandbox.files.read(file_path)

        # Split into lines
        lines = content.splitlines()

        # If end_line not specified, read to the end
        if end_line is None:
            end_line = len(lines)

        # Validate end_line
        if end_line < start_line:
            raise ValueError("end_line must be >= start_line")

        # Adjust for 0-indexed list
        start_idx = start_line - 1
        end_idx = end_line

        # Return the specified lines
        return lines[start_idx:end_idx]

    async def write_lines(self, file_path: str, new_lines: List[str],
                         start_line: int = 1, end_line: Optional[int] = None) -> None:
        """
        Replace lines in a file within the specified range.

        Args:
            file_path: Path to the file in the sandbox
            new_lines: New lines to write
            start_line: First line to replace (1-indexed)
            end_line: Last line to replace (inclusive, 1-indexed)
                     If None, it will replace from start_line to start_line + len(new_lines) - 1
        """
        if not self.sandbox:
            raise RuntimeError("Sandbox not connected. Call connect() first.")

        if start_line < 1:
            raise ValueError("start_line must be >= 1")

        # Read the current content
        content = await self.sandbox.files.read(file_path)
        lines = content.splitlines()

        # If end_line not specified, calculate based on new_lines length
        if end_line is None:
            end_line = start_line + len(new_lines) - 1

        # Validate end_line
        if end_line < start_line:
            raise ValueError("end_line must be >= start_line")

        # Adjust for 0-indexed list
        start_idx = start_line - 1
        end_idx = end_line

        # Create new content by replacing specified lines
        new_content = lines[:start_idx] + new_lines + lines[end_idx:]

        # Join lines and write back to file
        await self.sandbox.files.write(file_path, "\n".join(new_content) + "\n")

    async def count_lines(self, file_path: str) -> int:
        """
        Count the number of lines in a file.

        Args:
            file_path: Path to the file in the sandbox

        Returns:
            Number of lines in the file
        """
        if not self.sandbox:
            raise RuntimeError("Sandbox not connected. Call connect() first.")

        content = await self.sandbox.files.read(file_path)
        lines = content.splitlines()
        return len(lines)

    async def patch_file(self, file_path: str, start_line: int,
                        end_line: int, new_content: List[str]) -> None:
        """
        Patch a file by replacing a specific range of lines.
        Shorthand for write_lines().

        Args:
            file_path: Path to the file in the sandbox
            start_line: First line to replace (1-indexed)
            end_line: Last line to replace (inclusive, 1-indexed)
            new_content: New lines to insert in place of the specified range
        """
        await self.write_lines(file_path, new_content, start_line, end_line)

    async def create_file(self, file_path: str, content: List[str]) -> None:
        """
        Create a new file with the given content.

        Args:
            file_path: Path to the file in the sandbox
            content: Lines to write to the file
        """
        if not self.sandbox:
            raise RuntimeError("Sandbox not connected. Call connect() first.")

        await self.sandbox.files.write(file_path, "\n".join(content) + "\n")

    async def close(self) -> None:
        """
        Close the sandbox connection and release resources.
        """
        if self.sandbox:
            await self.sandbox.kill()
            self.sandbox = None


# Example usage
async def example():
    sdk = SandboxLineSDK()
    await sdk.connect()

    # Create a file
    await sdk.create_file(
        "/mnt/data/example.py",
        [
            "def greet(name):",
            "    print(f\"Hello, {name}!\")",
            "",
            "def farewell(name):",
            "    print(f\"Goodbye, {name}!\")"
        ]
    )

    # Count lines
    line_count = await sdk.count_lines("/mnt/data/example.py")
    print(f"File has {line_count} lines")

    # Read specific lines
    lines = await sdk.read_lines("/mnt/data/example.py", 3, 5)
    print("Lines 3-5:")
    print("\n".join(lines))

    # Patch the file
    await sdk.patch_file(
        "/mnt/data/example.py",
        4, 5,  # Replace the farewell function
        ["# Replacement", "def farewell(name):", "    print(f\"See you later, {name}!\")"]
    )

    # Read the updated file
    all_lines = await sdk.read_lines("/mnt/data/example.py")
    print("\nUpdated file:")
    print("\n".join(all_lines))

    await sdk.close()

if __name__ == "__main__":
    asyncio.run(example())

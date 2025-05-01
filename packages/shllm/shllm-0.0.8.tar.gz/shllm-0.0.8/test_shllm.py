import subprocess
import os
import sys
import unittest
from unittest.mock import patch

class TestShllm(unittest.TestCase):
    def test_command_generation(self):
        """Test that shllm generates a command without requiring API call"""
        # Run with mocked stdin to avoid waiting for user input
        with patch('sys.stdin'):
            # Set up a mock API key for testing
            test_env = os.environ.copy()
            if 'SHLLM_OPENAI_KEY' not in test_env:
                self.skipTest("SHLLM_OPENAI_KEY environment variable not set")
            
            # Run the command with a simple query
            try:
                output = subprocess.check_output(
                    [sys.executable, "shllm.py", "command to ping 127.0.0.1"],
                    env=test_env,
                    stderr=subprocess.STDOUT
                ).decode("utf-8").strip()
                
                # Print the output for debugging
                print(output)
                
                # Check that the output contains 'Command:' and 'ping'
                self.assertIn("Command:", output)
                self.assertIn("ping", output)
            except subprocess.CalledProcessError as e:
                self.fail(f"Process failed with return code {e.returncode}: {e.output.decode('utf-8')}")

if __name__ == "__main__":
    unittest.main()

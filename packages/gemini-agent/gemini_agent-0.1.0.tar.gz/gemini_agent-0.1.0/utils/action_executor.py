import re
import pyautogui
import time
from typing import List, Optional, Dict, Any, Union


class ActionExecutor:
    """
    Executes actions on the GUI based on commands from the agent.
    """
    
    def __init__(self):
        """Initialize the action executor."""
        # Set pyautogui pause between actions
        pyautogui.PAUSE = 0.5
        
        # For safety, enable fail-safe
        pyautogui.FAILSAFE = True
    
    def execute_python_action(self, code: str) -> Dict[str, Any]:
        """
        Execute a Python code snippet that interacts with the GUI.
        
        Args:
            code: Python code string to execute
            
        Returns:
            Dictionary with execution result
        """
        # Sanitize and validate code
        safe_code = self._sanitize_code(code)
        
        try:
            # Prepare local namespace for execution
            local_vars = {
                "pyautogui": pyautogui,
                "time": time
            }
            
            # Execute the code
            exec(safe_code, {}, local_vars)
            
            return {
                "success": True,
                "message": "Action executed successfully",
                "executed_code": safe_code
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error executing action: {str(e)}",
                "executed_code": safe_code
            }
    
    def _sanitize_code(self, code: str) -> str:
        """
        Sanitize Python code to ensure it only uses allowed modules and functions.
        
        Args:
            code: Python code string to sanitize
            
        Returns:
            Sanitized code
        """
        # Remove any imports except for allowed modules
        code_lines = code.split('\n')
        sanitized_lines = []
        
        for line in code_lines:
            # Skip potentially dangerous imports
            if re.match(r'^\s*import\s+(?!pyautogui|time)', line) or \
               re.match(r'^\s*from\s+(?!pyautogui|time)', line):
                sanitized_lines.append(f"# Removed potentially unsafe import: {line}")
                continue
            
            # Allow pyautogui actions and safe functions
            sanitized_lines.append(line)
        
        return '\n'.join(sanitized_lines)
    
    def execute_action_by_type(self, action_type: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a specific type of action with provided parameters.
        
        Args:
            action_type: Type of action to execute (click, type, etc.)
            **kwargs: Parameters for the action
            
        Returns:
            Dictionary with execution result
        """
        try:
            if action_type == "click":
                x, y = kwargs.get("x"), kwargs.get("y")
                pyautogui.click(x=x, y=y)
                return {"success": True, "message": f"Clicked at position ({x}, {y})"}
                
            elif action_type == "type":
                text = kwargs.get("text", "")
                pyautogui.typewrite(text)
                return {"success": True, "message": f"Typed text: {text}"}
                
            elif action_type == "hotkey":
                keys = kwargs.get("keys", [])
                pyautogui.hotkey(*keys)
                return {"success": True, "message": f"Pressed hotkey: {'+'.join(keys)}"}
                
            else:
                return {"success": False, "message": f"Unknown action type: {action_type}"}
                
        except Exception as e:
            return {"success": False, "message": f"Error executing {action_type}: {str(e)}"}
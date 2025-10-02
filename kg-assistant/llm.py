from typing import Dict, Any, Optional
import logging
import os
import json
import aiohttp
from pydantic import Field, PrivateAttr
from urllib.parse import urljoin

from utils.types import BaseTool

logger = logging.getLogger(__name__)

class Tool(BaseTool):
    """LLM tool for processing prompts using XsAI"""
    
    api_key: str = Field(default_factory=lambda: os.getenv("DSX_API_KEY", ""))
    base_url: str = Field(default_factory=lambda: os.getenv("LLM_BASE_URL", ""))
    model: str = Field(default_factory=lambda: os.getenv("LLM_MODEL", "llama3"))
    
    # Private attributes
    _session: Optional[aiohttp.ClientSession] = PrivateAttr(default=None)
    
    def __init__(self, **data):
        super().__init__(
            name="llm",
            description="Processes prompts using local LLM via XsAI",
            **data
        )
        
    async def ensure_session(self):
        """Ensure aiohttp session exists"""
        if not self._session:
            connector = aiohttp.TCPConnector(ssl=False)
            self._session = aiohttp.ClientSession(
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                connector=connector
            )
            
    async def execute(self, params: Dict[str, Any]) -> Any:
        """Execute LLM processing"""
        await self.ensure_session()
        
        # Add detailed environment logging
        logger.info("LLM Tool Configuration:")
        logger.info(f"Base URL: {self.base_url}")
        logger.info(f"Model: {self.model}")
        logger.info(f"API Key present: {bool(self.api_key)}")
        
        if not self.base_url:
            raise ValueError("LLM_BASE_URL environment variable is not set")
        if not self.api_key:
            raise ValueError("DSX_API_KEY environment variable is not set")
            
        prompt = params.get("prompt")
        if not prompt:
            raise ValueError("No prompt provided")
            
        try:
            # Ensure base_url ends with /
            base_url = self.base_url.rstrip("/")
            
            # Prepare request payload
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": 0.0,
                "max_tokens": 1000,
                "stream": False
            }
            
            # Log the full request details for debugging
            logger.debug(f"Making request to {base_url}/completions")
            logger.debug(f"Request payload: {json.dumps(payload, indent=2)}")
            
            async with self._session.post(
                f"{base_url}/completions",
                json=payload,
                timeout=30
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"XsAI API error: Status={response.status}, Response={error_text}")
                    logger.error(f"Request URL: {base_url}/completions")
                    logger.error(f"Request payload: {json.dumps(payload, indent=2)}")
                    raise RuntimeError(f"XsAI API error: {response.status}, {error_text}")
                    
                data = await response.json()
                logger.debug(f"API Response: {json.dumps(data, indent=2)}")
                
                if not data:
                    raise RuntimeError("Empty response from XsAI API")
                
                # Handle different response formats
                if isinstance(data, dict):
                    if "choices" in data and data["choices"]:
                        response_text = data["choices"][0].get("text", "").strip()
                        logger.debug(f"Raw response text: {response_text}")
                        
                        try:
                            # Try to parse as JSON first
                            json_response = json.loads(response_text)
                            return json_response
                        except json.JSONDecodeError:
                            # If not JSON, return as text response
                            return {
                                "response": response_text
                            }
                        
                    logger.error(f"Unexpected response format: {data}")
                    raise RuntimeError("Unexpected response format from XsAI API")
                else:
                    logger.error(f"Unexpected response type: {type(data)}")
                    raise RuntimeError("Invalid response type from XsAI API")
                
        except aiohttp.ClientError as e:
            logger.error(f"Network error calling XsAI API: {e}")
            raise RuntimeError(f"Failed to connect to XsAI API: {e}")
        except Exception as e:
            logger.error(f"Error processing prompt with LLM: {e}")
            raise
            
    async def close(self):
        """Close the client session"""
        if self._session:
            await self._session.close()
            self._session = None 
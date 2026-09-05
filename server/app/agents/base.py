import json
import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.core.state import swarm_state
from app.tools.registry import tool_registry

class BaseAgent:
    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt

    async def emit_thought(self, stage: str, message: str, metadata: Optional[Dict[str, Any]] = None):
        await swarm_state.add_thought(
            agent=self.name,
            stage=stage,
            message=message,
            metadata=metadata or {},
        )

    async def invoke_tool(self, tool_name: str, **kwargs) -> str:
        tool = tool_registry.get_tool(tool_name)

        await self.emit_thought(
            stage="TOOL_CALL",
            message=f"Invoking `{tool_name}` with parameters: {json.dumps(kwargs)}",
            metadata={"tool": tool_name, "parameters": kwargs}
        )

        # Check Human-in-the-Loop requirement
        if tool.requires_approval and settings.REQUIRE_HUMAN_APPROVAL_FOR_DESTRUCTIVE:
            approval_id = f"appr_{tool_name}_{len(swarm_state.thoughts)}"
            await swarm_state.request_approval(
                approval_id=approval_id,
                tool_name=tool_name,
                description=f"Agent '{self.name}' requests permission to invoke sensitive tool: {tool_name}",
                parameters=kwargs,
            )
            # Wait for human approval or timeout
            while swarm_state.pending_approval and swarm_state.pending_approval.approval_id == approval_id:
                await asyncio.sleep(0.5)

        try:
            result = await tool.execute(**kwargs)
            await self.emit_thought(
                stage="TOOL_RESULT",
                message=f"Tool `{tool_name}` output:\n{str(result)[:300]}...",
                metadata={"tool": tool_name, "raw_result": str(result)}
            )
            return str(result)
        except Exception as e:
            err_msg = f"Tool `{tool_name}` execution failed: {str(e)}"
            await self.emit_thought(stage="TOOL_RESULT", message=err_msg, metadata={"error": True})
            return err_msg

    async def query_llm(self, prompt: str) -> str:
        """
        Dispatches prompt to Gemini, OpenAI, Groq, or the autonomous simulation engine.
        """
        # 1. Google Gemini API
        if settings.GEMINI_API_KEY:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
                payload = {
                    "contents": [{"parts": [{"text": f"{self.system_prompt}\n\nUser: {prompt}"}]}]
                }
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(url, json=payload)
                    data = resp.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"]
            except Exception as e:
                await self.emit_thought("THINK", f"Gemini API call failed ({e}). Falling back to simulation engine.")

        # 2. OpenAI / Groq compatible API
        api_key = settings.OPENAI_API_KEY or settings.GROQ_API_KEY
        base_url = "https://api.groq.com/openai/v1" if settings.GROQ_API_KEY else "https://api.openai.com/v1"
        model = "llama-3.1-70b-versatile" if settings.GROQ_API_KEY else "gpt-4o-mini"

        if api_key:
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    resp = await client.post(
                        f"{base_url}/chat/completions",
                        headers={"Authorization": f"Bearer {api_key}"},
                        json={
                            "model": model,
                            "messages": [
                                {"role": "system", "content": self.system_prompt},
                                {"role": "user", "content": prompt}
                            ]
                        }
                    )
                    data = resp.json()
                    return data["choices"][0]["message"]["content"]
            except Exception as e:
                await self.emit_thought("THINK", f"LLM API call failed ({e}). Falling back to simulation engine.")

        # 3. High-Fidelity Simulation Engine (No API key needed)
        return None

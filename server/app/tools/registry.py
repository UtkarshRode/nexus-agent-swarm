from typing import Callable, Dict, Any, List
import inspect

class Tool:
    def __init__(self, name: str, description: str, func: Callable, parameters_schema: Dict[str, Any], requires_approval: bool = False):
        self.name = name
        self.description = description
        self.func = func
        self.parameters_schema = parameters_schema
        self.requires_approval = requires_approval

    async def execute(self, **kwargs) -> Any:
        if inspect.iscoroutinefunction(self.func):
            return await self.func(**kwargs)
        return self.func(**kwargs)

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register(self, name: str, description: str, parameters_schema: Dict[str, Any], requires_approval: bool = False):
        def decorator(func: Callable):
            tool = Tool(
                name=name,
                description=description,
                func=func,
                parameters_schema=parameters_schema,
                requires_approval=requires_approval,
            )
            self.tools[name] = tool
            return func
        return decorator

    def get_tool(self, name: str) -> Tool:
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' not found in registry.")
        return self.tools[name]

    def get_all_schemas(self) -> List[Dict[str, Any]]:
        schemas = []
        for name, tool in self.tools.items():
            schemas.append({
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters_schema,
                "requires_approval": tool.requires_approval,
            })
        return schemas

tool_registry = ToolRegistry()

import os
import logging
import json
import click
import asyncio
from typing import Optional, Dict, Any, List
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from ragflow_sdk import RAGFlow
from dotenv import load_dotenv



logger = logging.getLogger('ragflow_mcp_server')
logger.info("Starting RAGFlow MCP Server")
# 全局变量
ragflow: Optional[RAGFlow] = None
api_key: str = ''
base_url: str = ''
# 存储聊天会话的字典
active_sessions: Dict[str, Any] = {}


async def initialize_server(api_key:str, base_url: str):
    """初始化 RAGFlow MCP 服务器"""
    global ragflow
    load_dotenv()

    api_key = os.getenv("RAGFLOW_API_KEY",'')
    base_url = os.getenv("RAGFLOW_BASE_URL", "http://ragflow.tmeoa.com")

    # if not api_key or not base_url:
    #     raise ValueError("RAGFLOW_API_KEY environment variables must be set")

    ragflow = RAGFlow(api_key=api_key, base_url=base_url)


# def get_ragflow_client():
#     """获取RAGFlow客户端实例"""
#     load_dotenv()
#
#     api_key = os.getenv('RAGFLOW_API_KEY')
#     base_url = os.getenv("RAGFLOW_BASE_URL", "http://ragflow.tmeoa.com")
#
#     if not api_key:
#         raise ValueError("RAGFLOW_API_KEY environment variable must be set")
#
#     return RAGFlow(api_key=api_key, base_url=base_url)


async def serve() -> Server:
    server = Server("ragflow-mcp-server")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """处理工具列表请求"""
        return [
            types.Tool(
                name="list_datasets",
                title="列出数据集",
                description="列出 RAGFlow 中的所有数据集",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                },
            ),
            types.Tool(
                name="ragflow_retrieval",
                title="知识库检索",
                description="在用户指定知识库或文档内进行检索，若未找到指定知识库，则范围为全知识库",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string", 
                            "description": "提问问题"
                        },
                        "dataset_ids": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "数据集ID"
                        },
                        "document_ids": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "文档ID"
                        }
                    },
                    "required": ["question", "dataset_ids"]
                },
            )
        ]
        
    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        """处理工具调用请求"""
        try:
            # 每次请求时获取RAGFlow客户端
            # ragflow = get_ragflow_client()
            
            if name == "list_datasets":
                # 获取参数，使用默认值
                dataset_id = arguments.get("id", None) if arguments else None
                dataset_name = arguments.get("name", None) if arguments else None
                
                try:
                    # 调用 RAGFlow SDK
                    datasets = ragflow.list_datasets()
                    
                    # 只返回 id 和 name 属性
                    result = [{"id": ds.id, "name": ds.name} for ds in datasets]
                    
                    # 返回格式化的 JSON 结果
                    return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
                    
                except Exception as e:
                    return [types.TextContent(type="text", text=f"Error: {str(e)}")]
            
            elif name == "create_chat":
                if not arguments:
                    return [types.TextContent(type="text", text="Error: 未提供参数")]
                    
                dataset_id = arguments.get("dataset_id")
                chat_name = arguments.get("name", "RAGFlow助手")
                
                if not dataset_id:
                    return [types.TextContent(type="text", text="Error: 必须提供数据集ID")]
                    
                try:
                    # 获取数据集
                    datasets = ragflow.list_datasets(id=dataset_id)
                    if not datasets:
                        return [types.TextContent(type="text", text=f"Error: 找不到ID为 {dataset_id} 的数据集")]
                    
                    # 创建聊天助手
                    assistant = ragflow.create_chat(name=chat_name, dataset_ids=[dataset_id])
                    
                    # 创建会话
                    session = assistant.create_session(name=f"{chat_name}会话")
                    
                    # 存储会话信息
                    session_id = session.id
                    active_sessions[session_id] = session
                    
                    result = {
                        "session_id": session_id,
                        "chat_id": assistant.id,
                        "name": chat_name
                    }
                    
                    return [types.TextContent(type="text", text=f"已创建聊天会话。请使用以下会话ID进行对话：\n\n{json.dumps(result, ensure_ascii=False, indent=2)}")]
                    
                except Exception as e:
                    return [types.TextContent(type="text", text=f"Error: 创建聊天会话失败 - {str(e)}")]
            
            elif name == "chat":
                if not arguments:
                    return [types.TextContent(type="text", text="Error: 未提供参数")]
                    
                session_id = arguments.get("session_id")
                question = arguments.get("question")
                
                if not session_id or not question:
                    return [types.TextContent(type="text", text="Error: 必须提供会话ID和问题")]
                    
                if session_id not in active_sessions:
                    return [types.TextContent(type="text", text=f"Error: 找不到ID为 {session_id} 的会话，请先创建会话")]
                    
                try:
                    session = active_sessions[session_id]
                    
                    response = ""
                    for ans in session.ask(question, stream=True):
                        response = ans.content
                    
                    if not response:
                        return [types.TextContent(text="Error: 未收到任何响应")]
                    
                    # 直接返回回答    
                    return [types.TextContent(type="text", text=response)]

                except Exception as e:
                    return [types.TextContent(type="text", text=f"Error: 处理问题时出错 - {str(e)}")]
            
            elif name == "ragflow_retrieval":
                if not arguments:
                    return [types.TextContent(type="text", text="Error: 未提供参数")]
                    
                question = arguments.get("question")
                dataset_ids = arguments.get("dataset_ids", [])
                document_ids = arguments.get("document_ids", [])
                
                if not question or not dataset_ids:
                    return [types.TextContent(type="text", text="Error: 必须提供问题和数据集ID")]
                    
                try:
                    # 调用 RAGFlow SDK 进行检索
                    retrieval_results = ragflow.retrieve(
                        question=question, 
                        dataset_ids=dataset_ids, 
                        document_ids=document_ids
                    )
                    
                    # 将结果转为可序列化的字典
                    result = []
                    for item in retrieval_results:
                        chunk_data = {
                            "content": item.content
                        }
                        # 安全地检查属性是否存在
                        if hasattr(item, 'metadata'):
                            chunk_data["metadata"] = item.metadata
                        if hasattr(item, 'score'):
                            chunk_data["score"] = item.score
                        
                        result.append(chunk_data)
                    
                    return [types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
                    
                except Exception as e:
                    return [types.TextContent(type="text", text=f"Error: 检索时出错 - {str(e)}")]
                
            return []
            
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: 处理请求时出错 - {str(e)}")]

    # 确保明确返回server对象
    return server

@click.command()
def main():
    async def _run():
        await initialize_server(api_key, base_url)
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            server = await serve()
            if server is None:
                raise ValueError("Server initialization failed, server object is None")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="ragflow-mcp-server",
                    server_version="0.1.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )

    asyncio.run(_run())

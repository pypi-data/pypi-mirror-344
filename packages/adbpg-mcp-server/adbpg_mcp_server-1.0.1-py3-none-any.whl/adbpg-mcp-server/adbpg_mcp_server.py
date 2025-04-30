import asyncio
import logging
import os
import sys
import psycopg
from psycopg import OperationalError as Error
from mcp.server import Server
from mcp.types import Resource, Tool, TextContent, ResourceTemplate
from pydantic import AnyUrl
from dotenv import load_dotenv
from mcp.server.stdio import stdio_server

# 配置日志，输出到标准错误
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("adbpg-mcp-server")

# 加载环境变量
try:
    load_dotenv()
    logger.info("Environment variables loaded")
    
    # 检查必要的环境变量
    required_vars = ["ADBPG_HOST", "ADBPG_PORT", "ADBPG_USER", "ADBPG_PASSWORD", "ADBPG_DATABASE"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("All required environment variables are set")
except Exception as e:
    logger.error(f"Error loading environment variables: {e}")
    sys.exit(1)

SERVER_VERSION = "0.1.0"

def get_db_config():
    """从环境变量获取数据库配置信息"""
    try:
        config = {
            "host": os.getenv("ADBPG_HOST", "localhost"),
            "port": os.getenv("ADBPG_PORT"),
            "user": os.getenv("ADBPG_USER"),
            "password": os.getenv("ADBPG_PASSWORD"),
            "dbname": os.getenv("ADBPG_DATABASE"),
            "application_name": f"adbpg-mcp-server-{SERVER_VERSION}"
        }
        
        # 记录配置信息（不包含密码）
        logger.info(f"Database config: host={config['host']}, port={config['port']}, user={config['user']}, dbname={config['dbname']}")
        
        return config
    except Exception as e:
        logger.error(f"Error getting database config: {str(e)}")
        raise

# 初始化服务器
try:
    app = Server("adbpg-mcp-server")
    logger.info("MCP server initialized")
except Exception as e:
    logger.error(f"Error initializing MCP server: {e}")
    sys.exit(1)

@app.list_resources()
async def list_resources() -> list[Resource]:
    """列出可用的基本资源"""
    try:
        return [
            Resource(
                uri="adbpg:///schemas",
                name="All Schemas",
                description="AnalyticDB PostgreSQL schemas. List all schemas in the database",
                mimeType="text/plain"
            )
        ]
    except Exception as e:
        logger.error(f"Error listing resources: {str(e)}")
        raise

@app.list_resource_templates()
async def list_resource_templates() -> list[ResourceTemplate]:
    """
    定义动态资源模板
    
    返回:
        list[ResourceTemplate]: 资源模板列表
        包含以下模板：
        - 列出schema中的表
        - 获取表DDL
        - 获取表统计信息
    """
    return [
        ResourceTemplate(
            uriTemplate="adbpg:///{schema}/tables",  # 表列表模板
            name="Schema Tables",
            description="List all tables in a specific schema",
            mimeType="text/plain"
        ),
        ResourceTemplate(
            uriTemplate="adbpg:///{schema}/{table}/ddl",  # 表DDL模板
            name="Table DDL",
            description="Get the DDL script of a table in a specific schema",
            mimeType="text/plain"
        ),
        ResourceTemplate(
            uriTemplate="adbpg:///{schema}/{table}/statistics",  # 表统计信息模板
            name="Table Statistics",
            description="Get statistics information of a table",
            mimeType="text/plain"
        )
    ]

@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """
    读取资源内容
    
    参数:
        uri (AnyUrl): 资源URI
        
    返回:
        str: 资源内容
        
    支持的URI格式：
    - adbpg:///schemas: 列出所有schema
    - adbpg:///{schema}/tables: 列出指定schema中的表
    - adbpg:///{schema}/{table}/ddl: 获取表的DDL
    - adbpg:///{schema}/{table}/statistics: 获取表的统计信息
    """
    config = get_db_config()
    uri_str = str(uri)
    
    if not uri_str.startswith("adbpg:///"):
        raise ValueError(f"Invalid URI scheme: {uri_str}")
    
    try:
        with psycopg.connect(**config) as conn:  # 建立数据库连接
            conn.autocommit = True  # 设置自动提交
            with conn.cursor() as cursor:  # 创建游标
                path_parts = uri_str[9:].split('/')  # 解析URI路径
                
                if path_parts[0] == "schemas":
                    # 列出所有schema
                    query = """
                        SELECT schema_name 
                        FROM information_schema.schemata 
                        WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
                        ORDER BY schema_name;
                    """
                    cursor.execute(query)
                    schemas = cursor.fetchall()
                    return "\n".join([schema[0] for schema in schemas])
                    
                elif len(path_parts) == 2 and path_parts[1] == "tables":
                    # 列出指定schema中的表
                    schema = path_parts[0]
                    query = f"""
                        SELECT table_name, table_type
                        FROM information_schema.tables
                        WHERE table_schema = %s
                        ORDER BY table_name;
                    """
                    cursor.execute(query, (schema,))
                    tables = cursor.fetchall()
                    return "\n".join([f"{table[0]} ({table[1]})" for table in tables])
                    
                elif len(path_parts) == 3 and path_parts[2] == "ddl":
                    # 获取表的DDL
                    schema = path_parts[0]
                    table = path_parts[1]
                    query = f"""
                        SELECT pg_get_ddl('{schema}.{table}'::regclass);
                    """
                    cursor.execute(query)
                    ddl = cursor.fetchone()
                    return ddl[0] if ddl else f"No DDL found for {schema}.{table}"
                    
                elif len(path_parts) == 3 and path_parts[2] == "statistics":
                    # 获取表的统计信息
                    schema = path_parts[0]
                    table = path_parts[1]
                    query = """
                        SELECT 
                            schemaname,
                            tablename,
                            attname,
                            null_frac,
                            avg_width,
                            n_distinct,
                            most_common_vals,
                            most_common_freqs
                        FROM pg_stats
                        WHERE schemaname = %s AND tablename = %s
                        ORDER BY attname;
                    """
                    cursor.execute(query, (schema, table))
                    rows = cursor.fetchall()
                    if not rows:
                        return f"No statistics found for {schema}.{table}"
                    
                    result = []
                    for row in rows:
                        result.append(f"Column: {row[2]}")
                        result.append(f"  Null fraction: {row[3]}")
                        result.append(f"  Average width: {row[4]}")
                        result.append(f"  Distinct values: {row[5]}")
                        if row[6]:
                            result.append(f"  Most common values: {row[6]}")
                            result.append(f"  Most common frequencies: {row[7]}")
                        result.append("")
                    return "\n".join(result)
                
                raise ValueError(f"Invalid resource URI format: {uri_str}")
      
    except Error as e:
        raise RuntimeError(f"Database error: {str(e)}")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    列出可用的工具
    
    返回:
        list[Tool]: 工具列表
        包含以下工具：
        - execute_select_sql: 执行SELECT查询
        - execute_dml_sql: 执行DML操作
        - execute_ddl_sql: 执行DDL操作
        - analyze_table: 分析表统计信息
        - explain_query: 获取查询执行计划
    """
    return [
        Tool(
            name="execute_select_sql",
            description="Execute SELECT SQL to query data from ADBPG database.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The (SELECT) SQL query to execute"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="execute_dml_sql",
            description="Execute (INSERT, UPDATE, DELETE) SQL to modify data in ADBPG database.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The DML SQL query to execute"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="execute_ddl_sql",
            description="Execute (CREATE, ALTER, DROP) SQL statements to manage database objects.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The DDL SQL query to execute"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="analyze_table",
            description="Execute ANALYZE command to collect table statistics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "schema": {
                        "type": "string",
                        "description": "Schema name"
                    },
                    "table": {
                        "type": "string",
                        "description": "Table name"
                    }
                },
                "required": ["schema", "table"]
            }
        ),
        Tool(
            name="explain_query",
            description="Get query execution plan.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The SQL query to analyze"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    执行工具操作
    
    参数:
        name (str): 工具名称
        arguments (dict): 工具参数
        
    返回:
        list[TextContent]: 执行结果
        
    支持的工具：
    - execute_select_sql: 执行SELECT查询
    - execute_dml_sql: 执行DML操作
    - execute_ddl_sql: 执行DDL操作
    - analyze_table: 分析表统计信息
    - explain_query: 获取查询执行计划
    """
    config = get_db_config()
    
    # 根据工具名称处理不同的操作
    if name == "execute_select_sql":
        query = arguments.get("query")
        if not query:
            raise ValueError("Query is required")
        if not query.strip().upper().startswith("SELECT"):
            raise ValueError("Query must be a SELECT statement")
    elif name == "execute_dml_sql":
        query = arguments.get("query")
        if not query:
            raise ValueError("Query is required")
        if not any(query.strip().upper().startswith(keyword) for keyword in ["INSERT", "UPDATE", "DELETE"]):
            raise ValueError("Query must be a DML statement (INSERT, UPDATE, DELETE)")
    elif name == "execute_ddl_sql":
        query = arguments.get("query")
        if not query:
            raise ValueError("Query is required")
        if not any(query.strip().upper().startswith(keyword) for keyword in ["CREATE", "ALTER", "DROP"]):
            raise ValueError("Query must be a DDL statement (CREATE, ALTER, DROP)")
    elif name == "analyze_table":
        schema = arguments.get("schema")
        table = arguments.get("table")
        if not all([schema, table]):
            raise ValueError("Schema and table are required")
        query = f"ANALYZE {schema}.{table}"
    elif name == "explain_query":
        query = arguments.get("query")
        if not query:
            raise ValueError("Query is required")
        query = f"EXPLAIN {query}"
    else:
        raise ValueError(f"Unknown tool: {name}")
    
    try:
        with psycopg.connect(**config) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(query)
                
                if name == "analyze_table":
                    return [TextContent(type="text", text=f"Successfully analyzed table {schema}.{table}")]
                
                if cursor.description:
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    result = [",".join(map(str, row)) for row in rows]
                    return [TextContent(type="text", text="\n".join([",".join(columns)] + result))]
                else:
                    return [TextContent(type="text", text="Query executed successfully")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error executing query: {str(e)}")]

async def main():
    """服务器主入口点"""
    try:
        config = get_db_config()
        logger.info("Starting ADBPG MCP server...")
        
        # 测试数据库连接
        try:
            with psycopg.connect(**config) as conn:
                logger.info("Successfully connected to database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            sys.exit(1)
        
        # 使用 stdio 传输
        async with stdio_server() as (read_stream, write_stream):
            try:
                logger.info("Running MCP server with stdio transport...")
                await app.run(
                    read_stream=read_stream,
                    write_stream=write_stream,
                    initialization_options=app.create_initialization_options()
                )
            except Exception as e:
                logger.error(f"Error running server: {str(e)}")
                raise
    except Exception as e:
        logger.error(f"Server initialization error: {str(e)}")
        raise

def run():
    """同步运行入口点"""
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run() 
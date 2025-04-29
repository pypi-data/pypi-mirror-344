from mcp.server.fastmcp import FastMCP
import os
import time
from mcp_asr import submit_asr_task, query_asr_task
from mcp.types import TextContent

mcp = FastMCP('asr-mcp-server')

@mcp.tool("audio-to-text")
def asr_server(url:str) ->list[TextContent]:
    """Convert audio link to text"""
    app_id = os.environ.get("APP_ID")
    token = os.environ.get("TOKEN")
    task_id, x_tt_log_id = submit_asr_task(app_id, token, url)
    while True:
        query_response = query_asr_task(app_id, token, task_id, x_tt_log_id)
        code = query_response.headers.get('X-Api-Status-Code', "")
        if code == '20000000':  # task finished
            data = query_response.json()
            if isinstance(data ,dict):
                result = data.get('result')
                if  isinstance(result ,dict):
                    text = result.get("text")
                    return [TextContent(type="text", text=text)]
                else:
                    return [TextContent(type="text", text=f'服务生成失败 task_id={task_id}')]
            else:
                return [TextContent(type="text", text=f'服务生成失败 task_id={task_id}')]
        elif code != '20000001' and code != '20000002':  # task failed
            return [TextContent(type="text", text='调用失败')]
        time.sleep(0.5)

def main():
    mcp.run(transport="stdio")


if __name__ == '__main__':
    main()
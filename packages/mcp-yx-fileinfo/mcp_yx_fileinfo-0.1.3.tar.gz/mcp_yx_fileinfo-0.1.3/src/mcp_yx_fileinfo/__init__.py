
import logging
from mcp_yx_fileinfo.yxfileInfo.file_info import mcp
def main():
    print(f'Hi,mcp-yx-fileinfo-0.1.3')


if __name__ == "__main__":
    main()
    logging.info("文件信息服务已成功启动！")
    # 初始化并运行 server
    mcp.run(transport='stdio')

# PyServe

一个基于 Flask 的轻量级多功能 Web 服务器，支持动态脚本执行、文件服务和自定义配置。

## ✨ 功能特性

### 🌐 核心功能
- **静态文件服务**：支持多种文件类型的 HTTP 服务
- **目录浏览**：可配置的目录列表功能
- **动态脚本支持**：
  - **Python 脚本 (.pys)**：内嵌 Python 代码执行
  - **PHP 支持**：通过 PHP-CGI 执行 PHP 脚本
- **自定义错误页面**：支持自定义 HTTP 错误页面
- **请求日志**：按日期记录所有 HTTP 请求

## 📋 系统需求

- Python 3.8+
- Flask
- colorama
- PHP-CGI（如需 PHP 支持）

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install flask colorama
```

### 2. 项目结构

```
PyServe/
├── PyServe.py      # 主程序文件
├── config/
│   └── config.cfg      # 配置文件
├── WWW/                # Web 根目录
│   └── error/          # 错误页面目录
│       ├── 404.html
│       └── ...
├── PHP/                # PHP 相关文件
│   └── php-cgi.exe     # PHP-CGI 执行文件
└── log/                # 日志目录
```

### 3. 运行服务器

```bash
python PyServe.py
```

服务器默认在 80 端口启动，访问 http://localhost 即可。

## ⚙️ 配置说明

编辑 `config/config.cfg` 文件来自定义服务器行为：

```python
# 基础配置
Config.PORT = 80                  # 服务器端口
Config.ENCODING = 'utf-8'         # 文件编码
Config.WWW_ROOT = './WWW'         # Web 根目录
Config.ERROR_DIR = '/error'       # 错误页面目录
Config.DIR_LISTING = False        # 是否启用目录列表
Config.LOG_DIR = './log'          # 日志文件目录

# PHP 配置
Config.PHP_CGI_PATH = "./PHP/php-cgi"  # PHP-CGI 路径
```

## 🎯 使用示例

### Python 动态页面 (.pys)

创建 `WWW/index.pys` 文件：

```html
<!DOCTYPE html>
<html>
<body>
    <h1>欢迎访问 PyServe</h1>
    <python>
echo("<p>当前时间：" + str(datetime.datetime.now()) + "</p>")
echo("<p>您的 IP 地址：" + remote_addr() + "</p>")
    </python>
</body>
</html>
```

### 可用的 Python 函数

在 .pys 文件中可以使用以下内置函数：

- `print()` - 即支持直接输出 HTML，也支持输出到控制台
- `echo()` - 直接输出 HTML
- `h1()` ~ `h6()` - 输出标题标签
- `p()` - 输出段落标签
- `get()` - 获取 GET 参数
- `post()` - 获取 POST 参数
- `remote_addr()` - 获取访客 IP 地址
- `headers()` - 获取请求头信息
- `get_file()` - 处理文件上传

## 🔒 安全考虑

1. **沙箱执行**：Python 代码在受限环境中执行
2. **函数限制**：可以通过 `DISABLE_PYTHON_FUNCTIONS` 禁用特定函数
3. **库控制**：仅允许使用 `ENABLE_PYTHON_LIBRARIES` 中指定的库
4. **文件访问**：限制在 WWW_ROOT 目录内

## 📝 日志记录

服务器会在 `log/` 目录下按日期创建日志文件，记录格式：

```
{'timestamp': '2025-01-09T10:30:45', 'ip': '127.0.0.1', 'method': 'GET', 'path': '/', ...}
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 GNU General Public License v3.0 (GPL-3.0) 许可证。详见 [LICENSE](LICENSE) 文件。

## 👤 作者

- **zplbFelix**

## ☕ 支持作者

如果这个项目对你有帮助，欢迎请作者喝杯咖啡！

<p align="center">
  <img src="https://zplb.org.cn/images/pay.jpg" alt="打赏二维码" width="300">
</p>

<p align="center">
  <strong>感谢你的支持！</strong> 🙏
</p>

# <img src="pyserve.png" alt="icon" width="50" align="center"> PyServe

<div align="left">
  <a href="README_ZH.md">中文</a> | <a href="README.md">English</a>
</div>
</br>


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
- **日志自动清理**：可按保留天数自动删除过期日志

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
Config.LOG_RETENTION_DAYS = None  # 日志保留天数（None 表示不自动删除）
Config.CONFIG_DIR = "./config"    # 配置文件目录

# PHP 配置
Config.PHP_CGI_PATH = "./PHP/php-cgi"  # PHP-CGI 路径
```

此外，你可以在 `config.cfg` 中配置文件类型分类、MIME 类型映射，以及 Python 执行白名单：

```python
# 文件类型分类（可扩展）
Config.HTML_EXTENSIONS = ['html', 'htm', 'pys', 'php', 'pp']

# MIME 类型映射（常见类型已内置，可按需扩展）
Config.MIME_TYPES.update({
    'md': 'text/markdown'
})

# Python 执行限制
DISABLE_PYTHON_FUNCTIONS = []  # 禁用的函数
ENABLE_PYTHON_LIBRARIES = ['sys', 'os', 'math', 'datetime', 'time', 'json', ...]  # 允许导入的库
```

## 🎯 使用示例

### 动态页面支持

#### Python 脚本 (.pys)

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

#### PHP+Python 混合文件 (.pp)

创建 `WWW/index.pp` 文件，可以同时包含 PHP 和 Python 代码：

```html
<!DOCTYPE html>
<html>
<body>
    <?php
        echo "<h1>PHP 生成的内容</h1>";
        echo "<p>服务器时间：".date('Y-m-d H:i:s')."</p>";
    ?>
    
    <python>
echo("<p>Python 说：当前时间戳是 " + str(time.time()) + "</p>")
    </python>
</body>
</html>
```

### 可用的 Python 函数

- 完整技术说明： [FUNCTIONS_ZH.md](file:///d:/Users/felix/Desktop/PyServe/PyServe/FUNCTIONS_ZH.md)

## 🔒 安全考虑

1. **沙箱执行**：Python 代码在受限环境中执行
2. **函数限制**：可以通过 `DISABLE_PYTHON_FUNCTIONS` 禁用特定函数
3. **库控制**：仅允许使用 `ENABLE_PYTHON_LIBRARIES` 中指定的库
4. **文件访问**：限制在 WWW_ROOT 目录内

## 📝 日志记录

服务器会在 `log/` 目录下按日期创建日志文件，并支持自动清理过期日志：

```
{'timestamp': '2025-01-09T10:30:45', 'ip': '127.0.0.1', 'method': 'GET', 'path': '/', ...}
```

- 设置 `Config.LOG_RETENTION_DAYS` 为正整数（例如 `7`）时，会在写入日志时自动删除早于该天数的旧日志文件。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 GNU General Public License v3.0 (GPL-3.0) 许可证。详见 [LICENSE](LICENSE) 文件。

## 👤 作者

- **zplbFelix**

## ☕ 支持作者

如果这个项目对你有帮助，欢迎请作者喝杯咖啡！

<p align="center">
  <img src="pay.jpg" alt="打赏二维码" width="300">
</p>

<p align="center">
  <i>扫码打赏，您的支持是我持续开发的动力！</i>
</p>

<p align="center">
  <strong>感谢你的支持！</strong> 🙏
</p>

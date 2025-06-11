# PyServe

<div align="left">
  <a href="README_ZH.md">中文</a> | <a href="README.md">English</a>
</div>

--

A lightweight multi-functional web server based on Flask, supporting dynamic script execution, file serving, and custom configuration.

## ✨ Features

### 🌐 Core Functions
- **Static File Serving**: HTTP service supporting various file types
- **Directory Browsing**: Configurable directory listing functionality
- **Dynamic Script Support**:
  - **Python Scripts (.pys)**: Embedded Python code execution
  - **PHP Support**: Execute PHP scripts through PHP-CGI
- **Custom Error Pages**: Support for custom HTTP error pages
- **Request Logging**: Log all HTTP requests by date

## 📋 System Requirements

- Python 3.8+
- Flask
- colorama
- PHP-CGI (for PHP support)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install flask colorama
```

### 2. Project Structure

```
PyServe/
├── PyServe.py      # Main program file
├── config/
│   └── config.cfg      # Configuration file
├── WWW/                # Web root directory
│   └── error/          # Error pages directory
│       ├── 404.html
│       └── ...
├── PHP/                # PHP related files
│   └── php-cgi.exe     # PHP-CGI executable
└── log/                # Log directory
```

### 3. Run the Server

```bash
python PyServe.py
```

The server starts on port 80 by default. Visit http://localhost to access.

## ⚙️ Configuration

Edit the `config/config.cfg` file to customize server behavior:

```python
# Basic Configuration
Config.PORT = 80                  # Server port
Config.ENCODING = 'utf-8'         # File encoding
Config.WWW_ROOT = './WWW'         # Web root directory
Config.ERROR_DIR = '/error'       # Error pages directory
Config.DIR_LISTING = False        # Enable directory listing
Config.LOG_DIR = './log'          # Log files directory

# PHP Configuration
Config.PHP_CGI_PATH = "./PHP/php-cgi"  # PHP-CGI path
```

## 🎯 Usage Examples

### Python Dynamic Pages (.pys)

Create `WWW/index.pys` file:

```html
<!DOCTYPE html>
<html>
<body>
    <h1>Welcome to PyServe</h1>
    <python>
echo("<p>Current time: " + str(datetime.datetime.now()) + "</p>")
echo("<p>Your IP address: " + remote_addr() + "</p>")
    </python>
</body>
</html>
```

### Available Python Functions

The following built-in functions are available in .pys files:

- `print()` - Supports both HTML output and console output
- `echo()` - Direct HTML output
- `h1()` ~ `h6()` - Output heading tags
- `p()` - Output paragraph tags
- `get()` - Get GET parameters
- `post()` - Get POST parameters
- `remote_addr()` - Get visitor IP address
- `headers()` - Get request headers
- `get_file()` - Handle file uploads

## 🔒 Security Considerations

1. **Sandbox Execution**: Python code executes in a restricted environment
2. **Function Restrictions**: Disable specific functions via `DISABLE_PYTHON_FUNCTIONS`
3. **Library Control**: Only libraries specified in `ENABLE_PYTHON_LIBRARIES` are allowed
4. **File Access**: Restricted within WWW_ROOT directory

## 📝 Logging

The server creates log files by date in the `log/` directory with the following format:

```
{'timestamp': '2025-01-09T10:30:45', 'ip': '127.0.0.1', 'method': 'GET', 'path': '/', ...}
```

## 🤝 Contributing

Welcome to submit Issues and Pull Requests!

## 📄 License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). See [LICENSE](LICENSE) file for details.

## 👤 Author

- **zplbFelix**

## ☕ Support the Author

If this project helps you, feel free to buy the author a coffee! (WeChat Pay)

<p align="center">
  <img src="pay.jpg" alt="Donation QR Code" width="300">
</p>

<p align="center">
  <i>Scan to donate. Your support is my motivation for continuous development!</i>
</p>

<p align="center">
  <strong>Thank you for your support!</strong> 🙏
</p>

# -*- coding:utf-8 -*-
"""
PyServe.py
Copyright (c) 2025 zplbFelix
License: GPL-3.0

A lightweight web server implementation using Flask
This program is free software under the GNU General Public License v3.0
"""
import datetime
import os
import logging
from flask import Flask, request, make_response, Response
import colorama
import sys
import subprocess

# Initialize colorama for colored console output
colorama.init()


# ================
# Configuration
# ================

class Config:
    """Server configuration with default values"""
    PORT = 80
    ENCODING = 'utf-8'
    WWW_ROOT = './WWW'
    ERROR_DIR = '/error'
    DIR_LISTING = False
    LOG_DIR = './log'
    
    # Large file download settings
    LARGE_FILE_THRESHOLD = 50 * 1024 * 1024  # 50MB threshold for streaming
    CHUNK_SIZE = 64 * 1024  # 64KB chunks for streaming

    # File type categories
    HTML_EXTENSIONS = ['html', 'htm', 'pys', 'php', 'pp']
    IMAGE_EXTENSIONS = ['bmp', 'gif', 'jpg', 'png', 'jpeg', 'webp', 'svg', 'ico', 'tif', 'tiff']
    VIDEO_EXTENSIONS = ['mp4', 'webm', 'avi', 'mov', 'wmv', 'flv', 'mkv']
    AUDIO_EXTENSIONS = ['mp3', 'wav', 'ogg', 'aac', 'flac', 'm4a']
    FONT_EXTENSIONS = ['ttf', 'otf', 'woff', 'woff2']
    DOWNLOAD_EXTENSIONS = [
        'exe', 'com', 'zip', 'rar', '7z', 'iso', 'jar', 'pdf', 'doc', 'docx',
        'xls', 'xlsx', 'ppt', 'pptx', 'msi', 'dmg', 'pkg', 'deb', 'rpm'
    ]

    # MIME Type Mapping
    MIME_TYPES = {
        # Images
        'bmp': 'image/bmp',
        'gif': 'image/gif',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'webp': 'image/webp',
        'svg': 'image/svg+xml',
        'ico': 'image/x-icon',
        'tif': 'image/tiff',
        'tiff': 'image/tiff',

        # Videos
        'mp4': 'video/mp4',
        'webm': 'video/webm',
        'avi': 'video/x-msvideo',
        'mov': 'video/quicktime',
        'wmv': 'video/x-ms-wmv',
        'flv': 'video/x-flv',
        'mkv': 'video/x-matroska',

        # Audio
        'mp3': 'audio/mpeg',
        'wav': 'audio/wav',
        'ogg': 'audio/ogg',
        'aac': 'audio/aac',
        'flac': 'audio/flac',
        'm4a': 'audio/mp4',

        # Fonts
        'ttf': 'font/ttf',
        'otf': 'font/otf',
        'woff': 'font/woff',
        'woff2': 'font/woff2',

        # Documents
        'pdf': 'application/pdf',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'ppt': 'application/vnd.ms-powerpoint',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',

        # Archives
        'zip': 'application/zip',
        'rar': 'application/x-rar-compressed',
        '7z': 'application/x-7z-compressed',

        # Other
        'json': 'application/json',
        'xml': 'application/xml',
        'js': 'application/javascript',
        'css': 'text/css',
        'txt': 'text/plain',
        'csv': 'text/csv'
    }

    #Python functions or libraries that are prohibited or allowed to run
    DISABLE_PYTHON_FUNCTIONS = []
    ENABLE_PYTHON_LIBRARIES = ['sys', 'os', 'math', 'datetime', 'time', 'random', 'json',
                               're', 'collections', 'subprocess', 'socket', 'urllib',
                               'csv', 'pickle', 'sqlite3', 'hashlib', 'itertools', 'logging',
                               'secret', 'base64', 'email', 'functools', 'glob', 'html',
                               'string', 'shutil', 'smtplib']

    #PHP related content
    PHP_CGI_PATH = "./PHP/php-cgi"


# Try to load custom configuration
try:
    config_path = os.path.join('config', 'config.cfg')
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as config_file:
            exec(config_file.read())
        print(colorama.Fore.GREEN + 'Configuration loaded successfully')
    else:
        print(colorama.Fore.YELLOW + 'No config file found, using defaults')
except Exception as e:
    print(colorama.Fore.RED + f'Error loading config: {str(e)}\nUsing default configuration')

# Initialize Flask app
app = Flask(__name__)

# Suppress Flask logging if possible
try:
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
except:
    print(colorama.Fore.YELLOW + 'Warning: Could not suppress Flask logging')

print(colorama.Fore.RESET)


# ================
# Python Interpreter
# ================

def extract_all_python_tags(html):
    """Extract the content of all<python>tags from HTML and execute"""
    def run_python(text):
        try:
            content = ''
            def new_print(*args, sep=' ', end='\n', file=None, flush=False, output=False):
                nonlocal content
                output_file = file if file is not None else sys.stdout
                text = sep.join(str(arg) for arg in args)
                if output:
                    output_file.write(text + end)
                    if flush:
                        output_file.flush()
                content += text
            def new_echo(text):
                nonlocal content
                content += text
            def new_h1(text):
                nonlocal content
                content += '<h1>' + html.escape(text) + '</h1>'
            def new_h2(text):
                nonlocal content
                content += '<h2>' + html.escape(text) + '</h2>'
            def new_h3(text):
                nonlocal content
                content += '<h3>' + html.escape(text) + '</h3>'
            def new_h4(text):
                nonlocal content
                content += '<h4>' + html.escape(text) + '</h4>'
            def new_h5(text):
                nonlocal content
                content += '<h5>' + html.escape(text) + '</h5>'
            def new_h6(text):
                nonlocal content
                content += '<h6>' + html.escape(text) + '</h6>'
            def new_p(text):
                nonlocal content
                content += '<p>' + html.escape(text) + '</p>'
            def new_get(text):
                return request.args.get(text)
            def new_post(text):
                return request.form.get(text)
            def new_remote_addr():
                cloudflare_ip = request.headers.get('CF-Connecting-IP')
                if cloudflare_ip:
                    visitor_ip = cloudflare_ip
                else:
                    x_forwarded_for = request.headers.get('X-Forwarded-For')
                    if x_forwarded_for:
                        visitor_ip = x_forwarded_for.split(',')[0].strip()
                    else:
                        visitor_ip = request.remote_addr
                return visitor_ip
            def new_headers():
                header = str(request.headers).strip().split('\n')
                headers = {}
                for i in header:
                    headers[i.split(':')[0].strip()] = ':'.join(i.split(':')[1:]).strip()
                return headers
            def new_get_file(text, path):
                file = request.files.get(text)
                file.save(Config.WWW_ROOT.replace('\\','/') + '/' + str(path).replace('\\', '/'))

            def ERROR(*args,**kwargs):
                raise NameError('This function has been disabled')
            exec_scope = {'__builtins__': __builtins__}
            new = {'print': new_print, 'echo': new_echo,
                   'h1': new_h1, 'h2': new_h2, 'h3': new_h3, 'h4': new_h4, 'h5': new_h5, 'h6': new_h6, 'p': new_p,
                   'get': new_get, 'post': new_post, 'remote_addr': new_remote_addr, 'headers': new_headers, 'get_file': new_get_file}
            for i in new:
                if i in Config.DISABLE_PYTHON_FUNCTIONS:
                    continue
                exec_scope[i] = new[i]
            for func in Config.DISABLE_PYTHON_FUNCTIONS:
                exec_scope[func] = ERROR
            for i in Config.ENABLE_PYTHON_LIBRARIES:
                try:
                    exec_scope[i] = __import__(i)
                except:
                    continue
            exec(text, exec_scope)
        except Exception as e:
            error_msg = html.escape(str(e))
            content = f'<span class="python-error">{error_msg}</span>'
        return content

    i = 0
    depth = 0
    results = []
    current_content = []
    in_tag = False
    in_string = None
    escape_next = False
    new_html_parts = []
    last_index = 0
    while i < len(html):
        char = html[i]
        if escape_next:
            if in_tag and depth > 0:
                current_content.append(char)
            escape_next = False
            i += 1
            continue
        if in_string:
            if in_tag and depth > 0:
                current_content.append(char)
            if char == '\\':
                escape_next = True
            elif char == in_string[0]:
                if in_string in ("'''", '"""'):
                    if i + 2 < len(html) and html[i:i + 3] == in_string:
                        if in_tag and depth > 0:
                            current_content.append(html[i + 1])
                            current_content.append(html[i + 2])
                        in_string = None
                        i += 3
                        continue
                else:
                    in_string = None
            i += 1
            continue
        if char == '<' and i + 4 < len(html) and html[i:i + 4] == '<!--':
            j = i + 4
            while j < len(html) and html[j:j + 3] != '-->':
                j += 1
            if j + 3 <= len(html) and html[j:j + 3] == '-->':
                i = j + 3
                continue
            else:
                i = j
                continue
        if char == '<':
            if i + 1 < len(html) and html[i + 1] == '/':
                j = i + 2
                while j < len(html) and html[j] not in ('>', ' ', '\t', '\n', '\r'):
                    j += 1
                tag = html[i + 2:j].lower()
                k = j
                while k < len(html) and html[k] != '>':
                    k += 1
                if tag == 'python':
                    if depth > 0:
                        depth -= 1
                        if depth == 0 and in_tag:
                            content = ''.join(current_content).strip()
                            content = run_python(content)
                            results.append(content)
                            current_content = []
                            in_tag = False
                            new_html_parts.append(content)
                            last_index = k + 1
                i = k + 1 if k < len(html) else i + 1
                continue
            else:
                start_tag_index = i
                j = i + 1
                while j < len(html) and html[j] not in ('>', ' ', '\t', '\n', '\r', '/'):
                    j += 1
                tag = html[i + 1:j].lower()
                self_closing = False
                k = j
                while k < len(html) and html[k] != '>':
                    if html[k] == '/' and (k + 1 < len(html) and html[k + 1] == '>'):
                        self_closing = True
                    k += 1
                if k < len(html) and html[k] == '>':
                    end_tag_index = k + 1
                    if tag == 'python':
                        if self_closing:
                            results.append('')
                            new_html_parts.append(html[last_index:start_tag_index])
                            last_index = end_tag_index
                        else:
                            if depth == 0:
                                in_tag = True
                                new_html_parts.append(html[last_index:start_tag_index])
                                last_index = end_tag_index
                            depth += 1
                    i = end_tag_index
                else:
                    i = k
                continue
        if char in ("'", '"'):
            if i + 2 < len(html) and html[i:i + 3] == char * 3:
                in_string = char * 3
                if in_tag and depth > 0:
                    current_content.append(char)
                    current_content.append(char)
                    current_content.append(char)
                i += 3
                continue
            else:
                in_string = char
                if in_tag and depth > 0:
                    current_content.append(char)
                i += 1
                continue
        if in_tag and depth > 0:
            current_content.append(char)
        i += 1
    if in_tag and depth > 0 and current_content:
        content = ''.join(current_content).strip()
        results.append(content)
        content = run_python(content)
        new_html_parts.append(content)
    if last_index < len(html):
        new_html_parts.append(html[last_index:])
    new_html = ''.join(new_html_parts)
    return (results, new_html)

# ================
# PHP Interpreter
# ================

def run_php(filepath):
    filepath = filepath.replace('\\','/')
    filename = filepath.split('/')[-1]
    env = {
        'GATEWAY_INTERFACE': 'CGI/1.1',
        'SERVER_SOFTWARE': 'Flask/PyServe',
        'SERVER_NAME': request.host.split(':')[0],
        'SERVER_PORT': str(request.host.split(':')[1] if ':' in request.host else '80'),
        'SERVER_PROTOCOL': request.environ.get('SERVER_PROTOCOL', 'HTTP/1.1'),
        'REQUEST_URI': request.full_path,
        'REMOTE_ADDR': request.remote_addr,
        'REMOTE_HOST': request.remote_addr,
        'SCRIPT_NAME': request.path,
        'SCRIPT_FILENAME': os.path.abspath(filepath),
        'DOCUMENT_ROOT': os.path.abspath(Config.WWW_ROOT),
        'REQUEST_METHOD': request.method,
        'QUERY_STRING': request.query_string.decode('utf-8'),
        'CONTENT_TYPE': request.headers.get('Content-Type', ''),
        'REDIRECT_STATUS': '0', 
        'HTTP_USER_AGENT': request.headers.get('User-Agent', ''),
        'HTTP_ACCEPT': request.headers.get('Accept', ''),
        'HTTP_ACCEPT_LANGUAGE': request.headers.get('Accept-Language', ''),
        'HTTP_ACCEPT_ENCODING': request.headers.get('Accept-Encoding', ''),
        'HTTP_CONNECTION': request.headers.get('Connection', ''),
        'HTTP_HOST': request.headers.get('Host', ''),
        'PATH_INFO': filename,
        **os.environ
    }
    stdin_data = None
    if request.method in ['POST', 'PUT', 'PATCH']:
        content_type = request.content_type
        if 'application/x-www-form-urlencoded' in content_type:
            stdin_data = request.get_data()
        elif 'multipart/form-data' in content_type:
            stdin_data = request.get_data()
        elif 'application/json' in content_type:
            stdin_data = request.get_data()
        else:
            stdin_data = request.get_data()
        env['CONTENT_LENGTH'] = str(len(stdin_data)) if stdin_data else '0'
    app.logger.debug(f"PHP Request: {env}")
    app.logger.debug(f"POST Data: {stdin_data}")
    try:
        result = subprocess.run(
            [Config.PHP_CGI_PATH],
            env=env,
            input=stdin_data if stdin_data else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        app.logger.debug(f"PHP Exit Code: {result.returncode}")
        app.logger.debug(f"PHP Output: {result.stdout[:200]}")
        app.logger.debug(f"PHP Error: {result.stderr[:200]}")

        if result.returncode != 0:
            error_msg = result.stderr.decode('utf-8', 'ignore') or "Unknown PHP error"
            return f"PHP Execution Error (Code {result.returncode}): {error_msg}", 500

        output = result.stdout

        if b'\r\n\r\n' in output:
            headers, body = output.split(b'\r\n\r\n', 1)
        else:
            headers = b''
            body = output
        response = Response(body)

        if headers:
            for line in headers.split(b'\r\n'):
                if b':' in line:
                    key, value = line.split(b':', 1)
                    if key.strip().decode().lower() not in ['status', 'connection']:
                        response.headers[key.strip().decode()] = value.strip().decode()

        if 'Content-Type' not in response.headers:
            response.headers['Content-Type'] = 'text/html; charset=utf-8'
        
        return response, body.decode()

    except Exception as e:
        app.logger.error(f"Server Error: {str(e)}")
        return f"Server Error: {str(e)}", 500


# ================
# pp File
# ================

def run_pp(file_path):
    html = run_php(file_path)[1]
    return extract_all_python_tags(html)[1]

# ================
# Helper Functions
# ================

def get_file_extension(path):
    """Extract file extension from path in lowercase"""
    return path.split('.')[-1].lower() if '.' in path else ''


def is_allowed_file(path, extensions):
    """Check if file exists and has allowed extension"""
    ext = get_file_extension(path)
    return os.path.isfile(path) and ext in extensions


def serve_file(path, content_type, as_attachment=False):
    """Serve file with proper Content-Type header"""
    try:
        with open(path, 'rb') as f:
            content = f.read()
    except IOError:
        return serve_error_page(404)

    response = make_response(content)
    response.headers['Content-Type'] = content_type
    if as_attachment:
        filename = os.path.basename(path)
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def serve_large_file(path, content_type, as_attachment=False):
    """Serve large files using streaming to avoid memory issues"""
    try:
        # Get file size for Content-Length header
        file_size = os.path.getsize(path)
        
        # Check if we should use streaming based on file size
        if file_size < Config.LARGE_FILE_THRESHOLD:
            # For smaller files, use the regular function
            return serve_file(path, content_type, as_attachment)
        
        # For large files, use streaming
        def generate():
            with open(path, 'rb') as f:
                while True:
                    chunk = f.read(Config.CHUNK_SIZE)
                    if not chunk:
                        break
                    yield chunk
        
        response = Response(
            generate(),
            mimetype=content_type,
            direct_passthrough=True
        )
        
        # Set headers
        response.headers['Content-Length'] = file_size
        response.headers['Accept-Ranges'] = 'bytes'
        
        if as_attachment:
            filename = os.path.basename(path)
            response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
        
    except IOError:
        return serve_error_page(404)


def serve_error_page(status_code):
    """Serve appropriate error page"""
    error_page = (Config.WWW_ROOT+os.path.join(Config.ERROR_DIR.replace('\\','/'), f'{status_code}.html')).replace('\\','/')
    print(error_page)
    if os.path.exists(error_page):
        with open(error_page, 'r', encoding=Config.ENCODING) as f:
            return f.read(), status_code
    return f"Error {status_code}", status_code


def generate_directory_listing(path, url_path):
    """Generate HTML directory listing"""
    if not Config.DIR_LISTING:
        return serve_error_page(403)

    items = []
    parent_dir = os.path.dirname(url_path.rstrip('/'))

    # Add parent directory link
    if parent_dir != url_path:
        items.append('<li><a href="../">Parent Directory</a></li>')

    # Add directory contents
    try:
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)
            item_url = os.path.join(url_path, item)

            if os.path.isdir(item_path):
                items.append(f'<li><a href="{item_url}/">{item}/</a></li>')
            else:
                items.append(f'<li><a href="{item_url}">{item}</a></li>')
    except OSError:
        return serve_error_page(403)

    listing = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Index of {url_path}</title>
    <style>
        body {{ font-family: sans-serif; line-height: 1.5; }}
        ul {{ list-style-type: none; padding-left: 20px; }}
        a {{ text-decoration: none; color: #0366d6; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Index of {url_path}</h1>
    <ul>
        {"".join(items)}
    </ul>
</body>
</html>
"""
    return listing


def log_request():
    """Log request details to file and console"""
    if not os.path.exists(Config.LOG_DIR):
        os.makedirs(Config.LOG_DIR)

    log_date = datetime.datetime.now().strftime('%Y-%m-%d')
    log_file = os.path.join(Config.LOG_DIR, f'{log_date}.log')

    log_entry = {
        'timestamp': datetime.datetime.now().isoformat(),
        'ip': request.remote_addr,
        'method': request.method,
        'path': request.path,
        'url': request.url,
        'user_agent': request.headers.get('User-Agent'),
        'status': getattr(request, 'status_code', 200)
    }

    log_str = str(log_entry)
    print(f"\n{log_str}\n")

    with open(log_file, 'a', encoding=Config.ENCODING) as f:
        f.write(log_str + '\n')


# ================
# Request Handlers
# ================

@app.before_request
def before_request():
    """Log all requests"""
    log_request()


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS'])
def serve(path):
    """Main request handler"""
    Config.WWW_ROOT = Config.WWW_ROOT.replace('/','\\')
    fs_path = os.path.join(Config.WWW_ROOT, path)
    if os.path.isdir(fs_path):
        # Check for index files
        for index_file in Config.HTML_EXTENSIONS:
            index_path = os.path.join(fs_path, 'index.'+index_file)
            if os.path.exists(index_path):
                if index_file == 'pys':
                    with open(index_path, 'r', encoding=Config.ENCODING) as f:
                        html_content = f.read()
                    return extract_all_python_tags(html_content)[1]
                if index_file == 'php':
                    return run_php(index_path)[1]
                if index_file == 'pp':
                    return run_pp(index_path)
                return serve_file(index_path, 'text/html')
        # Generate directory listing if no index file found
        return generate_directory_listing(fs_path, '/' + path)

    # Handle file requests
    if os.path.isfile(fs_path):
        ext = get_file_extension(fs_path).lower()
        # HTML files
        if ext in Config.HTML_EXTENSIONS:
            if ext == 'pys':
                with open(fs_path, 'r', encoding=Config.ENCODING) as f:
                    html_content = f.read()
                return extract_all_python_tags(html_content)[1]
            if ext == 'php':
                return run_php(fs_path)[1]
            if ext == 'pp':
                return run_pp(fs_path)
            return serve_file(fs_path, 'text/html')

        # Images
        elif ext in Config.IMAGE_EXTENSIONS:
            return serve_large_file(fs_path, Config.MIME_TYPES.get(ext, 'image/' + ext))

        # Videos
        elif ext in Config.VIDEO_EXTENSIONS:
            return serve_large_file(fs_path, Config.MIME_TYPES.get(ext, 'video/' + ext))

        # Audio
        elif ext in Config.AUDIO_EXTENSIONS:
            return serve_large_file(fs_path, Config.MIME_TYPES.get(ext, 'audio/' + ext))

        # Fonts
        elif ext in Config.FONT_EXTENSIONS:
            return serve_large_file(fs_path, Config.MIME_TYPES.get(ext, 'application/octet-stream'))

        # Downloadable files
        elif ext in Config.DOWNLOAD_EXTENSIONS:
            return serve_large_file(fs_path, Config.MIME_TYPES.get(ext, 'application/octet-stream'), as_attachment=True)

        # Other files
        else:
            # Try to determine MIME type or fall back to octet-stream
            mime_type = Config.MIME_TYPES.get(ext, 'application/octet-stream')
            return serve_large_file(fs_path, mime_type)

    # File not found
    return serve_error_page(404)

for code in [400, 401, 403, 404, 405, 406, 408, 409, 410,
             411, 412, 413, 414, 415, 416, 417, 418, 422,
             423, 424, 428, 429, 431, 451, 500, 501, 502,
             503, 504, 505]:
    @app.errorhandler(code)
    def generic_error(e, status_code=code):
        return serve_error_page(status_code)

# ================
# Main Execution
# ================

if __name__ == "__main__":
    print(f"Starting server on port {Config.PORT}")
    app.run(host='0.0.0.0', port=Config.PORT)


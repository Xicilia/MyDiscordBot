from datetime import datetime

def simpleLog(prefix: str, text: str):
    """
    Creates a log entry with prefix
    
    :param prefix: Log entry prefix with brackets
    :param text: Log text
    """
    
    print(f"[{datetime.now().strftime('%d.%m.%Y - %H:%M:%S')}][{prefix}] {text}")
    
def errorLog(prefix: str, text: str):
    """
    Creates a log with error prefix (shortcut for error logs)
    """
    
    simpleLog(f"[ERROR]{prefix}", text)
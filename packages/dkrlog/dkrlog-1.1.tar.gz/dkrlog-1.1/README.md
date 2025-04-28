## **Dkr Log**

> This Python library is designed to standardize all logs_exceptions that a Python application may encounter. By implementing a uniform logging system, it ensures consistency in how errors are displayed in the terminal and recorded in an external database. Not only does it enhance readability and debugging efficiency, but it also provides structured error tracking for improved application maintenance.

<br>

### **Installation**

```plaintext
pip install dkrlog
```

<br>

### **Configuration**

Before using this library, it is necessary to define specific environment variables that facilitate logging and error tracking:

- **LOGGER_URL**: The URL to which logs will be sent.
- **LOGGER_TOKEN**: The authentication token used in API requests.

Additionally, the following function must be executed at the beginning of the code to set up the execution ID, as it will be used in all log entries:

```python
def set_vars(exec_id: str, app_name:str):
    ''' Define o ID da execução '''
    global EXEC_ID, APPLICATION_NAMESPACE

    EXEC_ID = exec_id # The execution ID will be used to identify the execution in the destination database.
    APPLICATION_NAMESPACE = app_name # The name by which the application will be identified in the destination database.
```

> This execution ID and application  name **must** be populated with the information at the start of the program, ensuring that all logs maintain consistency throughout the application's lifecycle.

### **Usage**

```python
from dkrlog import log_exception, log, set_vars, set_logfile, get_date

# Initialize the execution ID at the beginning of your script
set_vars("your_execution_id")

# Set up a log file (optional but recommended)
set_logfile("execution_log")

# == Logging messages and exceptions ==

# Standard log message:
log("This is an informational message", type="i")

# Logging exceptions within a try-except block:
try:
    # Some operation that may fail
    result = 10 / 0
except Exception as e:
    log_exception("An error occurred while processing", e)

# By following these steps, all logs will be properly recorded in the terminal, saved to log files, and sent to the external logging API
```

## **License**

This project is licensed under the MIT License.
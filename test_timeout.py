import sys
import signal
from pytholog import KnowledgeBase

# Set a timeout to prevent hanging
def timeout_handler(signum, frame):
    raise TimeoutError("Query timed out!")

# Windows doesn't support signal.SIGALRM, so we'll just try it without timeout for now
kb = KnowledgeBase("test")

# Add the fact
kb([
    "nonempty([_|_])"
])

print("Knowledge base loaded. Attempting query...")

# Try the query
try:
    result = kb.query("nonempty([a])")
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

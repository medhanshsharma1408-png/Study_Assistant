import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import uvicorn

print("Python path:", sys.path[0])
print("Files here:", os.listdir(sys.path[0]))

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
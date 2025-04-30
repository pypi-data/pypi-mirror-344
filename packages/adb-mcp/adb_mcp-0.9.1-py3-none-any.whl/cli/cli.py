import subprocess
import sys

def main():
    subprocess.run(["mcp", "run", "main.py"] + sys.argv[1:], check=True)

if __name__ == "__main__":
    main()

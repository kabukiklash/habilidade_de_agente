import subprocess
import sys
import os

def run_in_sandbox(image, command, workdir="/workspace"):
    cwd = os.getcwd()
    docker_cmd = [
        "docker", "run", "--rm",
        "-v", f"{cwd}:{workdir}",
        "-w", workdir,
        image
    ] + command.split()
    
    try:
        print(f"Executing in sandbox ({image}): {command}")
        result = subprocess.run(docker_cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error in sandbox: {e.stderr}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python sandbox_run.py <image> <command>")
        sys.exit(1)
    
    img = sys.argv[1]
    cmd = " ".join(sys.argv[2:])
    output = run_in_sandbox(img, cmd)
    if output:
        print(output)

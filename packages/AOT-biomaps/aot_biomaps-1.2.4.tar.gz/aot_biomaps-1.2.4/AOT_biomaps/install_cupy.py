import subprocess
import sys

def get_cuda_version():
    try:
        result = subprocess.run(['nvcc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            version_line = [line for line in result.stdout.split('\n') if 'release' in line][0]
            cuda_version = version_line.split(' ')[-1].replace(',', '')
            return cuda_version
    except FileNotFoundError:
        return None

def install_cupy():
    cuda_version = get_cuda_version()
    if cuda_version:
        cuda_major_minor = ''.join(cuda_version.split('.')[:2])  # e.g., '11.2' becomes '112'
        print(f"Installing CuPy with CUDA {cuda_version} support...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', f'cupy-cuda{cuda_major_minor}'], check=True)
    else:
        print("CUDA not found. Installing CPU version of CuPy...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'cupy'], check=True)

if __name__ == "__main__":
    install_cupy()

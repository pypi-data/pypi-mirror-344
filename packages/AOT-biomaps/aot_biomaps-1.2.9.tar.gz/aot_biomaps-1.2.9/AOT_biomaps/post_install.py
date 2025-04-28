import subprocess
import sys

def get_cuda_version():
    print("Checking CUDA version...")
    try:
        result = subprocess.run(['nvcc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            version_line = [line for line in result.stdout.split('\n') if 'release' in line][0]
            cuda_version = version_line.split(' ')[-1].replace(',', '')
            print(f"CUDA version detected: {cuda_version}")
            return cuda_version
    except FileNotFoundError:
        print("nvcc not found. CUDA is not installed or not in PATH.")
        return None

def install_cupy():
    print("Starting CuPy installation process...")
    cuda_version = get_cuda_version()
    if cuda_version:
        cuda_major_minor = ''.join(cuda_version.split('.')[:2])  # e.g., '11.2' becomes '112'
        print(f"Installing CuPy with CUDA {cuda_version} support...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', f'cupy-cuda{cuda_major_minor}'], check=True)
    else:
        print("CUDA not found. Skipping CuPy installation.")

def main():
    install_cupy()

if __name__ == "__main__":
    main()
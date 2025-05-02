from ipykernel import kernelapp as app_module
import time
import platform
import asyncio

if platform.system() == "Windows":
    import msvcrt
else:
    import fcntl


class FileLock:
    def __init__(self, filepath, timeout=10, delay=0.05):
        self.filepath = filepath
        self.timeout = timeout
        self.delay = delay
        self.file = None

    def acquire(self):
        start_time = time.time()
        self.file = open(self.filepath, "a+")
        while True:
            try:
                if platform.system() == "Windows":
                    msvcrt.locking(self.file.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    fcntl.flock(self.file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except (BlockingIOError, OSError):
                if (time.time() - start_time) >= self.timeout:
                    self.file.close()
                    raise TimeoutError(
                        f"Timeout occurred trying to lock {self.filepath}"
                    )
                time.sleep(self.delay)

    def release(self):
        if self.file:
            if platform.system() == "Windows":
                msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
            self.file.close()

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()


class AsyncFileLock:
    def __init__(self, filepath, timeout=10, delay=0.05):
        self.filepath = filepath
        self.timeout = timeout
        self.delay = delay
        self.file = None

    async def acquire(self):
        start_time = time.time()
        self.file = open(self.filepath, "a+")
        while True:
            try:
                if platform.system() == "Windows":
                    msvcrt.locking(self.file.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    fcntl.flock(self.file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except (BlockingIOError, OSError):
                if (time.time() - start_time) >= self.timeout:
                    self.file.close()
                    raise TimeoutError(
                        f"Timeout occurred trying to lock {self.filepath}"
                    )
                await asyncio.sleep(self.delay)
        return None

    async def release(self):
        if self.file:
            if platform.system() == "Windows":
                msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)
            self.file.close()
        return None

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.release()


def load_ipython_extension(ip):
    def juvio(line):
        import subprocess, os, sys

        command = ["uv", "pip"] + line.split()
        try:
            subprocess.check_call(command)
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
        original_no_color = os.environ.get("NO_COLOR", "1")
        os.environ["NO_COLOR"] = "1"
        try:
            result = subprocess.run(
                ["uv", "pip", "freeze", "--no-color"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding="utf-8",
                text=True,
                check=True,
            )
            deps = result.stdout.split("\n")
        except subprocess.CalledProcessError as e:
            print(f"Error: {e}")
            print("Stdout:", e.stdout)
            print("Stderr:", e.stderr)
        finally:
            os.environ["NO_COLOR"] = original_no_color

        notebook_path = os.environ.get("JPY_SESSION_NAME", None)
        if notebook_path is None:
            raise ValueError(
                "No notebook path found in environment variable JPY_SESSION_NAME."
            )
        with FileLock(notebook_path):
            with open(notebook_path, "r+", encoding="utf-8") as f:
                content = f.read()
                blocks = content.split("# ///")
                cells = blocks[2:]
                pyver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
                lines = [
                    "# /// script",
                    f'# requires-python = "=={pyver}"',
                    "# dependencies = [",
                ]
                for d in deps:
                    if len(d) > 0:
                        lines.append(f'#   "{d}",')
                lines.append("# ]\n")
                f.seek(0)
                metadata = "\n".join(lines)
                new = "# ///".join([metadata] + cells)
                f.write(new)
                f.truncate()

    ip.register_magic_function(juvio, "line")


def start():
    kernel_app = app_module.IPKernelApp.instance()
    kernel_app.initialize()
    load_ipython_extension(kernel_app.shell)
    kernel_app.start()

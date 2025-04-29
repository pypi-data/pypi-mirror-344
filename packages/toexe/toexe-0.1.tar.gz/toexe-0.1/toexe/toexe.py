import subprocess
import shutil
import os

class ToExe:
    def __init__(self, filename, onefile=True, windowed=True, icon=None):
        self.filename = filename
        self.onefile = onefile
        self.windowed = windowed
        self.icon = icon

    def is_pyinstaller_installed(self):
        """بررسی می‌کند آیا pyinstaller نصب شده یا نه."""
        return shutil.which("pyinstaller") is not None

    def build(self):
        if not self.is_pyinstaller_installed():
            print("Error: pyinstaller is not installed!")
            print("You can install it with: pip install pyinstaller")
            return

        command = ["pyinstaller"]

        if self.onefile:
            command.append("--onefile")
        if self.windowed:
            command.append("--windowed")
        if self.icon:
            command.append(f"--icon={self.icon}")

        command.append(self.filename)

        full_command = " ".join(command)
        print(f"Running command: {full_command}")

        try:
            subprocess.run(full_command, shell=True, check=True)
            print("Build completed successfully!")

            if self.onefile:
                self.move_exe_and_cleanup()

        except subprocess.CalledProcessError as e:
            print(f"Build failed with error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def move_exe_and_cleanup(self):
        """انتقال فایل exe و پاکسازی فولدرهای اضافی"""
        base_name = os.path.splitext(os.path.basename(self.filename))[0]
        exe_path = os.path.join("dist", base_name + ".exe")

        # اگر فایل exe قبلا وجود داشت، آن را حذف کن
        if os.path.exists(base_name + ".exe"):
            os.remove(base_name + ".exe")
            print(f"Deleted old {base_name}.exe file.")

        if os.path.exists(exe_path):
            # انتقال فایل exe کنار فایل py
            shutil.move(exe_path, base_name + ".exe")
            print(f"Moved {base_name}.exe to project root.")

        # پاک کردن فولدرهای اضافی
        for folder in ["build", "dist"]:
            if os.path.exists(folder):
                shutil.rmtree(folder)
                print(f"Deleted folder: {folder}")

        # پاک کردن فایل spec
        spec_file = base_name + ".spec"
        if os.path.exists(spec_file):
            os.remove(spec_file)
            print(f"Deleted file: {spec_file}")

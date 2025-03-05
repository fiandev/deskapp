import os
import time
import subprocess
import sys

def get_folder_modification_time(folder_path, file_extension=".py"):
    """Get the latest modification time of any file in the folder with the specified extension."""
    latest_time = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(file_extension):
                file_path = os.path.join(root, file)
                mod_time = os.path.getmtime(file_path)
                if mod_time > latest_time:
                    latest_time = mod_time
    
    return latest_time

def run_on_folder_change(folder_path, command, file_extension=".py"):
    """Run a command when any file with the specified extension in the folder changes.
    Force closes any previous process before running the command again."""
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return
        
    print(f"Watching folder '{folder_path}' for changes to *{file_extension} files...")
    print(f"Will run: {command}")
    print("Press Ctrl+C to stop watching.")
    
    last_modified_time = get_folder_modification_time(folder_path, file_extension)
    if os.name == 'nt':  # Windows
        current_process = subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:  # Unix-like systems
        current_process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    
    try:
        while True:
            current_modified_time = get_folder_modification_time(folder_path, file_extension)
            
            if current_modified_time > last_modified_time:
                print(f"\nChange detected at {time.strftime('%H:%M:%S')}!")
                
                # Kill previous process if it exists
                if current_process and current_process.poll() is None:
                    print("Terminating previous process...")
                    
                    # Force close on Windows
                    if os.name == 'nt':
                        subprocess.call(f'taskkill /F /T /PID {current_process.pid}', shell=True)
                    # Force close on Unix-like systems (Linux, macOS)
                    else:
                        import signal
                        os.killpg(os.getpgid(current_process.pid), signal.SIGTERM)
                
                print(f"Running: {command}")
                # Start new process in a way that we can track and terminate it
                if os.name == 'nt':  # Windows
                    current_process = subprocess.Popen(command, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
                else:  # Unix-like systems
                    current_process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
                
                last_modified_time = current_modified_time
                print(f"Watching again... (Press Ctrl+C to stop)")
            
            time.sleep(1)
    except KeyboardInterrupt:
        # Make sure to terminate the process when the script is interrupted
        if current_process and current_process.poll() is None:
            print("\nTerminating running process...")
            if os.name == 'nt':
                subprocess.call(f'taskkill /F /T /PID {current_process.pid}', shell=True)
            else:
                import signal
                os.killpg(os.getpgid(current_process.pid), signal.SIGTERM)
        print("\nWatching stopped.")

if __name__ == "__main__":
    # Default values
    folder_to_watch = "."  # Current directory
    command_to_run = "python main.py"
    file_ext = ".py"
    
    # Get command line arguments if provided
    if len(sys.argv) > 1:
        folder_to_watch = sys.argv[1]
    if len(sys.argv) > 2:
        command_to_run = sys.argv[2]
    if len(sys.argv) > 3:
        file_ext = sys.argv[3]
    
    # Run the watcher
    run_on_folder_change(folder_to_watch, command_to_run, file_ext)
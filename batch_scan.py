import subprocess
import shutil
import sys

# Function to execute rapidscan.py for each website sequentially
def run_scans_sequentially(websites, output_file):
    for website in websites:
        print(f"Launching scan for {website} in a new terminal...")
        
        # Format the website name for the log file
        website_header = f"\n--- Scanning: {website} ---\n"

        try:
            # Write the website header to the output file
            with open(output_file, "a") as file:
                file.write(website_header)

            # Command for xterm with real-time output display
            if shutil.which("xterm"):
                subprocess.run(
                    [
                        "xterm", 
                        "-e", 
                        f"bash -c 'echo \"{website_header}\"; python3 rapidscan.py {website} | tee -a {output_file}; exit'"
                    ],
                    check=True,
                )
            # Fallback to gnome-terminal with real-time output display
            elif shutil.which("gnome-terminal"):
                subprocess.run(
                    [
                        "gnome-terminal", 
                        "--", 
                        "bash", 
                        "-c", f'echo "{website_header}"; python3 rapidscan.py {website} | tee -a {output_file}; exit'
                    ],
                    check=True,
                )
            else:
                print("No suitable terminal emulator found. Install xterm or gnome-terminal.")
                return

            print(f"Scan for {website} completed.")
        except Exception as e:
            print(f"Error launching terminal for {website}: {e}")

# Main script logic
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 batch_scan.py <websites_file>")
        sys.exit(1)

    websites_file = sys.argv[1]
    output_file = "scan_results.txt"

    # Read websites from file
    try:
        with open(websites_file, "r") as file:
            websites = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {websites_file} not found.")
        sys.exit(1)

    if not websites:
        print("No websites found in the file. Exiting.")
        sys.exit(1)

    print(f"Scanning {len(websites)} websites sequentially. Results will be saved to {output_file}.")
    run_scans_sequentially(websites, output_file)

import subprocess
import json
import time

# Define the command to run
command = ["sudo", "batctl", "n"]  # Example command to list neighbors

# Set the loop count and delay interval
loop_count = 10
delay_interval = 1  # Seconds

for _ in range(loop_count):
  # Run the command using subprocess.run()
  try:
    completed_process = subprocess.run(command, capture_output=True, text=True)
    # Check the return code (0 for success)
    if completed_process.returncode == 0:
      print("Command '{}' executed successfully!".format(" ".join(command)))

      # Process the output
      output_text = completed_process.stdout.strip()
      if output_text:
        lines = output_text.split("\n")[2:]  # Skip header lines

        # Initialize empty list for neighbor data
        neighbor_data_list = []

        for line in lines:
          # Split line by spaces
          parts = line.split()
          if len(parts) == 3:
            # Extract neighbor data
            neighbor_data = {
                "IF": parts[0],
                "Neighbor MAC": parts[1],
                "Last Seen": parts[2]
            }
            # Add dictionary to list
            neighbor_data_list.append(neighbor_data)

        # Convert list to JSON string
        json_data = json.dumps(neighbor_data_list, indent=4)
        print(json_data)
      else:
        print("No neighbors detected by 'batctl n'")
    else:
      print("Command '{}' failed with return code: {}".format(" ".join(command), completed_process.returncode))
  except subprocess.CalledProcessError as error:
    print("Error occurred:", error)

  # Add a one-second delay between iterations
  time.sleep(delay_interval)

print("Loop completed.")

# import json
# import time

# def monitor_bgp(file_path, baseline_file):
#     # Load baseline routes
#     with open(baseline_file, 'r') as bl:
#         baseline = json.load(bl)

#     while True:
#         with open(file_path, 'r') as file:
#             current_config = json.load(file)
#             missing_routes = [route for route in baseline["routes"] if route not in current_config["routes"]]
#             if missing_routes:
#                 print(f"ALERT: Missing routes detected: {missing_routes}")
#                 generate_error_report(missing_routes)
#         time.sleep(10)  # Check every 10 seconds

# def generate_error_report(missing_routes):
#     with open("logs/error_report.log", "a") as log:
#         log.write(f"Missing routes: {missing_routes}\n")
#         print(f"Error report generated for missing routes: {missing_routes}")

# if __name__ == "__main__":
#     monitor_bgp("configs/faulty_bgp.json", "configs/baseline_bgp.json")

import json
import time

def monitor_bgp(file_path, baseline_file):
    # Load baseline routes
    with open(baseline_file, 'r') as bl:
        baseline = json.load(bl)

    print("Starting BGP monitoring...")
    while True:
        try:
            with open(file_path, 'r') as file:
                current_config = json.load(file)
                missing_routes = [route for route in baseline["routes"] if route not in current_config["routes"]]

                if missing_routes:
                    print(f"ALERT: Missing routes detected: {missing_routes}")
                    generate_error_report(missing_routes)
                else:
                    print("No anomalies detected.")

        except Exception as e:
            print(f"Error reading file: {e}")

        # Ensure the loop doesn't block forever
        time.sleep(5)  # Check every 5 seconds

def generate_error_report(missing_routes):
    with open("logs/error_report.log", "a") as log:
        log.write(f"Missing routes: {missing_routes}\n")
        print(f"Error report generated for missing routes: {missing_routes}")

if __name__ == "__main__":
    monitor_bgp("configs/faulty_bgp.json", "configs/baseline_bgp.json")

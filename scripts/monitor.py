# import json
# import time

# def monitor_bgp(file_path, baseline_file):
#     # Load baseline routes
#     with open(baseline_file, 'r') as bl:
#         baseline = json.load(bl)

#     print("Starting BGP monitoring...")
#     while True:
#         try:
#             with open(file_path, 'r') as file:
#                 current_config = json.load(file)
#                 missing_routes = [route for route in baseline["routes"] if route not in current_config["routes"]]

#                 if missing_routes:
#                     print(f"ALERT: Missing routes detected: {missing_routes}")
#                     generate_error_report(missing_routes)
#                 else:
#                     print("No anomalies detected.")

#         except Exception as e:
#             print(f"Error reading file: {e}")

#         # Ensure the loop doesn't block forever
#         time.sleep(5)  # Check every 5 seconds

# def generate_error_report(missing_routes):
#     with open("logs/error_report.log", "a") as log:
#         log.write(f"Missing routes: {missing_routes}\n")
#         print(f"Error report generated for missing routes: {missing_routes}")

# if __name__ == "__main__":
#     monitor_bgp("configs/faulty_bgp.json", "configs/baseline_bgp.json")

import json
import time
from threading import Thread
import matplotlib.pyplot as plt

def monitor_bgp(file_path, baseline_file):
    with open(baseline_file, 'r') as bl:
        baseline = json.load(bl)

    print("Starting BGP monitoring...")
    while True:
        try:
            with open(file_path, 'r') as file:
                current_config = json.load(file)
                missing_routes = [route for route in baseline["routes"] if route not in current_config["routes"]]
                
                threshold = 0.2
                if len(missing_routes) / len(baseline["routes"]) > threshold:
                    print(f"ALERT: Missing routes exceed threshold: {missing_routes}")
                    generate_error_report(missing_routes)
                    visualize_routes(missing_routes, len(baseline["routes"]))

                    choice = input("Would you like to apply the suggested fix? (yes/no): ").strip().lower()
                    if choice == "yes":
                        from rollback import rollback_to_backup
                        rollback_to_backup("configs/baseline_bgp.json", file_path)
                    else:
                        print("No action taken.")
                else:
                    print("No significant anomalies detected.")
        except Exception as e:
            print(f"Error reading file: {e}")
        time.sleep(5)

def generate_error_report(missing_routes):
    with open("logs/error_report.log", "a") as log:
        log.write(f"Missing routes: {missing_routes}\n")
        print(f"Error report generated for missing routes: {missing_routes}")

def visualize_routes(missing_routes, total_routes):
    labels = ["Active Routes", "Missing Routes"]
    sizes = [total_routes - len(missing_routes), len(missing_routes)]
    colors = ["green", "red"]
    plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
    plt.title("Route Health")
    plt.show()

if __name__ == "__main__":
    monitor_bgp("configs/faulty_bgp.json", "configs/baseline_bgp.json")

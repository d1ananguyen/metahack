import json
import time
from threading import Thread

def monitor_bgp(region, active_file, baseline_file):
    with open(baseline_file, 'r') as bl:
        baseline = json.load(bl)

    print(f"Monitoring {region}...")

    while True:
        try:
            with open(active_file, 'r') as af:
                active_config = json.load(af)
                missing_routes = [route for route in baseline["routes"] if route not in active_config["routes"]]

                if missing_routes:
                    print(f"ALERT for {region}: Missing routes: {missing_routes}")
                    generate_error_report(region, missing_routes)
                else:
                    print(f"{region}: All routes healthy.")
        except Exception as e:
            print(f"Error monitoring {region}: {e}")

        time.sleep(10)

def generate_error_report(region, missing_routes):
    with open("logs/error_report.log", "a") as log:
        log.write(f"{region}: Missing routes: {missing_routes}\n")

if __name__ == "__main__":
    regions = {
        "North America": {
            "active": "configs/active_bgp_north_america.json",
            "baseline": "configs/baseline_north_america.json"
        },
        "Europe": {
            "active": "configs/active_bgp_europe.json",
            "baseline": "configs/baseline_europe.json"
        },
        "Asia": {
            "active": "configs/active_bgp_asia.json",
            "baseline": "configs/baseline_asia.json"
        }
    }

    threads = []
    for region, files in regions.items():
        t = Thread(target=monitor_bgp, args=(region, files["active"], files["baseline"]))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


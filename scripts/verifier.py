import json
from deploy import deploy_config

def verify_bgp_config(new_config_file, baseline_files):
    validation_results = {}

    for region, baseline_file in baseline_files.items():
        try:
            # Load new config and baseline for the region
            with open(new_config_file, 'r') as nc, open(baseline_file, 'r') as bl:
                new_config = json.load(nc)
                baseline = json.load(bl)

            # Check for missing routes
            missing_routes = [route for route in baseline["routes"] if route not in new_config["routes"]]
            if missing_routes:
                validation_results[region] = {
                    "status": "Invalid",
                    "missing_routes": missing_routes
                }
            else:
                validation_results[region] = {
                    "status": "Valid",
                    "missing_routes": []
                }

        except FileNotFoundError as e:
            validation_results[region] = {
                "status": "Error",
                "error": str(e)
            }
            print(f"Error: Missing file for {region}: {baseline_file}")

    # Log validation results
    log_validation_results(validation_results)

    # Deploy only valid configurations
    for region, result in validation_results.items():
        if result["status"] == "Valid":
            print(f"{region}: Configuration valid. Deploying...")
            deploy_config(new_config_file, f"configs/active_bgp_{region}.json")
        elif result["status"] == "Invalid":
            print(f"{region}: Configuration invalid. Missing routes: {result['missing_routes']}")
        else:
            print(f"{region}: Validation skipped due to errors.")

def log_validation_results(results):
    with open("logs/validation_log.log", "a") as log:
        for region, result in results.items():
            log.write(f"{region}: {result['status']}\n")
            if result["missing_routes"]:
                log.write(f"  Missing routes: {result['missing_routes']}\n")
            if "error" in result:
                log.write(f"  Error: {result['error']}\n")

if __name__ == "__main__":
    baselines = {
        "North America": "configs/baseline_north_america.json",
        "Europe": "configs/baseline_europe.json",
        "Asia": "configs/baseline_asia.json"
    }
    verify_bgp_config("configs/new_bgp.json", baselines)

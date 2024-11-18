# import json

# def verify_bgp_config(new_config_file, baseline_file):
#     # Load configurations
#     with open(new_config_file, 'r') as nc, open(baseline_file, 'r') as bl:
#         new_config = json.load(nc)
#         baseline = json.load(bl)

#     # Check for missing critical routes
#     missing_routes = [route for route in baseline["routes"] if route not in new_config["routes"]]
#     if missing_routes:
#         print(f"Configuration invalid. Missing critical routes: {missing_routes}")
#         return False
#     print("Configuration valid.")
#     return True

# if __name__ == "__main__":
#     verify_bgp_config("configs/new_bgp.json", "configs/baseline_bgp.json")

import json
from deploy import deploy_config

def verify_bgp_config(new_config_file, baseline_file):
    with open(new_config_file, 'r') as nc, open(baseline_file, 'r') as bl:
        new_config = json.load(nc)
        baseline = json.load(bl)

    missing_routes = [route for route in baseline["routes"] if route not in new_config["routes"]]
    if missing_routes:
        print(f"Configuration invalid. Missing critical routes: {missing_routes}")
        return False

    print("Configuration valid. Deploying now...")
    deploy_config(new_config_file, "configs/active_bgp.json")
    return True

if __name__ == "__main__":
    verify_bgp_config("configs/new_bgp.json", "configs/baseline_bgp.json")

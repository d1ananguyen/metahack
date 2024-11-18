import shutil

def deploy_config(new_config_file, active_config_file):
    shutil.copy(new_config_file, active_config_file)
    print(f"Configuration deployed successfully: {new_config_file}")

if __name__ == "__main__":
    deploy_config("configs/new_bgp.json", "configs/active_bgp_north_america.json")

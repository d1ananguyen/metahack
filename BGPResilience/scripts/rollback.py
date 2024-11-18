import shutil

def rollback_to_backup(backup_file, current_file):
    shutil.copy(backup_file, current_file)
    print(f"Rollback successful. Restored to {backup_file}.")

if __name__ == "__main__":
    rollback_to_backup("configs/baseline_bgp.json", "configs/faulty_bgp.json")

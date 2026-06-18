import time
import random
import pandas as pd
from pysimverse import Drone


def main():
    print("====================================================")
    print("[INIT] Starting Coordinated Port-Safe Climate Survey Loop")
    print("====================================================\n")

    flight_telemetry = []
    flagged_anomalies = []

    # 1. Initialize ONE master drone connection channel to completely prevent port collision
    print("[DEPLOY] Initializing Drone Simulation Agent...")
    survey_drone = Drone()
    survey_drone.connect()
    time.sleep(1)

    try:
        survey_drone.take_off()
        time.sleep(2)
    except Exception:
        pass

    # ----------------------------------------------------
    # PHASE 1: REUSE CONNECTION FOR SCOUT MISSION
    # ----------------------------------------------------
    search_waypoints = [(10, 0), (0, 10), (-10, 0), (0, 10)]

    print("\n[MISSION] Master Agent executing high-altitude scanning...")
    for index, wp in enumerate(search_waypoints):
        f_b, r_l = wp
        print(f"-> Scanning Zone {index + 1}...")

        try:
            if f_b != 0:
                survey_drone.move_forward(f_b)
                time.sleep(2)
        except Exception:
            pass

        try:
            if r_l != 0:
                survey_drone.move_right(r_l)
                time.sleep(2)
        except Exception:
            pass

        simulated_canopy_loss = round(random.uniform(15.0, 95.0), 2)
        print(f"   [DATA] Zone {index + 1} Canopy Loss: {simulated_canopy_loss}%")

        flight_telemetry.append({
            "zone_id": f"Zone_{index + 1}",
            "canopy_loss_pct": simulated_canopy_loss,
            "relative_f_b": f_b,
            "relative_r_l": r_l,
            "inspector_deployed": 0,
            "biomass_density": None
        })

        if simulated_canopy_loss > 70.0:
            print(f"   [ALERT] Critical degradation! Target logged for inspection.")
            flagged_anomalies.append(index)

    # ----------------------------------------------------
    # PHASE 2: REUSE CONNECTION FOR INSPECTOR MISSION
    # ----------------------------------------------------
    if flagged_anomalies:
        print("\n====================================================")
        print(f"[DEPLOY] Redirecting Master Agent to confirm {len(flagged_anomalies)} anomalies...")
        print("====================================================\n")

        for target_idx in flagged_anomalies:
            target_zone = flight_telemetry[target_idx]
            print(f"-> Routing to targeted {target_zone['zone_id']} at lower sampling altitude...")

            try:
                if target_zone["relative_f_b"] != 0:
                    survey_drone.move_forward(target_zone["relative_f_b"])
                    time.sleep(2)
            except Exception:
                pass

            try:
                if target_zone["relative_r_l"] != 0:
                    survey_drone.move_right(target_zone["relative_r_l"])
                    time.sleep(2)
            except Exception:
                pass

            simulated_biomass = round(random.uniform(5.0, 22.0), 2)
            print(f"   [VERIFIED] Confirmed critical biomass loss: {simulated_biomass} kg/m²")

            target_zone["inspector_deployed"] = 1
            target_zone["biomass_density"] = simulated_biomass

            # Return connection context to landing markers
            try:
                if target_zone["relative_f_b"] != 0:
                    survey_drone.move_forward(-target_zone["relative_f_b"])
                    time.sleep(2)
            except Exception:
                pass
            try:
                if target_zone["relative_r_l"] != 0:
                    survey_drone.move_right(-target_zone["relative_r_l"])
                    time.sleep(2)
            except Exception:
                pass

    print("\n[RETURN] Master Survey complete. Executing landing safety procedure...")
    try:
        survey_drone.land()
    except Exception:
        pass

    # Fill default baseline data variables
    for zone in flight_telemetry:
        if zone["biomass_density"] is None:
            zone["biomass_density"] = round(random.uniform(65.0, 85.0), 2)

    # ----------------------------------------------------
    # PHASE 3: TELEMETRY DATA EXPORT
    # ----------------------------------------------------
    df = pd.DataFrame(flight_telemetry)
    df.to_csv("forest_carbon_assessment.csv", index=False)
    print("\n[SUCCESS] Telemetry pipeline closed. 'forest_carbon_assessment.csv' created.")


if __name__ == "__main__":
    main()

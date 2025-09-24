"""
    Python program to create a parflow project directory and populate with the input files
    such as the forcing files and initial pressure and topology files of a HUC domain.
    Then run parflow using that project directory.
"""

import project
import parflow
import hf_hydrodata as hf
import time

def main():
    """
    An example generating a parflow directory and execute model and assert start/end pressure values for a box
    Use a box with radius 5 around the same target point that is the center of HUC 02080203
    """

    duration_start = time.time()

    # Set email and pin of hf_hydrodata to gain access to parflow input files
    hf.register_api_pin("<your_hf_hydrodata_email>, "<your_hf_hydrodata_pin"")
    directory_path = "./demo"

    # Create a parflow project directory populated with input files
    time_steps = 10
    parflow_options = {
        "run_type": "transient",
        "huc_id": "02070001",
        "start_date": "2005-10-01",
        "end_date": "2005-10-02",
        "time_steps": time_steps,
        "topology": [5, 5, 1]
    }
    # Use the utility "create_project" that uses subsettools to get the input files
    runscript_path = project.create_project(parflow_options, directory_path)

    # Run the parflow model
    input_duration = time.time() - duration_start
    parflow_start = time.time()
    model = parflow.Run.from_definition(runscript_path)
    model.run()

    # Print timing
    parflow_duration = time.time() - parflow_start
    full_duration = time.time() - duration_start
    print(f"Duration {input_duration} seconds to collect inputs.")
    print(f"Duration {parflow_duration} seconds to run parflow.")
    print(f"Duration {full_duration} seconds to collect inputs and run parflow.")
    print()

    # Verify the result
    time_step = time_steps - 1
    nx = model.ComputationalGrid.NX
    ny = model.ComputationalGrid.NY
    nz = model.ComputationalGrid.NZ
    x = int(nx / 2)
    y = int(ny / 2)
    z = nz - 1
    out_path = f"{directory_path}/{runname}.out.press.{time_step:05d}.pfb"
    out_press_np = parflow.read_pfb(out_path)
    print(f"OUT PRESS ({z},{y},{x}) {out_press_np[z, y, x]} [{time_step}]")
    top_layer_pressure = out_press_np
    #assert round(top_layer_pressure[z, y, x], 5) == 0.00325

   
main()
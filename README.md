# ftc_dose
A calculation of the dose around the fuel transfer cask (ftc).

File Structure and Description:
 - **input_generator**
    - **given** (files used to start the problem)
        - senior_design.i (the original starting input file)
        - senior_design_mesh.adv (an example advantg script that works for senior_design_mesh.i)
        - senior_design_mesh.i (the original file with a mesh tally imposed)
    - **source_spectra**
        - element_3684.txt (the element we are measuring)
        - hot_element_2989_measured.txt (an example of a hot element [decaying time ~ 10 days])
        - hot_element_3684.txt (another example of a hot element [decaying time ~ 10 days])
        - senior_design_source.txt (the source from the original senior design model)
        - source_plotter.py (a script that plots the source term currently being used)
        - source_terms.png (the plot of the source term)
    - senior_design_template.py (houses the mcnp template)
    - senior_design_writer.py (user inputs case 1 or 2 and outputs an mcnp input file)
 - **case1** (Steel Collimator Inserted, Fuel Rod in Line-of-Sight)
    - case1.adv (advantg input for case1.i)
    - case1.i (mcnp input for case1)
    - case1.qsub (eigendoit submission script for mcnp after advantg has been run)
    - case1_advantg.qsub (eigendoit submission script for case1.adv)
    - convert_to_vtk.py (converts .imsht file from mcnp to vts file for use in visit)
 - **case2** (Collimator Removed, Fuel Rod Raised)
    - all files analagous to **case1**

# How we obtained the shape models:


1.   We manually selected the control points on the initial template mesh and saved them in a csv file.
2.   We manually selected the control points on the final mesh and saved them in a csv file.
3.   Using the csv files we computed the displacements.
4.   We tuned the parameter ϵ of the RBF for each shape model.
5.   We created a script that automatically creates the .geo files.


These are the RBF used for the 4 models:
*   CS: multiquadratic, ϵ = 5
*   CW: [already provided]
*   WS: gaussian, ϵ = 50
*   CF: inverse quadratic, ϵ = 6
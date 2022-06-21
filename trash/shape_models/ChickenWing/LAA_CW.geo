// Coronaries bifurcation

//parameter
sten1 = 0;  // % [0,100]
sten2 = 0;  // %
sten3 = 0;  // %
noise1 = 0;  // % [-1,1]
noise2 = 0;  // % [-1,1]
noise3 = 0;  // % [-1,1]
noise4 = 0;  // % [-1,1]
noise5 = 0;  // % [-1,1]
noise6 = 0;  // % [-1,1]

// local rrefinement
ref1 = 0.02;
ref2 = 0.02;
ref3 = 0.02;

// points
Point(2) = {0, 0, 0, ref1};
Point(3) = {0, 1, 0, ref1};
Point(4) = {1.25, 1.33, 0, ref1};
Point(5) = {2.5, -0.5, 0, ref1};
Point(6) = {2.15, -0.6, 0, ref1};
Point(7) = {1.25, 0.33, 0, ref1};

Spline(1) = {2,7,6,5,4,3};
Line(2) = {3,2};


Physical Curve(1) = {1};
Physical Curve(2) = {2};


Curve Loop(1) = {1,2};


Plane Surface(1) = {1};
Field[2] = BoundaryLayer;
//Field[2].FanPointsList = {1};
Field[2].CurvesList = {1};
Field[2].SizeFar = 1.5;
Field[2].Size = 0.008;
Field[2].Ratio = 1.2;
Field[2].Thickness = .03;

BoundaryLayer Field = 2;

Physical Surface(2) = {1};

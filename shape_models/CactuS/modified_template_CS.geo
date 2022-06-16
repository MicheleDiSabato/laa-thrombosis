ref1 = 0.02;

Point(1) = {0.0,0.0,0,ref1};

Point(20) = {0.306,1.02,0,ref1};
Point(19) = {0.787,1.15,0,ref1};
Point(18) = {1.074,1.388,0,ref1};
Point(17) = {1.351,1.386,0,ref1};
Point(16) = {1.479,1.01,0,ref1};
Point(15) = {1.687,0.834,0,ref1};
Point(14) = {1.883,0.769,0,ref1};
Point(13) = {2.065,0.777,0,ref1};
Point(12) = {2.261,0.657,0,ref1};
Point(11) = {2.245,0.471,0,ref1};
Point(10) = {2.465,0.346,0,ref1};
Point(9) = {2.385,0.085,0,ref1};
Point(8) = {2.093,0.055,0,ref1};
Point(7) = {2.077,-0.246,0,ref1};
Point(6) = {2.285,-0.66,0,ref1};
Point(5) = {2.073,-0.725,0,ref1};
Point(4) = {1.574,-0.319,0,ref1};
Point(3) = {1.44254,-0.10318,0,ref1};
Point(2) = {0.61404,0.18162,0,ref1};

Point(21) = {0.0,1.0,0,ref1};


Spline(1)={21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1};
Line(2)={1,21};

Physical Curve(1) = {1};
Physical Curve(2) = {2};
Curve Loop(1) = {1,2};
Plane Surface(1) = {1};
Field[2] = BoundaryLayer;
Field[2].CurvesList = {1};
Field[2].SizeFar = 1.5;
Field[2].Size = 0.008;
Field[2].Ratio = 1.2;
Field[2].Thickness = .03;
BoundaryLayer Field = 2;
Physical Surface(2) = {1};
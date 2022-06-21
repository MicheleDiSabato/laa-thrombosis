ref1 = 0.02;

Point(1) = {0,0,0,ref1};

Point(21) = {0.39706,1.09317,0,ref1};
Point(20) = {1.0,1.05,0,ref1};
Point(19) = {1.13959,0.99004,0,ref1};
Point(18) = {1.29429,0.86628,0,ref1};
Point(17) = {1.40773,0.71158,0,ref1};
Point(16) = {1.46961,0.61876,0,ref1};
Point(15) = {1.59336,0.495,0,ref1};
Point(14) = {1.68618,0.37124,0,ref1};
Point(13) = {1.779,0.25779,0,ref1};
Point(12) = {1.88212,0.13403,0,ref1};
Point(11) = {1.96463,0.04121,0,ref1};
Point(10) = {2.01619,-0.06193,0,ref1};
Point(9) = {2.1,-0.15,0,ref1};
Point(8) = {2.17476,-0.29913,0,ref1};
Point(7) = {2.0,-0.35,0,ref1};
Point(6) = {1.8123,-0.2623,0,ref1};
Point(5) = {1.6311,-0.1817,0,ref1};
Point(4) = {1.44254,-0.10318,0,ref1};
Point(3) = {0.61404,0.18162,0,ref1};

Point(2) = {0,1,0,ref1};

Spline(1)={2,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,1};
Line(2)={1,2};

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
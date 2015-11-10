// http://www.tridimake.com/2014/09/how-to-use-openscad-tricks-and-tips-to.html
$fa=0.5; // default minimum facet angle is now 0.5
$fs=0.5; // default minimum facet size is now 0.5 mm
p = 2.5;
difference() {
    union() {
        color([1, 0, 0]) sphere(p);
        translate([0,0,p/2]) cylinder(r=p/2, h=p*3, center=false);    
    }
    translate([p,0,0]) cylinder(r=p/2, h=p*3, center=true);
}
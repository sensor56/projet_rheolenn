
module 90BracketMin(){

// 90 degree bracket
// modifié par X. HINAULT - www.mon-club-elec.fr

$fn = 25;
length = 22.5;
width = 20;
walls = 3;

rHole = 2.6;

rotate([90, 0, 0])
difference()
{
    cube([length, length, width], center=true);
    
    translate([4, 4, 0])
    cube([length, length, width-(walls * 2)], center=true);
    
    rotate([0,0,45])
    translate([length/2 + 3, 0, 0])
    cube([length, length + 20, width+2], center= true);
    
    // bottom screw holes
    //translate([length/2 - 8, -length/2 + 5, 0])
    //rotate([90, 0, 0])
    //#cylinder(r=rHole, h=10);

    translate([-length/2 + 16, -length/2 + 5, 0])
    rotate([90, 0, 0])
    #cylinder(r=rHole, h=10);
    
    
    // side screw holes
    //translate([-length/2 - 5, length/2 - 8, 0])
    //rotate([0, 90, 0])
    //#cylinder(r=rHole, h=10);

    translate([-length/2 - 5, -length/2 + 16, 0])
    rotate([0, 90, 0])
    #cylinder(r=rHole, h=10);
}

} // fin module 

90BracketMin();
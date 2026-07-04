size(1600, 1000);


// air
background(#CECECE);


// ground
fill(#7C7C7C);
rect(0, 0.6*height, width, height);


// lava
stroke(#C8643C);
strokeWeight(36);
noFill();
arc(0, 0.6*height, width, 1.5*height, radians(0), radians(60));  // left stream

strokeWeight(24);
arc(width, 0.6*height, width, 0.75*height, radians(90), radians(180)); // right stream
arc(0.5*width, 0.6*height, 0.75*width, 1.5*height, radians(125), radians(175)); // leftmost stream


// mountain range
stroke(0);
strokeWeight(2);

fill(#3E3E3E);  // backmost mountains
triangle(0.1*width, 0.6*height, 0.6*width, 0.6*height, 0.275*width, 0.45*height);  // left mountain
triangle(0.6*width, 0.6*height, 1.2*width, 0.6*height, 0.825*width, 0.425*height);  // right mountain

fill(#5D5D5D);  // background mountains
triangle(0, 0.6*height, 0.1*width, 0.6*height, 0, 0.475*height);  // leftmost mountain
triangle(0, 0.6*height, 0.3*width, 0.6*height, 0.15*width, 0.375*height);  // left mountain
triangle(0.75*width, 0.6*height, width, 0.425*height, width, 0.6*height);  // right mountain
triangle(0.25*width, 0.6*height, 0.9*width, 0.6*height, 0.5*width, 0.225*height);  // middle mountain

fill(#7C7C7C);  // front mountains
triangle(0-50, 0.6*height, 0.275*width, 0.6*height, 0.075*width, 0.4*height);  // left mountain
triangle(0.825*width, 0.6*height, 1.05*width, 0.6*height, 0.925*width, 0.375*height);  // right mountain


// lava stream from mountain
stroke(#D2643C);
strokeWeight(24);
noFill();
arc(width, 0.6*height, width, 1.75*height, radians(180), radians(200));  // top lava stream
strokeWeight(30);
arc(width, 0.6*height, width, 1.75*height, radians(180), radians(195));  // middle lava stream
strokeWeight(36);
arc(width, 0.6*height, width, 1.75*height, radians(180), radians(190));  // bottom lava stream


// lava pool
noStroke();
fill(#C8643C);
ellipse(0.6125*width, 0.8*height, 0.175*width, 0.125*height);
for(int i=1; i<5; i++){
  fill(200-10*i, 100-5*i, 60-2.5*i);
  ellipse(0.6125*width, 0.8*height, 0.175*width-37.5*i, 0.125*height-10*i);
}


// small island on lava pool
stroke(0);
strokeWeight(2);
fill(#3E3E3E);
arc(0.575*width, 0.7975*height, 0.06*width, 0.04*height, radians(180), radians(360));


// dust clouds
noStroke();
fill(#7C7C7C, 160);  // left cloud
ellipse(0.25*width, 0.15*height, 0.15*width, 0.125*height);  // middle ellipse
ellipse(0.2*width, 0.1125*height, 0.125*width, 0.1*height);  // left ellipse
ellipse(0.3*width, 0.1*height, 0.175*width, 0.1*height);  // right ellipse

fill(#7C7C7C, 240);  // right cloud
ellipse(0.75*width, 0.2*height, 0.15*width, 0.125*height);  // middle ellipse
ellipse(0.725*width, 0.15*height, 0.175*width, 0.1125*height);  // left ellipse
ellipse(0.8125*width, 0.175*height, 0.15*width, 0.0875*height);  // right ellipse

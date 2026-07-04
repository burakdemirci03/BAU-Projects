void setup(){
  size(800, 1000);
  background(255);
  
  X=width/2;
  Y=height/6;
}

float X;
float Y;

void draw(){
  background(255);
  drawCharged();
  drawSpike();
  drawBrute();
}
  
 
int angle=0;
float amp=0;
float ampDir=0.1;
void drawCharged(){
  float Y1=Y;
  /* Body */
  noFill();
  strokeWeight(10);
  ellipse(X, Y1, 200, 250);
  
  /* Axis */
  strokeWeight(2);
  for(int i = 0; i < 40; i++){    
    point(X + 100 * cos(radians(0.5*angle+i)), (Y1-50) + 25 * sin(radians(angle+i)));
    point(X + 125 * cos(radians(-angle+i)), (Y1-25) + 50 * sin(radians(-2*angle+i)));
    point(X + 150 * cos(radians(4*angle+i)), Y1 + 100 * sin(radians(3*angle+i)));
    point(X + 125 * cos(radians(-1.5*angle+i)), (Y1+25) + 50 * sin(radians(-2*angle+i)));
    point(X + 100 * cos(radians(angle+i)), (Y1+50) + 25 * sin(radians(5*angle+i)));
  }
  
  /* Charged Axis */
  strokeWeight(12);
  for(int i = 0; i < 20; i++){    
    point(X + 150 * cos(radians(-0.25*angle+3*i)), Y1 + 25 * sin(radians(-0.25*angle+3*i)));
  }
  
  /* Eyes */
  strokeWeight(4);
  for(int i = 0; i < 360; i += 4){    
    float deviationX = 6 * cos(radians(3*angle + 13*i)); 
    float deviationY = 6 * sin(radians(2*angle + 10*i));
    
    float rX = 12.5 + amp;
    float rY = 10 + amp;
    
    point(X - 30 + rX * cos(radians(angle + i)) + deviationX, (Y-25) + rY * sin(radians(angle + i)) + deviationY);
    point(X + 30 + rX * cos(radians(angle + i)) + deviationX, (Y-25) + rY * sin(radians(angle + i)) + deviationY);
  }
  
  angle++;
  amp+=ampDir;
  if (amp < 0 || amp > 3){
    ampDir *= -1;
  }
}


float h=200;
float halfH=h/2;
float b=200;
float halfB=b/2;
float incB=0;
float incH=0;
float speed=1;
int waitDelay=0;
float waitSec=2.5;
void drawSpike(){
  float Y2=3*Y;
  /* Body */
  strokeWeight(10);
  triangle(X-halfB, Y2+halfH, X, Y2-halfH, X+halfB, Y2+halfH);
  line(X-halfB/2, Y2, X+halfB/2, Y2);
  line(X-halfB/4, Y2-halfH/2, X+halfB/4, Y2-halfH/2);
  
  /* Summoned Triangles */
  int summonH=50;
  int summonB=10;
  float summonRightX=X+halfB+25+summonB/2;
  float summonLeftX=X-halfB-25-summonB/2;;
  float summonY=Y2+halfH+5;
  int triSpace = 30;
  strokeWeight(5);
  for(int i=0; i<8; i++){
    triangle(summonRightX - incB + triSpace*i, summonY, summonRightX + triSpace*i, summonY-incH, summonRightX + triSpace*i + incB, summonY);
    triangle(summonLeftX - incB - triSpace*i, summonY, summonLeftX - triSpace*i, summonY-incH, summonLeftX - triSpace*i + incB, summonY);
  }
  incB+=0.05*speed;
  incH+=0.25*speed;
  
  if(incB>=summonB && incH>=summonH){
    incB=summonB;
    incH=summonH;
    speed=1;
    
    waitDelay++;
    
    if(waitDelay==waitSec*60){
      incB=0;
      incH=0;
      speed=1;
      waitDelay=0;
    }
  }
  
  if(incB > 0.4*summonB || incH > 0.4*summonH){
    speed *= 1.3;
  }
  
  /* Eyes */
  float eyeH=25;
  float eyeHalfB=10;
  strokeWeight(6);
  triangle(X-halfB/4-eyeHalfB, Y2+halfH/2, X-halfB/4+eyeHalfB, Y2+halfH/2, X-halfB/4, Y2+halfH/2+eyeH);
  triangle(X+halfB/4-eyeHalfB, Y2+halfH/2, X+halfB/4+eyeHalfB, Y2+halfH/2, X+halfB/4, Y2+halfH/2+eyeH);
  strokeWeight(4);
  line(X-halfB/4, Y2+halfH/2+eyeH, X-halfB/4, Y2+halfH/2);
  line(X+halfB/4, Y2+halfH/2+eyeH, X+halfB/4, Y2+halfH/2);
  
}


float sideLen=200;
float halfSide=sideLen/2;
int inc=2;
int incDir=1;
void drawBrute(){
  float Y3=5*Y;
  /* Body */
  strokeWeight(25);
  rect((X-halfSide), (Y3-halfSide), sideLen, sideLen);
  
  /* Inner Squares */
  strokeWeight(15);
  line((X-halfSide), Y3-inc, X, (Y3-halfSide));
  line(X+inc, (Y3-halfSide), (X+halfSide), Y3);
  line((X+halfSide), Y3+inc, X, (Y3+halfSide));
  line(X-inc, (Y3+halfSide), (X-halfSide), Y3);
  
  line((X-halfSide), Y3, X-inc, (Y3-halfSide));
  line(X, (Y3-halfSide), (X+halfSide), Y3-inc);
  line((X+halfSide), Y3, X+inc, (Y3+halfSide));
  line(X, (Y3+halfSide), (X-halfSide), Y3+inc);
  
  inc+=incDir;
  if(inc > halfSide || inc < -1*halfSide){
    incDir *= -1;
  }
  
  /* Middle Separators */
  strokeWeight(5);
  line(X-halfSide, Y3, X+halfSide, Y3);
  line(X, Y3-halfSide, X, Y3+halfSide);
  
  /* Eyes */
  float eyeSize=10;
  float eyeGap=10;
  strokeWeight(7.5);
  rect(X-eyeSize-eyeGap, Y3-eyeSize-eyeGap, eyeSize, eyeSize);
  rect(X+eyeGap, Y3-eyeSize-eyeGap, eyeSize, eyeSize);
  rect(X-eyeSize-eyeGap, Y3+eyeGap, eyeSize, eyeSize);
  rect(X+eyeGap, Y3+eyeGap, eyeSize, eyeSize);
}

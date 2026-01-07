//Script Spectrophotometer

//Arduino Ports
//D7: Push Button to start the scan
//D9: Blue LED
//D10: Green LED
//D11: Red LED

//Input Variables
//nscan: Number of scan

double r; //variable used to store the irradiance values for the red color
double g; //variable used to store the irradiance values for the green color
double b; //variable used to store the irradiance values for the blue color
double t; //parametric variable
int rr; //normalized irradiance output for red color
int gg; //normalized irradiance output for green color
int bb; //normalized irradiance output for blue color
int j; //auxiliar variable
int nscan = 10; //number of scans
double l; //wavelenght [400nm,700nm]
int photocell; //input values read on the LDR sensor
void setup ()
{
  Serial.begin(9600); //this value must be set for you computer
  pinMode (7, INPUT); //start button
  pinMode (9, OUTPUT); //blue LED
  pinMode (10, OUTPUT); //green LED
  pinMode (11, OUTPUT); //red LED
}
void loop () {
  if (digitalRead(7) == LOW) {
    {
      for (j = 1; j < (nscan + 1); j++) {
        for (l = 400; l < 701; l++) {
          r = 0.0;
          g = 0.0;
          b = 0.0;
          if ((l >= 400.0) && (l < 410.0)) {
            t = (l - 400.0) / (410.0 - 400.0);
            r = +(0.33 * t) - (0.20 * t * t);
          }
          else if ((l >= 410.0) && (l < 475.0)) {
            t = (l - 410.0) / (475.0 - 410.0);
            r = 0.14 - (0.13 * t * t);
          }
          else if ((l >= 545.0) && (l < 595.0)) {
            t = (l - 545.0) / (595.0 - 545.0);
            r = +(1.98 * t) - ( t * t);
          }
          else if ((l >= 595.0) && (l < 650.0)) {
            t = (l - 595.0) / (650.0 - 595.0);
            r = 0.98 + (0.06 * t) - (0.40 * t * t);
          }
          else if ((l >= 650.0) && (l < 700.0)) {
            t = (l - 650.0) / (700.0 - 650.0);
            r = 0.65 - (0.84 * t) + (0.20 * t * t);
          }
          if ((l >= 415.0) && (l < 475.0)) {
            t = (l - 415.0) / (475.0 - 415.0);
            g = +(0.80 * t * t);
          }
          else if ((l >= 475.0) && (l < 590.0)) {
            t = (l - 475.0) / (590.0 - 475.0);
            g = 0.8 + (0.76 * t) - (0.80 * t * t);
          }
          else if ((l >= 585.0) && (l < 639.0)) {
            t = (l - 585.0) / (639.0 - 585.0);
            g = 0.84 - (0.84 * t) ;
          }
          if ((l >= 400.0) && (l < 475.0)) {
            t = (l - 400.0) / (475.0 - 400.0);
            b = +(2.20 * t) - (1.50 * t * t);
          }
          else if ((l >= 475.0) && (l < 560.0)) {
            t = (l - 475.0) / (560.0 - 475.0);
            b = 0.7 - ( t) + (0.30 * t * t);
          }
          rr = r * 255;
          gg = g * 255;
          bb = b * 255;
          analogWrite(9, bb);
          analogWrite(10, gg);
          analogWrite(11, rr);
          delay(50);
          photocell = analogRead(0);
          Serial.print(int(l));
          Serial.print(",");
          Serial.println(photocell);
          delay(50);
        }
      }
    }
  }
}

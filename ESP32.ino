#include <FastLED.h>
#define LED_NUM 96

// Avail GPIO
// L(8 ): 32 33 25 26 27 14 12 13  /  /  /  /  /
// R(13): 15  2  4 16 17  5 18 19 21  1  3 22 23
// Total: 21Pins
#define C1_Pin 19
#define C2_Pin 18
#define C3_Pin 5
#define C4_Pin 16
#define C5_Pin 17
#define C6_Pin 4
#define C7_Pin 2
#define C8_Pin 15



CRGB C1_LED[LED_NUM];
CRGB C2_LED[LED_NUM];
CRGB C3_LED[LED_NUM];
CRGB C4_LED[LED_NUM];
CRGB C5_LED[LED_NUM];
CRGB C6_LED[LED_NUM];
CRGB C7_LED[LED_NUM];
CRGB C8_LED[LED_NUM];



int str_index, r, g, b, column_group, column_subindex, row_group, tmp_led_index;
char CMD[5377];
char N;



void serial_clean() {
  while(Serial.available() > 0) {
    N = Serial.read();
  }
  Serial.println("Serial buffer cleaned!");
}


void serial_read() {
  for(int i=0; i < sizeof(char) * 5377; i++) {
    CMD[i] = Serial.read();
  }
  serial_clean();
}



int char2hex(char target) {
  if (target == '0') {
    return 0;
  } else if (target == '1') {
    return 1;
  } else if (target == '2') {
    return 2;
  } else if (target == '3') {
    return 3;
  } else if (target == '4') {
    return 4;
  } else if (target == '5') {
    return 5;
  } else if (target == '6') {
    return 6;
  } else if (target == '7') {
    return 7;
  } else if (target == '8') {
    return 8;
  } else if (target == '9') {
    return 9;
  } else if (target == 'A') {
    return 10;
  } else if (target == 'B') {
    return 11;
  } else if (target == 'C') {
    return 12;
  } else if (target == 'D') {
    return 13;
  } else if (target == 'E') {
    return 14;
  } else if (target == 'F') {
    return 15;
  } else {
    return 0;
  }
}



int LED_index(int column_subindex, int row_group) {
  if (column_subindex == 1){
    return row_group - 1;
  } else if (column_subindex == 2){
    return 64 - row_group; // Reversed row, cuz group starts from 1, so it is automatically subtracted.
  } else if (column_subindex == 3){
    return row_group + 63; // row + 64 - 1
  } else {
    return 0;
  }
}



void setup() {
  // Wait until Serial established
  Serial.setRxBufferSize(8192);
  Serial.begin(2000000);
  while(!Serial){;}
  // Add all columns
  FastLED.addLeds<WS2812B, C1_Pin>(C1_LED, LED_NUM);
  FastLED.addLeds<WS2812B, C2_Pin>(C2_LED, LED_NUM);
  FastLED.addLeds<WS2812B, C3_Pin>(C3_LED, LED_NUM);
  FastLED.addLeds<WS2812B, C4_Pin>(C4_LED, LED_NUM);
  FastLED.addLeds<WS2812B, C5_Pin>(C5_LED, LED_NUM);
  FastLED.addLeds<WS2812B, C6_Pin>(C6_LED, LED_NUM);
  FastLED.addLeds<WS2812B, C7_Pin>(C7_LED, LED_NUM);
  FastLED.addLeds<WS2812B, C8_Pin>(C8_LED, LED_NUM);
  // Announce init
  Serial.println("Live");
}



void loop() {
  if (Serial.available() >= sizeof(char) * 5377) {
    // Read CMD
    serial_read();
    // Verify integrety
    if (CMD[5375] != ';' || CMD[5376]  != ';' ) {
      serial_clean();
    } else {
      // Update pixels using data
      for (int i = 0; i < 768; i++) {
        // The index of the first char of the CMD
        str_index = i * 7;
        // Get RGB value
        r = char2hex(CMD[str_index]) * 16;
        r += char2hex(CMD[str_index + 1]);
        g = char2hex(CMD[str_index + 2]) * 16;
        g += char2hex(CMD[str_index + 3]);
        b = char2hex(CMD[str_index + 4]) * 16;
        b += char2hex(CMD[str_index + 5]);
        if (CMD[str_index + 6] != ';') {break;}
        // Update RGB value of the corresponding LED
        // ** Following index & group starts from 1 **
        column_group = ((i / 3) + 1) % 8;
        column_subindex = ((i % 24) % 3) + 1;
        row_group = (i / 24) + 1;
        tmp_led_index = LED_index(column_subindex, row_group);
        if (column_group == 1) {
          C1_LED[tmp_led_index].setRGB(g, r, b);
        } else if (column_group == 2) {
          C2_LED[tmp_led_index].setRGB(g, r, b);
        } else if (column_group == 3) {
          C3_LED[tmp_led_index].setRGB(g, r, b);
        } else if (column_group == 4) {
          C4_LED[tmp_led_index].setRGB(g, r, b);
        } else if (column_group == 5) {
          C5_LED[tmp_led_index].setRGB(g, r, b);
        } else if (column_group == 6) {
          C6_LED[tmp_led_index].setRGB(g, r, b);
        } else if (column_group == 7) {
          C7_LED[tmp_led_index].setRGB(g, r, b);
        } else if (column_group == 0) {
          C8_LED[tmp_led_index].setRGB(g, r, b);
        }
      }
      // Show new pattern
      Serial.println("Pattern updated");
      FastLED.show();
    }
  }
  // Request new frame
    Serial.println("Poll");
    delay(20);
}
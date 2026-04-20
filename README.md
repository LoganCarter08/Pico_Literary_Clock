# Literary Clock Running on a Raspberry Pi Pico W

Display a book quote for each minute of the day!

litclock_annotated.csv is sourced from https://github.com/JohannesNE/literature-clock/tree/master

## Hardware and Tools Required:

1. Pico Pi 2 W. Likely a Pico Pi W would work, but I have only tested a 2. A W model is needed for a wifi connection.
2. A display. [This one](https://www.buydisplay.com/4-3-inch-tft-lcd-display-capacitive-touchscreen-ra8875-controller) was used. A touchscreen version was selected for this, but they likely have cheaper ones without touchscreen capabilities.
   1. If you use the one linked I used the following configuration:
      1. Interface: Pin Header Connection-4-Wire SPI
      2. Power Supply: VDD=5.0V
      3. Font Chip: ER3301-1
   2. If you use a different one you will need to modify the 3D models and likely the code

3. 3D printer or ability to get 3D printed parts
4. Soldering iron
5. Solder
6. Wire
7. Wire Strippers
8. [3mm x 20mm flat chamfer headed bolts](https://www.amazon.com/Hoomuy-100pcs-Socket-Countersunk-Threaded/dp/B0GDWH9DZK?crid=2WICLVJN2FODD&dib=eyJ2IjoiMSJ9.ZhA4o0xRLSrXNxFYLA3Pb8-Had3o9e3dYBh0-yxXm27UoT51629bp5x8gKhQTJavWhE-p8RPsT5Cob4ZZy1swNB3AomqiCugNbvahoUtx93Q6kl0NMneoVTK1UKJwEqR5PJSKMVyvpxDUpQgrH0wLN5XB7ZFd_eBj7qMEJkOBbeXxgvK9t9WnLiPWXueCmXxNedJua4juk-tvX9JKNjTSFFN_uQ-woQRW6VOQN6nhvU.QZC1CGUMsFsEaoztxkBXy-KBrk9beYUTDEHT6qn16kg&dib_tag=se&keywords=3mm%2Bx%2B20mm%2Bflat%2Bhead&qid=1776655790&sprefix=3mm%2Bx%2B20mm%2Bflat%2Bhead%2B%2Caps%2C172&sr=8-3&th=1)
9. [3mm x 8mm flat chamfer headed bolts](https://www.amazon.com/DTGN-M3-0-5x8mm-Socket-Screws-Countersunk/dp/B0CQ1VJTMK?crid=2JBE6YGSNMU9L&dib=eyJ2IjoiMSJ9.6vbU1pRlW60ScH-nzQ_APQhkACpJKEIeEEt16qbBAkmbuJBBsgBT8inw8Te2mK359rmkwAA695bpFRxYs-0dbHDBj_UtTOQHoYoePCyZAp1WcG7OaMTrmkZea65q9rg2rrKZPTrcB9ZWQQv_6dnQ6HZxUUYzVn4ttLN1xcMLGHBAF-CrLRd7VBiGf8TkTgzsfVNY8aMqMl-Yn0GZrD6GGa58uglwDs5KrGCbpoLDjqk.fg4DdWQaGrE_JhMc6Wju9-mxggIBH4T_JSlaaH4UScY&dib_tag=se&keywords=3mm%2Bflat%2Bhead%2B8mm&qid=1776691656&sprefix=3mm%2Bflat%2Bhead%2B8mm%2Caps%2C204&sr=8-3&th=1)
10. [3mm threaded heat inserts](https://www.amazon.com/Ktehloy-Threaded-Printing-Components-M3x4x5mm/dp/B0CLKCQ2SH?crid=3KLTFV16JSJ47&dib=eyJ2IjoiMSJ9.p05Rl_3Sshmon-3QzJ6LxC0_NVr5Sf54tspQ3xpiwOMozMMk4bo2aax3zB5-04vxi5KZOzUmMslAwZ-cZ7uR_iHxz3IWYASPRDiL0BAoXCPYhu2-_QnOjUOWNE2euzF7-Oz9kZYLs-emKbUN9aCoyU9knTLc9qzn7gJFWfB0r5YOeB9SG5CsWT43hgE78BhmuY1a_FD5RPRNYybq9nAQHoQs7_98pVcGHaiv4sN-DFs.u9lB67KWbCGUKsFRZrazvrGTjcHfaRv9pQEPMAlK5rg&dib_tag=se&keywords=3mm%2Bthreaded%2Bheat%2Binserts&qid=1776655878&sprefix=3mm%2Bthreaded%2Bheat%2Bin%2Caps%2C354&sr=8-14&th=1)
11. Micro USB cable
12. USB power supply. Must match the other end of the micro USB cable.

## Software Instructions:

1. [Configure your Pico](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython) to use CircuitPython. Be sure to select the correct uf2 file for your board. The link in the guide will just take you to the original Pico.
1. Go to [Adafruit](https://accounts.adafruit.com/) and create an account.
1. Sign into [Adafruit IO](io.adafruit.com) with your Adafruit account.
1. Click My Key on the top bar.
1. Open circuit_python_files/settings.toml
   a. Replace ADAFRUIT_AIO_USERNAME and ADAFRUIT_AIO_KEY with your Adafruit account details.
   b. Use the [TZ identifier values on Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) to set your timezone.
   c. Set CIRCUITPY_WIFI_SSID as your wifi name.
   d. Set CIRCUITPY_WIFI_PASSWORD as your wifi password.
1. Change the rest of the settings in settings.toml to match your preferences. Descriptions of each setting can be found below.

   Note: Some sample colors are provided. More can be added within the COLORS dict in code.py. They are in RGB format and can be modified or more can be added for your needs.

1. Make sure you have Python installed on your computer. Latest version is recommended.
1. Open a terminal and navigate to the folder containing these files and run `python .\csv_to_json.py`
1. Make sure Circuit Python is installed on your Pico Pi
1. Connect your Pico to your computer
1. Upload the contents of circuit_python_files to your Pico

## settings.toml

The following settings are for you to be able to configure certain parts of the display without changing actual code.

### CIRCUITPY_WIFI_SSID

Name of your wifi router.

### CIRCUITPY_WIFI_PASSWORD

Password for your wifi router.

### ADAFRUIT_AIO_USERNAME

Username for your Adafruit AIO account.

### ADAFRUIT_AIO_KEY

Access key for your Adafruit AIO account.

### TIMEZONE

Timezone you live in. [List of timezones.](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

### DISPLAY_MERIDIEM

Display a.m. or p.m. in the time at the top of the screen. Is not applied if using military time. Set to either "true" or "false".

### USE_MILITARY_TIME

Display time at the top of the screen in military time instead of 12 hour. Set to either "true" or "false".

### SCREEN_OFF_TIME

Time the screen should turn off. This will save power and increase the lifespan of your screen. Set to "[-1, -1]" to always be on.

### SCREEN_ON_TIME

Time the screen should turn on. Set to "[-1, -1]" to always be on.

### BACKGROUND_COLOR

Color to choose for the background of the screen. Options: BLACK, RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, WHITE

### TEXT_COLOR

Color for any text that is not the time of day in the quote. Options: BLACK, RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, WHITE

### HIGHLIGHT_COLOR

Color for the time in the quote. Options: BLACK, RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, WHITE

## Assembly Instructions:

1. todo

## Other Notes:

- Other microcontroller boards than the Pico Pi W can be used. The 3D models will need updated and likely some code changes to support the correct pinout.
- A Pico W is required because the device needs to connect to the internet to keep the clock synchronized as there tends to be some time drift relying on internal time keeping.
- If you want to add/edit/delete any quotes you can edit the litclock_annotated.csv file, delete the quotes off the pico, and then load the new quotes from the circuit_python_files/lib/quotes folder. Otherwise you may get errors about not enough storage space.
- A few times of the day currently do not have quotes. If you find any please feel free to let me know and I can update the file with them. Current 11:46, 12:31, 13:36, and 18:44 are missing.

# Literary Clock Running on Raspberry Pi Pico W

Display a book quote for each minute of the day! 

litclock_annotated.csv is sourced from https://github.com/JohannesNE/literature-clock/tree/master

## Hardware and Tools Required: 
1. Pico Pi 2 W. Likely a Pico Pi W would work, but I have only tested a 2. A W model is needed for a wifi connection. 
2. A display. [This one](https://www.buydisplay.com/4-3-inch-tft-lcd-display-capacitive-touchscreen-ra8875-controller) was used. A touchscreen version was selected for this, but they likely have cheaper ones without touchscreen capabilities.
  a. If you use the one linked I used the following configuration:
    i. Interface: Pin Header Connection-4-Wire SPI
    ii. Power Supply: VDD=5.0V
    iii. Font Chip: ER3301-1
3. 3D printer or ability to get 3D printed parts
4. Soldering iron
5. Solder
6. Wire
7. Wire Strippers
8. [3mm x 20mm flat chamfer headed bolt](https://www.amazon.com/Hoomuy-100pcs-Socket-Countersunk-Threaded/dp/B0GDWH9DZK?crid=2WICLVJN2FODD&dib=eyJ2IjoiMSJ9.ZhA4o0xRLSrXNxFYLA3Pb8-Had3o9e3dYBh0-yxXm27UoT51629bp5x8gKhQTJavWhE-p8RPsT5Cob4ZZy1swNB3AomqiCugNbvahoUtx93Q6kl0NMneoVTK1UKJwEqR5PJSKMVyvpxDUpQgrH0wLN5XB7ZFd_eBj7qMEJkOBbeXxgvK9t9WnLiPWXueCmXxNedJua4juk-tvX9JKNjTSFFN_uQ-woQRW6VOQN6nhvU.QZC1CGUMsFsEaoztxkBXy-KBrk9beYUTDEHT6qn16kg&dib_tag=se&keywords=3mm%2Bx%2B20mm%2Bflat%2Bhead&qid=1776655790&sprefix=3mm%2Bx%2B20mm%2Bflat%2Bhead%2B%2Caps%2C172&sr=8-3&th=1)
9. [3mm threaded heat inserts](https://www.amazon.com/Ktehloy-Threaded-Printing-Components-M3x4x5mm/dp/B0CLKCQ2SH?crid=3KLTFV16JSJ47&dib=eyJ2IjoiMSJ9.p05Rl_3Sshmon-3QzJ6LxC0_NVr5Sf54tspQ3xpiwOMozMMk4bo2aax3zB5-04vxi5KZOzUmMslAwZ-cZ7uR_iHxz3IWYASPRDiL0BAoXCPYhu2-_QnOjUOWNE2euzF7-Oz9kZYLs-emKbUN9aCoyU9knTLc9qzn7gJFWfB0r5YOeB9SG5CsWT43hgE78BhmuY1a_FD5RPRNYybq9nAQHoQs7_98pVcGHaiv4sN-DFs.u9lB67KWbCGUKsFRZrazvrGTjcHfaRv9pQEPMAlK5rg&dib_tag=se&keywords=3mm%2Bthreaded%2Bheat%2Binserts&qid=1776655878&sprefix=3mm%2Bthreaded%2Bheat%2Bin%2Caps%2C354&sr=8-14&th=1)

## Software Instructions: 
1. Go to https://accounts.adafruit.com/ and create an account.
2. Sign into io.adafruit.com with your Adafruit account.
3. Click My Key on the top bar.
4. Open circuit_python_files/settings.toml
   a. Replace ADAFRUIT_AIO_USERNAME and ADAFRUIT_AIO_KEY with your Adafruit account details.
   b. Use the TZ identifier values on wikipedia to set your timezone. https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
   c. Set CIRCUITPY_WIFI_SSID as your wifi name.
   d. Set CIRCUITPY_WIFI_PASSWORD as your wifi password.
5. Open cicuit_python_files/code.py
   a. Change BACKGROUND_COLOR to the color you would like the background to be 
   b. Change TEXT_COLOR to the color you would like the primary text color to be
   c. Change HIGHLIGHT_COLOR to the color you would like the quote to be
   Note: Some sample colors are provided in this file. They are in RGB format and can be modified or more can be added for your needs.
6. Make sure you have Python installed on your computer. Latest version is recommended.
7. Open a terminal and navigate to the folder containing these files and run ```python .\csv_to_json.py```
8. Make sure Circuit Python is installed on your Pico Pi
9. Upload the contents of circuit_python_files to your Pico

## Assembly Instructions: 
1. todo 

## Other Notes: 
* Other microcontroller boards than the Pico Pi W can be used. The 3D models will need updated and likely some code changes to support the correct pinout.
* A Pico W is required because the device needs to connect to the internet to keep the clock synchronized as there tends to be some time drift relying on internal time keeping.
* If you want to add/edit/delete any quotes you can edit the litclock_annotated.csv file, delete the quotes off the pico, and then reload the new quotes from the circuit_python_files/lib/quotes folder.
* A few times of the day currently do not have quotes. If you find any please feel free to let me know and I can update the file with them. Current 11:46, 12:31, 13:36, and 18:44 are missing.
* Currently time is displayed as a 12 hour clock without am/pm designation. 

version 0.1

This is a project to create a Raspberry PI Weather Display. It was a fun way for me to pick up Python. The weather data comes from the Weather Underground API. There are a number of Python libraries required including pygame. 

I used a Raspberry Pi and a LCD Touch Screen. I ordered both from adafruit.com:
https://www.adafruit.com/products/2380
https://www.adafruit.com/products/2441

To exit out of the screen, hit the "q" key. I'm still working on a way to exit using the touchscreen. 

For now I've hardcoded the city. Also you will need to add a "config.json" file in the source directory with the following json structure.

{
    "api-key":"your-api-key-from-weather-underground"
}
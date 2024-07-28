# Time of Actual Death (TOAD)
Time of Actual Death, aka TOAD, is a lightweight, open-source time of death identifier for https://dragcave.net.

![image](https://github.com/user-attachments/assets/11abb6ea-8f60-4aae-b966-bfe426272de9)

To use TOAD requires your own private API key. Use that key, plus the code of the dragon whose time of death you want to calculate, and wait. Based on your network speed, you can adjust how often to send requests to Dragon Cave, with options from every .1 to 60 seconds. It does not add any views to the egg or hatchling.

Currently, TOAD is only available as a python app, but I plan on creating a web app so that it can be accessed with no downloads required by users.

### To compile TOAD yourself:
TOAD is prebuilt as an EXE, but if you'd rather compile it yourself, you can follow the steps below.
- Ensure python is downloaded
- Install pyinstaller: `pip install pyinstaller`
- Navigate to the folder containing toad.py and execute `pyinstaller -F .\TOADv1.py --noconsole`

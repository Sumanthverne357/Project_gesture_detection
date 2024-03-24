# Project_gesture_detection
1. Use file esp32_BLE_Guesture.ino to upload to esp32 seed studio
   
     download guesture library from : https://github.com/Seeed-Studio/Grove_Gesture/tree/dev
2. keep the Grove Smart IR Gesture Sensor in SPI mode
   
     All switches need to be toggled to the ON position
    ![SPI_I2C_config](https://github.com/Sumanthverne357/Project_gesture_detection/assets/151477718/140b4a3f-643a-48ae-9f7c-6acb266c5685)

3. Installation

            #On Windows
               python -m venv venv
           #On macOS/Linux
              python3 -m venv venv
         
           # Activate the virtual environment
           # On Windows
              .\venv\Scripts\activate
         
           # On macOS/Linux
               source venv/bin/activate
         
            # installation of LIB files to prject
               pip install -r requirements.txt
               #runing appliaction
               python app.py
4.Runing appliaction

   
            ./run.sh 
            
or 
            
            bash run.sh

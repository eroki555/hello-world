#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import wiringpi as wpi
import time

wpi.wiringPiSetup()
wpi.pinMode(7, 1)
wpi.digitalWrite(7, 1)
time.sleep(1)
wpi.digitalWrite(7, 0)
time.sleep(1)


# In[ ]:





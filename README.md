# LidarLiteV3 Library
#### Install:
```
pip install lidarlite_v3
```
#### Usage:
```python
import lidarlite_v3

lidar = lidarlite_v3.Connect()
distance = lidar.getDistance()
print("Distance: %d" % distance)
```
```
Distance: 267
```
#### Change the address from the default 0x62 to 0x64
```python
import lidarlite_v3

lidar = lidarlite_v3.Connect() # the same as lidarlite_v3.Connect(0x62)
lidar.changeAddress(0x64)

distance = lidar.getDistance()
print("Distance: %d" % distance)
```
```
Distance: 267
```
#### Address check
```
i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- 64 -- 66 -- 68 -- -- -- -- -- -- -- 
70: 70 -- -- -- -- -- -- --                 
```
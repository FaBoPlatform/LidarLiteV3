#coding: utf-8
import smbus

class Connect():

    def __init__(self, address=0x62):
        self.address = address
        # Resgiter Address
        self.ADDR_ACQ_COMMAND = 0x00 # DevieConnand
        self.ADDR_STATUS = 0x01 # SystemStatus
        self.ADDR_FULL_DELAY_HIGH = 0x0f # Diatance measurement high byte
        self.ADDR_FULL_DELAY_LOW = 0x10 # Diatance measurement low byte
        self.ADDR_UNIT_ID_HIGH = 0x16 # Serial number high byte
        self.ADDR_UNIT_ID_LOW = 0x17 # Serial number low byte
        self.ADDR_I2C_ID_HIGH = 0x18 # Write serial number high byte for I2C address unlock
        self.ADDR_I2C_ID_LOW = 0x19 # Write serial number low byte for I2C address unlock
        self.ADDR_I2C_SEC_ADDR = 0x1a # Write new I2C address after unlock
        self.ADDR_I2C_CONFIG = 0x1e # Default address response control

        # ACQ_COMMAND VALUE
        self.TAKE_DISTANCE_MEASUREMENT_WITH_RECEIVER_BIAS_CORRECTION = 0x04
        # I2C_CONFIG VALUE
        self.DISABLE_DEFAULT_ADDRESS_RESPONSE_CONTROL = 0x08

        self.bus = smbus.SMBus(1)


    def getDistance(self):
        # デバイスコマンドを距離取得に設定する(毎回実行が必要)
        self.bus.write_byte_data(self.address, self.ADDR_ACQ_COMMAND, self.TAKE_DISTANCE_MEASUREMENT_WITH_RECEIVER_BIAS_CORRECTION)
        # 0x01を読み込んで、最下位bitが0になるまで読み込む
        value = self.bus.read_byte_data(self.address, self.ADDR_STATUS)
        while value & 0x01 == 1:
            value = self.bus.read_byte_data(self.address, self.ADDR_STATUS)

        # 桁上がりの値となるhigh、0-255の値となるlowを取得し、high * 256 + lowを測定距離(cm)として返す
        high = self.bus.read_byte_data(self.address, self.ADDR_FULL_DELAY_HIGH)
        low = self.bus.read_byte_data(self.address, self.ADDR_FULL_DELAY_LOW)
        dist = ( high << 8 ) + low
        return dist


    def changeAddress(self, new_address):
        if new_address == None:
            return
        elif new_address == self.address:
            return
        else:
            # 0x16,0x17の値を読み込みます
            high = self.bus.read_byte_data(self.address, self.ADDR_UNIT_ID_HIGH)
            low = self.bus.read_byte_data(self.address, self.ADDR_UNIT_ID_LOW)

            # 0x18,0x19に書き込みます
            self.bus.write_byte_data(self.address, self.ADDR_I2C_ID_HIGH, high)
            self.bus.write_byte_data(self.address, self.ADDR_I2C_ID_LOW, low)

            # 新しいアドレスを0x1aに書き込みます
            self.bus.write_byte_data(self.address, self.ADDR_I2C_SEC_ADDR, new_address)
            # デフォルトのアドレス(0x62)を使用しないように0x1eに0x08を書き込みます
            self.bus.write_byte_data(self.address, self.ADDR_I2C_CONFIG, self.DISABLE_DEFAULT_ADDRESS_RESPONSE_CONTROL)

            self.address = new_address


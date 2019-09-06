import tkinter as tk
import serial
import serial.tools.list_ports
import json
from time import sleep


class BackLightTest:
	def __init__(self):
		root = tk.Tk()
		#canvas1 = tk.Canvas(root, width = 200, height = 200)
		#canvas1.pack()
		self.var = tk.StringVar()
		l = tk.Label(root, textvariable=self.var, bg='grey', fg='white', font=('Arial', 8), width=30, height=2)
		self.var.set('test')
		l.pack()

		self.current_cmd = tk.StringVar()
		l = tk.Label(root, textvariable=self.current_cmd, bg='green', fg='white', font=('Arial', 12), width=40, height=2)
		self.current_cmd.set('回车将设置2D电流 5ma， 3D电流 28ma')
		l.pack()

		self.CheckVar1 = tk.IntVar()
		C1 = tk.Checkbutton(root, text = "打印开关", variable = self.CheckVar1, \
		onvalue = 1, offvalue = 0, height=1, \
		width = 10)
		C1.pack()

		#self.print_switch = True

		#panel = tk.Label(root, text = '1')
		#panel.pack(side = "top", fill = "both", expand = "yes")
		button1 = tk.Button(root, text= '帮助信息', width="20",height="1", command=self.test_HELP)

		button2 = tk.Button(root, text= '显示版本信息', width="20",height="1", command=self.test_INFO)

		button3 = tk.Button(root, text= 'DUMP寄存器', width="20",height="1", command=self.test_DUMP)
		button4 = tk.Button(root, text= '读写寄存器', width="20",height="1", command=self.test_I2C)
		button5 = tk.Button(root, text= '获取当前系统配置', width="20",height="1", command=self.test_BLSETTINGSGET)
		button6 = tk.Button(root, text= '亮度设置', width="20",height="1", command=self.test_BLSETBRIGHTNESS)
		button7 = tk.Button(root, text= '切换2D、3D模式', width="20",height="1", command=self.test_BLSWITCH)
		button8 = tk.Button(root, text= '设置2D、3D亮度比率', width="20",height="1", command=self.test_BLSETRATIOS)
		button9 = tk.Button(root, text= '切换2D控制模式', width="20",height="1", command=self.test_SET2DCTRLMODE)
		button10 = tk.Button(root, text= '设置2D、3D PWM占空比', width="20",height="1", command=self.test_BLSETPWM)
		button11 = tk.Button(root, text= '设置2D电流值', width="20",height="1", command=self.test_BLSET2DCURRENT)
		button12 = tk.Button(root, text= '设置3D电流值', width="20",height="1", command=self.test_BLSET3DCURRENT)
		button13 = tk.Button(root, text= '断电保存配置到flash', width="20",height="1", command=self.test_SAVETOFLASH)
		button14 = tk.Button(root, text= '恢复出厂设置', width="20",height="1", command=self.test_BLFACTORYRESET)
		#canvas1.create_window(40, 40, window=button2)
		button1.pack()
		button2.pack()
		button3.pack()
		button4.pack()
		button5.pack()
		button6.pack()
		button7.pack()
		button8.pack()
		button9.pack()
		button10.pack()
		button11.pack()
		button12.pack()
		button13.pack()
		button14.pack()

		frame=tk.Frame(root,width=20,height=20)

		frame.bind("<KeyPress>",self.callBack)

		frame.pack()

		frame.focus_set()

		self.enter_counter = 0

	def test_HELP(self):
		self.S.write("HELP\r\n".encode())
		print("[TEST]:帮助信息")
		j = self.recv()
		self.check_json_ret(j)

	def test_INFO(self):
		self.S.write("INFO\r\n".encode())
		print("[TEST]:版本信息")
		j = self.recv()
		self.check_json_ret(j)

	def test_DUMP(self):
		self.S.write("DUMP\r\n".encode())
		print("[TEST]:DUMP寄存器")
		j = self.recv()
		print(j)
		chip0_list = j['8556 chipid 0']
		chip1_list = j['8556 chipid 1']
		list0_exp = [{'address': 0xa1, 'val': 0x5F}, {'address': 0xa0, 'val': 0xff}, \
		{'address': 0x16, 'val': 0x16}, {'address': 0xa9, 'val': 0x40}, \
		{'address': 0x9e, 'val': 0x22}, {'address': 0xa2, 'val': 0x2b}, \
		{'address': 0xa6, 'val': 0x05}, {'address': 0x01, 'val': 0x05}, \
		{'address': 0x1f, 'val': 0xff}]
		list1_exp = [{'address': 0xa1, 'val': 0x5F}, {'address': 0xa0, 'val': 0xff}, \
		{'address': 0x16, 'val': 0x16}, {'address': 0xa9, 'val': 0x60}, \
		{'address': 0x9e, 'val': 0x22}, {'address': 0xa2, 'val': 0x2b}, \
		{'address': 0xa6, 'val': 0x05}, {'address': 0x01, 'val': 0x05}, \
		{'address': 0x1f, 'val': 0xff}]
		if chip0_list == list0_exp and chip1_list == list1_exp:
			print('pass')
		else:
			print('fail')
			print('chip 0')
			for p in chip0_list:
				print(p)
			print('chip 1')
			for p in chip1_list:
				print(p)


	def test_I2C(self):
		print('[TEST]:I2C读写寄存器')
		self.S.write("I2CREAD 0\r\n".encode())
		j = self.recv()
		print(j)
		if j['result'] == 'success' and j['8556 chipid 0']['0x0'] == '0x0':
			print('pass')
		else:
			print('fail')

		self.S.write("I2CREAD 2\r\n".encode())
		j = self.recv()
		print(j)

		if j['result'] == 'success' and j['8556 chipid 0']['0x2'] == '0x0':
			print('pass')
		else:
			print('fail')

		self.S.write("I2CWRITE 0 1f\r\n".encode())
		j = self.recv()
		self.S.write("I2CREAD 0\r\n".encode())
		j = self.recv()

		if j['result'] == 'success' and j['8556 chipid 0']['0x0'] == '0x1f':
			print('pass')
		else:
			print('fail')

		self.S.write("I2CWRITE AF FF\r\n".encode())
		j = self.recv()
		self.S.write("I2CREAD AF\r\n".encode())
		j = self.recv()

		if j['result'] == 'success' and j['8556 chipid 0']['0xaf'] == '0xff':
			print('pass')
		else:
			print('fail')


	def test_BLSETTINGSGET(self):
		print("[TEST]:获取系统设置")
		self.S.write("BLSETTINGSGET\r\n".encode())
		j = self.recv()
		self.check_json_ret(j)
		print(j)

	def get_brightness(self):
		self.S.write("BLSETTINGSGET\r\n".encode())
		j = self.recv()
		return j['brightness']

	def test_BLSETBRIGHTNESS(self):
		print("[TEST]:亮度设置")
		brightness_list = [0, 50, 100, 200, 255, 50]

		for brightness in brightness_list:
			cmd = "BLSETBRIGHTNESS " + str(brightness) + "\r\n"
			self.S.write(cmd.encode())
			j = self.recv()
			self.check_json_ret(j)
			sleep(1)
			
			if self.get_brightness() == brightness:
				print("brightness " + str(brightness) + ' success')
			else:
				print("brightness " + str(brightness) + ' fail')

	def test_BLSWITCH(self):
		print("[TEST]:切换2D、3D模式")
		cmd = "BLSWITCH 3\r\n"
		self.S.write(cmd.encode())
		j = self.recv()
		self.check_json_ret(j)
		cmd = "BLSETTINGSGET\r\n"
		self.S.write(cmd.encode())
		j = self.recv()
		if(j['mode'] != 3):
			print("BLSWITCH fail")

		cmd = "BLSWITCH 2\r\n"
		self.S.write(cmd.encode())
		j = self.recv()
		self.check_json_ret(j)

		cmd = "BLSETTINGSGET\r\n"
		self.S.write(cmd.encode())
		j = self.recv()
		if(j['mode'] != 2):
			print("BLSWITCH fail")

		for i in range(3):
			cmd = "BLSWITCH 2\r\n"
			self.S.write(cmd.encode())
			j = self.recv()
			self.check_json_ret(j)
			sleep(1)
			cmd = "BLSWITCH 3\r\n"
			self.S.write(cmd.encode())
			j = self.recv()
			self.check_json_ret(j)
			sleep(1)

	def test_BLSETRATIOS(self):
		print("[TEST]:切换2D、3D亮度比率")
		cmd_list = ["BLSWITCH 2\r\n",
		"BLSETRATIOS 2 0.5 0.3\r\n",
		"BLSETBRIGHTNESS 255\r\n",
		"BLSETTINGSGET\r\n",

		"BLSWITCH 2\r\n",
		"BLSETRATIOS 2 0.5 0.3\r\n",
		"BLSETBRIGHTNESS 50\r\n",
		"BLSETTINGSGET\r\n",

		"BLSWITCH 2\r\n",
		"BLSETRATIOS 2 1 0\r\n",
		"BLSETBRIGHTNESS 255\r\n",
		"BLSETTINGSGET\r\n",

		"BLSWITCH 2\r\n",
		"BLSETRATIOS 2 1 0\r\n",
		"BLSETBRIGHTNESS 50\r\n",
		"BLSETTINGSGET\r\n",

		"BLSWITCH 3\r\n",
		"BLSETRATIOS 2 0.1 1\r\n",
		"BLSETBRIGHTNESS 255\r\n",
		"BLSETTINGSGET\r\n",

		"BLSWITCH 3\r\n",
		"BLSETRATIOS 2 0.1 1\r\n",
		"BLSETBRIGHTNESS 50\r\n",
		"BLSETTINGSGET\r\n",

		"BLSWITCH 3\r\n",
		"BLSETRATIOS 2 0 0.5\r\n",
		"BLSETBRIGHTNESS 255\r\n",
		"BLSETTINGSGET\r\n",

		"BLSWITCH 3\r\n",
		"BLSETRATIOS 2 0 0.5\r\n",
		"BLSETBRIGHTNESS 50\r\n",
		"BLSETTINGSGET\r\n"]
		for cmd in cmd_list:
			self.S.write(cmd.encode())
			j = self.recv()
			self.check_json_ret(j)
			sleep(1)


	def test_SET2DCTRLMODE(self):
		print("[TEST]:切换2D控制模式")
		cmd_list = ["BLSWITCH 2\r\n",
		"SET2DCTRLMODE 0\r\n",
		"BLSETBRIGHTNESS 50\r\n",
		"BLSETBRIGHTNESS 200\r\n",
		"BLSETTINGSGET\r\n",

		"BLSWITCH 2\r\n",
		"SET2DCTRLMODE 1\r\n",
		"BLSETBRIGHTNESS 50\r\n",
		"BLSETBRIGHTNESS 200\r\n",
		"BLSETTINGSGET\r\n"]
		
		for cmd in cmd_list:
			self.S.write(cmd.encode())
			j = self.recv()
			self.check_json_ret(j)
			sleep(1)

	def test_BLSETPWM(self):
		print("[TEST]:设置2D、3D PWM占空比")
		cmd_list = ["SET2DCTRLMODE 1\r\n",
		"BLSETPWM 2 0\r\n",

		"SET2DCTRLMODE 1\r\n",
		"BLSETPWM 2 4096\r\n",

		"BLSETPWM 3 0\r\n",

		"BLSETPWM 3 2400\r\n"]
		for cmd in cmd_list:
			self.S.write(cmd.encode())
			j = self.recv()
			self.check_json_ret(j)
			sleep(1)

	def test_BLSET2DCURRENT(self):
		print("[TEST]:设置2D电流值")
		cmd_list = ["BLSET2DCURRENT 0\r\n",
		"BLSET2DCURRENT 25.0\r\n",
		"BLSET2DCURRENT 10\r\n"]
		for cmd in cmd_list:
			self.S.write(cmd.encode())
			j = self.recv()
			self.check_json_ret(j)
			sleep(1)

	def test_BLSET3DCURRENT(self):
		print("[TEST]:设置3D电流值")
		cmd_list = ["BLSET2DCURRENT 0\r\n",
		"BLSET2DCURRENT 30.0\r\n",
		"BLSET2DCURRENT 10\r\n"]
		for cmd in cmd_list:
			self.S.write(cmd.encode())
			j = self.recv()
			self.check_json_ret(j)
			sleep(1)
		print("test_3")

	def test_SAVETOFLASH(self):
		print("[TEST]:断电保存配置到flash")
		'''
发送命令：BLSETBRIGHTNESS 50\r\n
插拔电源
发送命令：BLSWITCH 3\r\n
插拔电源
发送命令：BLSETRATIOS 2 1 0\r\n
插拔电源
发送命令：SET2DCTRLMODE 1\r\n
插拔电源
		'''
		pass
	def test_BLFACTORYRESET(self):
		print("[TEST]:恢复出厂设置")
		'''
发送命令：BLFACTORYRESET\r\n
发送命令：BLSETTINGSGET\r\n
		'''
		self.S.write("BLFACTORYRESET\r\n".encode())
		#j = self.recv()
		#self.check_json_ret(j)

	def callBack(self, event):
		print(event.keysym)
		current_list = [[5,28], [13,14], [25,5]]

		cmd_2d = 'BLSET2DCURRENT ' + str(current_list[self.enter_counter][0]) + '\r\n'
		cmd_3d = 'BLSET3DCURRENT ' + str(current_list[self.enter_counter][1]) + '\r\n'
		self.S.write(cmd_2d.encode())
		j = self.recv()
		self.check_json_ret(j)
		self.S.write(cmd_3d.encode())
		j = self.recv()
		self.check_json_ret(j)

		self.enter_counter += 1
		if self.enter_counter == 3:
			self.enter_counter = 0
		self.current_cmd.set("回车将设置2D电流 %dma， 3D电流 %dma" % (current_list[self.enter_counter][0], current_list[self.enter_counter][1]))

	def BackLightSerial(self):
		plist = list(serial.tools.list_ports.comports())
		serialName = []
		if len(plist) <= 1:
			print ("The Serial port can't find!")
			self.var.set("串口连接失败")
		else:
			for com_port in plist:
				if(com_port[0] != 'COM1'):
					serialName = com_port[0]
			try:
				self.S = serial.Serial(serialName,115200,timeout = 0.5)
				self.var.set(serialName + " 连接成功.")
			except:
				self.var.set("串口连接失败")
				print("Serial Port Fail.")
	def recv(self):
		line = []
		data = ''
		while True:
			cc = self.S.readline().decode()
			#print(cc)
			if len(cc) == 0:
				break 
			data += cc
		if self.CheckVar1.get():
			print (data)
		text = json.loads(data)
		if self.CheckVar1.get():
			print (text)
		return text

		#print (text['result'])		

	@staticmethod
	def check_json_ret(j):
		if j['result'] == 'success':
			print(j['CMD'] + ' success')
		else:
			print(j['CMD'] + ' fail')

def main():

	backtest = BackLightTest()
	backtest.BackLightSerial()


main()

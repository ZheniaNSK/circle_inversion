import turtle
import math
import tkinter as tk
import sys
import re
from pyautogui import size as screen_size
import pyperclip

screen_width, screen_heigth = screen_size()
painting = None
info_is_open = False
circle_info_is_open = False
turtle_created = False
root2_destroyed = True
objects = []
object = 0
InversionObjects = True
t = None
root2 = None
root3 = None
root6 = None
root7 = None
root10 = None
turtle_inputs = []
circle_info = [300, 0, 0]
turtle_info = [12, 1, 1]
coordinats_info = [1.0, 0, 0]

def painting_paint(text1, text2, text3, text4, root5, InversionObjects = None, root8 = None):
	if (InversionObjects != None):
		root8.destroy()
	
	global objects
	global circle_info
	global turtle_info
	global coordinats_info
	
	turtle.setworldcoordinates(-screen_width / 2 * coordinats_info[0] - coordinats_info[2], -screen_heigth / 2 * coordinats_info[0] - coordinats_info[1], screen_width / 2 * coordinats_info[0] - coordinats_info[2], screen_heigth / 2 * coordinats_info[0] - coordinats_info[1])
	
	t.reset()
	
	if (turtle_info[0] == 12):
		turtle.tracer(0)
	elif (turtle_info[0] == 11):
		turtle.tracer(1)
		t.speed(0)
	else:
		turtle.tracer(1)
		t.speed(turtle_info[0])
	
	t.width(turtle_info[2])
	
	figure_corners = 0
	segment_length = 0
	figure_x = 0
	figure_y = 0
	
	if (text1 != None):
		#получение значений из текстов для построения равностороннего многоугольника
		
		if (text1.get() != ""):
			figure_corners = int(text1.get())
		if (text2.get() != ""):
			segment_length = int(text2.get())
		if (text3.get() != ""):
			figure_x = int(text3.get())
		if (text4.get() != ""):
			figure_y = int(text4.get())
		
		root5.destroy()
	
	radius = circle_info[0]
	
	t.up()
	t.goto(circle_info[1], circle_info[2] - radius)
	t.down()
	
	t.circle(radius)
	
	t.up()
	
	t.width(turtle_info[1])
	
	if (InversionObjects == None or InversionObjects == True):
		#построение изначальных объектов
		
		for figure in range(int(len(objects))):
			t.up()
			t.goto(objects[figure][0], objects[figure][1])
			t.down()
			
			t.dot(turtle_info[1] + 1)
			
			for i in range(int(len(objects[figure]) / 2 - 1)):
				t.goto(objects[figure][i * 2 + 2], objects[figure][i * 2 + 3])
			t.goto(objects[figure][0], objects[figure][1])
		
		t.up()
		
		if (figure_corners > 0):
			#построение равностороннего многоугольника
			
			if (figure_corners == 1):
				objects.extend([[figure_x, figure_y]])
				
				t.goto(figure_x, figure_x)
				
				t.dot(turtle_info[1] + 1)
			else:
				rotate = (figure_corners - 2) * 180 / figure_corners + 180
				
				objects.extend([[]])
				
				if (figure_corners % 2):
					t.goto(figure_x - segment_length / 2, figure_y - (segment_length / (2 * math.sin(math.radians(180 / figure_corners)))))
				else:
					t.goto(figure_x - segment_length / 2, figure_y - (segment_length / 2 * pow(math.tan(math.radians(180 / figure_corners)), -1)))
				
				t.down()
				
				for i in range(figure_corners):
					t.forward(segment_length)
					t.rt(rotate)
					
					objects[len(objects) - 1].extend([int(round(t.xcor(), 0)), int(round(t.ycor(), 0))])
			
			t.up()
			
			close_painting_paint(0, 0)
	
	if (InversionObjects != None):
		#запись в массив каждого пикселя каждого объекта
		
		__objects = objects
		_objects = []
		
		for figure in range(int(len(__objects))):
			_objects.extend([[]])
			_objects[figure].extend([__objects[figure][0], __objects[figure][1]])
			
			for i in range(int((len(__objects[figure]) / 2) - 1)):
				if (abs(abs(__objects[figure][i * 2 + 3]) - abs(__objects[figure][i * 2 + 1])) > abs(abs(__objects[figure][i * 2 + 2]) - abs(__objects[figure][i * 2]))):
					if (__objects[figure][i * 2 + 3] != __objects[figure][i * 2 + 1]):
						many_coordinates_y(__objects, figure, i, _objects)
					elif (__objects[figure][i * 2 + 2] != __objects[figure][i * 2]):
						many_coordinates_x(__objects, figure, i, _objects)
				else:
					if (__objects[figure][i * 2 + 2] != __objects[figure][i * 2]):
						many_coordinates_x(__objects, figure, i, _objects)
					elif (__objects[figure][i * 2 + 3] != __objects[figure][i * 2 + 1]):
						many_coordinates_y(__objects, figure, i, _objects)
			
			if (len(__objects[figure]) > 4):
				if (abs(abs(_objects[figure][1]) - abs(__objects[figure][len(__objects[figure]) - 1])) > abs(abs(__objects[figure][0]) - abs(__objects[figure][len(__objects[figure]) - 2]))):
					if (__objects[figure][1] != __objects[figure][len(__objects[figure]) - 1]):
						end_many_coordinates_y(__objects, figure, _objects)
					elif (__objects[figure][0] != __objects[figure][len(__objects[figure]) - 2]):
						end_many_coordinates_x(__objects, figure, _objects)
				else:
					if (__objects[figure][0] != __objects[figure][len(__objects[figure]) - 2]):
						end_many_coordinates_x(__objects, figure, _objects)
					elif (__objects[figure][1] != __objects[figure][len(__objects[figure]) - 1]):
						end_many_coordinates_y(__objects, figure, _objects)
		
		#вычитание координат круга из каждой точки для корректной инверсии
		
		for figure in range(int(len(_objects))):
			for i in range(int(len(_objects[figure]) / 2)):
				_objects[figure][i * 2] -= circle_info[1]
				_objects[figure][i * 2 + 1] -= circle_info[2]
		
		for figure in range(int(len(_objects))):
			# проверка первой точки на координату (0, 0)
			
			if (_objects[figure][0] == 0 and _objects[figure][1] == 0):
				if (len(_objects[figure]) == 2):
					_objects[figure][0] = 0.01
					_objects[figure][1] = 0.01
					inversion_error(figure, 1, "+", "+")
				else:
					if (_objects[figure][2] >= 0):
						cor1 = "+"
						_objects[figure][0] = 0.01
					else:
						cor1 = "-"
						_objects[figure][0] = -0.01
					if (_objects[figure][3] >= 0):
						cor2 = "+"
						_objects[figure][1] = 0.01
					else:
						cor2 = "-"
						_objects[figure][1] = -0.01
					inversion_error(figure, 1, cor1, cor2)
			
			#начало инверсирования каждого пикселя объектов
			
			# инверсия первой точки
			
			op1 = math.sqrt(_objects[figure][0] * _objects[figure][0] + _objects[figure][1] * _objects[figure][1]) / (radius * radius / math.sqrt(_objects[figure][0] * _objects[figure][0] + _objects[figure][1] * _objects[figure][1]))
			t.goto((_objects[figure][0] / op1) + circle_info[1], (_objects[figure][1] / op1) + circle_info[2])
			
			t.dot(turtle_info[1] + 1)
			
			t.down()
			
			for i in range(int(len(_objects[figure]) / 2 - 1)):
				# проверка остальных точек на координату (0, 0)
				if (_objects[figure][i * 2 + 2] == 0 and _objects[figure][i * 2 + 3] == 0):
					if (_objects[figure][i * 2 + 2] >= 0):
						cor1 = "+"
						_objects[figure][i * 2 + 2] = 0.01
					else:
						cor1 = "-"
						_objects[figure][i * 2 + 2] = -0.01
					if (_objects[figure][i * 2 + 3] >= 0):
						cor2 = "+"
						_objects[figure][i * 2 + 3] = 0.01
					else:
						cor2 = "-"
						_objects[figure][i * 2 + 3] = -0.01
						inversion_error(figure, 1, cor1, cor2)
				
				# инверсия остальных точек
				op = math.sqrt(_objects[figure][i * 2 + 2] * _objects[figure][i * 2 + 2] + _objects[figure][i * 2 + 3] * _objects[figure][i * 2 + 3]) / (radius * radius / math.sqrt(_objects[figure][i * 2 + 2] * _objects[figure][i * 2 + 2] + _objects[figure][i * 2 + 3] * _objects[figure][i * 2 + 3]))
				t.goto((_objects[figure][i * 2 + 2] / op) + circle_info[1], (_objects[figure][i * 2 + 3] / op) + circle_info[2])
			
			t.up()
	
	t.hideturtle()
	
	if (turtle_info[0] == 12):
		turtle.update()

def end_many_coordinates_y(__objects, figure, _objects):
	b = float((__objects[figure][0] - __objects[figure][len(__objects[figure]) - 2]) / (__objects[figure][1] - __objects[figure][len(__objects[figure]) - 1]))
	if (__objects[figure][1] < __objects[figure][len(__objects[figure]) - 1]):
		for middleCoordinat in range(abs(__objects[figure][1] - __objects[figure][len(__objects[figure]) - 1])):
			_objects[figure].extend([__objects[figure][len(__objects[figure]) - 2] - b * (middleCoordinat + 1), __objects[figure][len(__objects[figure]) - 1] - middleCoordinat - 1])
	else:
		for middleCoordinat in range(abs(__objects[figure][1] - __objects[figure][len(__objects[figure]) - 1])):
			_objects[figure].extend([__objects[figure][len(__objects[figure]) - 2] + b * (middleCoordinat + 1), __objects[figure][len(__objects[figure]) - 1] + middleCoordinat + 1])

def end_many_coordinates_x(__objects, figure, _objects):
	b = float((__objects[figure][1] - __objects[figure][len(__objects[figure]) - 1]) / (__objects[figure][0] - __objects[figure][len(__objects[figure]) - 2]))
	if (__objects[figure][0] < __objects[figure][len(__objects[figure]) - 2]):
		for middleCoordinat in range(abs(__objects[figure][0] - __objects[figure][len(__objects[figure]) - 2])):
			_objects[figure].extend([__objects[figure][len(__objects[figure]) - 2] - middleCoordinat - 1, __objects[figure][len(__objects[figure]) - 1] - b * (middleCoordinat + 1)])
	else:
		for middleCoordinat in range(abs(__objects[figure][0] - __objects[figure][len(__objects[figure]) - 2])):
			_objects[figure].extend([__objects[figure][len(__objects[figure]) - 2] + middleCoordinat + 1, __objects[figure][len(__objects[figure]) - 1] + b * (middleCoordinat + 1)])

def many_coordinates_y(__objects, figure, i, _objects):
	b = float((__objects[figure][i * 2 + 2] - __objects[figure][i * 2]) / (__objects[figure][i * 2 + 3] - __objects[figure][i * 2 + 1]))
	if (__objects[figure][i * 2 + 3] < __objects[figure][i * 2 + 1]):
		for middleCoordinat in range(abs(__objects[figure][i * 2 + 3] - __objects[figure][i * 2 + 1])):
			_objects[figure].extend([__objects[figure][i * 2] - b * (middleCoordinat + 1), __objects[figure][i * 2 + 1] - middleCoordinat - 1])
	else:
		for middleCoordinat in range(abs(__objects[figure][i * 2 + 3] - __objects[figure][i * 2 + 1])):
			_objects[figure].extend([__objects[figure][i * 2] + b * (middleCoordinat + 1), __objects[figure][i * 2 + 1] + middleCoordinat + 1])

def many_coordinates_x(__objects, figure, i, _objects):
	b = float((__objects[figure][i * 2 + 3] - __objects[figure][i * 2 + 1]) / (__objects[figure][i * 2 + 2] - __objects[figure][i * 2]))
	if (__objects[figure][i * 2 + 2] < __objects[figure][i * 2]):
		for middleCoordinat in range(abs(__objects[figure][i * 2 + 2] - __objects[figure][i * 2])):
			_objects[figure].extend([__objects[figure][i * 2] - middleCoordinat - 1, __objects[figure][i * 2 + 1] - b * (middleCoordinat + 1)])
	else:
		for middleCoordinat in range(abs(__objects[figure][i * 2 + 2] - __objects[figure][i * 2])):
			_objects[figure].extend([__objects[figure][i * 2] + middleCoordinat + 1, __objects[figure][i * 2 + 1] + b * (middleCoordinat + 1)])

def inversion_error(object, text, cor1, cor2):
	#открытие ошибки инверсии
    
	root9 = tk.Tk()
	root9.focus_force()
	root9.title("Ошибка инверсии")
	root9.resizable(False, False)
	root9.attributes('-toolwindow', True)
    
	root9.bind("<Escape>", lambda event: quit())
	root9.bind("r", lambda event: reference())
	
	if (text == 0):
		root9.geometry("270x70+500+300")
		tk.Label(root9, text="Невозможно корректно инверсировать").pack()
		tk.Label(root9, text="объекты, так как в объекте " + str(object + 1)).pack()
		tk.Label(root9, text="присутствует всего одна координата").pack()
	else:
		root9.geometry("330x110+500+300")
		tk.Label(root9, text="Невозможно корректно инверсировать объекты так как").pack()
		tk.Label(root9, text="в объекте " + str(object + 1) + " присутствует точка лежащая").pack()
		tk.Label(root9, text="на координате (0, 0) которая должна быть инверсирована").pack()
		tk.Label(root9, text="в (бесконечность, бесконечность) поэтому будет").pack()
		tk.Label(root9, text="инверсирована как точка (" + cor1 + "0.01, " + cor2 + "0.01)").pack()

def painting_paint_and_save_object_info(text1 = None, text2 = None, text3 = None, text4 = None, root5 = None):
    close_object_info()
    painting_paint(text1, text2, text3, text4, root5)

def is_validate(newval):
	#для того чтобы вводились только цифры
	
	return re.match("^-?\d*$", newval) is not None

def is_validate2(newval):
	#для того чтобы вводились только цифры с возможностью вводить дробную часть
	
	return re.match("^\d*[.]?\d*?$", newval) is not None

def add_objects_to_object(frame):
	#добавление координаты в объект
	
	i = int(len(objects[object - 1]) / 2)
	
	check_validate = (root3.register(is_validate), "%P")
	
	l = tk.Label(frame, text=str(i + 1) + ")")
	l.grid(row = i + 1, column = 0, padx = 1, pady = 1)
	
	x_text = tk.Entry(frame, width = 4, validate="key", validatecommand = check_validate)
	x_text.grid(row = i + 1, column = 1, padx = 3, pady = 1)
	y_text = tk.Entry(frame, width = 4, validate="key", validatecommand = check_validate)
	y_text.grid(row = i + 1, column = 2, padx = 3, pady = 1)
	
	if (i % 2):
		root3.geometry("125x150+100+0")
	else:
		root3.geometry("125x151+100+0")
	
	objects[object - 1].extend([0, 0])
	
	turtle_inputs.extend([x_text, y_text])

def open_circle_info():
	#открытие параметров круга
	
	global info_is_open
	
	if (info_is_open == False):
		global root6
		global turtle_inputs
		global circle_info
		
		info_is_open = True
		
		root6 = tk.Tk()
		root6.focus_force()
		root6.protocol("WM_DELETE_WINDOW", lambda: close_object_info())
		root6.title("Круг")
		root6.geometry("90x80+100+0")
		root6.resizable(False, False)
		root6.attributes('-toolwindow', True)
		
		check_validate = (root6.register(is_validate), "%P")
		
		tk.Label(root6, text="Радиус").grid(row = 0, column = 0, padx = 1, pady = 1)
		text1 = tk.Entry(root6, width = 4, validate="key", validatecommand = check_validate)
		text1.grid(row = 0, column = 1, padx = 3, pady = 1)
		text1.insert(0, str(circle_info[0]))
		tk.Label(root6, text="X").grid(row = 1, column = 0, padx = 3, pady = 1)
		text2 = tk.Entry(root6, width = 4, validate="key", validatecommand = check_validate)
		text2.grid(row = 1, column = 1, padx = 3, pady = 1)
		text2.insert(0, str(circle_info[1]))
		tk.Label(root6, text="Y").grid(row = 2, column = 0, padx = 3, pady = 1)
		text3 = tk.Entry(root6, width = 4, validate="key", validatecommand = check_validate)
		text3.grid(row = 2, column = 1, padx = 3, pady = 1)
		text3.insert(0, str(circle_info[2]))
        
		turtle_inputs.extend([[text1, text2, text3, 1]])
		
		root6.bind("<Escape>", lambda event: quit())
		root6.bind("r", lambda event: reference())
		
		root6.mainloop()
	else:
		close_object_info()
		
		open_circle_info()

def open_coordinates_info():
	#открытие параметров координат
	
	global info_is_open
	
	if (info_is_open == False):
		global root10
		global turtle_inputs
		global coordinats_info
		
		info_is_open = True
		
		root10 = tk.Tk()
		root10.focus_force()
		root10.protocol("WM_DELETE_WINDOW", lambda: close_object_info())
		root10.title("Координаты")
		root10.geometry("200x80+100+0")
		root10.resizable(False, False)
		root10.attributes('-toolwindow', True)
		
		check_validate = (root10.register(is_validate), "%P")
		check_validate2 = (root10.register(is_validate2), "%P")
		
		tk.Label(root10, text="1 пиксель = (координат)").grid(row = 0, column = 0, padx = 1, pady = 1)
		text1 = tk.Entry(root10, width = 4, validate="key", validatecommand = check_validate2)
		text1.grid(row = 0, column = 1, padx = 3, pady = 1)
		text1.insert(0, str(coordinats_info[0]))
		tk.Label(root10, text="Смещение координат по X").grid(row = 1, column = 0, padx = 3, pady = 1)
		text2 = tk.Entry(root10, width = 4, validate="key", validatecommand = check_validate)
		text2.grid(row = 1, column = 1, padx = 3, pady = 1)
		text2.insert(0, str(coordinats_info[2]))
		tk.Label(root10, text="Смещение координат по Y").grid(row = 2, column = 0, padx = 3, pady = 1)
		text3 = tk.Entry(root10, width = 4, validate="key", validatecommand = check_validate)
		text3.grid(row = 2, column = 1, padx = 3, pady = 1)
		text3.insert(0, str(coordinats_info[1]))
        
		turtle_inputs.extend([[text1, text3, text2, 2]])
		
		root10.bind("<Escape>", lambda event: quit())
		root10.bind("r", lambda event: reference())
		
		root10.mainloop()
	else:
		close_object_info()
		
		open_coordinates_info()

def open_turtle_info():
	#открытие параметров кисти
	
	global info_is_open
	
	if (info_is_open == False):
		global root7
		global turtle_inputs
		global turtle_info
		
		info_is_open = True
		
		root7 = tk.Tk()
		root7.focus_force()
		root7.protocol("WM_DELETE_WINDOW", lambda: close_object_info())
		root7.title("Кисть")
		root7.geometry("175x80+100+0")
		root7.resizable(False, False)
		root7.attributes('-toolwindow', True)
		
		check_validate = (root7.register(is_validate), "%P")
		
		tk.Label(root7, text="Скорость кисти (1-12)").grid(row = 0, column = 0, padx = 1, pady = 1)
		text1 = tk.Entry(root7, width = 4, validate="key", validatecommand = check_validate)
		text1.grid(row = 0, column = 1, padx = 3, pady = 1)
		text1.insert(0, str(turtle_info[0]))
		tk.Label(root7, text="Толщина круга").grid(row = 1, column = 0, padx = 3, pady = 1)
		text2 = tk.Entry(root7, width = 4, validate="key", validatecommand = check_validate)
		text2.grid(row = 1, column = 1, padx = 3, pady = 1)
		text2.insert(0, str(turtle_info[2]))
		tk.Label(root7, text="Толщина объектов").grid(row = 2, column = 0, padx = 3, pady = 1)
		text3 = tk.Entry(root7, width = 4, validate="key", validatecommand = check_validate)
		text3.grid(row = 2, column = 1, padx = 3, pady = 1)
		text3.insert(0, str(turtle_info[1]))
        
		turtle_inputs.extend([[text1, text3, text2, 0]])
		
		root7.bind("<Escape>", lambda event: quit())
		root7.bind("r", lambda event: reference())
		
		root7.mainloop()
	else:
		close_object_info()
		
		open_turtle_info()

def open_object_info(_object):
	#открытие параметров объекта
	
	global info_is_open
	
	if (info_is_open == False):
		global root3
		global turtle_inputs
		global object
		
		info_is_open = True
		object = _object
		
		root3 = tk.Tk()
		root3.focus_force()
		root3.protocol("WM_DELETE_WINDOW", lambda: close_object_info())
		root3.title("Объект " + str(object))
		root3.geometry("125x150+100+0")
		root3.resizable(False, False)
		root3.attributes('-toolwindow', True)
		
		LabelFrame3 = tk.LabelFrame(root3)
		canvas3 = tk.Canvas(LabelFrame3)
		canvas3.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
		scroll3 = tk.Scrollbar(root3, orient = "vertical", command = canvas3.yview)
		scroll3.pack(side = tk.RIGHT, fill = tk.Y)
		canvas3.configure(yscrollcommand = scroll3.set)
		canvas3.bind("<Configure>", lambda event: canvas3.configure(scrollregion = canvas3.bbox("all")))
		frame3 = tk.Frame(canvas3)
		frame3.pack(fill = tk.X)
		canvas3.create_window((0, 0), window = frame3, anchor = "nw")
		LabelFrame3.pack(fill = tk.BOTH, expand = True)
		
		tk.Label(frame3, text="№").grid(row = 0, column = 0, padx = 1, pady = 1)
		tk.Label(frame3, text="X").grid(row = 0, column = 1, padx = 3, pady = 1)
		tk.Label(frame3, text="Y").grid(row = 0, column = 2, padx = 3, pady = 1)
		
		check_validate = (root3.register(is_validate), "%P")
		
		for i in range(int(len(objects[object - 1]) / 2)):
			l = tk.Label(frame3, text=str(i + 1) + ")")
			l.grid(row = i + 1, column = 0, padx = 1, pady = 1)
		for i in range(int(len(objects[object - 1]) / 2)):
			x_text = tk.Entry(frame3, width = 4, validate="key", validatecommand = check_validate)
			x_text.grid(row = i + 1, column = 1, padx = 3, pady = 1)
			x_text.insert(0, str(objects[object - 1][i * 2]))
			y_text = tk.Entry(frame3, width = 4, validate="key", validatecommand = check_validate)
			y_text.grid(row = i + 1, column = 2, padx = 3, pady = 1)
			y_text.insert(0, str(objects[object - 1][i * 2 + 1]))
			turtle_inputs.extend([x_text, y_text])
		
		root3.bind("c", func = lambda event: add_objects_to_object(frame3))
		root3.bind("<Escape>", lambda event: quit())
		root3.bind("r", lambda event: reference())
		root3.bind("<Delete>", lambda event: delete_object(object))
		
		root3.mainloop()
	else:
		close_object_info()
		
		open_object_info(_object)

def delete_object(object):
	#удаление объекта
	
	global root3
	global turtle_inputs
	global info_is_open
	
	objects.pop(object - 1)
	
	turtle_inputs.clear()
	info_is_open = False
	root3.destroy()
	
	close_painting_paint(0, 0)
	open_painting_paint()

def close_object_info():
	#закрытие параметров
	
	global info_is_open
	
	if (info_is_open == True):
		global turtle_inputs
		
		if (len(turtle_inputs) == 1):
			if (turtle_inputs[0][3] == 0):
				#закрытие параметров кисти
				
				global root7
				global turtle_info
				
				turtle_info.clear()
				
				for i in range(3):
					if (turtle_inputs[0][i].get() != ""):
						turtle_info.extend([int(turtle_inputs[0][i].get())])
					else:
						turtle_info.extend([0])
				
				root7.destroy()
				turtle_inputs.clear()
				info_is_open = False
			elif (turtle_inputs[0][3] == 1):
				#закрытие параметров круга
				
				global root6
				global circle_info
				
				circle_info.clear()
				
				for i in range(3):
					if (turtle_inputs[0][i].get() != "" and turtle_inputs[0][i].get() != "-"):
						circle_info.extend([int(turtle_inputs[0][i].get())])
					else:
						circle_info.extend([0])
				
				root6.destroy()
				turtle_inputs.clear()
				info_is_open = False
			else:
				#закрытие параметров координат
				
				global root10
				global coordinats_info
				
				coordinats_info.clear()
				
				if (turtle_inputs[0][0].get() != "" and turtle_inputs[0][0].get() != "-"):
					coordinats_info.extend([float(turtle_inputs[0][0].get())])
				else:
					coordinats_info.extend([0.0])
				
				for i in range(2):
					if (turtle_inputs[0][i + 1].get() != ""):
						coordinats_info.extend([int(turtle_inputs[0][i + 1].get())])
					else:
						coordinats_info.extend([0])
				
				root10.destroy()
				turtle_inputs.clear()
				info_is_open = False
		else:
			#закрытие параметров объекта
			
			global root3
			global object
			
			objects[object - 1].clear()
				
			for i in range(len(turtle_inputs)):
				if (turtle_inputs[i].get() != "" and turtle_inputs[i].get() != "-"):
					objects[object - 1].extend([int(turtle_inputs[i].get())])
				else:
					objects[object - 1].extend([0])
			
			root3.destroy()
			turtle_inputs.clear()
			info_is_open = False

def create_object(frame):
	#создание объекта
	
	global objects
	
	objects.extend([[0, 0]])
	objects_length = len(objects)
	tk.Button(frame, text="Объект " + str(objects_length), command = lambda: open_object_info(objects_length)).pack(fill = tk.X, pady = 1)
	
	if (objects_length % 2):
		root2.geometry("100x150+0+0")
	else:
		root2.geometry("100x151+0+0")

def respawn_object(frame, i):
	#показ уже созданного объекта
	
	tk.Button(frame, text="Объект " + str(i), command = lambda: open_object_info(i)).pack(fill = tk.X, pady = 1)

def reference():
	#открытие справки
	
	root4 = tk.Tk()
	root4.focus_force()
	root4.title("Справка")
	root4.geometry("225x220+500+300")
	root4.resizable(False, False)
	root4.attributes('-toolwindow', True)
	
	root4.bind("<Escape>", lambda event: quit())
	
	tk.Label(root4, text="R - Справка").place(x = 0, y = 0)
	tk.Label(root4, text="Escape - Выйти").place(x = 0, y = 20)
	tk.Label(root4, text="W - Открыть окно объектов").place(x = 0, y = 40)
	tk.Label(root4, text="L - Обновить сцену").place(x = 0, y = 60)
	tk.Label(root4, text="I - Инверсировать объекты").place(x = 0, y = 80)
	tk.Label(root4, text="G - Создать равностороннюю фигуру").place(x = 0, y = 100)
	tk.Label(root4, text="O - Создать объект").place(x = 0, y = 120)
	tk.Label(root4, text="C - Создать координату").place(x = 0, y = 140)
	tk.Label(root4, text="X - Скопировать координаты").place(x = 0, y = 160)
	tk.Label(root4, text="V - Вставить координаты").place(x = 0, y = 180)
	tk.Label(root4, text="Delete - Удалить объект").place(x = 0, y = 200)

def quit():
	#выход из программы
	
	sys.exit()

def open_window_create_geometry_figure():
	#открытие окна для создания равностороннего многоугольника
	
	root5 = tk.Tk()
	root5.focus_force()
	root5.title("Фигура")
	root5.geometry("175x130+500+300")
	root5.resizable(False, False)
	root5.attributes('-toolwindow', True)
	
	frame = tk.Frame(root5, padx = 1, pady = 1)
	frame.pack()
	
	check_validate = (root5.register(is_validate), "%P")
	
	l1 = tk.Label(frame, text="Количество углов:")
	l1.grid(row = 0, column = 0, padx = 1, pady = 1)
	text1 = tk.Entry(frame, width = 4, validate="key", validatecommand = check_validate)
	text1.grid(row = 0, column = 1, padx = 3, pady = 1)
	l2 = tk.Label(frame, text="Длина одной стороны:")
	l2.grid(row = 1, column = 0, padx = 1, pady = 1)
	text2 = tk.Entry(frame, width = 4, validate="key", validatecommand = check_validate)
	text2.grid(row = 1, column = 1, padx = 3, pady = 1)
	l3 = tk.Label(frame, text="Координата X:")
	l3.grid(row = 3, column = 0, padx = 1, pady = 1)
	text3 = tk.Entry(frame, width = 4, validate="key", validatecommand = check_validate)
	text3.grid(row = 3, column = 1, padx = 3, pady = 1)
	l4 = tk.Label(frame, text="Координата Y:")
	l4.grid(row = 4, column = 0, padx = 1, pady = 1)
	text4 = tk.Entry(frame, width = 4, validate="key", validatecommand = check_validate)
	text4.grid(row = 4, column = 1, padx = 3, pady = 1)
	b1 = tk.Button(root5, text="Нарисовать", command = lambda: painting_paint_and_save_object_info(text1, text2, text3, text4, root5))
	b1.pack(pady = 3)
	
	root5.bind("r", lambda event: reference())
	root5.bind("<Escape>", lambda event: quit())
	
	root5.mainloop()

def open_paste_coordinats():
	#открытие окна для вставки массива координат
	
	root11 = tk.Tk()
	root11.focus_force()
	root11.title("Вставка")
	root11.geometry("260x80+500+300")
	root11.resizable(False, False)
	root11.attributes('-toolwindow', True)
	
	tk.Label(root11, text="Введите ранее скопированные координаты").pack(padx = 1, pady = 1)
	text1 = tk.Entry(root11, width = 30)
	text1.pack(padx = 3, pady = 1)
	tk.Button(root11, text="Ок", command = lambda: paste_coordinats(text1.get(), root11)).pack(pady = 3)
	
	root11.bind("r", lambda event: reference())
	root11.bind("<Escape>", lambda event: quit())
	
	root11.mainloop()

def copy_coordinats():
	global objects
	pyperclip.copy(str(objects))
	#сообщение о копировании координат
    
	root12 = tk.Tk()
	root12.focus_force()
	root12.title("Копирование")
	root12.geometry("230x30+500+300")
	root12.resizable(False, False)
	root12.attributes('-toolwindow', True)
	
	root12.bind("<Escape>", lambda event: quit())
	root12.bind("r", lambda event: reference())
	
	tk.Label(root12, text="Координаты успешно скопированы").pack()

def paste_coordinats(string, root11):
	#вставка координат в массив
	
	global objects
	end = -2
	
	while True:
		start = end + 4
		if (start > len(string)):
			break
		end = string.find("]", start)
		objects.extend([list(map(int, string[start:end].split(",")))])
	
	root11.destroy()

def close_painting_paint(x, y):
	#закрытия окна объектов
	
	global root2_destroyed
	
	if (root2_destroyed == False):
		global root2
		
		root2_destroyed = True
		
		root2.destroy()
		
		close_object_info()

def open_painting_paint():
	#открытие окна объектов
	
	global root2_destroyed
	
	if (root2_destroyed == True):
		global root2
		
		root2_destroyed = False
		
		root2 = tk.Tk()
		root2.focus_force()
		root2.protocol("WM_DELETE_WINDOW", lambda: close_painting_paint(0, 0))
		root2.title("Объекты")
		root2.geometry("100x150+0+0")
		root2.resizable(False, False)
		root2.attributes('-toolwindow', True)
		
		LabelFrame = tk.LabelFrame(root2)
		canvas = tk.Canvas(LabelFrame)
		canvas.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
		scroll = tk.Scrollbar(root2, orient = "vertical", command = canvas.yview)
		scroll.pack(side = tk.RIGHT, fill = tk.Y)
		canvas.configure(yscrollcommand = scroll.set)
		canvas.bind("<Configure>", lambda event: canvas.configure(scrollregion = canvas.bbox("all")))
		frame = tk.Frame(canvas)
		frame.pack(padx = 3)
		canvas.create_window((0, 0), window = frame, anchor = "nw")
		LabelFrame.pack(fill = tk.BOTH, expand = True)
		
		root2.bind("o", lambda event: create_object(frame))
		root2.bind("l", lambda event: painting_paint_and_save_object_info())
		root2.bind("g", lambda event: open_window_create_geometry_figure())
		root2.bind("i", lambda event: open_inversion())
		root2.bind("r", lambda event: reference())
		root2.bind("x", lambda event: copy_coordinats())
		root2.bind("v", lambda event: open_paste_coordinats())
		root2.bind("<Escape>", lambda event: quit())
		
		tk.Button(frame, text="Круг", command = lambda: open_circle_info()).pack(fill = tk.X, pady = 1)
		tk.Button(frame, text="Кисть", command = lambda: open_turtle_info()).pack(fill = tk.X, pady = 1)
		tk.Button(frame, text="Координаты", command = lambda: open_coordinates_info()).pack(fill = tk.X, pady = 1)
		
		for i in range(len(objects)):
			respawn_object(frame, i + 1)
		
		root2.mainloop()

def anclose_turtle():
	#блокировка закрытия сцены
	
	pass

def open_inversion():
	#открытие окна для инверсирования
	
	root8 = tk.Tk()
	root8.focus_force()
	root8.title("Инверсировать объекты")
	root8.geometry("225x75+500+300")
	root8.resizable(False, False)
	root8.attributes('-toolwindow', True)
	
	root8.bind("<Escape>", lambda event: quit())
	root8.bind("r", lambda event: reference())
	
	tk.Label(root8, text="Нарисовать изначальные объекты?").pack()
	tk.Button(root8, text="Нет", command = lambda: painting_paint(None, None, None, None, None, False, root8)).place(x = 51, y = 40, width = 50, height = 20)
	tk.Button(root8, text="Да", command = lambda: painting_paint(None, None, None, None, None, True, root8)).place(x = 124, y = 40, width = 50, height = 20)

def open_turtle():
	#открытие сцены
	
	global t
	
	root1.destroy()
	
	t = turtle.Turtle()
	wn = turtle.Screen()
	wn.setup(1.0, 1.0)
	canvas = wn.getcanvas()
	root = canvas.winfo_toplevel()
	root.overrideredirect(1)
	root.focus_force()
	root.protocol("WM_DELETE_WINDOW", anclose_turtle)
	
	wn.onkey(fun = open_inversion, key = "i")
	wn.onkey(fun = open_painting_paint, key = "w")
	wn.onkeypress(fun = quit, key = "Escape")
	wn.onkey(fun = reference, key = "r")
	wn.onkey(fun = open_window_create_geometry_figure, key = "g")
	wn.onkey(fun = painting_paint_and_save_object_info, key = "l")
	wn.onkey(fun = copy_coordinats, key = "x")
	wn.onkey(fun = open_paste_coordinats, key = "v")
	wn.onclick(fun = close_painting_paint)
	
	t.hideturtle()
	
	wn.listen()
	wn.mainloop()

#открытие начального окна-обучения

root1 = tk.Tk()
root1.title("Инверсия относительно окружности")
root1.geometry("325x200+500+300")
root1.resizable(False, False)
root1.attributes('-toolwindow', True)

frame = tk.Frame(root1).pack(pady = 5)

tk.Label(frame, text="Это программа по созданию").pack()
tk.Label(frame, text="инверсии относительно окружности").pack()
tk.Label(frame, text="Для получения справки об управлении нажмите R").pack()
tk.Label(frame, text="Требуется включить английскую раскладку").pack()
tk.Label(frame, text="Перед использованием желательно").pack()
tk.Label(frame, text="свернуть все открытые приложения").pack()
tk.Label(frame, text="В измерениях может присутствовать погрешность").pack()
tk.Button(root1, text="ОК", command = lambda: open_turtle()).place(x = 112, y = 165, width = 100, height = 25)

root1.bind("<Escape>", lambda event: quit())

root1.mainloop()
#pyinstaller -w -F -i"E:\python\python.ico" circle_inversion.py
import tkinter as tk
import base64

class EncodingApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.geometry = "750x750"
		self.title = "Encoding App"
		self.resizable(0,0)
		
		self.colors = {'dark-brown':  "#cb997e", 
						'brown': 	  "#ddbea9", 
						'light-brown': "#ffe8d6",
						'light-green': "#b7b7a4", 
						'green': 	  "#a5a58d", 
						'dark-green':  "#6b705c"}
		self.grid_rowconfigure((0,6), weight = 1)
		self.grid_columnconfigure((0,1), weight=1)
		self.configure(background=self.colors['light-brown'])
		self.widgets = self.get_widgets()
	

	def get_widgets(self):
		tk.Label(self, text= 'ENCODE or DECODE your message!', font=('Calibri', 30, 'bold'), background=self.colors['light-brown']).grid(row=0, columnspan=2, padx=50, pady=20)
		
		tk.Label(self, text="Message", font=('Calibri', 15), background=self.colors['light-brown']).grid(row=1, column=0, sticky='w', padx=20, pady=(0,20))
		self.message_sv = tk.StringVar(self)
		self.message_sv.trace("w", lambda name, index, mode: self.entry_callback())
		self.message_entry = tk.Entry(self, bd=3, textvariable=self.message_sv, width=75)
		self.message_entry.grid(row=1, column=1, sticky='w', padx=20, pady=(0,20))
		
		
		tk.Label(self, text="Key", font=('Calibri', 15), background=self.colors['light-brown']).grid(row=2, column=0, sticky='w', padx=20, pady=(0,20))
		self.key_sv = tk.StringVar(self)
		self.key_sv.trace("w", lambda name, index, mode: self.entry_callback())
		self.key_entry = tk.Entry(self, bd=3, textvariable=self.key_sv, width=75)
		self.key_entry.grid(row=2, column=1, sticky='w', padx=20, pady=(0,20))

		tk.Label(self, text="Mode", font=('Calibri', 15), background=self.colors['light-brown']).grid(row=3, column=0, sticky='w', padx=20, pady=(0,20))
		self.mode_sv = tk.StringVar(self)
		self.mode_sv.trace("w", lambda name, index, mode: self.entry_callback())
		self.mode_sv.set('encode')
		self.mode_entry = tk.OptionMenu(self, self.mode_sv, 'encode', 'decode')
		self.mode_entry.configure(width=70)
		self.mode_entry.grid(row=3, column=1, sticky='w', padx=20)

		
		self.result_lbl = tk.Label(self, text="Result", font=('Calibri 20 underline'), background=self.colors['light-brown'])
		self.result_lbl.grid(row=4, columnspan=2, sticky='w', padx=20, pady=(40,10))
		self.result_lbl_desc = tk.Text(self,  font=('Calibri', 15), background='white', height=10)
		self.result_lbl_desc.grid(row=5, columnspan=2, sticky='ew', padx=20)

		self.reset_btn = tk.Button(self, text='Reset', bg='red', font=('Calibri', 20, 'bold'), command=self.clear_all_input)
		self.reset_btn.grid(row=6, columnspan=2, pady=20)

	def clear_all_input(self):
		self.result_lbl_desc.delete('1.0', tk.END)
		for child in self.winfo_children():
			if(child.widgetName == 'entry'):
				child.delete(0, 'end')

	def encode(self, key = None, message = None):
		enc = []
		if key != '' and message != '':
			for i in range(len(message)):
				key_c = key[i % len(key)]
				enc.append(chr((ord(message[i]) + ord(key_c)) % 256))

			self.result_lbl_desc.delete('1.0', tk.END)
			encoded_message = base64.urlsafe_b64encode(''.join(enc).encode()).decode()
			self.result_lbl_desc.insert('1.0', encoded_message)

	
	def decode(self, key, message):
		dec=[]

		if key != '' and message != '':
			message = base64.urlsafe_b64decode(message).decode()

			for i in range(len(message)):
				key_c = key[i % len(key)]
				dec.append(chr((256 + ord(message[i]) - ord(key_c)) % 256))
			
			self.result_lbl_desc.delete('1.0', tk.END)
			decoded_message = ''.join(dec)
			self.result_lbl_desc.insert('1.0', decoded_message)

	def entry_callback(self):
		if self.mode_sv.get() == 'encode':
			self.encode(key=self.key_sv.get(), message=self.message_sv.get())
		elif self.mode_sv.get() == 'decode':
			self.decode(key=self.key_sv.get(), message=self.message_sv.get())



app = EncodingApp()
app.mainloop()
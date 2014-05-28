import PacketType

class Marshal:

	def __init__(self):
		self.marshalledData = bytearray()
		self.unmarshalledData = bytearray()

	def put_marshalled(self, data):
		if not type(data) is int:
			dataLen = len(data)

		print repr(data)

		self.marshalledData += bytearray(data)

	def put_unmarshalled(self, data):
		self.unmarshalledData += bytearray(data)

	def marshal(self, data):
		self.put_marshalled(PacketType.PACKET_HEADER)
		self.put_marshalled(bytes([0,0,0,0]))

		if type(data) is tuple:
			self.marshal_tuple(data)

	def processData(self, data):

		# Base data types
		if type(data) is int:
			self.marshal_int(data)
		
		elif type(data) is long:
			self.marshal_long(data)
		
		elif type(data) is float:
			self.marshal_float(data)
		
		elif type(data) is bool:
			self.marshal_bool(data)
		
		elif type(data) is None:
			self.marshal_none(data)
		
		elif type(data) is list:
			self.marshal_list(data)
		
		elif type(data) is tuple:
			self.marshal_tuple(data)

		elif type(data) is dict:
			self.marshal_dict(data)

		elif type(data) is str:
			self.marshal_string(data)

		elif type(data) is unicode:
			self.marshal_unicode_str(data)

		elif type(data) is chr:
			self.marshal_char(data)

		elif type(data) is buffer:
			self.marshal_buffer(data)

	def marshal_int(self, data):
		pass

	def marshal_long(self, data):
		pass

	def marshal_float(self, data):
		pass

	def marshal_bool(self, data):
		pass

	def marshal_none(self, data):
		pass

	def marshal_list(self, data):
		pass

	def marshal_tuple(self, data):
		pass

	def marshal_dict(self, data):
		pass

	def marshal_string(self, data):
		pass

	def marshal_unicode_str(self, data):
		pass

	def marshal_char(self, data):
		pass

	def marshal_buffer(self, data):
		pass

	def marshal_tuple(self, data):
		tupleLen = len(data)

		if tupleLen == 0:
			self.put_marshalled(PacketType.TYPE_TUPLE0)
		elif tupleLen == 1:
			self.put_marshalled(PacketType.TYPE_TUPLE1)
			self.processElement(data[0])
		elif tupleLen == 2:
			self.put_marshalled(PacketType.TYPE_TUPLE2)
			self.processElement(data[0])
			self.processElement(data[1])
		else:
			self.put_marshalled(PacketType.TYPE_TUPLE)
			self.put_marshalled(tupleLen)

			for element in data:
				self.processElement(element)




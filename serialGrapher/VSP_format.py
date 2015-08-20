import struct
import binascii

log_info = "VSP_format: "

class Formatter(object):
        def __init__(self, len_packet, format_string, token='$$$', verbose=False):
                self.len_packet = len_packet # in bytes
                self.format_string = format_string # struct formatting
                self.token = token
                self.verbose = verbose
                self.raw_data = ""
		
	def parse(self, new_data, finish=False):
                if self.verbose:
                        #print log_info, "New data", new_data
                        pass
		if new_data != None and len(new_data) > 0 or finish:
                        if new_data != None:
                                self.raw_data += new_data[0] # get data
			if self.verbose:
                                print log_info + "Raw data " + binascii.hexlify(self.raw_data)
			index = self.raw_data.find(self.token)
			if index != -1:
                                if self.verbose:
                                        print log_info + "Token found at ", index
				substring = self.raw_data[index+len(self.token):]
				if self.verbose:
                                        print log_info + "Length of substring", len(substring)
				if len(substring) >= self.len_packet:
                                        if self.verbose:
                                                print log_info + "Substring in hex " + binascii.hexlify(substring[0:self.len_packet])
					data = struct.unpack(self.format_string, substring[0:self.len_packet])
					self.raw_data = substring[self.len_packet:] #TODO I don't think I need to add 1
					if self.verbose:
                                                print log_info + "Raw data in hex " + binascii.hexlify(self.raw_data)
					return data
				else:
					return None
    
		return None
		

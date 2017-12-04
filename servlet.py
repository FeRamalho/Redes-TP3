import socket
import sys
import struct

def main():

	# Input arguments
	port = int(sys.argv[1])
	input_name = sys.argv[2]
	peer_list = sys.argv[3]
	#print(port,'\n',input_name,'\n',peer_list)
	print('Starting at port-', port,'\n','Reading file-',input_name)

	# DICT
	keys = {}
	connections = []
	seen_req = {}

	# Peer connections    peer_list = string   connections  = tupla
	peer_list = peer_list.replace('[', ' ')
	peer_list = peer_list.replace(']', '')
	peer_list = peer_list.split()
	for peer in peer_list:
		peer_ip, x , peer_port = peer.partition(':')
		connections.append( (peer_ip, int(peer_port)) )

	# Reading keys from input
	input_file = open(input_name, 'r')
	for line in input_file:
		# Not comments
		if not line.startswith('#'):
			key, x, value = line.partition(' ')
			value = value.strip(' ')
			value = value.strip('\n')
			keys[key] = value
	input_file.close()

	# Create udp socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	# Bind socket to port
	my_address = ('127.0.0.1', port)
	sock.bind(my_address)

	# Start application
	while(1):
		data, address = sock.recvfrom(500)
		ip_origem = address[0]
		port_origem = address[1]
		typ = struct.unpack('!H',data[:2])[0]

		# KEY REQ
		if(typ == 5):
			numsq = struct.unpack('!I', data[2:6])[0]
			reqkey = data[6:].decode()
			print(reqkey)
			if(reqkey in keys.keys()):
				print(keys[reqkey])
				#answer = struct.pack('!H', 9) + struct.pack('!I', numsq) + keys[key].encode()
				####################################################################
				answer = struct.pack('!H', 9) + struct.pack('!I', numsq) + keys[reqkey].encode()
				sock.sendto(answer, address)
			# Not seen this req
			if(address not in seen_req.keys() or [address] != numsq):
				##print(address[0], address[0].encode())
				ip4bytes = socket.inet_aton(address[0]) 
# ERRO AQUI IP ORIGEM
				##keyflood = struct.pack('!H', 7) + struct.pack('!H', 3) + struct.pack('!I', numsq) + address[0].encode() + struct.pack('!H', address[1]) + reqkey.encode()
				keyflood = struct.pack('!H', 7) + struct.pack('!H', 3) + struct.pack('!I', numsq) + \
				ip4bytes + struct.pack('!H', address[1]) + reqkey.encode()
				seen_req[address] = numsq
				for peer in connections:
					if( peer != address ):
						print("PEER: ",peer)
						sock.sendto(keyflood, peer)


		# TOPO REQ
		elif(typ == 6):
			numsq = struct.unpack('!I', data[2:6])[0]
			# Not seen this req
			if(address not in seen_req.keys() or seen_req[address] != numsq):
# ERRO AQUI IP ORIGEM
				ip4bytes = socket.inet_aton(address[0])
				#topoflood = struct.pack('!H', 8) + struct.pack('!H', 3) + struct.pack('!I', numsq) + address[0].encode() + struct.pack('!H', address[1])
				topoflood = struct.pack('!H', 8) + struct.pack('!H', 3) + struct.pack('!I', numsq) + ip4bytes + struct.pack('!H', address[1])
				seen_req[address] = numsq
				for peer in connections:
					if( peer != address ):
						sock.sendto(topoflood, peer)

		#  FLOOD
		elif(typ == 7 or typ == 8):
			ttl = struct.unpack('!H', data[2:4])[0]
			numsq = struct.unpack('!I', data[4:8])[0]
# ERRO AQUI IP ORIGEM
			ip_origem = socket.inet_ntoa(data[8:12])
			print('flood de ip origem = ', ip_origem)
			port_origem = struct.unpack('!H', data[12:14])[0]
			print('port origem = ', port_origem)
			origem = (ip_origem, port_origem)
			# KEY FLOOD
			if(typ == 7):
				reqkey = data[14:].decode()
				print(data)
				if(reqkey in keys.keys()):
					print(keys[reqkey])
					#answer = struct.pack('!H', 9) + struct.pack('!I', numsq) + keys[key].encode()
					####################################################################
					answer = struct.pack('!H', 9) + struct.pack('!I', numsq) + keys[reqkey].encode()
					sock.sendto(answer, origem)
			# TOPO FLOOD
			elif(typ == 8):
				#answer = struct.pack('!H', 9) + struct.pack('!I', numsq) + data[6:] + my_address[0].encode() + struct.pack('!H', my_address[1])
				ip4bytes = socket.inet_aton(my_address[0])
				answer = struct.pack('!H', 9) + struct.pack('!I', numsq) + data[6:] + ip4bytes + struct.pack('!H', my_address[1])
				sock.sendto(answer, origem)
			# FLOOD
			if(ttl > 0):
				ttl = ttl -1
# ERRO AQUI IP ORIGEM
				ip4bytes = socket.inet_aton(origem[0])
				#flood = struct.pack('!H', typ) + struct.pack('!H', ttl) + struct.pack('!I', numsq) + origem[0].encode() + struct.pack('!H', origem[1]) + data[14:]
				flood = struct.pack('!H', typ) + struct.pack('!H', ttl) + struct.pack('!I', numsq) + \
				ip4bytes + struct.pack('!H', origem[1]) + data[14:]
				#if(typ == 8):
					#colocar um espaço e o meu ip no final como string ip:port

				for peer in connections:
					if( peer != address ):
						sock.sendto(flood, peer)

	sock.close()

if __name__ == "__main__":
	main()

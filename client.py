import socket
import sys
import struct

def main():

	# Input arguments
	ip = sys.argv[1]
	port = int(sys.argv[2])

	# Create udp socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.settimeout(4)

	# Socket to servlet address
	address = ('localhost', port)

	numsq = 0
	# Client
	while(1):
		print('=========================================')
		print('O que deseja fazer?')
		print('?  + chave = Consulta por uma chave')
		print('T          = Consulta a topologia da rede')
		print('Q          = Terminar')
		print('=========================================')
		typ = input()
		# QUIT
		if typ.startswith('Q') or typ.startswith('q'):
			print('fim\n')
			break
		# KEY REQ
		if typ.startswith('?'):
			key = typ[1:]
			key = key.strip(' ')
			key = key.strip('	')
			print('Consulta por: ',key)
			numsq = numsq + 1
			keyreq = struct.pack('!H', 5) + struct.pack('!I', numsq) + key.encode()
			sock.sendto(keyreq, address)
			# Answer
			try:
				data, ans_address = sock.recvfrom(500)
				# Recvd answer
				while(1):
					try:
						ans_typ = struct.unpack('!H', data[:2])[0]
						ans_numsq = struct.unpack('!I', data[2:6])[0]
						if(ans_typ == 9 and ans_numsq == numsq):
							ans_value = data[6:].decode()
							print(ans_value, ans_address[0],':',ans_address[1])
						else:
							print('Mensagem incorreta recebida de', ans_address[0],':',ans_address[1])
						data, ans_address = sock.recvfrom(500)
					except socket.timeout:
						break

			# Timed out once
			except socket.timeout:
				numsq = numsq + 1
				keyreq = struct.pack('!H', 5) + struct.pack('!I', numsq) + key.encode()
				sock.sendto(keyreq, address)
				try:
					data, ans_address = sock.recvfrom(500)
					# Recvd answer
					while(1):
						try:
							ans_typ = struct.unpack('!H', data[:2])[0]
							ans_numsq = struct.unpack('!I', data[2:6])[0]
							if(ans_typ == 9 and ans_numsq == numsq):
								ans_value = data[6:].decode()
								print(ans_value, ans_address[0],':',ans_address[1])
							else:
								print('Mensagem incorreta recebida de', ans_address[0],':',ans_address[1])
							data, ans_address = sock.recvfrom(500)
						except socket.timeout:
							break
				# Timed out twice
				except socket.timeout:
					print('Nenhuma resposta recebida')

		# TOPO REQ
		if typ.startswith('T') or typ.startswith('t'):
			print ('Topologia da rede')
			numsq = numsq + 1
			toporeq = struct.pack('!H', 6) + struct.pack('!I', numsq)
			sock.sendto(toporeq, address)
			# Answer
			# RECEBER A RESPOSTA IGUAL NO KEY REQ (ONDE TEM #ANSWER ATE O FINAL)
			try:
				data, ans_address = sock.recvfrom(500)
				# Recvd answer
				while(1):
					try:
						ans_typ = struct.unpack('!H', data[:2])[0]
						ans_numsq = struct.unpack('!I', data[2:6])[0]
						if(ans_typ == 9 and ans_numsq == numsq):
							ans_value = data[6:].decode()
							#print(ans_value, ans_address[0],':',ans_address[1])
							print(ans_value)
						else:
							print('Mensagem incorreta recebida de', ans_address[0],':',ans_address[1])
						data, ans_address = sock.recvfrom(500)
					except socket.timeout:
						break

			# Timed out once
			except socket.timeout:
				numsq = numsq + 1
				toporeq = struct.pack('!H', 6) + struct.pack('!I', numsq)
				sock.sendto(toporeq, address)
				try:
					data, ans_address = sock.recvfrom(500)
					# Recvd answer
					while(1):
						try:
							ans_typ = struct.unpack('!H', data[:2])[0]
							ans_numsq = struct.unpack('!I', data[2:6])[0]
							if(ans_typ == 9 and ans_numsq == numsq):
								ans_value = data[6:].decode()
								#print(ans_value, ans_address[0],':',ans_address[1])
								print(ans_value)
							else:
								print('Mensagem incorreta recebida de', ans_address[0],':',ans_address[1])
							data, ans_address = sock.recvfrom(500)
						except socket.timeout:
							break
				# Timed out twice
				except socket.timeout:
					print('Nenhuma resposta recebida')

	sock.close()

if __name__ == "__main__":
	main()

import heapq
import os

class binaryTree:
    def __init__(self,ele,freq):
        self.ele = ele
        self.freq = freq
        self.right = None
        self.left = None

    def __lt__(self,other):
        return self.freq < other.freq
    
    def __eq__(self,other):
        return self.freq == other.freq
    

class huffmanCode:

    def __init__(self,path):
        self.path = path
        self.__heap = []
        self.__code = {}
        self.__reversecode = {}

    def __freq_dict(self,text):
        data = {}
        for i in text:
            if i not in data:
                data[i] = 1
            else:
                data[i] += 1
        return data 

    def __build_heap(self,dictionary):
        for key in dictionary:
            freq_value = dictionary[key]
            binaryTree_node = binaryTree(key,freq_value)
            heapq.heappush(self.__heap,binaryTree_node)

    def __build_binaryTree(self):
        while len(self.__heap) > 1:
            node_1 = heapq.heappop(self.__heap)
            node_2 = heapq.heappop(self.__heap)
            node_3 = binaryTree('',node_1.freq + node_2.freq)
            node_3.left = node_1
            node_3.right = node_2
            heapq.heappush(self.__heap,node_3)
        return
    
    def __build_nodeCode_helper(self,root,s):
        if not root:
            return 
        if root.ele:
            self.__code[root.ele] = s
            self.__reversecode[s] = root.ele
            return
        self.__build_nodeCode_helper(root.left,s+'0')
        self.__build_nodeCode_helper(root.right,s+'1')

    def __build_nodeCode(self):
        root = heapq.heappop(self.__heap)
        self.__build_nodeCode_helper(root,'')

    def __build_encodedText(self,text):
        encoded_text = ''
        for c in text:
            encoded_text += self.__code[c]
        return encoded_text
    
    def __build_paddedText(self,encoded_text):
        padding_value = 8 - len(encoded_text)%8
        for i in range(padding_value):
            encoded_text += '0'
        padded_info = "{0:08b}".format(padding_value)
        padded_text = encoded_text + padded_info
        return padded_text

    def __build_bytesArray(self,padded_text):
        array = []
        for i in range(0,len(padded_text),8):
            byte = padded_text[i:i+8]
            array.append(int(byte,2))
        return array
    
    def __removePadding(self,bits):
        padded_info = bits[:8]
        padding_value = int(padded_info,2)
        bits = bits[8:]
        bits = bits[:-1*padding_value]
        return bits

    def compress(self):
        print('start hora h compression wait....')
        file_name, file_extension = os.path.splitext(self.path)
        output_path = file_name + '.bin'

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequecies = self.__freq_dict(text)
            self.__build_heap(frequecies)
            self.__build_binaryTree()
            self.__build_nodeCode()
            encoded_text = self.__build_encodedText(text)
            #padding of encoded text, 8 bits ke form mein
            padded_text = self.__build_paddedText(encoded_text)
            bytes_array = self.__build_bytesArray(padded_text)
            final_bytes = bytes(bytes_array)

            output.write(final_bytes)
        print('hogya bhai compress')
        return output_path

    def __decodedText(self,text):
        current_bits= ''
        decoded_text= ''
        for a in text:
            current_bits += a
            if current_bits in self.__reversecode:
                decoded_text += self.__reversecode[current_bits]
                current_bits = ''
        return decoded_text
    
    def decompress(self,input_path):
        print('start ho rha h decompression hold tight you are about to witness awesomeness')
        file_name, file_extension = os.path.splitext(input_path)
        output_path = file_name + '_decompressed' + '.txt'
        with open(input_path,'rb') as file, open(output_path,'w') as output:
            bit_string = ''
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8,'0')
                bit_string += bits
                byte = file.read(1)
            removed_padding = self.__removePadding(bit_string)
            actual_text = self.__decodedText(removed_padding)
            output.write(actual_text)
        print('hogya bhai decompress')
        return output_path

path = input('enter the path of your file u need to compress bimro: ')
h = huffmanCode(path)
compressed_file = h.compress()
h.decompress(compressed_file)
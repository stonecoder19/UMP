

class BHeap:

	def __init__(self):
		self.heap = [0]
		self.heap_size = 0

	def up_heap(self,i):
		while i // 2 > 0:
			if self.heap[i][2] < self.heap[i//2][2]:
				temp  = self.heap[i]
				self.heap[i] = self.heap[i//2]
				self.heap[i//2] = temp
			i = i // 2

	def down_heap(self,i):
		while(i*2) <= self.heap_size:
			mc = self.min_child(i)
			if self.heap[i][2] > self.heap[mc][2]:
				temp = self.heap[i]
				self.heap[i] = self.heap[mc]
				self.heap[mc] = temp
			i = mc

	def min_child(self,i):
		if i * 2 +1 > self.heap_size:
			return i *2
		else:
			if self.heap[i*2+1][2] < self.heap[i*2][2]:
				return i*2+1
			else:
				return i *2

	def extract_min(self):
		if self.heap_size < 1:
			return None
		min_val = self.heap[1]
		self.heap[1] = self.heap[self.heap_size]
		self.heap_size = self.heap_size -1
		self.heap.pop()
		self.down_heap(1)
		return min_val

	def insert(self,el):
		self.heap.append(el)
		self.heap_size = self.heap_size + 1
		self.up_heap(self.heap_size)


	def peak(self):
		if self.heap_size < 1:
			return None
		return self.heap[1]


	def build_heap(self,adj_list):
		i = len(adj_list) // 2
		self.heap_size = len(adj_list)
		self.heap = [0] + adj_list[:]
		while(i > 0):
			self.down_heap(i)
			i = i - 1





if __name__ == '__main__':
	bheap = BHeap()
	bheap.insert(('A','B',70))
	bheap.insert(('C','D',30))
	bheap.insert(('G','F',10))
	bheap.insert(('J','K',40))
	bheap.insert(('L','T',5))
	bheap.insert(('R','S',20))

	print(bheap.extract_min())
	print(bheap.extract_min())
	print(bheap.extract_min())








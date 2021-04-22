
import numpy as np
from vispy import app, gloo
from math import floor




SIZE = 256






def read(a):
	"""
		open file and read data
	"""
	with open(a) as file:
		return file.read()


render_vertex = read('render_shaders/vertex.shader')
render_fragment = read('render_shaders/fragment.shader')

compute_vertex = read('compute_shaders/vertex.shader')
compute_fragment = read('compute_shaders/fragment.shader')



class Canvas(app.Canvas):

	def __init__(self):
		super().__init__(size=(SIZE, SIZE), title='Game of Life')

		self.compute_size = self.size

		size = self.compute_size + (4,)
		Z = np.zeros(size, dtype=np.float32)
		Z[...] = np.random.randint(0, 2, size)
		Z[:floor(SIZE / 2), :floor(SIZE / 2), :] = 0
		gun = """
		........................O...........
		......................O.O...........
		............OO......OO............OO
		...........O...O....OO............OO
		OO........O.....O...OO..............
		OO........O...O.OO....O.O...........
		..........O.....O.......O...........
		...........O...O....................
		............OO......................"""
		x, y = 0, 0
		for i in range(len(gun)):
			if gun[i] == '\n':
				y += 1
				x = 0
			elif gun[i] == 'O':
				Z[y, x] = 1
			x += 1

		self.compute = gloo.Program(compute_vertex, compute_fragment, count=4)
		self.compute["texture"] = Z
		self.compute["position"] = [(-1,-1), (-1,+1), (+1,-1), (+1, +1)]
		self.compute["texture_coordinates"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
		self.compute['texel_distance'] = (1.0 / size[0], 1.0 / size[1])

		self.render = gloo.Program(render_vertex, render_fragment, count=4)
		self.render["position"] = [(-1,-1), (-1,+1), (+1,-1), (+1, +1)]
		self.render["texture_coordinates"] = [(0, 0), (0, 1), (1, 0), (1, 1)]
		self.render["texture"] = self.compute["texture"]

		self.frame_buffer = gloo.FrameBuffer(self.compute["texture"],
							gloo.RenderBuffer(self.compute_size))
		gloo.set_state(depth_test=False, clear_color='black')

		self._timer = app.Timer('auto', connect=self.update, start=True)

		gloo.set_viewport(0, 0, *self.physical_size)



	def on_draw(self, event):

		with self.frame_buffer:
			gloo.set_viewport(0, 0, *self.compute_size)
			self.compute["texture"].interpolation = 'nearest'
			self.compute.draw('triangle_strip')

		gloo.clear()
		gloo.set_viewport(0, 0, *self.physical_size)
		self.render["texture"].interpolation = 'linear'
		self.render.draw('triangle_strip')




c = Canvas()
c.show()
app.run()





# eof

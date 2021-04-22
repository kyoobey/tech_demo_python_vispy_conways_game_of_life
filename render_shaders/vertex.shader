
attribute vec2 position;
attribute vec2 texture_coordinates;
varying vec2 vertex_texture_coordinates;

void main() {
	gl_Position = vec4(position.x, position.y, 0.0, 1.0);
	vertex_texture_coordinates = texture_coordinates;
}





// eof
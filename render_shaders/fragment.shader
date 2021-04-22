

uniform sampler2D texture;
varying vec2 vertex_texture_coordinates;


void main() {
	float v = texture2D(texture, vertex_texture_coordinates).x;
	gl_FragColor = vec4(1.0-vec3(v), 1.0);
}



// eof
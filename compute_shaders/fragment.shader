
uniform sampler2D texture;
uniform vec2 texel_distance;
varying vec2 vertex_texture_coordinates;

void main() {
	vec2 p = vertex_texture_coordinates;
	vec2 t = texel_distance;

	float old_state = texture2D(texture, p).x;

	float count = (
		  texture2D(texture, p + vec2(-1.0,-1.0)*t.xy)
		+ texture2D(texture, p + vec2( 1.0,-1.0)*t.xy)
		+ texture2D(texture, p + vec2(-1.0, 1.0)*t.xy)
		+ texture2D(texture, p + vec2( 1.0, 1.0)*t.xy)
		+ texture2D(texture, p + vec2(-1.0, 0.0)*t.xy)
		+ texture2D(texture, p + vec2( 1.0, 0.0)*t.xy)
		+ texture2D(texture, p + vec2( 0.0,-1.0)*t.xy)
		+ texture2D(texture, p + vec2( 0.0, 1.0)*t.xy)
	).x;

	float new_state = old_state;

	if (old_state > 0.5) {
		if (count < 1.5) new_state = 0.0;
		else if (count > 3.5) new_state = 0.0;
	} else {
		if (count > 2.5 && count < 3.5) new_state = 1.0;
	}

	gl_FragColor = vec4(new_state, 0.0, 0.0, 1.0);
}


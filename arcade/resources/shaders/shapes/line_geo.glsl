#version 330

layout (lines) in;
layout (triangle_strip, max_vertices = 4) out;

uniform float thickness;

in vec2 vs_color[2];
out vec2 gs_color;

vec2 lineNormal2D(vec2 start, vec2 end) {
    vec2 n = end - start;
    return normalize(vec2(-n.x, n.y));
}

void main() {
    // Get the line segment
    vec2 line_start = gl_in[0].gl_Position.xy;
    vec2 line_end = gl_in[1].gl_Position.xy;

    // Calculate normal
    vec2 normal = lineNormal2D(line_start, line_end) * thickness / 2.0;

    gs_color = vs_color[0];
    gl_Position = vec4(line_start + normal, 0.0, 1.0);
    EmitVertex();
    gs_color = vs_color[0];
    gl_Position = vec4(line_start - normal, 0.0, 1.0);
    EmitVertex();
    gs_color = vs_color[0];
    gl_Position = vec4(line_end + normal, 0.0, 1.0);
    EmitVertex();
    gs_color = vs_color[0];
    gl_Position = vec4(line_end - normal, 0.0, 1.0);
    EmitVertex();

    EndPrimitive();
}

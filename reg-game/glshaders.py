import array

import moderngl


class glContext:
    def __init__(self) -> None:
        self.ctx = moderngl.create_context()
        # print("OpenGL version:", self.ctx.info["GL_VERSION"])
        self.quad_buffer = self.ctx.buffer(
            data=array.array(
                "f",
                [
                    -1.0,
                    1.0,
                    0.0,
                    0.0,
                    1.0,
                    1.0,
                    1.0,
                    0.0,
                    -1.0,
                    -1.0,
                    0.0,
                    1.0,
                    1.0,
                    -1.0,
                    1.0,
                    1.0,
                ],
            )
        )

    def filmgrain_shader(self):
        """
        Create a shader that applies film grain effect to the texture.
        """
        return self.ctx.program(
            vertex_shader="""
                #version 330 core
                in vec2 vert;
                in vec2 texcoord;
                out vec2 uvs;

                void main() {
                    uvs = texcoord;
                    gl_Position = vec4(vert.x, vert.y, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330 core
                uniform sampler2D tex;
                uniform float time;
                in vec2 uvs;
                layout (location = 0) out vec4 out_color;

                float hash13(vec3 p3) {
                    p3 = fract(p3 * .1031);
                    p3 += dot(p3, p3.zyx + 31.32);
                    return fract((p3.x + p3.y) * p3.z);
                }

                void main() {
                ivec2 at = ivec2(gl_FragCoord.x, (1. - gl_FragCoord.y / 600) * 600);
                float grain = hash13(vec3(gl_FragCoord.x, (1. - (gl_FragCoord.y / 600)) * 600 , time)) * 0.5 + 0.5;
                out_color = texelFetch(tex, at, 0) * grain;
            }
            """,
        )

    def passthrough_shader(self):
        """
        Create a simple passthrough shader that outputs the texture as is.
        """
        return self.ctx.program(
            vertex_shader="""
                #version 330 core
                in vec2 vert;
                in vec2 texcoord;
                out vec2 uvs;

                void main() {
                    uvs = texcoord;
                    gl_Position = vec4(vert.x, vert.y, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330 core
                uniform sampler2D tex;
                in vec2 uvs;
                layout (location = 0) out vec4 out_color;

                void main() {
                    out_color = texture(tex, uvs);
                }
            """,
        )

    def render(self, current_state):
        if current_state == "PlayGameState":
            self.program = self.filmgrain_shader()
        else:
            self.program = self.passthrough_shader()

        self.program["tex"] = 0
        self.render_object = self.ctx.vertex_array(
            self.program,
            [(self.quad_buffer, "2f 2f", "vert", "texcoord")],
        )
        self.render_object.render(moderngl.TRIANGLE_STRIP)

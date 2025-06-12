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
        https://github.com/moderngl/moderngl/tree/main/examples
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
                layout (location = 0) out vec4 out_colour;

                float hash13(vec3 p3) {
                    p3 = fract(p3 * .1031);
                    p3 += dot(p3, p3.zyx + 31.32);
                    return fract((p3.x + p3.y) * p3.z);
                }

                void main() {
                ivec2 at = ivec2(gl_FragCoord.x, (1. - gl_FragCoord.y / 600) * 600);
                float grain = hash13(vec3(gl_FragCoord.x, (1. - (gl_FragCoord.y / 600)) * 600 , time)) * 0.5 + 0.5;
                out_colour = texelFetch(tex, at, 0) * grain;
                out_colour = vec4(out_colour.r, out_colour.g * 1.2, out_colour.b, 1.0);
            }
            """,
        )

    def pipegame_shader(self):
        """
        Create a shader that applies a pipe game effect to the texture.
        https://blubberquark.tumblr.com/post/185013752945/using-moderngl-for-post-processing-shaders-with
        """
        return self.ctx.program(
            vertex_shader="""
            #version 330 core
            in vec2 vert;
            in vec2 texcoord;
            out vec2 uvs;
            void main() {
                gl_Position = vec4(vert, 0.0, 1.0);
                uvs = texcoord;
            }
            """,
            fragment_shader="""
                #version 330 core
                precision mediump float;
                uniform sampler2D tex;

                out vec4 colour;
                in vec2 uvs;
                void main() {
                    vec2 center = vec2(0.5, 0.5);
                    vec2 off_center = uvs - center;

                    off_center *= 1.0 + 0.95 * pow(abs(off_center.yx), vec2(2.5));

                    vec2 v_text2 = center+off_center;

                    if (v_text2.x > 1.0 || v_text2.x < 0.0 ||
                        v_text2.y > 1.0 || v_text2.y < 0.0){
                        colour=vec4(0.0, 0.0, 0.0, 1.0);
                    } else {
                        colour = vec4(texture(tex, v_text2).rgb, 1.0);
                        float fv = fract(v_text2.y * float(textureSize(tex,0).x));
                        fv=min(1.0, 0.7+0.5*min(fv, 1.0-fv));
                        colour.rgb*=fv;
                        colour = vec4(colour.r, colour.g * 1.2, colour.b, 1.0);
                    }
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
                layout (location = 0) out vec4 out_colour;

                void main() {
                    out_colour = texture(tex, uvs);
                }
            """,
        )

    def render(self, current_state):
        if current_state == "PlayGameState":
            self.program = self.filmgrain_shader()
        elif current_state == "PipeGameState":
            self.program = self.pipegame_shader()
        else:
            self.program = self.passthrough_shader()

        self.program["tex"] = 0
        self.render_object = self.ctx.vertex_array(
            self.program,
            [(self.quad_buffer, "2f 2f", "vert", "texcoord")],
        )
        self.render_object.render(moderngl.TRIANGLE_STRIP)

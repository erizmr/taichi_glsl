'''
Display images or animations using Taichi GUI
'''

import taichi as ti
import time
import os

@ti.data_oriented
class Animation:
    def __init__(self, img=None, circles=None, title='Animation'):
        self.title = title
        self.img = img
        self.circles = circles
        self.circle_color = 0xffffff
        self.circle_radius = 1
        self.background_color = 0x000000
        self.gui = None
        self.has_input = False
        self.screenshot_directory = None
        self.output_video = None
        self.start_time = time.time()
        self.on_init()

    def set_output_video(self, path, framerate=24):
        output_dir = os.path.dirname(path)
        output_file = os.path.basename(path)
        output_ext = output_file.split(os.path.extsep)[-1]
        assert output_ext in ['gif', 'mp4']
        self.video_manager = ti.VideoManager(output_dir, framerate=framerate)
        self.video_manager.taichi_glsl_output_ext = output_ext

        def _get_output_filename(suffix):
                path[:-(len(output_ext) + 2)] + suffix

        self.video_manager.get_output_filename = _get_output_filename

    def on_init(self):
        pass

    def on_advance(self):
        pass

    def on_render(self):
        pass

    def on_show(self):
        pass

    def on_press(self, key):
        pass

    def on_release(self, key):
        pass

    def on_click(self, x, y, btn):
        pass

    def on_unclick(self, x, y, btn):
        pass

    def on_hover(self, x, y):
        pass

    def on_drag(self, x, y):
        pass

    def on_close(self):
        self.gui.running = False

    def on_escape(self):
        self.on_close()

    def on_pre_event(self):
        pass

    def on_pre_start(self):
        pass

    def on_pre_exit(self):
        if hasattr(self, 'video_manager'):
            ext = self.video_manager.taichi_glsl_output_ext
            self.video_manager.make_video(
                    gif=(ext == 'gif'), mp4=(ext == 'mp4'))

    def on_exit(self):
        pass

    def define_input(self):
        self._iTime = ti.var(ti.f32, ())
        self._iFrame = ti.var(ti.i32, ())
        self._iMouse = ti.Vector(2, ti.f32, ())
        self.has_input = True

    def on_update_input(self):
        if self.has_input:
            self._iTime[None] = self.time
            self._iFrame[None] = self.frame
            self._iMouse[None] = self.mouse

    @property
    def iTime(self):
        if not self.has_input:
            raise Exception(
                    'Add ``self.define_input()`` to ``on_init`` if you '
                    'wish to use inputs')
        if ti.inside_kernel():
            return ti.subscript(self._iTime, None)
        else:
            return self._iTime[None]

    @property
    def iFrame(self):
        if not self.has_input:
            raise Exception(
                    'Add ``self.define_input()`` to ``on_init`` if you '
                    'wish to use inputs')
        if ti.inside_kernel():
            return ti.subscript(self._iFrame, None)
        else:
            return self._iFrame[None]

    @property
    def iMouse(self):
        if not self.has_input:
            raise Exception(
                    'Add ``self.define_input()`` to ``on_init`` if you '
                    'wish to use inputs')
        if ti.inside_kernel():
            return self._iMouse.subscript(None)
        else:
            return self._iMouse[None]

    @property
    def iResolution(self):
        return self.resolution

    def on_event(self, e):
        MOUSE = [ti.GUI.LMB, ti.GUI.MMB, ti.GUI.RMB]
        if e.type == ti.GUI.PRESS:
            if e.key in MOUSE:
                self.on_click(*e.pos, e.key)
            else:
                if e.key == ti.GUI.ESCAPE:
                    self.on_escape()
                if e.key == ti.GUI.EXIT:
                    self.on_close()
                self.on_press(e.key)
        elif e.type == ti.GUI.RELEASE:
            if e.key in MOUSE:
                self.on_unclick(*e.pos, e.key)
            else:
                self.on_release(e.key)
        elif e.type == ti.GUI.MOTION:
            had_any = False
            for btn in MOUSE:
                if gui.is_pressed(btn):
                    self.on_drag(*e.pos, btn)
                    had_any = True
            if not had_any:
                self.on_hover(*e.pos, btn)

    @property
    def mouse(self):
        return self.gui.get_cursor_pos()

    @property
    def resolution(self):
        return self.img.shape()[0:2]

    @property
    def time(self):
        return time.time() - self.start_time

    @property
    def frame(self):
        return self.gui.frame

    def start(self):
        self.on_pre_start()
        with ti.GUI(self.title, self.resolution,
                background_color=self.background_color) as self.gui:
            if not hasattr(self.gui, 'running'):
                self.gui.running = True
            if not hasattr(self.gui, 'frame'):
                self.gui.frame = 0
            if not hasattr(ti.GUI, 'EXIT'):
                ti.GUI.EXIT = 'WMClose'
            while self.gui.running:
                self._per_loop()
        self.on_pre_exit()
        self.on_exit()
        self.gui = None

    def _per_loop(self):
        self.on_pre_event()
        for e in self.gui.get_events():
            self.on_event(e)
        self.on_advance()
        self.on_update_input()
        self.on_render()
        if self.img is not None:
            self.gui.set_image(self.img)
        if self.circles is not None:
            self.gui.circles(self.circles,
                    self.circle_color, self.circle_radius)
        self.on_show()
        if self.screenshot_directory is None:
            self.gui.show()
        else:
            self.gui.show(f'{self.screenshot_directory}/{self.frame:06d}.png')
        self.gui.frame += 1
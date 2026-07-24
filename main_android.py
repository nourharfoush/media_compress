#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق "حرفوش لضغط الصوت والفيديو" لنظام أندرويد (KivyMD)
"""

import os
import sys
import threading
import subprocess
import shutil

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from plyer import filechooser

KV = '''
MDScreen:
    md_bg_color: 0.06, 0.09, 0.16, 1

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "حرفوش لضغط الصوت والفيديو"
            elevation: 4
            md_bg_color: 0.12, 0.16, 0.23, 1
            specific_text_color: 1, 1, 1, 1

        MDTabs:
            id: tabs
            background_color: 0.12, 0.16, 0.23, 1
            text_color_normal: 0.58, 0.64, 0.72, 1
            text_color_active: 0.39, 0.4, 0.95, 1
            indicator_color: 0.39, 0.4, 0.95, 1

            TabAudio:
                title: "🎵 ضغط MP3"

            TabVideo:
                title: "🎬 ضغط الفيديو"


<TabAudio@MDFloatLayout>:
    MDCard:
        size_hint: 0.9, 0.85
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0.12, 0.16, 0.23, 1
        radius: [16]
        padding: 16
        orientation: "vertical"

        MDLabel:
            text: "اختيار ملف الصوت (MP3):"
            font_style: "Subtitle1"
            theme_text_color: "Custom"
            text_color: 0.97, 0.98, 0.99, 1
            halign: "right"
            size_hint_y: None
            height: "30dp"

        MDRaisedButton:
            text: "📁 اختيار ملف صوتي"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.25, 0.33, 1
            on_release: app.select_audio_file()

        MDLabel:
            id: audio_file_label
            text: "لم يتم اختيار ملف بعد"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: 0.58, 0.64, 0.72, 1
            halign: "center"
            size_hint_y: None
            height: "30dp"

        MDSeparator:
            height: "1dp"

        MDLabel:
            text: "مستوى جودة الصوت:"
            font_style: "Subtitle2"
            theme_text_color: "Custom"
            text_color: 0.97, 0.98, 0.99, 1
            halign: "right"
            size_hint_y: None
            height: "30dp"

        MDRaisedButton:
            id: audio_quality_btn
            text: "128k (جودة جيدة - موصى بها)"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.25, 0.33, 1

        Widget:
            size_hint_y: 1

        MDProgressBar:
            id: audio_progress
            value: 0
            max: 100
            color: 0.06, 0.73, 0.5, 1

        MDLabel:
            id: audio_status
            text: "جاهز للبدء"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: 0.22, 0.74, 0.97, 1
            halign: "center"
            size_hint_y: None
            height: "30dp"

        MDRaisedButton:
            text: "⚡ ابدأ ضغط الصوت"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.39, 0.4, 0.95, 1
            elevation: 6
            on_release: app.start_audio_compression()


<TabVideo@MDFloatLayout>:
    MDCard:
        size_hint: 0.9, 0.85
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        md_bg_color: 0.12, 0.16, 0.23, 1
        radius: [16]
        padding: 16
        orientation: "vertical"

        MDLabel:
            text: "اختيار ملف الفيديو:"
            font_style: "Subtitle1"
            theme_text_color: "Custom"
            text_color: 0.97, 0.98, 0.99, 1
            halign: "right"
            size_hint_y: None
            height: "30dp"

        MDRaisedButton:
            text: "🎥 اختيار ملف فيديو"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.25, 0.33, 1
            on_release: app.select_video_file()

        MDLabel:
            id: video_file_label
            text: "لم يتم اختيار ملف بعد"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: 0.58, 0.64, 0.72, 1
            halign: "center"
            size_hint_y: None
            height: "30dp"

        MDSeparator:
            height: "1dp"

        MDLabel:
            text: "مستوى جودة الفيديو:"
            font_style: "Subtitle2"
            theme_text_color: "Custom"
            text_color: 0.97, 0.98, 0.99, 1
            halign: "right"
            size_hint_y: None
            height: "30dp"

        MDRaisedButton:
            id: video_quality_btn
            text: "متوازن (CRF 23) - موصى به"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.2, 0.25, 0.33, 1

        Widget:
            size_hint_y: 1

        MDProgressBar:
            id: video_progress
            value: 0
            max: 100
            color: 0.06, 0.73, 0.5, 1

        MDLabel:
            id: video_status
            text: "جاهز للبدء"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: 0.22, 0.74, 0.97, 1
            halign: "center"
            size_hint_y: None
            height: "30dp"

        MDRaisedButton:
            text: "⚡ ابدأ ضغط الفيديو"
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.39, 0.4, 0.95, 1
            elevation: 6
            on_release: app.start_video_compression()
'''


class HarfoushCompressorAndroidApp(MDApp):
    selected_audio = None
    selected_video = None

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_string(KV)

    def on_start(self):
        self.request_android_permissions()

    def request_android_permissions(self):
        if platform == "android":
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([
                    Permission.READ_EXTERNAL_STORAGE,
                    Permission.WRITE_EXTERNAL_STORAGE
                ])
            except Exception:
                pass

    def select_audio_file(self):
        try:
            filechooser.open_file(on_selection=self.on_audio_selected)
        except Exception as e:
            self.show_dialog("خطأ", str(e))

    def on_audio_selected(self, selection):
        if selection:
            self.selected_audio = selection[0]
            # تحديث عنوان الملف
            Clock.schedule_once(lambda dt: self._update_audio_label())

    def _update_audio_label(self):
        if self.selected_audio:
            fname = os.path.basename(self.selected_audio)
            # البحث عن المكون في الشاشة
            for tab in self.root.ids.tabs.get_slides():
                if hasattr(tab, 'ids') and 'audio_file_label' in tab.ids:
                    tab.ids.audio_file_label.text = fname

    def select_video_file(self):
        try:
            filechooser.open_file(on_selection=self.on_video_selected)
        except Exception as e:
            self.show_dialog("خطأ", str(e))

    def on_video_selected(self, selection):
        if selection:
            self.selected_video = selection[0]
            Clock.schedule_once(lambda dt: self._update_video_label())

    def _update_video_label(self):
        if self.selected_video:
            fname = os.path.basename(self.selected_video)
            for tab in self.root.ids.tabs.get_slides():
                if hasattr(tab, 'ids') and 'video_file_label' in tab.ids:
                    tab.ids.video_file_label.text = fname

    def start_audio_compression(self):
        if not self.selected_audio:
            self.show_dialog("تنبيه", "برجاء اختيار ملف صوت أولاً")
            return
        threading.Thread(target=self._run_audio_compression, daemon=True).start()

    def _run_audio_compression(self):
        out_dir = os.path.dirname(self.selected_audio)
        fname = os.path.basename(self.selected_audio)
        out_file = os.path.join(out_dir, f"compressed_{fname}")

        ffmpeg_cmd = shutil.which("ffmpeg") or "ffmpeg"
        cmd = [ffmpeg_cmd, "-y", "-i", self.selected_audio, "-b:a", "128k", "-vn", out_file]

        try:
            subprocess.run(cmd, check=True)
            Clock.schedule_once(lambda dt: self.show_dialog("تم بنجاح", f"تم ضغط الصوت وحفظه في:\n{out_file}"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_dialog("فشل الضغط", str(e)))

    def start_video_compression(self):
        if not self.selected_video:
            self.show_dialog("تنبيه", "برجاء اختيار ملف فيديو أولاً")
            return
        threading.Thread(target=self._run_video_compression, daemon=True).start()

    def _run_video_compression(self):
        out_dir = os.path.dirname(self.selected_video)
        fname = os.path.basename(self.selected_video)
        out_file = os.path.join(out_dir, f"compressed_{fname}")

        ffmpeg_cmd = shutil.which("ffmpeg") or "ffmpeg"
        cmd = [ffmpeg_cmd, "-y", "-i", self.selected_video, "-c:v", "libx264", "-crf", "23", "-preset", "fast", "-c:a", "aac", "-b:a", "128k", out_file]

        try:
            subprocess.run(cmd, check=True)
            Clock.schedule_once(lambda dt: self.show_dialog("تم بنجاح", f"تم ضغط الفيديو وحفظه في:\n{out_file}"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_dialog("فشل الضغط", str(e)))

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="موافق", on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()


if __name__ == "__main__":
    HarfoushCompressorAndroidApp().run()

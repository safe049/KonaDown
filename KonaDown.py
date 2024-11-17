import cloudscraper
import flet as ft
from functions.func import *

current_page = 1
results_per_page = 5  # 每页显示的结果数量
search_results = []  # 用于保存搜索结果
selected_image = None  # 用于保持哪个图像被选中
download_progress = None  # 下载进度条变量
download_thread = None  # 下载线程
stop_event = threading.Event()  # 控制下载停止的事件
pause_event = threading.Event()  # 控制下载暂停的事件
pause_event.set()  # 默认设置为不暂停

def main(page: ft.Page):
    global prev_button, next_button
    page.title = "Konachan 下载器"
    page.window.width = 600
    page.window.height = 400

    tags_input = ft.TextField(label="请输入标签进行搜索", width=500)
    results_listbox = ft.ListView(expand=True)
    
    search_button = ft.ElevatedButton(text="搜索", on_click=lambda e: search_images(page, tags_input, results_listbox))
    
    prev_button = ft.ElevatedButton(text="上一页", on_click=lambda e: go_to_prev_page(page, tags_input, results_listbox))
    next_button = ft.ElevatedButton(text="下一页", on_click=lambda e: go_to_next_page(page, tags_input, results_listbox))

    download_button = ft.ElevatedButton(text="下载图片", on_click=lambda e: on_download_image(page, results_listbox))
    pause_button = ft.ElevatedButton(text="暂停下载", on_click=lambda e: on_pause_download(page))
    resume_button = ft.ElevatedButton(text="继续下载", on_click=lambda e: on_resume_download(page))
    cancel_button = ft.ElevatedButton(text="取消下载", on_click=lambda e: on_cancel_download(page))

    page.add(tags_input, search_button, prev_button, next_button, results_listbox, download_button, pause_button, resume_button, cancel_button)

ft.app(target=main)
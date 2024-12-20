import cloudscraper
import flet as ft
import threading
import requests

# 全局变量
prev_button = ft.ElevatedButton(text="上一页", on_click=lambda e: go_to_prev_page(page, tags_input, results_listbox))
next_button = ft.ElevatedButton(text="下一页", on_click=lambda e: go_to_next_page(page, tags_input, results_listbox))
current_page = 1
results_per_page = 5  # 每页显示的结果数量
search_results = []  # 用于保存搜索结果
selected_image = None  # 用于保持哪个图像被选中
download_progress = None  # 下载进度条变量
download_thread = None  # 下载线程
stop_event = threading.Event()  # 控制下载停止的事件
pause_event = threading.Event()  # 控制下载暂停的事件
pause_event.set()  # 默认设置为不暂停
lock = threading.Lock()  # 用于同步操作

def fetch_data(tags):
    scraper = cloudscraper.create_scraper()
    url = f"https://konachan.net/post.json?tags={tags}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://konachan.net/"
    }

    try:
        response = scraper.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取数据时出现错误: {str(e)}")
        return None

def fetch_data_with_fallback(tags):
    scraper = cloudscraper.create_scraper()
    url = f"https://konachan.net/post.json?tags={tags}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://konachan.net/"
    }

    try:
        response = scraper.get(url, headers=headers)
        if response.status_code == 403:
            print("接收到 403 响应，尝试使用谷歌缓存重新请求。")
            google_cache_url = f"http://webcache.googleusercontent.com/search?q=cache:{url}"
            req = scraper.get(google_cache_url, headers={'Referer': url})
            req.raise_for_status()
            return req.json()
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取数据时出现错误: {str(e)}")
        return None

def download_image(url, file_name, progress_callback=None):
    global stop_event, pause_event
    response = requests.get(url, stream=True)  # 使用requests库进行流式下载
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))  # 获取总大小
    downloaded_size = 0

    with open(file_name, "wb") as f:
        for data in response.iter_content(chunk_size=1024):
            if stop_event.is_set():
                print("下载已停止")
                return False  # 返回 False 表示下载被取消
            if not pause_event.is_set():
                pause_event.wait()  # 如果暂停，则等待
            downloaded_size += len(data)  # 更新已下载大小
            f.write(data)
            # 计算并格式化进度
            downloaded_size_mb = downloaded_size / (1024 * 1024)  # 转换为MB
            total_size_mb = total_size / (1024 * 1024)  # 转换为MB
            progress = downloaded_size / total_size  # 计算实际的下载进度
            if progress_callback:
                progress_callback(progress)  # 调用回调函数更新进度条
    return True  # 返回 True 表示下载成功

def search_images(page, tags_input, results_listbox):
    global current_page, search_results
    tags = tags_input.value.strip()
    if not tags:
        page.add(ft.SnackBar(ft.Text("请输入标签进行搜索！"), open=True))
        return

    print(f"搜索标签: {tags}")
    current_page = 1

    try:
        search_results = fetch_data_with_fallback(tags)  # 获取所有搜索结果
        print("Response JSON:", search_results)

        if search_results:
            update_results_listbox(page, results_listbox)
            total_results = len(search_results)
            total_pages = (total_results + results_per_page - 1) // results_per_page
            print(f"找到 {total_results} 个结果，显示第 {current_page}/{total_pages} 页。")
            update_pagination_buttons(page, total_pages)

        else:
            page.add(ft.SnackBar(ft.Text("没有找到相关的结果！"), open=True))
            print("没有找到相关的结果。")
    except Exception as e:
        page.add(ft.SnackBar(ft.Text(f"请求发生错误: {str(e)}"), open=True))
        print(f"异常信息: {str(e)}")

def update_results_listbox(page, results_listbox):
    global current_page, selected_image
    start_index = (current_page - 1) * results_per_page
    end_index = min(start_index + results_per_page, len(search_results))

    results_listbox.controls.clear()
    for i, item in enumerate(search_results[start_index:end_index]):
        title = f"{item['id']} - {item['author']}"
        sample_url = item['sample_url']  # 使用sample_url作为缩略图
        is_selected = selected_image and selected_image['id'] == item['id']

        # 使用 Container 来实现高亮效果
        list_tile = ft.ListTile(
            title=ft.Text(title),
            leading=ft.Image(src=sample_url, width=50, height=50),
            on_click=lambda e, item=item: image_selected(page, item, results_listbox)  # 传递results_listbox
        )

        if is_selected:
            list_tile.bgcolor = ft.colors.BLUE  # 设置高亮背景颜色

        results_listbox.controls.append(list_tile)

    results_listbox.update()

def image_selected(page, item, results_listbox):  # 接受results_listbox参数
    global selected_image
    selected_image = item  # 更新选中的图像
    update_results_listbox(page, results_listbox)  # 刷新列表以更新高亮

def update_pagination_buttons(page, total_pages):
    global prev_button, next_button
    prev_button.enabled = current_page > 1
    next_button.enabled = current_page < total_pages

def go_to_next_page(page, tags_input, results_listbox):
    global current_page
    if current_page < ((len(search_results) + results_per_page - 1) // results_per_page):
        current_page += 1
        update_results_listbox(page, results_listbox)

def go_to_prev_page(page, tags_input, results_listbox):
    global current_page
    if current_page > 1:
        current_page -= 1
        update_results_listbox(page, results_listbox)

def update_progress(progress_bar, progress):
    if progress_bar:  # 确保 progress_bar 不是 None
        progress_bar.value = progress
        progress_bar.update()  # 更新进度条显示

def download_worker(page, url, file_name, progress_bar):
    try:
        success = download_image(url, file_name, lambda progress: update_progress(progress_bar, progress))
        if success:
            page.add(ft.SnackBar(ft.Text(f"已下载图片: {file_name}"), open=True))
            print(f"成功下载图片: {file_name}")
        else:
            page.add(ft.SnackBar(ft.Text(f"下载已取消: {file_name}"), open=True))
            print(f"下载已取消: {file_name}")
    except Exception as e:
        page.add(ft.SnackBar(ft.Text(f"发生错误: {str(e)}"), open=True))
        print(f"下载异常信息: {str(e)}")
    finally:
        # 在这里移除进度条
        with lock:
            if progress_bar in page.controls:
                page.remove(progress_bar)  # 下载完成后移除进度条
                page.update()  # 移除进度条后更新页面

def on_download_image(page, results_listbox):
    global selected_image, download_progress, download_thread, stop_event, pause_event
    if selected_image is None:
        page.add(ft.SnackBar(ft.Text("请先选择一张图片！"), open=True))
        return

    # 移除之前可能存在的进度条
    with lock:
        if download_progress and download_progress in page.controls:
            page.remove(download_progress)
            page.update()  # 移除旧进度条后更新页面
            download_progress = None  # 重置进度条为 None

    file_url = selected_image['file_url']
    file_name = f"{selected_image['id']}.png"

    # 创建下载进度条
    download_progress = ft.ProgressBar(value=0, width=500)
    page.add(download_progress)
    page.update()  # 添加新进度条后更新页面

    stop_event.clear()  # 清除停止事件
    pause_event.set()  # 设置为继续状态

    download_thread = threading.Thread(target=download_worker, args=(page, file_url, file_name, download_progress))
    download_thread.start()

def on_pause_download(page):
    global pause_event
    pause_event.clear()  # 设置为暂停状态

def on_resume_download(page):
    global pause_event
    pause_event.set()  # 设置为继续状态

def on_cancel_download(page):
    global stop_event, download_thread
    stop_event.set()  # 设置为停止状态
    if download_thread and download_thread.is_alive():
        download_thread.join()  # 等待线程结束
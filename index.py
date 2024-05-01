import os
import shutil
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler): # FileSystemEventHandler 확장
    def __init__(self, src_path, dest_path):
        self.src_path = src_path
        self.dest_path = dest_path

    def on_any_event(self, event):
        if event.is_directory:
            return
        elif event.event_type in ['created', 'modified']:
            # 파일이 생성되거나 수정된 경우 복사
            relative_path = os.path.relpath(event.src_path, self.src_path) # 상대 경로 계산
            dest_file_path = os.path.join(self.dest_path, relative_path) # join으로 경로 합치기

            # Create the destination folder if it doesn't exist
            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True) # exist_ok=True: 이미 존재해도 에러 발생 안함
            
            shutil.copy2(event.src_path, dest_file_path) # 파일 복사
            print(f"Copied: {event.src_path} -> {dest_file_path}")
        elif event.event_type in ['deleted']:
            # 파일이 삭제된 경우 대상 파일 삭제
            relative_path = os.path.relpath(event.src_path, self.src_path)
            dest_file_path = os.path.join(self.dest_path, relative_path)
            
            if os.path.exists(dest_file_path):
                if os.path.isdir(dest_file_path):
                    shutil.rmtree(dest_file_path) # 폴더와 하위 파일 전부 삭제
                else:
                    os.remove(dest_file_path) # 대상 파일 삭제
                print(f"Deleted: {dest_file_path}")
            else:
                print(f"File not found: {dest_file_path}")
        elif event.event_type in ['moved']:
            # 파일이나 폴더 이름이 변경된 경우 대상도 변경
            relative_src_path = os.path.relpath(event.src_path, self.src_path)
            relative_dest_path = os.path.relpath(event.dest_path, self.src_path)
            src_file_path = os.path.join(self.src_path, relative_dest_path)
            dest_file_path = os.path.join(self.dest_path, relative_src_path)
            dest_file_path_to_move = os.path.join(self.dest_path, relative_dest_path)

            print('relative_src_path', relative_src_path)
            print('relative_dest_path', relative_dest_path)
            print('src_file_path', src_file_path)
            print('dest_file_path', dest_file_path)

            if os.path.exists(src_file_path):
                shutil.move(dest_file_path, dest_file_path_to_move) # 파일 또는 폴더 이동
                print(f"Moved: {dest_file_path} -> {dest_file_path_to_move}")
            else:
                print(f"File or folder not found: {src_file_path}")

# 현재 py파일이 있는 경로
current_directory = os.path.dirname(os.path.abspath(__file__))

# JSON 파일 경로
json_file_path = current_directory + "\\define.json"

# JSON 파일 읽어오기
with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# 디버깅용 __name__
if __name__ == "__main__":
    src_folder = data['pathA']
    dest_folder = data['pathB']
    
    event_handler = MyHandler(src_folder, dest_folder)
    observer = Observer()
    observer.schedule(event_handler, src_folder, recursive=True)
    observer.start()
    print(f"Monitoring {src_folder} for changes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join() # 스레드가 종료될 때까지 대기

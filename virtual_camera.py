"""
虚拟摄像头核心模块
提供虚拟摄像头的基本功能
"""
import cv2
import numpy as np
import pyvirtualcam
from PIL import Image
import threading
import time
from typing import Optional, Tuple


class VirtualCamera:
    def __init__(self, width: int = 640, height: int = 480, fps: int = 30):
        """
        初始化虚拟摄像头
        
        Args:
            width: 宽度
            height: 高度
            fps: 帧率
        """
        self.width = width
        self.height = height
        self.fps = fps
        self.cam: Optional[pyvirtualcam.Camera] = None
        self.running = False
        self.current_frame = None
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()
        
    def start(self, retry_count: int = 3) -> bool:
        """
        启动虚拟摄像头
        
        Args:
            retry_count: 重试次数
            
        Returns:
            bool: 启动是否成功
        """
        for attempt in range(retry_count):
            try:
                # 创建虚拟摄像头
                self.cam = pyvirtualcam.Camera(
                    width=self.width,
                    height=self.height,
                    fps=self.fps,
                    fmt=pyvirtualcam.PixelFormat.BGR
                )
                self.running = True
                
                # 创建输出线程
                self.thread = threading.Thread(target=self._output_loop, daemon=True)
                self.thread.start()
                
                return True
            except Exception as e:
                print(f"启动虚拟摄像头失败 (尝试 {attempt + 1}/{retry_count}): {e}")
                if attempt < retry_count - 1:
                    time.sleep(1)  # 等待1秒后重试
                else:
                    return False
        return False
    
    def stop(self):
        """停止虚拟摄像头"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        if self.cam:
            self.cam.close()
            self.cam = None
        # 给OBS虚拟摄像头时间释放资源
        time.sleep(0.5)
    
    def _output_loop(self):
        """输出帧的循环"""
        while self.running and self.cam:
            try:
                with self.lock:
                    if self.current_frame is not None:
                        frame = self.current_frame
                    else:
                        # 默认显示黑色屏幕
                        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                
                # 调整帧大小以匹配摄像头输出分辨率
                if frame.shape[:2] != (self.height, self.width):
                    frame_resized = cv2.resize(frame, (self.width, self.height))
                else:
                    frame_resized = frame
                
                # 发送帧到虚拟摄像头
                self.cam.send(frame_resized)
                self.cam.sleep_until_next_frame()
            except Exception as e:
                print(f"输出帧时出错: {e}")
                break
    
    def update_frame(self, frame: np.ndarray):
        """
        更新当前帧
        
        Args:
            frame: numpy数组，BGR格式
        """
        with self.lock:
            self.current_frame = frame
    
    def load_image(self, image_path: str) -> bool:
        """
        从文件加载图片
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            bool: 加载是否成功
        """
        try:
            # 使用OpenCV读取图片（支持中文路径）
            # 使用numpy读取文件，然后使用imdecode解码，这样可以处理中文路径
            with open(image_path, 'rb') as f:
                img_array = np.frombuffer(f.read(), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if frame is None:
                return False
            
            self.update_frame(frame)
            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"加载图片失败: {e}")
            return False
    
    @staticmethod
    def get_image_resolution(image_path: str) -> Optional[Tuple[int, int]]:
        """
        获取图片的实际分辨率
        
        Args:
            image_path: 图片文件路径
            
        Returns:
            Tuple[int, int]: 图片的(宽度, 高度)，如果加载失败返回None
        """
        try:
            # 使用支持中文路径的方式读取图片
            with open(image_path, 'rb') as f:
                img_array = np.frombuffer(f.read(), dtype=np.uint8)
            frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if frame is None:
                return None
            
            height, width = frame.shape[:2]
            return (width, height)
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"获取图片分辨率失败: {e}")
            return None
    
    def set_resolution(self, width: int, height: int) -> bool:
        """
        设置分辨率
        
        Args:
            width: 新宽度
            height: 新高度
            
        Returns:
            bool: 设置是否成功（如果分辨率相同也返回True）
        """
        if self.width != width or self.height != height:
            self.width = width
            self.height = height
            # 重新启动摄像头以应用新分辨率
            if self.running:
                self.stop()
                return self.start()
        return True
    
    def set_fps(self, fps: int):
        """
        设置帧率
        
        Args:
            fps: 新帧率
        """
        self.fps = fps
        if self.running:
            self.stop()
            self.start()
    
    def is_running(self) -> bool:
        """检查摄像头是否正在运行"""
        return self.running
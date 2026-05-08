"""
图形界面模块
提供用户友好的GUI界面
"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QSlider, QSpinBox, QFileDialog, QMessageBox, 
                             QGroupBox, QGridLayout, QFrame, QCheckBox, 
                             QListWidget, QListWidgetItem, QSplitter)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QImage
from virtual_camera import VirtualCamera
import cv2
import numpy as np


class VirtualCameraGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.virtual_camera = None
        self.current_image_path = None
        self.auto_resolution = False
        self.current_folder = None
        self.image_list = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('虚拟摄像头控制器')
        self.setGeometry(100, 100, 1200, 700)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 标题
        title_label = QLabel('虚拟摄像头控制器')
        title_label.setFont(QFont('Arial', 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)
        
        # 内容区域 - 三栏布局
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # 左侧文件列表
        file_list_panel = self.create_file_list_panel()
        content_layout.addWidget(file_list_panel, stretch=1)
        
        # 中间控制面板
        control_panel = self.create_control_panel()
        content_layout.addWidget(control_panel, stretch=1)
        
        # 右侧预览区域
        preview_panel = self.create_preview_panel()
        content_layout.addWidget(preview_panel, stretch=2)
        
        # 状态栏
        self.status_label = QLabel('就绪')
        self.statusBar().addWidget(self.status_label)
        
    def create_file_list_panel(self) -> QGroupBox:
        """创建文件列表面板"""
        group = QGroupBox('文件列表')
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        # 文件夹选择按钮
        folder_layout = QHBoxLayout()
        self.select_folder_btn = QPushButton('选择文件夹')
        self.select_folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.select_folder_btn)
        
        self.select_image_btn = QPushButton('选择单个图片')
        self.select_image_btn.clicked.connect(self.select_image)
        folder_layout.addWidget(self.select_image_btn)
        
        layout.addLayout(folder_layout)
        
        # 图片列表
        self.image_list_widget = QListWidget()
        self.image_list_widget.itemDoubleClicked.connect(self.on_image_double_clicked)
        layout.addWidget(QLabel('双击图片加载:'))
        layout.addWidget(self.image_list_widget)
        
        # 当前图片显示
        self.image_path_label = QLabel('当前图片: 未选择')
        self.image_path_label.setWordWrap(True)
        self.image_path_label.setStyleSheet('color: #666; font-size: 11px;')
        layout.addWidget(self.image_path_label)
        
        return group
    
    def create_control_panel(self) -> QGroupBox:
        """创建控制面板"""
        group = QGroupBox('控制面板')
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        # 自适应分辨率设置
        auto_resolution_group = QGroupBox('自适应分辨率')
        auto_resolution_layout = QVBoxLayout()
        auto_resolution_group.setLayout(auto_resolution_layout)
        
        self.auto_resolution_checkbox = QCheckBox('自动匹配图片分辨率')
        self.auto_resolution_checkbox.stateChanged.connect(self.on_auto_resolution_changed)
        auto_resolution_layout.addWidget(self.auto_resolution_checkbox)
        
        self.auto_resolution_info = QLabel('启用后将自动使用图片的实际分辨率')
        self.auto_resolution_info.setStyleSheet('color: #666; font-size: 11px;')
        self.auto_resolution_info.setWordWrap(True)
        auto_resolution_layout.addWidget(self.auto_resolution_info)
        
        layout.addWidget(auto_resolution_group)
        
        # 分辨率设置
        resolution_group = QGroupBox('分辨率设置')
        resolution_layout = QGridLayout()
        resolution_group.setLayout(resolution_layout)
        
        resolution_layout.addWidget(QLabel('宽度:'), 0, 0)
        self.width_combo = QComboBox()
        self.width_combo.addItems(['640', '800', '960', '1280', '1600', '1920'])
        self.width_combo.setCurrentText('640')
        resolution_layout.addWidget(self.width_combo, 0, 1)
        
        resolution_layout.addWidget(QLabel('高度:'), 1, 0)
        self.height_combo = QComboBox()
        self.height_combo.addItems(['480', '600', '720', '960', '900', '1080'])
        self.height_combo.setCurrentText('480')
        resolution_layout.addWidget(self.height_combo, 1, 1)
        
        self.apply_resolution_btn = QPushButton('应用分辨率')
        self.apply_resolution_btn.clicked.connect(self.apply_resolution)
        resolution_layout.addWidget(self.apply_resolution_btn, 2, 0, 1, 2)
        
        layout.addWidget(resolution_group)
        
        # 帧率设置
        fps_group = QGroupBox('帧率设置')
        fps_layout = QVBoxLayout()
        fps_group.setLayout(fps_layout)
        
        self.fps_slider = QSlider(Qt.Horizontal)
        self.fps_slider.setMinimum(1)
        self.fps_slider.setMaximum(60)
        self.fps_slider.setValue(30)
        self.fps_slider.valueChanged.connect(self.update_fps_label)
        fps_layout.addWidget(self.fps_slider)
        
        self.fps_label = QLabel('帧率: 30 FPS')
        fps_layout.addWidget(self.fps_label)
        
        layout.addWidget(fps_group)
        
        # 控制按钮
        control_group = QGroupBox('控制')
        control_layout = QVBoxLayout()
        control_group.setLayout(control_layout)
        
        self.start_btn = QPushButton('启动虚拟摄像头')
        self.start_btn.clicked.connect(self.start_camera)
        self.start_btn.setStyleSheet('QPushButton { background-color: #4CAF50; color: white; padding: 10px; font-size: 14px; }')
        control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton('停止虚拟摄像头')
        self.stop_btn.clicked.connect(self.stop_camera)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setStyleSheet('QPushButton { background-color: #f44336; color: white; padding: 10px; font-size: 14px; }')
        control_layout.addWidget(self.stop_btn)
        
        layout.addWidget(control_group)
        
        # 支持的格式说明
        format_group = QGroupBox('支持的图片格式')
        format_layout = QVBoxLayout()
        format_group.setLayout(format_layout)
        
        format_label = QLabel('• JPG/JPEG\n• PNG\n• BMP\n• GIF (仅第一帧)')
        format_layout.addWidget(format_label)
        
        layout.addWidget(format_group)
        
        layout.addStretch()
        return group
    
    def create_preview_panel(self) -> QGroupBox:
        """创建预览面板"""
        group = QGroupBox('预览')
        layout = QVBoxLayout()
        group.setLayout(layout)
        
        self.preview_label = QLabel('图片预览')
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet('QLabel { background-color: #f0f0f0; border: 2px solid #ccc; }')
        self.preview_label.setMinimumSize(400, 300)
        layout.addWidget(self.preview_label)
        
        return group
    
    def select_image(self):
        """选择图片文件"""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                '选择图片',
                '',
                '图片文件 (*.jpg *.jpeg *.png *.bmp *.gif);;所有文件 (*.*)'
            )

            if file_path:
                self.current_image_path = file_path
                self.image_path_label.setText(f'已选择: {file_path}')

                # 加载并显示预览
                self.load_preview(file_path)

                # 如果启用了自适应分辨率，自动更新分辨率设置
                if self.auto_resolution:
                    try:
                        self.update_resolution_from_image()
                    except Exception as e:
                        QMessageBox.warning(self, '警告', f'更新分辨率时出错: {str(e)}')

                # 如果虚拟摄像头正在运行，立即更新输出图片
                self._update_camera_frame(file_path)
        except Exception as e:
            QMessageBox.critical(self, '错误', f'选择图片时出错: {str(e)}')
    
    def select_folder(self):
        """选择文件夹"""
        try:
            folder_path = QFileDialog.getExistingDirectory(
                self,
                '选择包含图片的文件夹',
                ''
            )
            
            if folder_path:
                self.current_folder = folder_path
                self.scan_folder(folder_path)
        except Exception as e:
            QMessageBox.critical(self, '错误', f'选择文件夹时出错: {str(e)}')
    
    def scan_folder(self, folder_path: str):
        """扫描文件夹中的图片文件"""
        try:
            # 支持的图片格式
            supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
            
            # 扫描文件夹
            self.image_list = []
            self.image_list_widget.clear()
            
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):
                        ext = os.path.splitext(filename)[1].lower()
                        if ext in supported_extensions:
                            self.image_list.append(file_path)
                
                # 按文件名排序
                self.image_list.sort()
                
                # 添加到列表控件
                for img_path in self.image_list:
                    filename = os.path.basename(img_path)
                    item = QListWidgetItem(filename)
                    item.setData(Qt.UserRole, img_path)  # 存储完整路径
                    self.image_list_widget.addItem(item)
                
                self.status_label.setText(f'文件夹: {folder_path} ({len(self.image_list)} 张图片)')
            else:
                QMessageBox.warning(self, '警告', '文件夹不存在')
                
        except Exception as e:
            QMessageBox.critical(self, '错误', f'扫描文件夹时出错: {str(e)}')
    
    def on_image_double_clicked(self, item: QListWidgetItem):
        """双击列表项加载图片"""
        try:
            image_path = item.data(Qt.UserRole)
            if image_path and os.path.exists(image_path):
                self.current_image_path = image_path
                self.image_path_label.setText(f'已选择: {os.path.basename(image_path)}')

                # 加载并显示预览
                self.load_preview(image_path)

                # 如果启用了自适应分辨率，自动更新分辨率设置
                if self.auto_resolution:
                    try:
                        self.update_resolution_from_image()
                    except Exception as e:
                        QMessageBox.warning(self, '警告', f'更新分辨率时出错: {str(e)}')

                # 如果虚拟摄像头正在运行，立即更新输出图片
                self._update_camera_frame(image_path)
            else:
                QMessageBox.warning(self, '警告', '图片文件不存在')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'加载图片时出错: {str(e)}')
    
    def load_preview(self, image_path: str):
        """加载图片预览"""
        try:
            # 使用OpenCV读取图片（支持中文路径）
            import numpy as np
            with open(image_path, 'rb') as f:
                img_array = np.frombuffer(f.read(), dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
            
            if img is not None:
                # 转换为RGB
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # 缩放以适应预览区域
                h, w = img_rgb.shape[:2]
                max_size = 400
                if w > max_size or h > max_size:
                    scale = max_size / max(w, h)
                    new_w = int(w * scale)
                    new_h = int(h * scale)
                    img_rgb = cv2.resize(img_rgb, (new_w, new_h))
                
                # 转换为QPixmap
                height, width, channel = img_rgb.shape
                bytes_per_line = 3 * width
                q_img = QImage(img_rgb.data, width, height, bytes_per_line, 
                               QImage.Format_RGB888).copy()
                q_pixmap = QPixmap.fromImage(q_img)
                
                self.preview_label.setPixmap(q_pixmap)
            else:
                self.preview_label.setText('无法加载图片')
        except Exception as e:
            self.preview_label.setText(f'加载失败: {str(e)}')
    
    def apply_resolution(self):
        """应用新的分辨率"""
        width = int(self.width_combo.currentText())
        height = int(self.height_combo.currentText())
        
        self.status_label.setText(f'分辨率已设置为 {width}x{height}')
        
        # 如果摄像头正在运行，更新分辨率
        if self.virtual_camera and self.virtual_camera.is_running():
            # 只有当分辨率不同时才需要重启
            if self.virtual_camera.width != width or self.virtual_camera.height != height:
                # 停止摄像头
                self.virtual_camera.stop()
                # 更新分辨率
                self.virtual_camera.width = width
                self.virtual_camera.height = height
                # 重新启动摄像头
                if self.virtual_camera.start():
                    self.status_label.setText(f'分辨率已更新为 {width}x{height}')
                    # 如果有当前图片，重新加载
                    if self.current_image_path:
                        self.virtual_camera.load_image(self.current_image_path)
                else:
                    self.status_label.setText('分辨率更新失败')
                    self.start_btn.setEnabled(True)
                    self.stop_btn.setEnabled(False)
    
    def on_auto_resolution_changed(self, state):
        """自适应分辨率复选框状态变化"""
        try:
            self.auto_resolution = (state == Qt.Checked)
            
            # 启用/禁用分辨率选择器
            self.width_combo.setEnabled(not self.auto_resolution)
            self.height_combo.setEnabled(not self.auto_resolution)
            self.apply_resolution_btn.setEnabled(not self.auto_resolution)
            
            if self.auto_resolution and self.current_image_path:
                # 如果已选择图片，自动更新分辨率
                self.update_resolution_from_image()
                self.status_label.setText('自适应分辨率已启用')
                
                # 如果虚拟摄像头正在运行，立即应用新分辨率
                if self.virtual_camera and self.virtual_camera.is_running():
                    resolution = VirtualCamera.get_image_resolution(self.current_image_path)
                    if resolution:
                        width, height = resolution
                        if self.virtual_camera.width != width or self.virtual_camera.height != height:
                            self.virtual_camera.stop()
                            self.virtual_camera.width = width
                            self.virtual_camera.height = height
                            self.virtual_camera.load_image(self.current_image_path)
                            if self.virtual_camera.start():
                                self.status_label.setText(f'自适应分辨率已启用，分辨率已调整为 {width}x{height}')
                                self.start_btn.setEnabled(False)
                                self.stop_btn.setEnabled(True)
                            else:
                                self.virtual_camera = None
                                self.start_btn.setEnabled(True)
                                self.stop_btn.setEnabled(False)
                                self.timer.stop()
                                self.status_label.setText('自适应分辨率已启用，但摄像头重启失败')
            else:
                self.status_label.setText(f'自适应分辨率已{"启用" if self.auto_resolution else "禁用"}')
        except Exception as e:
            print(f"自适应分辨率切换错误: {e}")
    
    def update_resolution_from_image(self):
        """根据图片的实际分辨率更新分辨率设置"""
        try:
            if not self.current_image_path:
                return
            
            resolution = VirtualCamera.get_image_resolution(self.current_image_path)
            
            if resolution:
                width, height = resolution
                
                # 更新分辨率选择器的显示
                # 先检查下拉列表中是否有对应的分辨率
                width_index = self.width_combo.findText(str(width))
                height_index = self.height_combo.findText(str(height))
                
                if width_index >= 0 and height_index >= 0:
                    self.width_combo.setCurrentIndex(width_index)
                    self.height_combo.setCurrentIndex(height_index)
                    self.status_label.setText(f'已自动匹配图片分辨率: {width}x{height}')
                else:
                    # 如果分辨率不在列表中，添加到列表
                    if width_index < 0:
                        self.width_combo.addItem(str(width))
                        self.width_combo.setCurrentText(str(width))
                    if height_index < 0:
                        self.height_combo.addItem(str(height))
                        self.height_combo.setCurrentText(str(height))
                    self.status_label.setText(f'已自动匹配图片分辨率: {width}x{height}')
            else:
                self.status_label.setText('无法获取图片分辨率')
        except Exception as e:
            self.status_label.setText('更新分辨率时出错')
    
    def update_fps_label(self):
        """更新帧率标签"""
        fps = self.fps_slider.value()
        self.fps_label.setText(f'帧率: {fps} FPS')
        
        # 如果摄像头正在运行，更新帧率
        if self.virtual_camera and self.virtual_camera.is_running():
            self.virtual_camera.set_fps(fps)
    
    def start_camera(self):
        """启动虚拟摄像头"""
        try:
            if not self.current_image_path:
                QMessageBox.warning(self, '警告', '请先选择一张图片！')
                return
            
            # 获取设置
            fps = self.fps_slider.value()
            
            # 确定使用的分辨率
            if self.auto_resolution:
                # 使用图片的实际分辨率
                resolution = VirtualCamera.get_image_resolution(self.current_image_path)
                if resolution:
                    width, height = resolution
                else:
                    QMessageBox.warning(self, '警告', '无法获取图片分辨率，将使用默认分辨率')
                    width = int(self.width_combo.currentText())
                    height = int(self.height_combo.currentText())
            else:
                # 使用手动选择的分辨率
                width = int(self.width_combo.currentText())
                height = int(self.height_combo.currentText())
            
            # 创建虚拟摄像头
            self.virtual_camera = VirtualCamera(width, height, fps)
            
            # 加载图片
            if not self.virtual_camera.load_image(self.current_image_path):
                QMessageBox.critical(self, '错误', '加载图片失败！')
                return
            
            # 启动摄像头
            if self.virtual_camera.start():
                self.start_btn.setEnabled(False)
                self.stop_btn.setEnabled(True)
                self.status_label.setText(f'虚拟摄像头已启动 - {width}x{height} @ {fps} FPS')
                self.timer.start(1000)  # 每秒更新一次状态
            else:
                QMessageBox.critical(self, '错误', '启动虚拟摄像头失败！请确保已安装OBS Studio并启用虚拟摄像头功能。')
                
        except Exception as e:
            QMessageBox.critical(self, '错误', f'启动失败: {str(e)}\n\n请确保已安装OBS Studio并启用虚拟摄像头功能。')
    
    def stop_camera(self):
        """停止虚拟摄像头"""
        try:
            if self.virtual_camera:
                self.virtual_camera.stop()
                self.virtual_camera = None
            
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.timer.stop()
            self.status_label.setText('虚拟摄像头已停止')
        except Exception as e:
            print(f"停止摄像头错误: {e}")
    
    def _update_camera_frame(self, image_path: str):
        """更新虚拟摄像头的输出帧

        Args:
            image_path: 新图片路径
        """
        cam = self.virtual_camera
        if not cam:
            return

        if self.auto_resolution:
            resolution = VirtualCamera.get_image_resolution(image_path)
            if resolution:
                width, height = resolution
                self.update_resolution_from_image()
                if cam.width != width or cam.height != height:
                    was_running = cam.is_running()
                    if was_running:
                        cam.stop()

                    cam.width = width
                    cam.height = height

                    if not cam.load_image(image_path):
                        self.status_label.setText('更新图片失败')
                        if was_running:
                            if cam.start():
                                self.start_btn.setEnabled(False)
                                self.stop_btn.setEnabled(True)
                            else:
                                self.virtual_camera = None
                                self.start_btn.setEnabled(True)
                                self.stop_btn.setEnabled(False)
                                self.timer.stop()
                                self.status_label.setText('更新图片失败，摄像头重启也失败')
                        return

                    if was_running:
                        if cam.start():
                            self.status_label.setText(f'图片已更新，分辨率已调整为 {width}x{height}')
                            self.start_btn.setEnabled(False)
                            self.stop_btn.setEnabled(True)
                        else:
                            self.virtual_camera = None
                            self.start_btn.setEnabled(True)
                            self.stop_btn.setEnabled(False)
                            self.timer.stop()
                            self.status_label.setText('图片已更新，但摄像头重启失败')
                    else:
                        self.status_label.setText(f'图片已更新，分辨率已调整为 {width}x{height}')
                    return

        if cam.is_running():
            if cam.load_image(image_path):
                self.status_label.setText(f'图片已更新 - {os.path.basename(image_path)}')
            else:
                self.status_label.setText('更新图片失败')

    def update_status(self):
        """更新状态"""
        if self.virtual_camera and self.virtual_camera.is_running():
            width = self.virtual_camera.width
            height = self.virtual_camera.height
            fps = self.virtual_camera.fps
            self.status_label.setText(f'运行中 - {width}x{height} @ {fps} FPS')
    
    def closeEvent(self, event):
        """关闭窗口时的处理"""
        self.stop_camera()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = VirtualCameraGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
"""
测试自动匹配分辨率修复
验证在摄像头运行时切换图片，分辨率是否正确更新
"""
import sys
import os
from unittest.mock import Mock, MagicMock, patch, call
from PyQt5.QtWidgets import QApplication
from gui import VirtualCameraGUI
from virtual_camera import VirtualCamera

def test_update_camera_frame_with_auto_resolution():
    """测试_update_camera_frame在自动匹配分辨率启用时的行为"""
    print("=" * 60)
    print("测试自动匹配分辨率修复")
    print("=" * 60)
    
    # 创建GUI实例（不启动应用程序）
    app = QApplication.instance() or QApplication(sys.argv)
    
    # 测试1：切换到相同分辨率的图片
    print("\n测试1: 切换到相同分辨率的图片")
    gui = VirtualCameraGUI()
    mock_camera = Mock(spec=VirtualCamera)
    mock_camera.is_running.return_value = True
    mock_camera.load_image.return_value = True
    mock_camera.width = 640
    mock_camera.height = 480
    mock_camera.fps = 30
    gui.virtual_camera = mock_camera
    gui.auto_resolution = True
    gui.current_image_path = 'sample_640x480.png'
    
    mock_camera.stop.reset_mock()
    mock_camera.start.reset_mock()
    mock_camera.load_image.reset_mock()
    
    gui._update_camera_frame('sample_640x480.png')
    
    # 验证load_image被调用
    assert mock_camera.load_image.called, "load_image应该被调用"
    # 由于分辨率相同，stop和start不应该被调用
    assert not mock_camera.stop.called, "分辨率相同时stop不应该被调用"
    assert not mock_camera.start.called, "分辨率相同时start不应该被调用"
    print("  [PASS] load_image被调用")
    print("  [PASS] 分辨率相同时摄像头不会重启")
    
    # 测试2：切换到不同分辨率的图片（成功情况）
    print("\n测试2: 切换到不同分辨率的图片（成功情况）")
    gui = VirtualCameraGUI()
    mock_camera = Mock(spec=VirtualCamera)
    mock_camera.is_running.return_value = True
    mock_camera.load_image.return_value = True
    mock_camera.width = 640
    mock_camera.height = 480
    mock_camera.start.return_value = True
    gui.virtual_camera = mock_camera
    gui.auto_resolution = True
    gui.current_image_path = 'sample_640x480.png'
    gui.start_btn = Mock()
    gui.stop_btn = Mock()
    
    mock_camera.stop.reset_mock()
    mock_camera.start.reset_mock()
    mock_camera.load_image.reset_mock()
    
    with patch.object(VirtualCamera, 'get_image_resolution', return_value=(1280, 720)):
        gui._update_camera_frame('sample_1280x720.png')
    
    # 验证stop被调用
    assert mock_camera.stop.called, "stop应该被调用"
    # 验证load_image被调用
    assert mock_camera.load_image.called, "load_image应该被调用"
    # 验证start被调用
    assert mock_camera.start.called, "start应该被调用"
    # 验证分辨率已更新
    assert mock_camera.width == 1280, f"宽度应该为1280，实际为{mock_camera.width}"
    assert mock_camera.height == 720, f"高度应该为720，实际为{mock_camera.height}"
    print("  [PASS] stop被调用")
    print("  [PASS] load_image被调用")
    print("  [PASS] start被调用")
    print("  [PASS] 分辨率已更新为1280x720")
    
    # 测试3：切换到不同分辨率的图片（start失败情况）
    print("\n测试3: 切换到不同分辨率的图片（start失败）")
    gui = VirtualCameraGUI()
    mock_camera = Mock(spec=VirtualCamera)
    mock_camera.is_running.return_value = True
    mock_camera.load_image.return_value = True
    mock_camera.width = 640
    mock_camera.height = 480
    mock_camera.start.return_value = False  # 模拟start失败
    gui.virtual_camera = mock_camera
    gui.auto_resolution = True
    gui.current_image_path = 'sample_640x480.png'
    gui.start_btn = Mock()
    gui.stop_btn = Mock()
    gui.status_label = Mock()
    gui.status_label.setText = Mock()
    
    mock_camera.stop.reset_mock()
    mock_camera.start.reset_mock()
    mock_camera.load_image.reset_mock()
    
    with patch.object(VirtualCamera, 'get_image_resolution', return_value=(1920, 1080)):
        gui._update_camera_frame('sample_1920x1080.png')
    
    # 验证stop被调用
    assert mock_camera.stop.called, "stop应该被调用"
    # 验证load_image被调用
    assert mock_camera.load_image.called, "load_image应该被调用"
    # 验证start被调用
    assert mock_camera.start.called, "start应该被调用"
    # 验证状态消息包含"摄像头重启失败"
    status_calls = [str(c) for c in gui.status_label.setText.call_args_list]
    assert any('摄像头重启失败' in s for s in status_calls), f"状态消息应该包含'摄像头重启失败'，实际为: {status_calls}"
    print("  [PASS] stop被调用")
    print("  [PASS] load_image被调用")
    print("  [PASS] start被调用（失败）")
    print("  [PASS] 状态消息正确显示失败信息")
    
    # 测试4：自动匹配分辨率禁用时
    print("\n测试4: 自动匹配分辨率禁用时")
    gui = VirtualCameraGUI()
    mock_camera = Mock(spec=VirtualCamera)
    mock_camera.is_running.return_value = True
    mock_camera.load_image.return_value = True
    mock_camera.width = 640
    mock_camera.height = 480
    gui.virtual_camera = mock_camera
    gui.auto_resolution = False
    gui.current_image_path = 'sample_640x480.png'
    
    mock_camera.stop.reset_mock()
    mock_camera.start.reset_mock()
    mock_camera.load_image.reset_mock()
    
    with patch.object(VirtualCamera, 'get_image_resolution', return_value=(1920, 1080)):
        gui._update_camera_frame('sample_1920x1080.png')
    
    # 验证load_image被调用
    assert mock_camera.load_image.called, "load_image应该被调用"
    # 验证stop和start不被调用
    assert not mock_camera.stop.called, "stop不应该被调用"
    assert not mock_camera.start.called, "start不应该被调用"
    print("  [PASS] load_image被调用")
    print("  [PASS] 摄像头不会重启（符合预期）")
    
    # 测试5：摄像头未运行时（但需要重启）
    print("\n测试5: 摄像头未运行时（分辨率不同）")
    gui = VirtualCameraGUI()
    mock_camera = Mock(spec=VirtualCamera)
    mock_camera.is_running.return_value = False
    mock_camera.load_image.return_value = True
    mock_camera.width = 640
    mock_camera.height = 480
    gui.virtual_camera = mock_camera
    gui.auto_resolution = True
    gui.current_image_path = 'sample_640x480.png'
    gui.status_label = Mock()
    gui.status_label.setText = Mock()
    
    mock_camera.stop.reset_mock()
    mock_camera.start.reset_mock()
    mock_camera.load_image.reset_mock()
    
    with patch.object(VirtualCamera, 'get_image_resolution', return_value=(1280, 720)):
        gui._update_camera_frame('sample_1280x720.png')
    
    # 验证stop不被调用（因为摄像头未运行）
    assert not mock_camera.stop.called, "stop不应该被调用"
    # 验证load_image被调用
    assert mock_camera.load_image.called, "load_image应该被调用"
    # 验证start不被调用（因为摄像头原来未运行）
    assert not mock_camera.start.called, "start不应该被调用"
    # 验证分辨率已更新
    assert mock_camera.width == 1280, f"宽度应该为1280，实际为{mock_camera.width}"
    assert mock_camera.height == 720, f"高度应该为720，实际为{mock_camera.height}"
    print("  [PASS] 摄像头未运行时不会调用stop")
    print("  [PASS] load_image被调用")
    print("  [PASS] 摄像头不会自动启动")
    print("  [PASS] 分辨率已更新为1280x720")
    
    print("\n" + "=" * 60)
    print("[PASS] 所有测试通过！")
    print("=" * 60)
    return True

def test_on_auto_resolution_changed():
    """测试on_auto_resolution_changed方法在摄像头运行时的行为"""
    print("\n" + "=" * 60)
    print("测试on_auto_resolution_changed方法")
    print("=" * 60)
    
    # 创建GUI实例
    app = QApplication.instance() or QApplication(sys.argv)
    
    # 测试1：启用自动匹配分辨率（分辨率不同，成功）
    print("\n测试1: 启用自动匹配分辨率（摄像头运行中，分辨率不同，成功）")
    gui = VirtualCameraGUI()
    mock_camera = Mock(spec=VirtualCamera)
    mock_camera.is_running.return_value = True
    mock_camera.width = 640
    mock_camera.height = 480
    mock_camera.start.return_value = True
    gui.virtual_camera = mock_camera
    gui.current_image_path = 'sample_1280x720.png'
    gui.start_btn = Mock()
    gui.stop_btn = Mock()
    gui.status_label = Mock()
    gui.status_label.setText = Mock()
    
    mock_camera.stop.reset_mock()
    mock_camera.start.reset_mock()
    mock_camera.load_image.reset_mock()
    
    with patch.object(VirtualCamera, 'get_image_resolution', return_value=(1280, 720)):
        from PyQt5.QtCore import Qt
        gui.on_auto_resolution_changed(Qt.Checked)
    
    # 验证stop被调用
    assert mock_camera.stop.called, "stop应该被调用"
    # 验证load_image被调用
    assert mock_camera.load_image.called, "load_image应该被调用"
    # 验证start被调用
    assert mock_camera.start.called, "start应该被调用"
    # 验证分辨率已更新
    assert mock_camera.width == 1280, f"宽度应该为1280，实际为{mock_camera.width}"
    assert mock_camera.height == 720, f"高度应该为720，实际为{mock_camera.height}"
    print("  [PASS] stop被调用")
    print("  [PASS] load_image被调用")
    print("  [PASS] start被调用")
    print("  [PASS] 分辨率已更新为1280x720")
    
    # 测试2：启用自动匹配分辨率（分辨率相同）
    print("\n测试2: 启用自动匹配分辨率（摄像头运行中，分辨率相同）")
    gui = VirtualCameraGUI()
    mock_camera = Mock(spec=VirtualCamera)
    mock_camera.is_running.return_value = True
    mock_camera.width = 1280
    mock_camera.height = 720
    gui.virtual_camera = mock_camera
    gui.current_image_path = 'sample_1280x720.png'
    gui.status_label = Mock()
    gui.status_label.setText = Mock()
    
    mock_camera.stop.reset_mock()
    mock_camera.start.reset_mock()
    mock_camera.load_image.reset_mock()
    
    with patch.object(VirtualCamera, 'get_image_resolution', return_value=(1280, 720)):
        gui.on_auto_resolution_changed(Qt.Checked)
    
    # 验证stop和start不被调用（因为分辨率相同）
    assert not mock_camera.stop.called, "分辨率相同时stop不应该被调用"
    assert not mock_camera.start.called, "分辨率相同时start不应该被调用"
    print("  [PASS] 分辨率相同时摄像头不会重启")
    
    # 测试3：摄像头未运行时
    print("\n测试3: 启用自动匹配分辨率（摄像头未运行）")
    gui = VirtualCameraGUI()
    mock_camera = Mock(spec=VirtualCamera)
    mock_camera.is_running.return_value = False
    mock_camera.width = 640
    mock_camera.height = 480
    gui.virtual_camera = mock_camera
    gui.current_image_path = 'sample_1280x720.png'
    gui.status_label = Mock()
    gui.status_label.setText = Mock()
    
    mock_camera.stop.reset_mock()
    mock_camera.start.reset_mock()
    mock_camera.load_image.reset_mock()
    
    with patch.object(VirtualCamera, 'get_image_resolution', return_value=(1280, 720)):
        gui.on_auto_resolution_changed(Qt.Checked)
    
    # 验证stop和start不被调用
    assert not mock_camera.stop.called, "stop不应该被调用"
    assert not mock_camera.start.called, "start不应该被调用"
    print("  [PASS] 摄像头未运行时不会重启")
    
    print("\n" + "=" * 60)
    print("[PASS] on_auto_resolution_changed方法测试通过！")
    print("=" * 60)
    return True

if __name__ == '__main__':
    success1 = test_update_camera_frame_with_auto_resolution()
    success2 = test_on_auto_resolution_changed()
    
    if success1 and success2:
        print("\n[SUCCESS] 所有测试通过！修复看起来正确。")
        sys.exit(0)
    else:
        print("\n[FAIL] 部分测试失败。")
        sys.exit(1)
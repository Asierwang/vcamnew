"""
测试脚本 - 验证程序环境是否正确配置
"""
import sys
import os

def test_imports():
    """测试所有必要的导入"""
    print("测试1: 检查Python模块导入...")
    try:
        import cv2
        print("  [PASS] OpenCV")
    except ImportError as e:
        print(f"  [FAIL] OpenCV 导入失败: {e}")
        return False
    
    try:
        import numpy as np
        print("  [PASS] NumPy")
    except ImportError as e:
        print(f"  [FAIL] NumPy 导入失败: {e}")
        return False
    
    try:
        from PIL import Image
        print("  [PASS] Pillow")
    except ImportError as e:
        print(f"  [FAIL] Pillow 导入失败: {e}")
        return False
    
    try:
        import pyvirtualcam
        print("  [PASS] pyvirtualcam")
    except ImportError as e:
        print(f"  [FAIL] pyvirtualcam 导入失败: {e}")
        return False
    
    try:
        from PyQt5.QtWidgets import QApplication
        print("  [PASS] PyQt5")
    except ImportError as e:
        print(f"  [FAIL] PyQt5 导入失败: {e}")
        return False
    
    return True


def test_virtual_camera_module():
    """测试虚拟摄像头模块"""
    print("\n测试2: 检查虚拟摄像头模块...")
    try:
        from virtual_camera import VirtualCamera
        print("  [PASS] virtual_camera 模块导入成功")
        
        # 尝试创建虚拟摄像头实例（不启动）
        cam = VirtualCamera(640, 480, 30)
        print("  [PASS] VirtualCamera 类实例化成功")
        
        return True
    except Exception as e:
        print(f"  [FAIL] 虚拟摄像头模块测试失败: {e}")
        return False


def test_gui_module():
    """测试GUI模块"""
    print("\n测试3: 检查GUI模块...")
    try:
        from gui import VirtualCameraGUI
        print("  [PASS] gui 模块导入成功")
        return True
    except Exception as e:
        print(f"  [FAIL] GUI 模块测试失败: {e}")
        return False


def test_sample_images():
    """检查示例图片"""
    print("\n测试4: 检查示例图片...")
    sample_images = [
        'sample_640x480.png',
        'sample_1280x720.png',
        'sample_1920x1080.png'
    ]
    
    all_exist = True
    for img in sample_images:
        if os.path.exists(img):
            print(f"  [PASS] {img}")
        else:
            print(f"  [FAIL] {img} 不存在")
            all_exist = False
    
    return all_exist


def test_image_loading():
    """测试图片加载功能"""
    print("\n测试5: 测试图片加载功能...")
    try:
        import cv2
        import numpy as np
        
        # 检查是否有示例图片
        if os.path.exists('sample_640x480.png'):
            img = cv2.imread('sample_640x480.png')
            if img is not None:
                print(f"  [PASS] 图片加载成功，尺寸: {img.shape}")
                return True
            else:
                print("  [FAIL] 图片加载失败")
                return False
        else:
            print("  ⊘ 跳过（示例图片不存在）")
            return True
    except Exception as e:
        print(f"  [FAIL] 图片加载测试失败: {e}")
        return False


def main():
    print("=" * 50)
    print("虚拟摄像头控制器 - 环境测试")
    print("=" * 50)
    
    results = []
    
    results.append(("模块导入", test_imports()))
    results.append(("虚拟摄像头模块", test_virtual_camera_module()))
    results.append(("GUI模块", test_gui_module()))
    results.append(("示例图片", test_sample_images()))
    results.append(("图片加载", test_image_loading()))
    
    print("\n" + "=" * 50)
    print("测试结果摘要")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "通过" if result else "失败"
        symbol = "[PASS]" if result else "[FAIL]"
        print(f"  {symbol} {test_name}: {status}")
    
    print("\n" + "-" * 50)
    print(f"总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("\n[PASS] 所有测试通过！环境配置正确。")
        print("\n下一步：")
        print("1. 确保已安装OBS Studio")
        print("2. 在OBS中启用虚拟摄像头功能")
        print("3. 运行 'python main.py' 或双击 'run.bat' 启动程序")
    else:
        print("\n[FAIL] 部分测试失败，请检查错误信息。")
        print("\n建议：运行 'setup.bat' 重新安装依赖。")
    
    print("=" * 50)
    
    return 0 if passed == total else 1


if __name__ == '__main__':
    sys.exit(main())
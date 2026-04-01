"""
测试自适应分辨率功能
"""
import sys
from virtual_camera import VirtualCamera

def test_get_image_resolution():
    """测试获取图片分辨率功能"""
    print("=" * 50)
    print("测试自适应分辨率功能")
    print("=" * 50)
    
    test_images = [
        ('sample_640x480.png', 640, 480),
        ('sample_1280x720.png', 1280, 720),
        ('sample_1920x1080.png', 1920, 1080)
    ]
    
    cam = VirtualCamera()
    
    all_passed = True
    
    for image_path, expected_width, expected_height in test_images:
        print(f"\n测试图片: {image_path}")
        resolution = cam.get_image_resolution(image_path)
        
        if resolution:
            width, height = resolution
            if width == expected_width and height == expected_height:
                print(f"  [PASS] 分辨率正确: {width}x{height}")
            else:
                print(f"  [FAIL] 分辨率错误: 期望 {expected_width}x{expected_height}, 实际 {width}x{height}")
                all_passed = False
        else:
            print(f"  [FAIL] 无法获取分辨率")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("[PASS] 所有测试通过！")
    else:
        print("[FAIL] 部分测试失败")
    print("=" * 50)
    
    return all_passed

if __name__ == '__main__':
    success = test_get_image_resolution()
    sys.exit(0 if success else 1)
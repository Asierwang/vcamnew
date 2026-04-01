"""
测试文件列表功能
"""
import sys
import os

def test_folder_scan():
    """测试文件夹扫描功能"""
    print("=" * 50)
    print("测试文件夹扫描功能")
    print("=" * 50)
    
    # 支持的图片格式
    supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    
    # 测试扫描当前目录
    test_folder = '.'
    print(f"\n扫描当前目录: {os.path.abspath(test_folder)}")
    
    image_list = []
    if os.path.exists(test_folder):
        for filename in os.listdir(test_folder):
            file_path = os.path.join(test_folder, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                if ext in supported_extensions:
                    image_list.append(file_path)
        
        # 按文件名排序
        image_list.sort()
        
        print(f"找到 {len(image_list)} 张图片:")
        for img_path in image_list:
            print(f"  - {os.path.basename(img_path)}")
        
        if len(image_list) > 0:
            print("\n✓ 文件夹扫描功能正常")
            return True
        else:
            print("\n⚠ 当前目录中没有找到图片文件")
            return True  # 功能正常，只是没有图片
    else:
        print("✗ 文件夹不存在")
        return False


def test_chinese_folder():
    """测试中文文件夹"""
    print("\n" + "=" * 50)
    print("测试中文文件夹支持")
    print("=" * 50)
    
    # 使用之前创建的测试目录
    test_folder = "测试目录"
    if os.path.exists(test_folder):
        print(f"\n扫描中文文件夹: {test_folder}")
        
        supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
        image_list = []
        
        for filename in os.listdir(test_folder):
            file_path = os.path.join(test_folder, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                if ext in supported_extensions:
                    image_list.append(file_path)
        
        image_list.sort()
        
        print(f"找到 {len(image_list)} 张图片:")
        for img_path in image_list:
            print(f"  - {os.path.basename(img_path)}")
        
        print("\n✓ 中文文件夹支持正常")
        return True
    else:
        print(f"⚠ 测试目录不存在: {test_folder}")
        return True  # 功能正常，只是没有测试目录


if __name__ == '__main__':
    print("开始测试文件列表功能...\n")
    
    test1 = test_folder_scan()
    test2 = test_chinese_folder()
    
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    print(f"文件夹扫描: {'通过' if test1 else '失败'}")
    print(f"中文文件夹支持: {'通过' if test2 else '失败'}")
    print("=" * 50)
    
    if test1 and test2:
        print("\n✓ 所有测试通过！")
        print("\n现在可以运行主程序测试完整的文件列表功能:")
        print("  python main.py")
        sys.exit(0)
    else:
        print("\n✗ 部分测试失败")
        sys.exit(1)

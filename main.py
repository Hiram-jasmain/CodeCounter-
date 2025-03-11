#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from pathlib import Path
def show_copyright():
    """显示版权信息"""
    print(r"""
    ██████╗  ██████╗ ██████╗ ███████╗     ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗
    ██╔══██╗██╔═══██╗██╔══██╗██╔════╝    ██╔════╝██╔═══██╗██║   ██║████╗  ██║╚══██╔══╝
    ██║  ██║██║   ██║██║  ██║█████╗      ██║     ██║   ██║██║   ██║██╔██╗ ██║   ██║   
    ██║  ██║██║   ██║██║  ██║██╔══╝      ██║     ██║   ██║██║   ██║██║╚██╗██║   ██║   
    ██████╔╝╚██████╔╝██████╔╝███████╗    ╚██████╗╚██████╔╝╚██████╔╝██║ ╚████║   ██║   
    ╚═════╝  ╚═════╝ ╚═════╝ ╚══════╝     ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   
    """)
    print("=" * 80)
    print("Code Counter 代码统计工具".center(78))
    print("版本: 1.0 | 作者: Hiram | © 2025 版权所有".center(78))
    print("=" * 80 + "\n")

def count_code_lines(start_dir, code_extensions, excluded_dirs, max_file_size=2097152):
    """
    统计指定目录下所有代码文件的行数（递归遍历子目录）
    :return: (总代码行数, 遇到的扩展名集合, 文件统计字典[路径:行数], 错误文件列表)
    """
    total_lines = 0
    extensions = set()
    file_details = {}
    error_files = []
    scanned_dirs = 0
    scanned_files = 0

    for root, dirs, files in os.walk(start_dir):
        scanned_dirs += 1
        # 过滤需要排除的目录
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for filename in files:
            scanned_files += 1
            file_path = os.path.join(root, filename)
            file_ext = os.path.splitext(filename)[1].lower()

            if file_ext not in code_extensions:
                continue

            try:
                # 跳过过大的文件
                if os.path.getsize(file_path) > max_file_size:
                    error_files.append(f"{file_path} (文件过大)")
                    continue

                with open(file_path, 'r', encoding='utf-8') as f:
                    file_lines = sum(1 for _ in f)
                    total_lines += file_lines
                    extensions.add(file_ext)
                    file_details[file_path] = file_lines
            except UnicodeDecodeError:
                error_files.append(f"{file_path} (二进制文件)")
            except PermissionError:
                error_files.append(f"{file_path} (权限不足)")
            except Exception as e:
                error_files.append(f"{file_path} ({str(e)})")

    return total_lines, extensions, file_details, error_files, scanned_dirs, scanned_files

if __name__ == "__main__":
    try:

        start_time = time.time()
        # Windows系统设置控制台编码
        if os.name == 'nt':
            os.system('chcp 65001 > nul')

        CODE_EXTENSIONS = {
            '.py', '.java', '.c', '.cpp', '.h', '.hpp',
            '.cs', '.dart', '.rs', '.go', '.swift', '.kt', '.kts',
            '.js', '.ts', '.jsx', '.tsx', '.php', '.rb', '.groovy',
            '.scala', '.lua', '.r', '.pl', '.sh', '.bash', '.ps1',
            '.html', '.css', '.scss', '.sass', '.less', '.vue', '.svelte',
            '.yml', '.yaml', '.toml', '.ini', '.xml', '.json',
            '.sql', '.m', '.mm', '.hs', '.elm', '.clj', '.cljc', '.cljs'
        }

        EXCLUDED_DIRS = {
            '.git', '.svn', '.hg', '.bzr', '.cvs',
            '.idea', '.vscode', '.vs', '.atom', '.settings',
            'venv', 'env', 'virtualenv', 'venv-win', 'venv27', 'venv34',
            'node_modules', 'jspm_packages', 'bower_components', 'vendor',
            'dist', 'build', 'target', 'out', 'bin', 'obj', 'release',
            '__pycache__', '.cache', '.pytest_cache', 'tmp', 'temp', 'logs',
            'coverage', '.nyc_output', 'test-results',
            'public', 'static', 'assets', 'media', 'migrations', 'data'
        }

        current_dir = os.getcwd()
        show_copyright()
        print(f"🔍 正在扫描目录: {current_dir}\n")

        dir_counts = {}
        current_files_details = {}
        current_exts = set()
        total_errors = []
        total_scanned_dirs = 0
        total_scanned_files = 0

        # 扫描子目录
        for entry in os.listdir(current_dir):
            entry_path = os.path.join(current_dir, entry)
            if os.path.isdir(entry_path) and entry not in EXCLUDED_DIRS:
                print(f"📂 扫描子目录: {entry}")
                dir_lines, dir_exts, dir_files, dir_errors, dir_count, file_count = count_code_lines(
                    entry_path, CODE_EXTENSIONS, EXCLUDED_DIRS
                )
                dir_counts[entry] = (dir_lines, dir_exts, dir_files)
                total_errors.extend(dir_errors)
                total_scanned_dirs += dir_count
                total_scanned_files += file_count

        # 扫描当前目录文件
        print("\n📝 扫描当前目录文件...")
        for entry in os.listdir(current_dir):
            entry_path = os.path.join(current_dir, entry)
            if os.path.isfile(entry_path):
                file_ext = os.path.splitext(entry)[1].lower()
                if file_ext in CODE_EXTENSIONS:
                    try:
                        if os.path.getsize(entry_path) > 2097152:
                            total_errors.append(f"{entry_path} (文件过大)")
                            continue

                        with open(entry_path, 'r', encoding='utf-8') as f:
                            file_lines = sum(1 for _ in f)
                            current_files_details[entry] = file_lines
                            current_exts.add(file_ext)
                            total_scanned_files += 1
                    except UnicodeDecodeError:
                        total_errors.append(f"{entry_path} (二进制文件)")
                    except PermissionError:
                        total_errors.append(f"{entry_path} (权限不足)")
                    except Exception as e:
                        total_errors.append(f"{entry_path} ({str(e)})")

        # 计算结果
        total_dir_lines = sum(lines for lines, _, _ in dir_counts.values())
        current_files_lines = sum(current_files_details.values())
        total_lines = total_dir_lines + current_files_lines
        time_elapsed = time.time() - start_time

        # 输出结果
        print("\n================ 📊 统计结果 ================")
        print(f"🕒 耗时: {time_elapsed:.2f}秒")
        print(f"📁 扫描目录总数: {total_scanned_dirs}")
        print(f"📄 扫描文件总数: {total_scanned_files}")
        print(f"❗ 遇到错误文件: {len(total_errors)}个")

        # 子目录统计
        for dir_name, (lines, exts, files) in dir_counts.items():
            exts_str = ', '.join(sorted(exts)) if exts else "无代码文件"
            print(f"\n📁 {dir_name}/: {lines} 行 ({exts_str})")
            sorted_files = sorted(files.items(), key=lambda x: (-x[1], x[0]))[:5]
            for file_path, line_count in sorted_files:
                rel_path = os.path.relpath(file_path, start=current_dir)
                print(f"  └─ {rel_path}: {line_count} 行")

        # 当前目录文件统计
        if current_files_details:
            print(f"\n📄 当前目录文件（共 {current_files_lines} 行）:")
            sorted_files = sorted(current_files_details.items(), key=lambda x: (-x[1], x[0]))
            for filename, line_count in sorted_files[:10]:  # 显示前10大文件
                print(f"  ├─ {filename}: {line_count} 行")
            print(f"  └─ 总计 {len(current_files_details)} 个代码文件")
        else:
            print("\n📄 当前目录没有代码文件")

        # 文件类型汇总
        all_exts = current_exts.union(*(exts for _, exts, _ in dir_counts.values()))
        print(f"\n🔤 检测到的文件类型 ({len(all_exts)} 种): {', '.join(sorted(all_exts))}")

        # 错误文件显示
        if total_errors:
            print(f"\n❌ 错误文件（前20个）:")
            for error in total_errors[:20]:
                print(f"  ! {error}")

        print(f"\n✅ 总代码行数: {total_lines} 行")
        input("\n🎉 统计完成，按 Enter 键退出...")

    except Exception as e:
        print(f"\n❌ 发生致命错误: {str(e)}")
        input("⚠ 按 Enter 键退出...")
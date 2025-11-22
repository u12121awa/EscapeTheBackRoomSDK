import os

# ===== 配置这里 =====
# 以脚本所在目录为基准，拼出 SDK\SDK 目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "SDK", "SDK")   # 如果实际不是这个路径，再改
OUTPUT_FILE = "a.txt"
# ====================


def collect_files(root):
    cpp_files = []
    hpp_files = []

    if not os.path.exists(root):
        print(f"[警告] ROOT_DIR 路径不存在: {root}")
        return cpp_files, hpp_files

    print(f"[信息] 开始扫描目录: {root}")

    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            lower = name.lower()
            if lower.endswith(".cpp") or lower.endswith(".hpp"):
                rel_path = os.path.join(os.path.relpath(dirpath, BASE_DIR), name)
                # 统一为 VS 常用反斜杠
                rel_path = os.path.normpath(rel_path).replace("/", "\\")
                if lower.endswith(".cpp"):
                    cpp_files.append(rel_path)
                else:
                    hpp_files.append(rel_path)

    cpp_files.sort()
    hpp_files.sort()

    print(f"[信息] 找到 {len(cpp_files)} 个 .cpp，{len(hpp_files)} 个 .hpp")
    return cpp_files, hpp_files


def main():
    cpp_files, hpp_files = collect_files(ROOT_DIR)

    lines = []

    # <ClCompile> 组
    lines.append('  <ItemGroup>')
    for path in cpp_files:
        lines.append(f'    <ClCompile Include="{path}">')
        lines.append("      <PrecompiledHeader Condition=\"'$(Configuration)|$(Platform)'=='Debug|x64'\">NotUsing</PrecompiledHeader>")
        lines.append("      <PrecompiledHeader Condition=\"'$(Configuration)|$(Platform)'=='Release|x64'\">NotUsing</PrecompiledHeader>")
        lines.append("    </ClCompile>")
    lines.append('  </ItemGroup>')

    # <ClInclude> 组
    lines.append('  <ItemGroup>')
    for path in hpp_files:
        lines.append(f'    <ClInclude Include="{path}" />')
    lines.append('  </ItemGroup>')

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[完成] 已生成: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

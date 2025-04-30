import subprocess
import time
from IPython.display import display, HTML, clear_output

def run_and_log(
        cmd, log_file="log.txt", expected_lines=None, interval=0.5, tail_lines=1):
    import os

    def progress_bar_html(percent, lineno, expected_lines):
        return f"""
        <div style='display: flex; align-items: center; margin-bottom: 5px;'>
            <div style='width:320px; background:#eee; border-radius:6px; height:20px; position:relative;'>
                <div style='width:{percent:.1f}%; height:100%; background:#4caf50; border-radius:6px;'></div>
                <div style='position:absolute; left:0; top:0; width:100%; height:100%; line-height:20px; text-align:center; font-weight:bold; color:#222;'>{percent:.1f}%</div>
            </div>
            <span style="margin-left: 12px; font-family: monospace; font-weight:bold; color:#333;">
                [{lineno}{f" / {expected_lines}" if expected_lines else ""} 行目]
            </span>
        </div>
        """

    # 既存ログファイルの行をカウント
    old_lines = []
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8", errors="ignore") as fr:
            old_lines = [line.rstrip() for line in fr]

    with open(log_file, "a", encoding="utf-8") as f:
        lines = old_lines.copy()
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1, universal_newlines=True)
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                f.write(line)
                f.flush()
                lines.append(line.rstrip())
                clear_output(wait=True)
                lineno = len(lines)
                percent = min(lineno / expected_lines * 100, 100) if expected_lines else 0
                pbar = progress_bar_html(percent, lineno, expected_lines)
                show_lines = lines[-tail_lines:] if tail_lines > 0 else []
                info = "<pre>" + "\n".join(
                    f"[{lineno-len(show_lines)+1+i}] {l}" for i, l in enumerate(show_lines)
                ) + "</pre>" if show_lines else ""
                display(HTML(pbar + info))
                time.sleep(interval)
        clear_output(wait=True)
        lineno = len(lines)
        percent = 100  # 完了時は必ず100%
        pbar = progress_bar_html(percent, lineno, expected_lines)
        show_lines = lines[-tail_lines:] if tail_lines > 0 else []
        info = "<pre>" + "\n".join(
            f"[{lineno-len(show_lines)+1+i}] {l}" for i, l in enumerate(show_lines)
        ) + "</pre>" if show_lines else ""
        display(HTML(pbar + info))
        process.wait()

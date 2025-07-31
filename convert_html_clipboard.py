import win32clipboard
import subprocess
import tempfile
import os
import argparse


def get_html_from_clipboard():
    win32clipboard.OpenClipboard()
    try:
        html_format = win32clipboard.RegisterClipboardFormat("HTML Format")

        if win32clipboard.IsClipboardFormatAvailable(html_format):
            raw_data = win32clipboard.GetClipboardData(html_format)

            # Decode bytes to string
            if isinstance(raw_data, bytes):
                data = raw_data.decode("utf-8", errors="ignore")
            else:
                data = raw_data  # Already a string

            # Extract HTML part (skip CF_HTML headers)
            start = data.lower().find("<html")
            if start != -1:
                return data[start:]
            else:
                return None
        else:
            return None
    finally:
        win32clipboard.CloseClipboard()


def convert_html_to(pandoc_path, html, output_type):
    # Use temporary file to pass HTML to Pandoc
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmp_in:
        tmp_in.write(html)
        tmp_in_path = tmp_in.name

    # Temporary output file for type
    tmp_out_path = tmp_in_path + "." + output_type
    try:
        subprocess.run([
            pandoc_path, tmp_in_path,
            "-f", "html", "-t", output_type,
            "-o", tmp_out_path
        ], check=True)

        with open(tmp_out_path, encoding="utf-8") as f:
            return f.read()
    finally:
        os.remove(tmp_in_path)
        if os.path.exists(tmp_out_path):
            os.remove(tmp_out_path)


def set_clipboard_text(text):
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    finally:
        win32clipboard.CloseClipboard()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Clipboard Converter', description='Convert HTML in clipboard to other type.')
    parser.add_argument('-p', '--pandoc', required=True, help='The path to pandoc.')
    parser.add_argument('-t', '--type', required=True, help='Convert to Org Mode format.')
    args = parser.parse_args()

    html_content = get_html_from_clipboard()
    org_content = convert_html_to(args.pandoc, html_content, args.type)
    set_clipboard_text(org_content)

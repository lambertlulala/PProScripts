import win32clipboard
import subprocess
import tempfile
import os
import argparse


def get_clipboard_data(format_name):
    win32clipboard.OpenClipboard()
    try:
        clipboard_format = win32clipboard.RegisterClipboardFormat(format_name)

        if win32clipboard.IsClipboardFormatAvailable(clipboard_format):
            raw_data = win32clipboard.GetClipboardData(clipboard_format)

            # Decode bytes to string if possible
            if isinstance(raw_data, bytes):
                try:
                    data = raw_data.decode("utf-8", errors="ignore")
                except UnicodeDecodeError:
                    data = raw_data  # Return bytes if decode fails
            else:
                data = raw_data

            return data
        else:
            return None
    finally:
        win32clipboard.CloseClipboard()


def get_text_from_clipboard():
    win32clipboard.OpenClipboard()
    try:
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
            return win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        else:
            return None
    finally:
        win32clipboard.CloseClipboard()


def get_html_from_clipboard():
    html_data = get_clipboard_data("HTML Format")
    if html_data:
        start = html_data.lower().find("<html")
        html_data = html_data[start:] if start != -1 else None

    return html_data


def pandoc_convert(pandoc_path, data, source_type, dest_type):
    # Use temporary file to pass source to Pandoc
    with tempfile.NamedTemporaryFile(delete=False, suffix= "." + source_type, mode="w", encoding="utf-8") as tmp_in:
        tmp_in.write(data)
        tmp_in_path = tmp_in.name

    # Temporary output file for type
    tmp_out_path = tmp_in_path + "." + dest_type
    try:
        subprocess.run([
            pandoc_path, tmp_in_path,
            "-f", source_type, "-t", dest_type,
            "-o", tmp_out_path
        ], check=True)

        with open(tmp_out_path, encoding="utf-8") as f:
            return f.read()
    finally:
        os.remove(tmp_in_path)
        if os.path.exists(tmp_out_path):
            os.remove(tmp_out_path)    


def convert_html_to(pandoc_path, html, output_type):
    return pandoc_convert(pandoc_path, html, "html", output_type)


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
    parser.add_argument('-s', '--source', required=True, help='Source format.')
    parser.add_argument('-o', '--output', required=True, help='Output format.')
    args = parser.parse_args()

    data_to_set_clipboard = ""
    if args.source == 'html':
        html_content = get_html_from_clipboard()
        data_to_set_clipboard = convert_html_to(args.pandoc, html_content, args.output)
    else:
        text = get_text_from_clipboard()
        data_to_set_clipboard = pandoc_convert(args.pandoc, text, args.source, args.output)
        
    set_clipboard_text(data_to_set_clipboard)

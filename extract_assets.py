import os
import zipfile

docx_path = r"c:\Users\marit\OneDrive\Desktop\Asociación Mexicana de Diabetes\diploma\certificates-2023-11-27-05-33-09-utc\Business Certificates Template\Certificate_MS_Word_(Docx)_Files\Certificate.docx"
output_dir = r"c:\Users\marit\OneDrive\Desktop\Asociación Mexicana de Diabetes\diploma"

def extract_docx_media(docx_file, dest_dir):
    if not os.path.exists(docx_file):
        print(f"Error: {docx_file} does not exist.")
        return
        
    print(f"Opening {docx_file}...")
    with zipfile.ZipFile(docx_file, 'r') as archive:
        media_files = [f for f in archive.namelist() if f.startswith('word/media/')]
        if not media_files:
            print("No media files found in word/media/")
            return
            
        print(f"Found {len(media_files)} media files:")
        largest_file = None
        largest_size = 0
        
        for file_path in media_files:
            filename = os.path.basename(file_path)
            dest_path = os.path.join(dest_dir, filename)
            
            # Extract file
            data = archive.read(file_path)
            with open(dest_path, 'wb') as f:
                f.write(data)
            
            size_bytes = len(data)
            size_kb = size_bytes / 1024
            print(f"  Extracted {filename} ({size_kb:.2f} KB) to {dest_path}")
            
            if size_bytes > largest_size:
                largest_size = size_bytes
                largest_file = dest_path
                
        if largest_file:
            bg_path = os.path.join(dest_dir, "background_template.png")
            with open(largest_file, 'rb') as src, open(bg_path, 'wb') as dst:
                dst.write(src.read())
            print(f"Saved largest image as background_template.png (Source: {os.path.basename(largest_file)})")

if __name__ == '__main__':
    extract_docx_media(docx_path, output_dir)

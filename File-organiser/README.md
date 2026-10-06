from pathlib import Path
import argparse, shutil

GROUPS={
"Images":{".jpg",".jpeg",".png",".gif",".webp",".bmp",".svg"},
"Videos":{".mp4",".mov",".avi",".mkv",".webm"},
"Audio":{".mp3",".wav",".flac",".m4a",".aac"},
"Documents":{".pdf",".doc",".docx",".txt",".rtf",".odt"},
"Archives":{".zip",".rar",".7z",".tar",".gz"},
"Spreadsheets":{".xls",".xlsx",".csv"},
}

def group(path):
    ext=path.suffix.lower()
    for name,exts in GROUPS.items():
        if ext in exts:return name
    return "Other"

def unique_destination(dest):
    if not dest.exists():return dest
    stem,suffix=dest.stem,dest.suffix
    i=1
    while True:
        candidate=dest.with_name(f"{stem}_{i}{suffix}")
        if not candidate.exists():return candidate
        i+=1

def main():
    p=argparse.ArgumentParser()
    p.add_argument("folder",type=Path)
    p.add_argument("--apply",action="store_true",help="actually move files")
    args=p.parse_args()
    folder=args.folder.expanduser().resolve()
    if not folder.is_dir(): raise SystemExit("Folder does not exist.")
    for f in sorted(folder.iterdir()):
        if not f.is_file() or f.name=="organizer.py":continue
        target_dir=folder/group(f); target=unique_destination(target_dir/f.name)
        print(f"{f.name}  ->  {target.relative_to(folder)}")
        if args.apply:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(f),str(target))
    if not args.apply: print("\nPreview only. Add --apply to make changes.")

if __name__=="__main__":main()

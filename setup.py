import os, sys




output= ".\dist"
target= "costom_vr_ui.py"
scripts_path= os.path.join(os.path.dirname(sys.executable), "Scripts", "pyinstaller")


# os.system(fr'{scripts_path} {target} --onefile -w --noconsole --clean --distpath={output} --workpath .\build --add-binary ".\static\ffmpeg\ffmpeg.exe;." --add-binary ".\static\ffmpeg\ffprobe.exe;."')



target= "costom_ui2.py"
os.system(fr'{scripts_path} {target} --onefile -w --noconsole --clean --distpath={output} --workpath=.\build --add-binary "static\ffmpeg\ffmpeg.exe;static\ffmpeg" --add-binary "static\ffmpeg\ffprobe.exe;static\ffmpeg" --add-data "static\images\left.png;static\images" --add-data "static\images\right.png;static\images"')

import os, sys

print('sys.path:', sys.path)
for path in sys.path:
    if path and 'site-packages' in path:
        try:
            for f in os.listdir(path):
                if 'genai' in f.lower():
                    print('found', f, 'in', path)
        except Exception as e:
            pass

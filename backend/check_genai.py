import pkgutil
import sys

print('sys.path', sys.path)
print('searching for genai modules:')
for finder, name, ispkg in pkgutil.iter_modules():
    if 'genai' in name.lower() or 'google' in name.lower():
        print(name)

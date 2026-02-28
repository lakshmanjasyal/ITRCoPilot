try:
    import google.genai as genai
    print('import google.genai successful,', genai)
except Exception as e:
    print('import google.genai failed', e)

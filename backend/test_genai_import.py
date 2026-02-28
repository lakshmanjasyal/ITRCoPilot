try:
    import google.generativeai as genai
    print('import succeeded, version', getattr(genai, '__version__', 'unknown'))
except Exception as e:
    print('import failed', e)

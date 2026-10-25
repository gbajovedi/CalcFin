import sys
sys.stdout.reconfigure(encoding='utf-8')

# Let's inspect the pdf using basic string search or streams
with open('Manual de uso hp 17bII.pdf', 'rb') as f:
    data = f.read()

import re
# Look for text streams in PDF
streams = re.findall(b'stream[\r\n]+(.*?)[\r\n]+endstream', data, re.DOTALL)
print(f"Found {len(streams)} streams")

import zlib
extracted_text = []
for i, s in enumerate(streams):
    try:
        decomp = zlib.decompress(s)
        # Search for text
        t = decomp.decode('utf-8', errors='ignore')
        extracted_text.append(t)
    except Exception:
        try:
            decomp = zlib.decompress(s, -zlib.MAX_WBITS)
            t = decomp.decode('utf-8', errors='ignore')
            extracted_text.append(t)
        except Exception:
            pass

full_text = "\n".join(extracted_text)
print(f"Total extracted characters: {len(full_text)}")

matches = [m.start() for m in re.finditer(r'padrão|padrao|default|configuração|predefinid', full_text, re.IGNORECASE)]
print(f"Matches found: {len(matches)}")
for idx in matches[:20]:
    print(full_text[max(0, idx-100):min(len(full_text), idx+150)])
    print('='*40)


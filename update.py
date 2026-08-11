from urllib.parse import quote
import os
import re

css = '''
/* Sub Gallery Styles */
.sub-gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
  margin-top: 30px;
}
.sub-gallery-item {
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--border);
  aspect-ratio: 1;
}
.sub-gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}
.sub-gallery-item:hover img {
  transform: scale(1.1);
}
.sub-gallery-title {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 40px 0 20px;
  color: var(--primary);
  border-bottom: 1px solid var(--border);
  padding-bottom: 10px;
}
'''
with open('style.css', 'a', encoding='utf-8') as f:
    f.write(css)

def get_images(folder):
    path = os.path.join('Plumber works', folder)
    if not os.path.exists(path): return ''
    files = [f for f in os.listdir(path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    html = ''
    for file in files:
        url = 'Plumber works/' + folder + '/' + file
        encoded_url = quote(url)
        html += f'          <div class="sub-gallery-item"><img src="{encoded_url}" alt="{folder} work" loading="lazy" /></div>\n'
    return html

sections = {
    'pprc': [('PPr Piping', 'PPRC Piping Work'), ('Sanitory', 'Sanitary Work')],
    'pvc': [('Pvc Piping', 'PVC Piping Work'), ('Mainhole', 'Mainhole Work')],
    'gi': [('Gi Fitting', 'GI Fitting Work')]
}

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# First, remove any existing sub-gallery sections to avoid duplication
html = re.sub(r'        <h3 class="sub-gallery-title">.*?</div>\n', '', html, flags=re.DOTALL)

for tab_id, folders in sections.items():
    gallery_html = ''
    for folder, title in folders:
        imgs = get_images(folder)
        if imgs:
            gallery_html += f'        <h3 class="sub-gallery-title">{title}</h3>\n        <div class="sub-gallery-grid">\n{imgs}        </div>\n'
    
    match = re.search(rf'(id="{tab_id}-details".*?)(?=<div class="tab-content"|</section>)', html, re.DOTALL)
    if match:
        tab_content = match.group(1)
        idx = tab_content.rfind('</div>')
        if idx != -1:
            new_tab_content = tab_content[:idx] + gallery_html + tab_content[idx:]
            html = html.replace(tab_content, new_tab_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

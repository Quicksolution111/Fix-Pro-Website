import re
import os
from urllib.parse import quote

# 1. Generate new gallery HTML for Plumbing and Electrical
def get_images(base, folder):
    path = os.path.join(base, folder)
    if not os.path.exists(path): return ''
    files = [f for f in os.listdir(path) if f.lower().endswith('.webp')]
    if not files: return ''
    html = ''
    for file in sorted(files):
        url = base + '/' + folder + '/' + file
        encoded_url = quote(url)
        # Using decoding="async" and explicit aspect ratio to prevent layout shifts
        html += f'          <div class="sub-gallery-item" style="aspect-ratio: 1;"><img src="{encoded_url}" alt="{folder} work" loading="lazy" decoding="async" /></div>\n'
    return html

sections = {
    'pprc': [('Plumber works', 'PPr Piping', 'PPRC Piping Work'), ('Plumber works', 'Sanitory', 'Sanitary Work')],
    'pvc': [('Plumber works', 'Pvc Piping', 'PVC Piping Work'), ('Plumber works', 'Mainhole', 'Mainhole Work')],
    'gi': [('Plumber works', 'Gi Fitting', 'GI Fitting Work')],
    'electrical': [
        ('Electriccal work', 'Dp Dressing', 'DP Dressing'),
        ('Electriccal work', 'Electrical Piping', 'Electrical Piping'),
        ('Electriccal work', 'Profile Lighting', 'Profile Lighting'),
        ('Electriccal work', 'Stair wiring', 'Stair Wiring')
    ]
}

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 2. Add Preloads in <head>
preload_tags = """  <!-- Preload Critical Assets -->
  <link rel="preload" href="hero_banner.jpg" as="image">
  <link rel="preload" href="style.css" as="style">
"""
if "<!-- Preload Critical Assets -->" not in html:
    html = html.replace('<link rel="preconnect" href="https://fonts.googleapis.com" />', preload_tags + '  <link rel="preconnect" href="https://fonts.googleapis.com" />')

# 3. Clean existing sub-galleries
html = re.sub(r'\s*<h3 class="sub-gallery-title">.*?</div>\s*(?=<div class="tab-content"|</section>|</div><!-- end tab -->)', '', html, flags=re.DOTALL)

# 4. Inject new sub-galleries
for tab_id, folders in sections.items():
    gallery_html = ''
    for base, folder, title in folders:
        imgs = get_images(base, folder)
        if imgs:
            gallery_html += f'\n        <h3 class="sub-gallery-title">{title}</h3>\n        <div class="sub-gallery-grid">\n{imgs}        </div>'
    
    # We find where the tab content ends
    # We look for <div class="tab-content" id="tab_id">...</div>
    # A safe way is to find the tab id, then find the last </div> before the next tab-content or </section>
    
    pattern = rf'(id="{tab_id}-details".*?)(?=\s*<div class="tab-content"|\s*</section>)'
    match = re.search(pattern, html, flags=re.DOTALL)
    
    if match:
        tab_content = match.group(1)
        # Append gallery_html right before the final </div> of this tab_content
        # Let's just append it to the end of the matched group if it doesn't already have it
        if gallery_html:
            # The tab_content usually ends with </div>.
            last_div_idx = tab_content.rfind('</div>')
            if last_div_idx != -1:
                new_tab_content = tab_content[:last_div_idx] + gallery_html + '\n      ' + tab_content[last_div_idx:]
                html = html.replace(tab_content, new_tab_content)

# Update hero image to webp if it exists, otherwise keep jpg (we didn't convert hero_banner.jpg yet, let's keep it jpg for now)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

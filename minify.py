import re

def minify_css(css):
    # Remove comments
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    # Remove extra spaces
    css = re.sub(r'\s+', ' ', css)
    # Remove spaces around important characters
    css = re.sub(r'\s*([\{\}\:\;\,\>])\s*', r'\1', css)
    return css.strip()

def minify_js(js):
    # Remove block comments
    js = re.sub(r'/\*.*?\*/', '', js, flags=re.DOTALL)
    # Remove line comments
    js = re.sub(r'//.*', '', js)
    # Remove extra whitespace
    js = re.sub(r'\s+', ' ', js)
    js = re.sub(r'\s*([\{\}\:\;\,\=\+\-\*\/\(\)])\s*', r'\1', js)
    return js.strip()

# Read style.css and append a few polish rules before minifying
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

polish_css = """
/* UI/UX Polish */
:root {
  --shadow-primary: 0 4px 14px 0 rgba(0,118,255,0.39);
}
body {
  font-family: 'Inter', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
h1, h2, h3, h4, h5, h6 {
  font-family: 'Outfit', sans-serif;
  letter-spacing: -0.02em;
}
.btn {
  box-shadow: var(--shadow-primary);
  transition: all 0.3s ease;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,118,255,0.23);
}
"""

minified_css = minify_css(css + polish_css)
with open('style.min.css', 'w', encoding='utf-8') as f:
    f.write(minified_css)

with open('script.js', 'r', encoding='utf-8') as f:
    js = f.read()

minified_js = minify_js(js)
with open('script.min.js', 'w', encoding='utf-8') as f:
    f.write(minified_js)

# Update index.html to point to minified versions
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('href="style.css"', 'href="style.min.css"')
html = html.replace('src="script.js"', 'src="script.min.js"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

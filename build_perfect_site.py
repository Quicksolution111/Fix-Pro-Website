import os
import urllib.parse
import re

# Helper to verify and format image tags
def make_gallery_items(folder, alt_prefix):
    if not os.path.exists(folder):
        print(f"WARNING: Folder not found: {folder}")
        return ""
    
    files = sorted([f for f in os.listdir(folder) if f.lower().endswith(('.webp', '.jpg', '.jpeg', '.png'))])
    items = []
    for f in files:
        rel_path = folder.replace('\\', '/') + '/' + f
        # Encode for web URL
        url = urllib.parse.quote(rel_path)
        items.append(f'          <div class="sub-gallery-item" style="aspect-ratio: 1;"><img src="{url}" alt="{alt_prefix}" loading="lazy" decoding="async" /></div>')
    return "\n".join(items)

# SVG Icons with semantic accuracy and consistent styling
ICONS = {
    # PPRC
    "pprc_new": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M3 3h18v18H3z" /><path stroke="var(--accent)" d="M3 9h18M9 3v18" /><path stroke="var(--primary)" d="M6 14l5-5 5 5" /></svg>""",
    "pprc_bath": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M4 4h12v4H4zM16 6h4M12 8v8a2 2 0 0 1-2 2H4" /><path stroke="var(--accent)" d="M10 12h.01M6 12h.01M8 15h.01" /></svg>""",
    "pprc_tank": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="7" ry="2" stroke="var(--primary)" /><path stroke="var(--primary)" d="M5 5v12c0 2.2 3.1 4 7 4s7-1.8 7-4V5" /><path stroke="var(--accent)" d="M5 11h14M5 16h14" /></svg>""",
    "pprc_motor": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8" stroke="var(--primary)" /><path stroke="var(--primary)" d="M12 2v4M12 18v4M2 12h4M18 12h4" /><circle cx="12" cy="12" r="3" stroke="var(--accent)" /></svg>""",
    "pprc_instant_geyser": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="3" width="12" height="18" rx="2" stroke="var(--primary)" /><path stroke="var(--accent)" d="M10 15h4M12 7v4" /><circle cx="12" cy="11" r="2" stroke="var(--accent)" /></svg>""",
    "pprc_standing_geyser": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="2" width="10" height="20" rx="4" stroke="var(--primary)" /><path stroke="var(--accent)" d="M10 8h4M10 16h4" /><circle cx="12" cy="12" r="2" stroke="var(--accent)" /></svg>""",
    "pprc_pump": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="7" stroke="var(--primary)" /><path stroke="var(--primary)" d="M12 5v7l4 4" /><path stroke="var(--accent)" d="M12 12m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /></svg>""",
    "repair": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" /><path stroke="var(--accent)" d="M18 18h.01M15 15h.01" /></svg>""",
    
    # PVC
    "pvc_no_dig": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M2 17h20" /><rect x="4" y="8" width="16" height="5" rx="1" stroke="var(--accent)" /><path stroke="var(--primary)" d="M6 13v4M18 13v4" /></svg>""",
    "pvc_dig": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M2 10h20" /><rect x="4" y="14" width="16" height="5" rx="1" stroke="var(--accent)" /><path stroke="var(--primary)" d="M14 6l3 3-8 8-3-3 8-8z" /></svg>""",
    "pvc_mainhole": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9" stroke="var(--primary)" /><circle cx="12" cy="12" r="5" stroke="var(--accent)" /><path stroke="var(--primary)" d="M12 3v18M3 12h18" /></svg>""",

    # GI
    "gi_feet": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="10" rx="2" stroke="var(--primary)" /><path stroke="var(--accent)" d="M6 7v10M12 7v10M18 7v10" /></svg>""",
    "gi_lump": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="14" height="10" rx="2" stroke="var(--primary)" /><circle cx="18" cy="12" r="3" stroke="var(--accent)" /><path stroke="var(--accent)" d="M18 10v4M16 12h4" /></svg>""",

    # Electrical
    "elec_piping": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" /><path stroke="var(--accent)" d="M9 22V12h6v10" /></svg>""",
    "elec_point": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .5 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5" /><path stroke="var(--primary)" d="M9 18h6M10 21h4" /><path stroke="var(--accent)" d="M12 2v3M4.9 4.9l2.1 2.1M17 7l2.1-2.1" /></svg>""",
    "elec_wiring": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10" /><path stroke="var(--accent)" d="M12 6a6 6 0 1 0 6 6" /><circle cx="18" cy="6" r="2" stroke="var(--primary)" /></svg>""",
    "elec_dp_normal": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="2" stroke="var(--primary)" /><path stroke="var(--accent)" d="M8 7h8M8 12h8M8 17h8" /></svg>""",
    "elec_dp_heavy": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="2" stroke="var(--primary)" /><path stroke="var(--accent)" d="M12 7v10M8 12h8" /><path stroke="var(--primary)" d="M12 9l-2 3h4l-2 3" /></svg>""",
    "elec_fanos": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9" stroke="var(--primary)" /><path stroke="var(--accent)" d="M12 12L8 8M12 12l4 4M12 12l-4 4M12 12l4-4" /><circle cx="12" cy="12" r="2" fill="var(--accent)" /></svg>""",

    # Solar
    "solar_install": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" stroke="var(--primary)" /><path stroke="var(--primary)" d="M12 3v18M3 12h18" /><circle cx="12" cy="12" r="4" stroke="var(--accent)" fill="var(--bg)" /></svg>""",
    "solar_idea": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .5 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5" /><path stroke="var(--primary)" d="M9 18h6M10 21h4" /><rect x="9" y="6" width="6" height="4" stroke="var(--accent)" /></svg>""",
    "solar_repair": """<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="12" rx="2" stroke="var(--primary)" /><path stroke="var(--accent)" d="M14.7 16.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" /></svg>"""
}

# Pre-render sub-galleries
pprc_gallery = make_gallery_items("Plumber works/PPr Piping", "PPRC Piping work")
sanitary_gallery = make_gallery_items("Plumber works/Sanitory", "Sanitary fitting work")
pvc_gallery = make_gallery_items("Plumber works/Pvc Piping", "PVC Piping work")
mainhole_gallery = make_gallery_items("Plumber works/Mainhole", "Mainhole work")
gi_gallery = make_gallery_items("Plumber works/Gi Fitting", "GI Fitting work")

dp_gallery = make_gallery_items("Electriccal work/Dp Dressing", "DP Dressing work")
elec_piping_gallery = make_gallery_items("Electriccal work/Electrical Piping", "Electrical Piping work")
profile_gallery = make_gallery_items("Electriccal work/Profile Lighting", "Profile Lighting work")
stair_gallery = make_gallery_items("Electriccal work/Stair wiring", "Stair Sensor Lighting work")

# Combined lighting gallery
lighting_combined = profile_gallery + ("\n" + stair_gallery if stair_gallery else "")

catalogue_html = f"""  <!-- ===== CATALOGUE ===== -->
  <section class="catalogue" id="catalogue">
    <div class="container">
      <div class="section-header">
        <span class="section-tag">Transparent Pricing</span>
        <h2 class="section-title">Our <span class="gradient-text">Rate Catalogue</span></h2>
        <p class="section-subtitle">Clear, honest pricing — no hidden charges. All rates negotiable for large projects.</p>
      </div>

      <div class="catalogue-tabs">
        <button class="tab-btn active" data-tab="pprc" id="tab-pprc">🟢 PPRC</button>
        <button class="tab-btn" data-tab="pvc" id="tab-pvc">⬜ PVC</button>
        <button class="tab-btn" data-tab="gi" id="tab-gi">🔩 GI</button>
        <button class="tab-btn" data-tab="electrical" id="tab-electrical">⚡ Electrical</button>
        <button class="tab-btn" data-tab="solar" id="tab-solar">☀️ Solar</button>
      </div>

      <!-- PPRC TAB -->
      <div class="tab-content active" id="pprc-details">
        <div class="rate-card-grid">
          <div class="rate-card">
            <div class="rate-icon">{ICONS['pprc_new']}</div>
            <h4>New Project (Piping Only)</h4>
            <div class="rate-price">Rs. 12,000 – 15,000</div>
            <p>Lump sum rate for complete PPRC piping only</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['pprc_bath']}</div>
            <h4>Bathroom Accessories Installation</h4>
            <div class="rate-price">Rs. 5,000 / bathroom</div>
            <p>Complete accessories installation per bathroom</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['pprc_tank']}</div>
            <h4>Water Tank</h4>
            <div class="rate-price">Rs. 2,500 / tank</div>
            <p>Water tank installation charge</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['pprc_motor']}</div>
            <h4>Motor Installation</h4>
            <div class="rate-price">Rs. 2,000 / motor</div>
            <p>Water motor fitting and installation</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['pprc_instant_geyser']}</div>
            <h4>Instant Geyser</h4>
            <div class="rate-price">Rs. 1,500 / unit</div>
            <p>Instant geyser installation</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['pprc_standing_geyser']}</div>
            <h4>Standing Geyser</h4>
            <div class="rate-price">Rs. 4,000 / unit</div>
            <p>Standing geyser installation</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['pprc_pump']}</div>
            <h4>Auto Pressure Pump</h4>
            <div class="rate-price">Rs. 5,000</div>
            <p>Auto pressure pump fitting</p>
          </div>
          <div class="rate-card note-card">
            <div class="rate-icon">{ICONS['repair']}</div>
            <h4>Repairing</h4>
            <div class="rate-price">On-Spot Rate</div>
            <p>Repair rates discussed on-site after inspection</p>
          </div>
        </div>

        <h3 class="sub-gallery-title">PPRC Piping Work</h3>
        <div class="sub-gallery-grid">
{pprc_gallery}
        </div>
        <h3 class="sub-gallery-title">Sanitary Work</h3>
        <div class="sub-gallery-grid">
{sanitary_gallery}
        </div>
      </div>

      <!-- PVC TAB -->
      <div class="tab-content" id="pvc-details">
        <div class="rate-card-grid">
          <div class="rate-card">
            <div class="rate-icon">{ICONS['pvc_no_dig']}</div>
            <h4>Piping (Without Excavation)</h4>
            <div class="rate-price">Rs. 90 / feet</div>
            <p>Surface-level PVC piping without digging</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['pvc_dig']}</div>
            <h4>Piping (With Excavation)</h4>
            <div class="rate-price">Rs. 130 / feet</div>
            <p>Underground PVC piping with full excavation & concrete pouring</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['pvc_mainhole']}</div>
            <h4>Mainhole Construction</h4>
            <div class="rate-price">Rs. 1,500</div>
            <p>Mainhole installation per unit</p>
          </div>
          <div class="rate-card note-card">
            <div class="rate-icon">{ICONS['repair']}</div>
            <h4>Repairing</h4>
            <div class="rate-price">On-Spot Rate</div>
            <p>Repair rates discussed on-site after inspection</p>
          </div>
        </div>

        <h3 class="sub-gallery-title">PVC Piping Work</h3>
        <div class="sub-gallery-grid">
{pvc_gallery}
        </div>
        <h3 class="sub-gallery-title">Mainhole Work</h3>
        <div class="sub-gallery-grid">
{mainhole_gallery}
        </div>
      </div>

      <!-- GI TAB -->
      <div class="tab-content" id="gi-details">
        <div class="rate-card-grid">
          <div class="rate-card">
            <div class="rate-icon">{ICONS['gi_feet']}</div>
            <h4>GI Fitting (Per Feet)</h4>
            <div class="rate-price">Rs. 45 / feet</div>
            <p>Per-feet rate for GI pipe fitting</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['gi_lump']}</div>
            <h4>GI Fitting (Lump Sum)</h4>
            <div class="rate-price">Lump Sum</div>
            <p>Negotiable lump-sum rate for large GI projects</p>
          </div>
          <div class="rate-card note-card">
            <div class="rate-icon">{ICONS['repair']}</div>
            <h4>Repairing</h4>
            <div class="rate-price">On-Spot Rate</div>
            <p>Repair rates discussed on-site after inspection</p>
          </div>
        </div>

        <h3 class="sub-gallery-title">GI Fitting Work</h3>
        <div class="sub-gallery-grid">
{gi_gallery}
        </div>
      </div>

      <!-- ELECTRICAL TAB -->
      <div class="tab-content" id="electrical-details">
        <div class="rate-card-grid">
          <div class="rate-card">
            <div class="rate-icon">{ICONS['elec_piping']}</div>
            <h4>Piping (Per Room)</h4>
            <div class="rate-price">Rs. 2,000 / room</div>
            <p>Electrical conduit piping per room</p>
          </div>
          <div class="rate-card featured-card">
            <div class="rate-icon">{ICONS['elec_point']}</div>
            <h4>Per Point (Full Package)</h4>
            <div class="rate-price">Rs. 350 / point</div>
            <p>Includes piping, wiring & sheet/light/fan installation</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['elec_wiring']}</div>
            <h4>Wiring (Per Room / Lump Sum)</h4>
            <div class="rate-price">Same as piping rate</div>
            <p>Per room, per point, or lump sum — same rate structure as piping</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['elec_dp_normal']}</div>
            <h4>DP Dressing (Normal)</h4>
            <div class="rate-price">Rs. 3,000</div>
            <p>8–10 breaker distribution panel dressing</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['elec_dp_heavy']}</div>
            <h4>DP Dressing (Heavy)</h4>
            <div class="rate-price">Rs. 5,000</div>
            <p>Up to 10+ breaker heavy distribution panel</p>
          </div>
          <div class="rate-card note-card">
            <div class="rate-icon">{ICONS['elec_fanos']}</div>
            <h4>Fanos (Exhaust Fan)</h4>
            <div class="rate-price">Extra Charge</div>
            <p>Fanos/exhaust fan charges not included in any package — charged separately</p>
          </div>
          <div class="rate-card note-card">
            <div class="rate-icon">{ICONS['repair']}</div>
            <h4>Repairing</h4>
            <div class="rate-price">On-Spot Rate</div>
            <p>Repair rates discussed on-site after inspection</p>
          </div>
        </div>

        <h3 class="sub-gallery-title">DP Dressing</h3>
        <div class="sub-gallery-grid">
{dp_gallery}
        </div>
        <h3 class="sub-gallery-title">Electrical Piping</h3>
        <div class="sub-gallery-grid">
{elec_piping_gallery}
        </div>
        <h3 class="sub-gallery-title">Profile Lighting & Stair Sensor Lighting</h3>
        <div class="sub-gallery-grid">
{lighting_combined}
        </div>
      </div>

      <!-- SOLAR TAB -->
      <div class="tab-content" id="solar-details">
        <div class="rate-card-grid">
          <div class="rate-card featured-card">
            <div class="rate-icon">{ICONS['solar_install']}</div>
            <h4>Solar Installation</h4>
            <div class="rate-price">Rs. 4 / watt</div>
            <p>Professional solar panel installation charges per watt</p>
          </div>
          <div class="rate-card">
            <div class="rate-icon">{ICONS['solar_idea']}</div>
            <h4>Solar Ideas / Consultation</h4>
            <div class="rate-price">FREE</div>
            <p>Get expert solar system advice and layout ideas at no cost</p>
          </div>
          <div class="rate-card note-card">
            <div class="rate-icon">{ICONS['solar_repair']}</div>
            <h4>Solar Repairing</h4>
            <div class="rate-price">On-Spot Rate</div>
            <p>Repair rates discussed on-site after inspection</p>
          </div>
        </div>
      </div>

      <!-- Important Notes -->
      <div class="catalogue-notes">
        <h3>📝 Important Notes</h3>
        <ul>
          <li>💡 <strong>Ideas are free of cost</strong> — get expert advice without any charge.</li>
          <li>🔧 Repairing and extra job rates are discussed on-the-spot after inspection.</li>
          <li>🪛 Grinder discs and heavy-duty tools (e.g., jackhammer) to be provided by the owner.</li>
          <li>🪟 Fanos/exhaust fan charges are not included in any package (per point, lump sum, or per room).</li>
          <li>💬 Call or WhatsApp for custom quotes on large projects.</li>
        </ul>
      </div>
    </div>
  </section>"""

# Read current index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace Catalogue block accurately
cat_start = html.find("<!-- ===== CATALOGUE ===== -->")
gal_start = html.find("<!-- ===== GALLERY ===== -->")

if cat_start != -1 and gal_start != -1:
    new_html = html[:cat_start] + catalogue_html + "\n\n  " + html[gal_start:]
else:
    print("ERROR: Catalogue or Gallery comment marker not found!")
    exit(1)

# Fix Gallery Section in new_html to use existing real images
old_gallery_block = re.search(r'<div class="gallery-grid">.*?</div>\s*<div class="gallery-tags">', new_html, re.DOTALL)
if old_gallery_block:
    new_gallery_grid = """<div class="gallery-grid">
        <div class="gallery-item large" data-label="PPRC Piping">
          <img src="Plumber%20works/PPr%20Piping/20260624_090853.webp" alt="PPRC Piping and Plumbing Services" loading="lazy" />
          <div class="gallery-overlay"><span>PPRC Piping &amp; Services</span></div>
        </div>
        <div class="gallery-item" data-label="Electrical DP Fitting">
          <img src="WhatsApp%20Image%202026-08-08%20at%2010.10.43%20PM.jpeg" alt="Electrical DP Panel Fitting" loading="lazy" />
          <div class="gallery-overlay"><span>Electrical DP Fitting</span></div>
        </div>
        <div class="gallery-item" data-label="Sanitary Installation">
          <img src="Plumber%20works/Sanitory/20260702_112818.webp" alt="Sanitary Fixtures and Plumbing" loading="lazy" />
          <div class="gallery-overlay"><span>Sanitary &amp; Bathroom Fitting</span></div>
        </div>
        <div class="gallery-item" data-label="PVC Underground">
          <img src="Plumber%20works/Pvc%20Piping/20251215_114143.webp" alt="PVC Underground Drainage" loading="lazy" />
          <div class="gallery-overlay"><span>PVC Drainage Work</span></div>
        </div>
        <div class="gallery-item profile-card-item" data-label="Khurram Shahzad">
          <img src="WhatsApp%20Image%202026-08-08%20at%2010.10.42%20PM%20%281%29.jpeg" alt="Khurram Shahzad - Lead Expert" loading="lazy" />
          <div class="gallery-overlay"><span>Khurram Shahzad — Lead Expert</span></div>
        </div>
        <div class="gallery-item profile-card-item" data-label="Muneeb Ahmed">
          <img src="muneeb.jpg" alt="Muneeb Ahmed - Electrical & Plumbing Specialist" loading="lazy" />
          <div class="gallery-overlay"><span>Muneeb Ahmed — Specialist</span></div>
        </div>
      </div>
      <div class="gallery-tags">"""
    new_html = new_html.replace(old_gallery_block.group(0), new_gallery_grid)

# Ensure script and style references
new_html = new_html.replace('href="style.min.css"', 'href="style.css"')
new_html = new_html.replace('src="script.min.js"', 'src="script.js"')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("SUCCESS: index.html has been completely rebuilt with all verified images and icons!")

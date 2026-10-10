import os
import yaml

def assemble():
    with open("data/site_config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    # 1. 识别选择的底盘车型，调取对应模具
    template_id = config.get("template_id", "chassis_bento")
    template_path = f"templates/{template_id}.html"
    
    if not os.path.exists(template_path):
        print(f"⚠️ 未找到 {template_path}，使用默认 Bento 模具。")
        template_path = "templates/chassis_bento.html"

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # 2. 组装业务卡片 (根据模具自适应排版)
    cards_html = []
    for item in config.get("services", []):
        if template_id == "chassis_linkr":
            # Linkr 样式的长条胶囊按钮
            card = f"""
            <a href="{item.get('link', '#')}" target="_blank" class="block w-full p-4 rounded-2xl bg-white/10 hover:bg-white/20 border border-white/10 backdrop-blur-md transition duration-200 transform hover:-translate-y-0.5 text-center font-bold text-sm tracking-wide">
                <i class="fa-solid {item['icon']} mr-2 text-purple-400"></i> {item['title']}
            </a>
            """
        else:
            # Bento/通用 样式的便当格子卡片
            card = f"""
            <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800/80 hover:border-purple-500/40 transition duration-300">
                <div class="w-10 h-10 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center text-lg mb-4">
                    <i class="fa-solid {item['icon']}"></i>
                </div>
                <h4 class="text-base font-bold text-white mb-1.5">{item['title']}</h4>
                <p class="text-xs text-slate-400 leading-relaxed">{item['desc']}</p>
            </div>
            """
        cards_html.append(card)
    services_html = "\n".join(cards_html)

    # 3. 组装选装配件 (收银按钮)
    payment_html = ""
    if config.get("addons", {}).get("payment_button"):
        pay_conf = config.get("payment", {})
        payment_html = f"""
        <a href="{pay_conf.get('link', '#')}" target="_blank" class="px-6 py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-sm shadow-lg shadow-purple-600/30 transition">
            {pay_conf.get('button_text', '立即支持')}
        </a>
        """

    # 4. 组装选装配件 (联系方式)
    contact_badges = []
    c = config.get("contact", {})
    if c.get("telegram"):
        contact_badges.append(f'<a href="https://t.me/{c["telegram"].replace("@","")}" target="_blank" class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold inline-flex items-center gap-1.5 transition"><i class="fa-brands fa-telegram text-blue-400"></i> {c["telegram"]}</a>')
    if c.get("email"):
        contact_badges.append(f'<span class="px-4 py-2.5 rounded-xl bg-slate-800 text-slate-300 text-xs font-semibold inline-flex items-center gap-1.5"><i class="fa-solid fa-envelope text-purple-400"></i> {c["email"]}</span>')
    contact_html = "\n".join(contact_badges)

    # 5. 组装选装配件 (多语言提示标)
    lang_bar_html = ""
    if config.get("addons", {}).get("i18n"):
        lang_bar_html = '<span class="text-xs text-slate-400 bg-slate-800 px-3 py-1.5 rounded-full inline-flex items-center gap-1.5 border border-slate-700"><i class="fa-solid fa-globe text-purple-400"></i> 6-Langs Ready</span>'

    # 6. 数据精准塞入插槽
    brand = config.get("brand_name", "My Brand")
    rendered = template \
        .replace("{{BRAND_NAME}}", brand) \
        .replace("{{AVATAR_INITIAL}}", brand[0].upper() if brand else "M") \
        .replace("{{TAGLINE}}", config.get("tagline", "")) \
        .replace("{{HERO_TITLE}}", config.get("hero_title", brand)) \
        .replace("{{HERO_DESC}}", config.get("hero_desc", "")) \
        .replace("{{SERVICES_CARDS_HTML}}", services_html) \
        .replace("{{PAYMENT_BUTTON_HTML}}", payment_html) \
        .replace("{{CONTACT_BADGES_HTML}}", contact_html) \
        .replace("{{LANG_BAR_HTML}}", lang_bar_html)

    with open("index.html", "w", encoding="utf-8") as out:
        out.write(rendered)
    print(f"✅ 成功调取模具 [{template_id}]，流水线装配完成！")

if __name__ == "__main__":
    assemble()

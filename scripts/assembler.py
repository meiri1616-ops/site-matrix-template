import os
import yaml

def assemble():
    with open("data/site_config.yml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    with open("templates/index.html", "r", encoding="utf-8") as f:
        template = f.read()

    # 1. 组装服务卡片 HTML
    cards_html = []
    for item in config.get("services", []):
        card = f"""
        <div class="p-8 rounded-2xl bg-slate-50 border border-slate-200/80 hover:border-blue-500/50 hover:shadow-xl hover:shadow-blue-500/5 transition duration-300">
            <div class="w-12 h-12 rounded-xl bg-blue-100 text-blue-600 flex items-center justify-center text-xl mb-6">
                <i class="fa-solid {item['icon']}"></i>
            </div>
            <h3 class="text-lg font-bold text-slate-900 mb-2">{item['title']}</h3>
            <p class="text-sm text-slate-600 leading-relaxed">{item['desc']}</p>
        </div>
        """
        cards_html.append(card)
    services_html = "\n".join(cards_html)

    # 2. 组装选配功能 (在线支付按钮)
    payment_html = ""
    if config.get("addons", {}).get("payment_button"):
        pay_conf = config.get("payment", {})
        payment_html = f"""
        <a href="{pay_conf.get('link', '#')}" target="_blank" class="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-slate-900 text-white font-bold text-base hover:bg-slate-800 transition">
            {pay_conf.get('button_text', '立即购买')}
        </a>
        """

    # 3. 组装选配功能 (联系方式徽标)
    contact_badges = []
    c = config.get("contact", {})
    if c.get("email"):
        contact_badges.append(f'<span class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 border border-slate-700 text-slate-200"><i class="fa-solid fa-envelope text-blue-400"></i> {c["email"]}</span>')
    if c.get("telegram"):
        contact_badges.append(f'<a href="https://t.me/{c["telegram"].replace("@","")}" target="_blank" class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600/30 border border-blue-500/40 text-blue-300 hover:bg-blue-600/50 transition"><i class="fa-brands fa-telegram text-blue-400"></i> {c["telegram"]}</a>')
    if c.get("phone"):
        contact_badges.append(f'<span class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 border border-slate-700 text-slate-200"><i class="fa-solid fa-phone text-green-400"></i> {c["phone"]}</span>')
    contact_html = "\n".join(contact_badges)

    # 4. 组装多语言栏
    lang_bar_html = ""
    if config.get("addons", {}).get("i18n"):
        lang_bar_html = """
        <div class="text-xs font-medium text-slate-500 bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200 flex items-center gap-1.5">
            <i class="fa-solid fa-language text-slate-400"></i>
            <span>多语言就绪 (Multi-Lang)</span>
        </div>
        """

    # 5. 插槽整体替换
    rendered = template \
        .replace("{{BRAND_NAME}}", config.get("brand_name", "")) \
        .replace("{{TAGLINE}}", config.get("tagline", "")) \
        .replace("{{HERO_TITLE}}", config.get("hero_title", "")) \
        .replace("{{HERO_DESC}}", config.get("hero_desc", "")) \
        .replace("{{CTA_PRIMARY}}", config.get("cta_primary", "立即咨询")) \
        .replace("{{SERVICES_CARDS_HTML}}", services_html) \
        .replace("{{PAYMENT_BUTTON_HTML}}", payment_html) \
        .replace("{{CONTACT_BADGES_HTML}}", contact_html) \
        .replace("{{LANG_BAR_HTML}}", lang_bar_html)

    # 输出到根目录供 GitHub Pages 直接展示
    with open("index.html", "w", encoding="utf-8") as out:
        out.write(rendered)
    print("✅ 网页装配完成！零幻觉生成完毕。")

if __name__ == "__main__":
    assemble()

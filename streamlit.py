"""
فایل راه‌انداز اپلیکیشن «گرماچین آفلاین» روی سرویس Streamlit Community Cloud
آدرس انتشار: https://share.streamlit.io/

نحوه استفاده:
این فایل (app.py) را به همراه فایل HTML برنامه (مثلاً index.html یا garmachin_offline.html)
در یک مخزن (Repository) گیت‌هاب قرار دهید و در سایت share.streamlit.io منتشر کنید.
"""

from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components


def find_html_file(base_dir: Path) -> Path | None:
    """
    جستجوی خودکار فایل HTML اپلیکیشن در پوشه پروژه.
    ابتدا نام‌های رایج را بررسی می‌کند و در صورت نبود، اولین فایل .html موجود را برمی‌گرداند.
    """
    preferred_names = [
        "index.html",
        "garmachin_offline.html",
        "api_tensorflow_js.html",
    ]
    for filename in preferred_names:
        candidate = base_dir / filename
        if candidate.is_file():
            return candidate

    # جستجوی هر فایل HTML دیگر در پوشه پروژه (برای جلوگیری از خطای تغییر نام)
    html_files = sorted(base_dir.glob("*.html"))
    return html_files[0] if html_files else None


def configure_fullscreen_layout() -> None:
    """
    حذف حاشیه‌ها، نوار بالا و فوتر پیش‌فرض Streamlit برای نمایش تمام‌صفحه اپلیکیشن.
    """
    st.set_page_config(
        page_title="گرماچین آفلاین | تحلیل گرمایش ساختمان",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(
        """
        <style>
            /* مخفی کردن منو و فوتر پیش‌فرض استریم‌لیت */
            #MainMenu { visibility: hidden; }
            header[data-testid="stHeader"] { display: none; }
            footer { visibility: hidden; }

            /* حذف فاصله‌های اضافی اطراف صفحه */
            .block-container {
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
            }
            [data-testid="stAppViewContainer"] {
                background-color: #060e14;
                overflow: hidden;
            }
            /* تمام‌صفحه کردن قاب نمایش HTML */
            iframe[title="streamlit_components_v1.html_v1"],
            iframe {
                width: 100% !important;
                height: 100vh !important;
                min-height: 100vh !important;
                border: none !important;
                display: block !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """
    نقطه ورود اصلی برنامه Streamlit.
    فایل HTML را می‌خواند و در قالب کامپوننت تمام‌صفحه رندر می‌کند.
    """
    configure_fullscreen_layout()

    base_dir = Path(__file__).resolve().parent
    html_path = find_html_file(base_dir)

    if html_path is None:
        st.error(
            "⚠️ فایل HTML اپلیکیشن پیدا نشد! لطفاً فایل `index.html` "
            "(یا فایل دانلودشده `api_tensorflow_js.html`) را کنار `app.py` در گیت‌هاب آپلود کنید."
        )
        return

    try:
        html_content = html_path.read_text(encoding="utf-8")
        # نمایش اپلیکیشن با قابلیت اسکرول داخلی
        components.html(html_content, height=1000, scrolling=True)
    except Exception as exc:
        st.error(f"خطا در خواندن یا اجرای فایل HTML: {exc}")


if __name__ == "__main__":
    main()
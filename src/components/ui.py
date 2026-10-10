import streamlit as st
from typing import Optional, Dict, Any


def load_custom_css():
    """
    Inject high-end corporate BI stylesheet with custom fonts, glassmorphic metric cards,
    and responsive layout styles.
    """
    st.markdown("""
        <style>
        /* Modern Font Imports */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        /* Top Header Container */
        .bi-header {
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            color: #FFFFFF;
            padding: 24px 32px;
            border-radius: 14px;
            margin-bottom: 24px;
            box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15), 0 8px 10px -6px rgba(15, 23, 42, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .bi-header-title {
            font-size: 26px;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin: 0;
            color: #F8FAFC;
        }

        .bi-header-subtitle {
            font-size: 13px;
            font-weight: 400;
            color: #94A3B8;
            margin-top: 4px;
        }

        .bi-badge {
            background: rgba(37, 99, 235, 0.2);
            border: 1px solid rgba(59, 130, 246, 0.4);
            color: #60A5FA;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Executive KPI Card */
        .kpi-card {
            background: #FFFFFF;
            border-radius: 12px;
            padding: 18px 20px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -2px rgba(0, 0, 0, 0.02);
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 12px;
            position: relative;
            overflow: hidden;
        }

        .kpi-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04);
            border-color: #CBD5E1;
        }

        .kpi-accent-primary { border-top: 4px solid #2563EB; }
        .kpi-accent-success { border-top: 4px solid #10B981; }
        .kpi-accent-warning { border-top: 4px solid #F59E0B; }
        .kpi-accent-danger  { border-top: 4px solid #EF4444; }
        .kpi-accent-purple  { border-top: 4px solid #8B5CF6; }
        .kpi-accent-cyan    { border-top: 4px solid #06B6D4; }

        .kpi-title {
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            color: #64748B;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .kpi-value {
            font-size: 26px;
            font-weight: 800;
            color: #0F172A;
            line-height: 1.1;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }

        .kpi-delta-container {
            display: flex;
            align-items: center;
            font-size: 12px;
            font-weight: 600;
            gap: 6px;
        }

        .delta-positive {
            color: #059669;
            background: #ECFDF5;
            padding: 2px 6px;
            border-radius: 6px;
        }

        .delta-negative {
            color: #DC2626;
            background: #FEF2F2;
            padding: 2px 6px;
            border-radius: 6px;
        }

        .delta-neutral {
            color: #64748B;
            background: #F1F5F9;
            padding: 2px 6px;
            border-radius: 6px;
        }

        .delta-context {
            color: #94A3B8;
            font-size: 11px;
            font-weight: 400;
        }

        /* Section Header */
        .section-header-box {
            margin-top: 24px;
            margin-bottom: 16px;
            display: flex;
            align-items: baseline;
            gap: 12px;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 8px;
        }

        .section-header-title {
            font-size: 18px;
            font-weight: 700;
            color: #1E293B;
            margin: 0;
        }

        .section-header-sub {
            font-size: 13px;
            color: #64748B;
            margin: 0;
        }

        /* Insight / Alert Box */
        .insight-box {
            border-radius: 10px;
            padding: 14px 18px;
            margin-top: 14px;
            margin-bottom: 14px;
            display: flex;
            gap: 12px;
            align-items: flex-start;
            font-size: 13.5px;
            line-height: 1.5;
        }

        .insight-info {
            background-color: #EFF6FF;
            border: 1px solid #BFDBFE;
            color: #1E40AF;
        }

        .insight-warning {
            background-color: #FFFBEB;
            border: 1px solid #FDE68A;
            color: #92400E;
        }

        .insight-success {
            background-color: #ECFDF5;
            border: 1px solid #A7F3D0;
            color: #065F46;
        }

        /* Active Filter Pills Bar */
        .filter-bar {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 10px 16px;
            margin-bottom: 18px;
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
            font-size: 12px;
            color: #475569;
        }

        .filter-pill {
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 500;
            color: #334155;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #F8FAFC !important;
            border-right: 1px solid #E2E8F0;
        }
        </style>
    """, unsafe_allow_html=True)


def render_dashboard_header(total_records: int, date_range_str: str):
    """
    Render executive dashboard top banner.
    """
    st.markdown(f"""
        <div class="bi-header">
            <div>
                <div class="bi-header-title">Executive Superstore Business Intelligence</div>
                <div class="bi-header-subtitle">Performance Analytics • Profitability Diagnostics • Customer RFM & Supply Chain</div>
            </div>
            <div style="text-align: right;">
                <span class="bi-badge">Active Portfolio</span>
                <div style="font-size: 12px; color: #CBD5E1; margin-top: 6px;">📅 {date_range_str}</div>
                <div style="font-size: 11px; color: #94A3B8;">{total_records:,} Transactions Loaded</div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def format_currency(val: float) -> str:
    """Format large currency numbers with K / M suffixes."""
    if abs(val) >= 1_000_000:
        return f"${val / 1_000_000:.2f}M"
    elif abs(val) >= 1_000:
        return f"${val / 1_000:.1f}K"
    else:
        return f"${val:,.2f}"


def format_number(val: float) -> str:
    """Format large counts with K / M suffixes."""
    if abs(val) >= 1_000_000:
        return f"{val / 1_000_000:.2f}M"
    elif abs(val) >= 1_000:
        return f"{val / 1_000:.1f}K"
    else:
        return f"{val:,}"


def render_kpi_card(
    title: str,
    value_str: str,
    delta: Optional[float] = None,
    delta_type: str = "pct",
    is_positive_good: bool = True,
    context: str = "vs Prior Period",
    accent_class: str = "kpi-accent-primary"
):
    """
    Render an executive KPI card with formatted value and delta badge.
    """
    delta_html = ""
    if delta is not None:
        if delta_type == "pts":
            delta_formatted = f"{delta:+.1f} pts"
        else:
            delta_formatted = f"{delta:+.1f}%"

        if abs(delta) < 0.05:
            badge_class = "delta-neutral"
            symbol = "●"
        elif (delta > 0 and is_positive_good) or (delta < 0 and not is_positive_good):
            badge_class = "delta-positive"
            symbol = "▲" if delta > 0 else "▼"
        else:
            badge_class = "delta-negative"
            symbol = "▲" if delta > 0 else "▼"

        delta_html = f"""
            <div class="kpi-delta-container">
                <span class="{badge_class}">{symbol} {delta_formatted}</span>
                <span class="delta-context">{context}</span>
            </div>
        """
    else:
        delta_html = f"""
            <div class="kpi-delta-container">
                <span class="delta-neutral">Live</span>
                <span class="delta-context">{context}</span>
            </div>
        """

    card_html = f"""
        <div class="kpi-card {accent_class}">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value_str}</div>
            {delta_html}
        </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: Optional[str] = None):
    """
    Render clean section header with title and subtitle.
    """
    sub_html = f'<p class="section-header-sub">{subtitle}</p>' if subtitle else ""
    st.markdown(f"""
        <div class="section-header-box">
            <h3 class="section-header-title">{title}</h3>
            {sub_html}
        </div>
    """, unsafe_allow_html=True)


def render_insight_box(text: str, alert_type: str = "info", title: str = "Executive Takeaway"):
    """
    Render executive insight callout block.
    """
    icon_map = {
        "info": "💡",
        "warning": "⚠️",
        "success": "✅"
    }
    icon = icon_map.get(alert_type, "💡")
    css_class = f"insight-{alert_type}"
    st.markdown(f"""
        <div class="insight-box {css_class}">
            <div style="font-size: 18px;">{icon}</div>
            <div>
                <strong>{title}:</strong> {text}
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_filter_summary(filters: Dict[str, Any]):
    """
    Render horizontal pill bar showing current filter state.
    """
    pills = []
    if "date_range" in filters and filters["date_range"]:
        pills.append(f'<span class="filter-pill">📅 {filters["date_range"]}</span>')
    if "region" in filters and filters["region"]:
        pills.append(f'<span class="filter-pill">🌎 Regions: {len(filters["region"])}</span>')
    if "category" in filters and filters["category"]:
        pills.append(f'<span class="filter-pill">🏷️ Categories: {len(filters["category"])}</span>')
    if "segment" in filters and filters["segment"]:
        pills.append(f'<span class="filter-pill">👥 Segments: {len(filters["segment"])}</span>')
    if "ship_mode" in filters and filters["ship_mode"]:
        pills.append(f'<span class="filter-pill">🚚 Ship Modes: {len(filters["ship_mode"])}</span>')

    if pills:
        pills_html = " ".join(pills)
        st.markdown(f"""
            <div class="filter-bar">
                <strong>Active Filters:</strong> {pills_html}
            </div>
        """, unsafe_allow_html=True)

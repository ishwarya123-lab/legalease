import io
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server-side rendering
import matplotlib.pyplot as plt
import re


def parse_currency(value: str) -> float:
    """Extract numeric value from currency strings like '$2,000', '120000', etc."""
    cleaned = re.sub(r'[^\d.]', '', value)
    return float(cleaned) if cleaned else 0.0


def parse_duration_months(duration: str) -> int:
    """Parse duration strings like '12 Months', '3 Years', '24 months' into months."""
    duration_lower = duration.lower().strip()
    match = re.search(r'(\d+)', duration_lower)
    if not match:
        return 12  # default
    num = int(match.group(1))
    if 'year' in duration_lower:
        return num * 12
    return num


def generate_lease_analytics(data: dict) -> tuple[dict, io.BytesIO]:
    """Generate lease financial analytics using NumPy and a Matplotlib chart."""
    rent = parse_currency(data.get('rent', '0'))
    deposit = parse_currency(data.get('security_deposit', '0'))
    duration_months = parse_duration_months(data.get('lease_duration', '12 Months'))

    # NumPy calculations
    months = np.arange(1, duration_months + 1)
    monthly_payments = np.full(duration_months, rent)
    cumulative_payments = np.cumsum(monthly_payments)
    total_rent = float(np.sum(monthly_payments))
    total_cost = total_rent + deposit
    average_monthly_cost = total_cost / duration_months if duration_months > 0 else 0

    metrics = {
        "monthly_rent": rent,
        "security_deposit": deposit,
        "lease_duration_months": duration_months,
        "total_rent_payable": round(total_rent, 2),
        "total_cost_including_deposit": round(total_cost, 2),
        "average_monthly_cost": round(average_monthly_cost, 2),
    }

    # Matplotlib chart: Cumulative Rent Over Lease Term
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.fill_between(months, cumulative_payments, alpha=0.3, color='#2563eb')
    ax.plot(months, cumulative_payments, color='#2563eb', linewidth=2, label='Cumulative Rent')
    ax.axhline(y=total_cost, color='#dc2626', linestyle='--', linewidth=1.5, label=f'Total Cost (incl. deposit): ₹{total_cost:,.0f}')
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Amount (₹)', fontsize=11)
    ax.set_title('Lease: Cumulative Payment Schedule', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return metrics, buf


def generate_employment_analytics(data: dict) -> tuple[dict, io.BytesIO]:
    """Generate employment compensation analytics using NumPy and a Matplotlib chart."""
    annual_comp = parse_currency(data.get('compensation', '0'))

    # NumPy calculations
    months = np.arange(1, 13)
    monthly_salary = annual_comp / 12
    monthly_salaries = np.full(12, monthly_salary)
    cumulative_earnings = np.cumsum(monthly_salaries)

    # Simulated breakdown (taxes, benefits, take-home)
    tax_rate = 0.22
    benefits_rate = 0.08
    gross_monthly = monthly_salary
    taxes = gross_monthly * tax_rate
    benefits = gross_monthly * benefits_rate
    take_home = gross_monthly - taxes - benefits

    metrics = {
        "annual_compensation": round(annual_comp, 2),
        "monthly_gross": round(gross_monthly, 2),
        "estimated_monthly_tax": round(taxes, 2),
        "estimated_monthly_benefits": round(benefits, 2),
        "estimated_monthly_take_home": round(take_home, 2),
        "estimated_annual_take_home": round(take_home * 12, 2),
    }

    # Matplotlib chart: Compensation Breakdown
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # Bar chart - monthly breakdown
    categories = ['Gross', 'Tax', 'Benefits', 'Take-Home']
    values = [gross_monthly, taxes, benefits, take_home]
    colors = ['#2563eb', '#dc2626', '#f59e0b', '#16a34a']
    ax1.bar(categories, values, color=colors, edgecolor='white', linewidth=0.5)
    ax1.set_ylabel('Amount (₹)', fontsize=10)
    ax1.set_title('Monthly Compensation Breakdown', fontsize=11, fontweight='bold')
    for i, v in enumerate(values):
        ax1.text(i, v + max(values) * 0.02, f'₹{v:,.0f}', ha='center', fontsize=8, fontweight='bold')

    # Line chart - cumulative earnings
    ax2.fill_between(months, cumulative_earnings, alpha=0.3, color='#16a34a')
    ax2.plot(months, cumulative_earnings, color='#16a34a', linewidth=2)
    ax2.set_xlabel('Month', fontsize=10)
    ax2.set_ylabel('Cumulative (₹)', fontsize=10)
    ax2.set_title('Cumulative Annual Earnings', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return metrics, buf


def generate_nda_analytics(data: dict) -> tuple[dict, io.BytesIO]:
    """Generate NDA term analytics using NumPy and a Matplotlib chart."""
    period = parse_duration_months(data.get('confidentiality_period', '3 Years'))

    # NumPy - risk decay model over confidentiality period
    months = np.arange(1, period + 1)
    # Simulated confidentiality risk score (decays over time)
    risk_score = 100 * np.exp(-0.03 * months)
    enforcement_strength = 100 - risk_score

    metrics = {
        "confidentiality_period_months": period,
        "initial_risk_score": 100.0,
        "final_risk_score": round(float(risk_score[-1]), 2),
        "average_risk_score": round(float(np.mean(risk_score)), 2),
    }

    # Matplotlib chart
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(months, risk_score, color='#dc2626', linewidth=2, label='Confidentiality Risk')
    ax.plot(months, enforcement_strength, color='#16a34a', linewidth=2, label='Enforcement Strength')
    ax.fill_between(months, risk_score, alpha=0.15, color='#dc2626')
    ax.fill_between(months, enforcement_strength, alpha=0.15, color='#16a34a')
    ax.set_xlabel('Month', fontsize=11)
    ax.set_ylabel('Score (%)', fontsize=11)
    ax.set_title('NDA: Confidentiality Risk vs Enforcement Over Time', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    buf.seek(0)
    return metrics, buf


def get_analytics(document_type: str, data: dict) -> tuple[dict, io.BytesIO]:
    """Route to the correct analytics generator based on document type."""
    if document_type == "Lease":
        return generate_lease_analytics(data)
    elif document_type == "Employment":
        return generate_employment_analytics(data)
    elif document_type == "NDA":
        return generate_nda_analytics(data)
    else:
        raise ValueError(f"Unknown document type: {document_type}")

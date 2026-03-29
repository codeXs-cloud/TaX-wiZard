def calculate_taxes(
    basic_salary: float, 
    hra_received: float = 0.0, 
    rent_paid: float = 0.0, 
    is_metro: bool = False,
    other_allowances: float = 0.0,
    investment_80c: float = 0.0, 
    health_insurance_80d: float = 0.0,
    nps_80ccd1b: float = 0.0
) -> dict:
    """Calculates tax liability including HRA exemptions and NPS."""
    gross_salary = basic_salary + hra_received + other_allowances
    standard_deduction = 50000
    
    # --- 1. HRA Exemption Logic ---
    hra_exemption = 0
    if rent_paid > 0 and hra_received > 0:
        rent_minus_10_percent_basic = max(0, rent_paid - (0.10 * basic_salary))
        percentage_of_basic = (0.50 * basic_salary) if is_metro else (0.40 * basic_salary)
        # HRA Exemption is the minimum of the three conditions
        hra_exemption = min(hra_received, rent_minus_10_percent_basic, percentage_of_basic)

    # --- 2. OLD REGIME CALCULATION ---
    capped_80c = min(investment_80c, 150000)
    capped_80d = min(health_insurance_80d, 25000)
    capped_nps = min(nps_80ccd1b, 50000) # Feature 2: The extra 50k NPS deduction
    
    total_deductions_old = standard_deduction + hra_exemption + capped_80c + capped_80d + capped_nps
    taxable_income_old = max(0, gross_salary - total_deductions_old)
    
    tax_old = 0
    if taxable_income_old > 250000: tax_old += min(taxable_income_old - 250000, 250000) * 0.05
    if taxable_income_old > 500000: tax_old += min(taxable_income_old - 500000, 500000) * 0.20
    if taxable_income_old > 1000000: tax_old += (taxable_income_old - 1000000) * 0.30
    if taxable_income_old <= 500000: tax_old = 0 # Rebate 87A
    tax_old *= 1.04 # Health & Education Cess

    # --- 3. NEW REGIME CALCULATION ---
    taxable_income_new = max(0, gross_salary - standard_deduction)
    tax_new = 0
    if taxable_income_new > 300000: tax_new += min(taxable_income_new - 300000, 300000) * 0.05
    if taxable_income_new > 600000: tax_new += min(taxable_income_new - 600000, 300000) * 0.10
    if taxable_income_new > 900000: tax_new += min(taxable_income_new - 900000, 300000) * 0.15
    if taxable_income_new > 1200000: tax_new += min(taxable_income_new - 1200000, 300000) * 0.20
    if taxable_income_new > 1500000: tax_new += (taxable_income_new - 1500000) * 0.30
    if taxable_income_new <= 700000: tax_new = 0 # Rebate 87A
    tax_new *= 1.04 # Health & Education Cess

    return {
        "gross_salary": gross_salary,
        "calculated_hra_exemption": round(hra_exemption, 2),
        "tax_old_regime": round(tax_old, 2),
        "tax_new_regime": round(tax_new, 2),
        "recommended_regime": "Old Regime" if tax_old < tax_new else "New Regime",
        "savings": round(abs(tax_old - tax_new), 2)
    }
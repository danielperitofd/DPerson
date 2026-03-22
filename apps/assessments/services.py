from decimal import Decimal, ROUND_HALF_UP


def quantize(value, places="0.01"):
    return Decimal(value).quantize(Decimal(places), rounding=ROUND_HALF_UP)


def calculate_bmi(weight_kg, height_cm):
    if not weight_kg or not height_cm:
        return Decimal("0")
    meters = Decimal(height_cm) / Decimal("100")
    return quantize(Decimal(weight_kg) / (meters * meters))


def classify_bmi(bmi):
    bmi = Decimal(bmi)
    if bmi < Decimal("18.5"):
        return "Baixo peso"
    if bmi < Decimal("25"):
        return "Adequado"
    if bmi < Decimal("30"):
        return "Sobrepeso"
    if bmi < Decimal("35"):
        return "Obesidade I"
    if bmi < Decimal("40"):
        return "Obesidade II"
    return "Obesidade III"


def calculate_waist_hip_ratio(waist_cm, hip_cm):
    if not waist_cm or not hip_cm:
        return Decimal("0")
    return quantize(Decimal(waist_cm) / Decimal(hip_cm))


def calculate_body_fat_percentage(sex, age, chest, abdomen, thigh, tricep, suprailiac):
    if sex == "male":
        total = Decimal(chest or 0) + Decimal(abdomen or 0) + Decimal(thigh or 0)
        if total <= 0:
            return Decimal("0")
        body_density = Decimal("1.10938") - (Decimal("0.0008267") * total) + (
            Decimal("0.0000016") * total * total
        ) - (Decimal("0.0002574") * Decimal(age or 0))
    else:
        total = Decimal(tricep or 0) + Decimal(suprailiac or 0) + Decimal(thigh or 0)
        if total <= 0:
            return Decimal("0")
        body_density = Decimal("1.0994921") - (Decimal("0.0009929") * total) + (
            Decimal("0.0000023") * total * total
        ) - (Decimal("0.0001392") * Decimal(age or 0))
    if body_density <= 0:
        return Decimal("0")
    return quantize((Decimal("495") / body_density) - Decimal("450"))


def calculate_composition(weight_kg, fat_percentage, target_fat_percentage):
    weight = Decimal(weight_kg or 0)
    fat = Decimal(fat_percentage or 0) / Decimal("100")
    target = Decimal(target_fat_percentage or 0) / Decimal("100") if target_fat_percentage else None
    fat_mass = quantize(weight * fat) if weight else Decimal("0")
    lean_mass = quantize(weight - fat_mass) if weight else Decimal("0")
    ideal_weight = Decimal("0")
    if target is not None and target < 1:
        divisor = Decimal("1") - target
        if divisor > 0:
            ideal_weight = quantize(lean_mass / divisor)
    return fat_mass, lean_mass, ideal_weight

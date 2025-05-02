import random

morning_steps = [
    "1. Cuci muka (biar gak kusam dan keliatan makin cantip)",
    "2. Toner (buat kulit kamu lembab dan balance PH pada kulit, )",
    "3. Serum (buat permasalahan kulit kamu, misal jerawat, pori-pori besar, bukan masalah hati)",
    "4. Moisturizer (biar lembab dan kenyal)",
    "5. SUNSCREEN! (PENTING JANGAN MALES!)"
]

night_steps = [
    "1. First cleanser (angkat dosa dosan dari muka kamu)",
    "2. Second cleanser (biar bersih luar dalam)",
    "3. Toner (jangan skip pokoknya)",
    "4. Essence / Serum (kalau kamu butuh lebih dari sekadar basic)",
    "5. Moisturizer (karena kulit juga butuh lembab)",
    "6. Sleeping mask (boleh biar kulit kamu sehat)"
]

motivations = [
    "Glowing itu perjuangan, bukan warisan.",
    "Kalau skincare aja kamu rajin, percaya deh kamu bakal lebih cantik.",
    "Jangan skip sunscreen. Sinar UV tuh toxic relationship-nya kulit.",
    "Skincare hari ini, glowing besok. Percaya!",
    "Self-care dimulai dari skincare."
]

def show_morning_routine():
    """Display the morning skincare routine."""
    print("🌞 Morning Skincare Routine 🌞")
    for step in morning_steps:
        print(step)

def show_night_routine():
    """Display the night skincare routine."""
    print("🌙 Night Skincare Routine 🌙")
    for step in night_steps:
        print(step)

def skincare_motivation():
    """Return a random skincare motivation."""
    return random.choice(motivations)

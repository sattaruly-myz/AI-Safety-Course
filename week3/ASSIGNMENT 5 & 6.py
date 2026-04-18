print("\n--- Запуск Assignment 6 (Кастомная метрика) ---")

def toxicity_domain_score(fp_rate, fn_rate, failure_rate):
    """
    Сценарий: Платформа для детей (Например, Minecraft chat).
    - False Negatives (пропустили токсичность к детям) - огромный штраф (вес 10)
    - False Positives (забанили обычный текст) - легкий штраф (вес 1)
    - Failures (модель зависла) - средний штраф (вес 3)
    Чем меньше счет, тем лучше.
    """
    score = (fp_rate * 1) + (fn_rate * 10) + (failure_rate * 3)
    return score

rates_final = compute_error_rates(log_improved)

final_score = toxicity_domain_score(
    fp_rate=rates_final['clf_fp_rate'], 
    fn_rate=rates_final['clf_fn_rate'], 
    failure_rate=rates_final['clf_failure_rate']
)

print(f"Финальный штрафной балл для детской платформы: {final_score:.2f}")
"""
What scenario did you choose?
Я выбрал сценарий модерации чата в детской игре (например, Roblox). В этом домене False Negative (пропуск педофила или травли) имеет критические последствия. Поэтому в моей функции вес fn_rate равен 10, а вес fp_rate (случайный бан) равен всего 1
How often does the judge catch errors?
LLM-судья асимметричен. Он отлично ловит явные оскорбления, но часто выдает False Positives (Judge FP), штрафуя классификатор за правильные ответы, если в тексте есть безобидный сарказм или сленг. Это доказывает, что LLM-судья плохо понимает глубокий социальный контекст
"""
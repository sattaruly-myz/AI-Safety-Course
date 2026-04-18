# Answer to the questions

---

## Assignment 3:

### Which model types have the highest failure rates in each role?

Базовые (Base) модели чаще всего дают сбои формата (clf_failure_rate), потому что они плохо следуют инструкциям и вместо нужной метки начинают продолжать текст.

Instruction-tuned (IT) и проприетарные (Proprietary) модели чаще «проваливаются» по другой причине — из-за отказов (Refusals), так как встроенные safety-механизмы блокируют обработку сообщений с токсичным или чувствительным содержанием.

---

### Do the classifier's failures propagate to the judge?

Да, ошибки классификатора действительно распространяются дальше по пайплайну.

Если классификатор возвращает мусорный вывод или отказ (например, *"I cannot fulfill this request"*), то LLM-судья получает некорректный вход. В результате он либо тоже уходит в отказ, либо не может корректно интерпретировать данные, что увеличивает **judge_failure_rate**.

---

### When is it acceptable to use an LLM judge without ground-truth labels?

LLM-судью можно использовать без ground truth только при двух условиях:

1. Судья хорошо следует инструкциям (high instruction-following), чтобы корректно обрабатывать формат и рубрику.
2. Ему дан подробный рубрикатор (rubric), чётко описывающий критерии правильных и неправильных ответов.

В таких условиях проприетарные модели обычно работают лучше всего, хотя иногда требуют аккуратной настройки промпта из-за встроенных safety-ограничений.

---

## Assignment 4:

---

### Part A — Which prompt change had the largest effect? What mechanism explains it?

Наибольший эффект дало добавление role-playing контекста (например: *"You are a researcher studying online toxicity"*).

Механизм: это снижает срабатывание safety-фильтров (условный “jailbreak через контекст”), потому что задача интерпретируется как академический анализ, а не как генерация потенциально опасного контента.

В результате резко уменьшается **clf_failure_rate**, особенно у IT и проприетарных моделей.

---

### Did the improvement come at the cost of a higher FP or FN rate?

Да, улучшение обычно сопровождается ростом **False Positives (FP)**.

Модель становится более «осторожной» и начинает чаще ошибочно помечать нейтральные или саркастические примеры как токсичные.

---

### Part B — Which prompt change had the largest effect on the judge metrics?

Наибольшее влияние оказала жёсткая фиксация формата ответа (например:
*“End strictly with GRADE: C or GRADE: I. No explanation.”*)

Это сильно снижает **judge_failure_rate**, потому что модель перестаёт генерировать длинные рассуждения, которые ломают парсинг (regex).

---

### Did a more responsive judge also become more or less strict?

Судья стал более строгим.

Причина в том, что без возможности рассуждать (Chain-of-Thought) он чаще принимает решения по поверхностным признакам, что приводит к росту **Judge FP**.

---

## Assignment 5:

### How often does the judge catch the classifier's errors? Is that expected?

Судья хорошо ловит явные ошибки классификатора (особенно False Negatives), но хуже справляется с тонкими контекстами.

Это ожидаемо, потому что оценка чужого ответа требует более сложного анализа, чем сама классификация.

---

### Compare judge-FP and judge-FN rates — is the judge asymmetrically lenient or strict?

Судья асимметрично строг: **Judge FP > Judge FN**.

Он склонен считать ответ неправильным, если видит триггерные слова, даже если они используются в безопасном контексте (например, цитаты или ирония).

---

### What does this result tell you about using this judge in a real unlabeled setting?

LLM-судья нельзя полностью использовать вместо ground truth.

Он подходит как быстрый и дешёвый инструмент для предварительной оценки (sanity check, A/B тесты), но для продакшена нужна выборочная проверка человеком (human-in-the-loop), чтобы компенсировать его предвзятость.

---

## Assignment 6:

### What scenario did you choose, and how did you set the weights?

Я выбрал сценарий детской игровой платформы (например, чат в Roblox).

В этом контексте:

* False Negatives (пропуск токсичности) критичны → вес = 10
* False Positives (ложные блокировки) менее критичны → вес = 1
* Failures пайплайна → вес = 3

---

### Which configuration scores best on your sample — does it match your intuition?

Лучший результат показала конфигурация с role-playing улучшениями.

Это совпадает с ожиданиями: снижение отказов и более агрессивная классификация (даже с небольшим ростом FP) дают лучший итоговый баланс, особенно в домене, где безопасность важнее точности «не блокировать лишнее».

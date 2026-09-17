# Пакети за раздаване

| Файл | Какво |
|---|---|
| `math-coach-skill/` | Самостоятелна версия на агента — справочните материали са вътре в `references/`, не в repo-то |
| `math-coach-skill.zip` | Същото, опаковано за качване в Claude.ai (Customize → Skills) |

Разликата с `.claude/skills/math-coach/`: версията в repo-то чете `docs/`,
`content/` и `progress/` и сама записва прогреса. Версията тук няма файлова
система и води прогреса чрез отчет, който ученикът носи от сесия на сесия.

**При промяна на агента се обновяват и двете.** Пакетът се пресъздава с:

```
cd share && rm -f math-coach-skill.zip && zip -qr math-coach-skill.zip math-coach-skill
```

Инструкции за предаване на ученика: `docs/handoff.md`.

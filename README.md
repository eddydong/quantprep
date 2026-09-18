# quantprep

A public, bank-agnostic prep site for **AI / ML Director interviews in Global Markets Quant**.

Open [the site](https://eddydong.github.io/quantprep/). One page: Words (live hover glossary), the typical seat, industry briefing, a 14-day plan, closed-book drills, and four timed mocks (ML, DL/GenAI, coding, project).

This is not a job advert and not tied to one house. Coding lives in `pack/mocks/coding/` — implement `candidate.py`, then `pytest`. Do not open `solutions.py` first.

```bash
python3 tools/build_portal.py
```

Rebuilds `index.html` from the markdown in `pack/`.

# Roadmap: 8 weeks, 5-10 hours a week

Website first (weeks 1-6), then a real phone app (weeks 7-8). Each week has
a goal, the work, and a "done when" check. Don't move on until it's done -
a finished narrow app beats a half-finished big one.

Keep `docs/decisions.md` as you go: one paragraph per real decision (what
you chose, what you rejected, why). It becomes your interview prep.

---

## Week 1 - Run it, read it, start real data

- Get both servers running (README). Put the project on GitHub; commit often.
- Read the backend in this order: `schemas.py` → `analyze.py` → `parse.py` →
  `categorize.py` → `pricing.py` → `main.py`.
- JavaScript warm-up: read `App.jsx` → `MenuInput.jsx` → `DishCard.jsx`.
  Small first change: highlight the **best value dish** on each menu.
- Start `data/menus.csv`: 30 real menus, focusing on the seven categories in
  `data/categories.json`. Record `source` (URL) and `collected_on` for each.

**Done when:** the app runs on your machine, the best-value highlight works,
and 30 real menus are in the CSV.

## Week 2 - More data you can trust

- Grow to ~150 menus across 4-6 neighborhoods.
- Write `scripts/validate_data.py`: load every row with a pydantic model,
  report bad prices, unknown categories, missing neighborhoods, duplicates.
- Fill `rating` and `price_tier` from the Google Places or Yelp API.
  Read their terms on how long you may store data.

**Done when:** 150 menus, the validator passes, and the sample-data notice
is gone from the website.

## Week 3 - A parser that survives real menus

- Save 20 real menus as text fixtures in `backend/tests/fixtures/`.
- Un-skip the tests in `test_parse.py` and make them pass: add-ons,
  descriptions, multi-size prices.
- Measure: % of dishes parsed with the right name and price across the 20
  fixtures. Write the number down.

**Done when:** no skipped parse tests, and you have an accuracy number.

## Week 4 - Read menu photos

- Implement `extract_text` in `ocr.py` (instructions are in the file).
- Photograph 20 menus; type out the correct dishes/prices by hand once.
- Measure end-to-end item/price accuracy. Try PaddleOCR vs EasyOCR (and,
  if you want, a vision LLM). Keep the comparison table.
- Test the Photo tab on your phone (`npm run dev -- --host`).

**Done when:** you can photograph a menu on your phone and see results.

## Week 5 - Smarter categories

- Label ~200 dish names → category in `data/labeled_dishes.csv`.
- Measure the keyword baseline's accuracy, then try sentence-transformer
  embeddings. Keep the winner; keep both numbers.
- Add 3-5 categories your data supports (e.g. wings, burrito, pho).

**Done when:** `test_tricky_name` passes and you can quote before/after accuracy.

## Week 6 - The price model, then launch

- Train LightGBM on category, neighborhood, rating, price tier, cuisine and
  ingredient keywords. Use quantile objectives for low/high ranges.
- Compare against the percentile baseline on held-out dishes (median
  absolute error, % within $2). Only ship the model if it wins.
- Deploy: backend on Render or Fly.io, website on Vercel or Netlify. Set
  `VITE_API_URL` and add the site's URL to CORS in `main.py`.
- Launch hook: a "Chicago Burger Price Index" page by neighborhood. Share it
  in local subreddits and food groups.

**Done when:** the site is live at a real URL and strangers have used it.

## Week 7 - Turn it into a real app

- `npx create-expo-app mobile`, then run it on your phone with Expo Go.
- Copy `api.js` and `format.js` over almost unchanged - that's why they're
  separate files.
- Rebuild the screens with React Native components (`View`, `Text`,
  `Pressable`) and use `expo-image-picker` for the camera.

**Done when:** you can scan a menu with the app on your own phone.

## Week 8 - Polish and tell the story

- App: loading/error states, recent scans, app icon. Share with friends via
  Expo Go or a TestFlight / internal testing build.
- Write the README's results section: users, menus collected, parse/OCR
  accuracy, categorization accuracy, model error vs baseline.
- Draft two resume bullets, each with a number.

**Done when:** the README tells the whole story with numbers, and the app is
on at least 10 phones besides yours.

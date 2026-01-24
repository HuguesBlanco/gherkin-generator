# Record browser actions with Playwright

This guide shows the minimal steps to **record your interactions in a browser** (clicks, typing, navigation) and generate a Playwright script.

## Prerequisites

### 1) Node.js

You need Node.js installed on your machine.

* Install it from the official download page: [https://nodejs.org/en/download](https://nodejs.org/en/download)
* Verify it’s installed:

```bash
node -v
npm -v
```

### 2) Playwright browsers

Playwright needs its own browser binaries (Chromium / Firefox / WebKit).

Install all supported browsers:

```bash
npx playwright install
```

Or alternatively, you can only install one browser (faster / smaller):

```bash
npx playwright install chromium
# or
npx playwright install firefox
# or
npx playwright install webkit
```

## Record a browser session

Open a terminal and start the recorder (it opens a browser + an inspector window showing generated code):

```bash
npx playwright codegen https://www.google.com
```

* Replace `https://www.google.com` with the site you want to record.

Alternatively, you can define more details of the command you're running:

```bash
npx playwright codegen -b chromium -o e2e/recording.spec.ts https://www.google.com
```

Notes:

* `-b <browser>` selects the browser engine to record with:

  * `-b chromium` (default-ish): Playwright’s bundled Chromium
  * `-b firefox`: Playwright’s bundled Firefox
  * `-b webkit`: Playwright’s bundled WebKit (Safari-like engine)
* `-o <file>` saves the generated script to a file (instead of only showing it in the inspector), e.g. `-o e2e/recording.spec.ts`.

  * The output path is relative to the directory where you run the command.

# CS 1430 · Practice 1: Say It Again

Write a program that asks for a **whole number**, then a **phrase**, and prints the phrase that many times. Along the way you'll practice the loop you'll use all semester: **copy the template → clone → write code → check → commit → push → check again.**

We'll do this together in class. If you finish early, help a neighbor.

**You're done when** `check.py` shows PASS on every line.

---

## Before you start

In person students -->  It would be idea to already have your GitHub Account set up and know your password and creditials.

If ONLINE --> You need the Assignment 1 toolchain: Python, Git, VS Code with the Python extension, and a GitHub account you're signed in to. If you haven't finished Assignment 1 yet, tell your instructor now. You can follow along with a neighbor.

---

## Step 1: Make your own copy

1. On this page, click the green **Use this template** button (top right) → **Create a new repository**.
2. **Owner:** your own account, not CS1430.
3. **Repository name:** `Practice1`
4. **Visibility:** Public
5. Click **Create repository**.

> **Do NOT click Fork.** Use this template only.

You now have your own repo at `github.com/YOUR-USERNAME/Practice1`.

---

## Step 2: Clone it to your computer

1. On **your** new repo's page, click the green **Code** button and copy the HTTPS URL.
2. Open VS Code. Open a terminal: **Terminal → New Terminal**.
3. Type this, using **your** URL (not CS1430's), and press Enter:

```
git clone https://github.com/YOUR-USERNAME/Practice1.git C:\CS1430\Practice1
```

This puts the files in `C:\CS1430\Practice1`. Keep your work out of Documents, Desktop, and OneDrive. Those folders cause lock errors that have nothing to do with your code.

---

## Step 3: Open the folder in VS Code

1. **File → Open Folder…** and choose `C:\CS1430\Practice1`. Pick the **whole folder**, not a single file.
2. If VS Code asks whether you trust the authors, click **Yes, I trust the authors**.
3. In the Explorer panel on the left you should see `README.md`, `main.py`, `check.py`, and two files that start with a dot.

---

## Step 4: Turn off Copilot for this one

Copilot would write this whole program the moment you start typing, and the point today is for **you** to type it.

- Click the **Copilot icon** in the status bar at the bottom right of VS Code.
- Turn off **code completions** (or click **Snooze**).
- Don't use Copilot Chat for this practice either.

Turn it back on when you're done.

---

## Step 5: Write the program

Open `main.py`. Write your code **below** the header comment. Your program needs three things, in this order:

1. **Ask for the number.** Use `input()` with a short prompt. `input()` always gives you **text**, even if the person types `5`, so wrap it in `int( ... )` to turn it into a whole number you can multiply by. Store it in a variable.
2. **Ask for the phrase.** Use `input()` again and store it in a second variable.
3. **Print the phrase that many times.** Use the `*` symbol. In Python, text times a whole number repeats the text.

**Rules the checker looks for**

| Rule | Why |
|---|---|
| Ask for the number **first**, then the phrase | The checker types them in that order |
| Use `int()` on the number | Text can't be multiplied by text |
| Use `*` to do the repeating | That's the skill this practice is about |
| **No** `for` or `while` loops | Let `*` do the work |

**What a run should look like** (your prompts can say whatever you want):

```
How many times? 5
What should I say? hi
hihihihihi
```

Want spaces between them? Type the phrase with a space at the end (`hi `) when you run it. Either way passes.

Save the file: **Ctrl + S**.

---

## Step 6: Run your program

Click the **▷ Run** button at the top right of `main.py`. Click in the terminal, type a number, press Enter, type a phrase, press Enter. Try a few different numbers.

---

## Step 7: Run the checker

Type this in the terminal:

```
python check.py
```

The **Your code** lines should all say PASS. Under **Git and GitHub**, `Your code is committed` will say **FAIL**. **That's expected.** You haven't saved your work to Git yet.

> **Rule of thumb:** fix only the **first** FAIL line, save, and run the checker again. Don't try to fix everything at once.

---

## Step 8: Commit and push

There are three saves, and only the last one reaches GitHub:

| Save | Where it lives |
|---|---|
| **Saved** (Ctrl + S) | Only this computer |
| **Committed** (a labeled snapshot) | Still only this computer |
| **Pushed** | On GitHub |

**In VS Code:**

1. Click the **Source Control** icon in the left sidebar (it has a number badge).
2. Type a short message in the box at the top, like `wrote practice 1`.
3. Click **✓ Commit**. If VS Code asks about staging changes, click **Yes**.
4. Click **Sync Changes** (or **Push**).

**Prefer the terminal?** Same thing:

```
git add .
git commit -m "wrote practice 1"
git push
```

---

## Step 9: Run the checker again

```
python check.py
```

Every line should say **PASS**. Open `github.com/YOUR-USERNAME/Practice1` in your browser and click `main.py`. Your code is there.

---

## If something breaks

| You see | What's happening | Fix |
|---|---|---|
| `'git' is not recognized` | Terminal opened before Git finished installing | Close every terminal, then close and reopen VS Code |
| `main.py is in this folder` FAIL | You opened a file, not the folder | **File → Open Folder** and pick `C:\CS1430\Practice1` |
| `invalid literal for int()` | You asked for the phrase first | Ask for the number first, then the phrase |
| `can't multiply sequence by non-int` | The number is still text | Wrap the number's `input()` in `int( ... )` |
| `You did not use a loop` FAIL | There's a `for` or `while` in your code | Take the loop out and use `*` |
| `Your copy is on your own GitHub account` FAIL | You cloned the class template, not your copy | Go back to Step 1 |
| `Your code is committed` FAIL | Saved but not committed | Step 8, parts 1 to 3 |
| `Your commit is pushed to GitHub` FAIL | Committed but not pushed | Click **Sync Changes**, or run `git push` |
| `python` opens the Microsoft Store | Windows is using a shortcut instead of real Python | Try `py check.py` instead, then ask your instructor |

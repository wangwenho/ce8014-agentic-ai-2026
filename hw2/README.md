# Homework 2

The sample implementation is a ReAct agent that can answer questions about the world and itself.

## Quick Start

### Prerequisites

- [uv](https://docs.astral.sh/uv/) : ensure it is installed on your machine.
- Python 3.x (installed automatically by `uv`).

### 1. Clone the repository

```bash
git clone https://github.com/wangwenho/ce8014-agentic-ai-2026.git
cd hw2
```

### 2. Install dependencies

```bash
uv sync
```

This command installs all packages required by the project.

### 3. Create a `.env` file

```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
echo "TAVILY_API_KEY=your_tavily_api_key_here" >> .env
```

### 4. Run the application

```bash
uv run python main.py --demo --verbose
```

> [!NOTE]
>
> - The `--demo` flag runs a predefined demonstration of the agent's capabilities.
> - The `--verbose` flag provides detailed output of the agent's reasoning process.

You should see an interactive prompt similar to the following:

<details>
<summary>click to expand </summary>

```plain
────────────────────── Task 1 ──────────────────────
╭────────────────────── User ──────────────────────╮
│ What fraction of Japan's population is Taiwan's  │
│ population as of 2025?                           │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I need to find the population of Japan  │
│ and Taiwan as of 2025 to calculate the fraction. │
│ Action: Search                                   │
│ Action Input: Japan population 2025, Taiwan      │
│ population 2025                                  │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: Japan's population   │
│ in 2025 is projected to be around 121.96         │
│ million. Taiwan's population in 2025 is          │
│ estimated to be about 23.3 million.              │
│ Top results:                                     │
│ 1. Country comparison Taiwan vs Japan Population │
│ 2026 score=1.00                                  │
│ (https://countryeconomy.com/countries/compare/ta │
│ iwan/japan?sc=XE23)                              │
│    | 4,578.5 | 2017 | [Remittance received ($M)  │
│ [+]](/demography/migration/remittance/japan      │
│ "Emigrants Remittance received ") | | 2.20% |    │
│ 2020 | [% Immigrant                              │
│ [+]](/demography/migration/immigration/japan     │
│ "International immigrant percent") | | 0.64% |   │
│ 2020 | [% Emigrant [+]](/demog...                │
│ 2. Japan Population (1950-2025) - Macrotrends    │
│ score=1.00                                       │
│ (https://www.macrotrends.net/global-metrics/coun │
│ tries/jpn/japan/population)                      │
│    ## Japan Population (1950-2025)  Population   │
│ Economy Trade Health Education Development Labor │
│ Force Environment Crime Immigration Other        │
│ Population Growth Rate Density Urban Rural Life  │
│ Expectancy Birth Rate Death Rate Infant          │
│ Mortality Rate Fertility Rate  ##### Total       │
│ current po...                                    │
│ 3. Demographics of Japan - Wikipedia score=1.00  │
│ (https://en.wikipedia.org/wiki/Demographics_of_J │
│ apan)                                            │
│    See also: Demographics of the Empire of Japan │
│ and Demographic history of Japan before the      │
│ Meiji Restoration  As of 2025, Japan was the     │
│ world's twelfth-most populous country. Japan's   │
│ population had declined by 0.8 percent from the  │
│ time of the 2012 census, the first time it       │
│ had...                                           │
│ 4. Demographics of Taiwan - Wikipedia score=0.99 │
│ (https://en.wikipedia.org/wiki/Demographics_of_T │
│ aiwan)                                           │
│    | 2023 | 23,420,000 | 135,571 | 205,368 |     │
│ −69,797 | 5.8 | 8.8 | −3.0 | 9.7 | 0.86 | | 2024 │
│ | 23,400,000 | 134,856 | 202,107 | −67,251 | 5.8 │
│ | 8.7 | −2.9 | 2.1 | 0.89 | | 2025 | 23,299,132  │
│ | 107,812 | 200,268 | −92,456 | 4.6 | 8.6 | -4.0 │
│ | −0.4 | 0.72 | [...] | Nationality | 20...      │
│ 5. Taiwan Population (1950-2025) - Macrotrends   │
│ score=0.99                                       │
│ (https://www.macrotrends.net/global-metrics/coun │
│ tries/twn/taiwan/population)                     │
│    ## Taiwan Population (1950-2025)  Population  │
│ Economy Trade Health Education Development Labor │
│ Force Environment Crime Immigration Other        │
│ Population Growth Rate Density Urban Rural Life  │
│ Expectancy Birth Rate Death Rate Infant          │
│ Mortality Rate Fertility Rate  ##### Total       │
│ current p...                                     │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: Now that I have the populations of      │
│ Japan and Taiwan for 2025, I can calculate the   │
│ fraction of Taiwan's population relative to      │
│ Japan's population.                              │
│ Action: Calculate                                │
│ Action Input: Fraction = Taiwan's population /   │
│ Japan's population = 23.3 million / 121.96       │
│ million                                          │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Unsupported action: Calculate       │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I will perform the calculation to find  │
│ the fraction of Taiwan's population relative to  │
│ Japan's population.                              │
│ Action: Calculate                                │
│ Action Input: 23.3 million / 121.96 million      │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Unsupported action: Calculate       │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I need to find the fraction of Taiwan's │
│ population compared to Japan's population using  │
│ the provided numbers.                            │
│ Action: Search                                   │
│ Action Input: Calculate fraction of 23.3 million │
│ to 121.96 million                                │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: The fraction of 23.3 │
│ million to 121.96 million is 23.3/121.96, which  │
│ simplifies to approximately 0.191.               │
│ Top results:                                     │
│ 1. Fraction Calculator score=0.65                │
│ (https://www.calculator.net/fraction-calculator. │
│ html)                                            │
│    Financial Fitness & Health Math Other [...]   │
│ sign in  home / math / fraction calculator  #    │
│ Fraction Calculator  Below are multiple fraction │
│ calculators capable of addition, subtraction,    │
│ multiplication, division, simplification, and    │
│ conversion between fractions and decimals.       │
│ Fie...                                           │
│ 2. How to Calculate ANY Fraction Easily! -       │
│ YouTube score=0.20                               │
│ (https://www.youtube.com/watch?v=EKoI1hYbpA4)    │
│    1590 comments ### Transcript: [...] see what  │
│ I mean. So, let's do this. The way we do this is │
│ as follows. We're going to keep the same bottom  │
│ numbers, the same denominators here. So, we're   │
│ going to have a two and we're going to have a    │
│ three. All right? And we're going to be ad...    │
│ 3. Free Fraction Calculator: Simplify, Add,      │
│ Subtract, Multiply score=0.14                    │
│ (https://www.hackmath.net/en/calculator/fraction │
│ )                                                │
│    ## Fractions in word problems: [...] #        │
│ Fraction Calculator  This fraction calculator    │
│ performs all basic fraction operations –         │
│ addition, subtraction, multiplication, and       │
│ division – and evaluates expressions with        │
│ fractions. Each calculation includes a detailed  │
│ step-by-step expla...                            │
│ 4. Fractions Calculator - Calculator Soup        │
│ score=0.11                                       │
│ (https://www.calculatorsoup.com/calculators/math │
│ /fractions.php)                                  │
│    ## Fraction Formulas  There is a way to add   │
│ or subtract fractions without finding the least  │
│ common denominator (LCD). This method involves   │
│ cross multiplication of the fractions. See the   │
│ formulas below.  You may find that it is easier  │
│ to use these formulas than to do the math t...   │
│ 5. Decimal to fraction converter -               │
│ RapidTables.com score=0.08                       │
│ (https://www.rapidtables.com/convert/number/deci │
│ mal-to-fraction.html)                            │
│    | Decimal | Fraction |  --- | | 0.00001 |     │
│ 1/100000 | | 0.0001 | 1/10000 | | 0.001 | 1/1000 │
│ | | 0.01 | 1/100 | | 0.08333333 | 1/12 | |       │
│ 0.09090909 | 1/11 | | 0.1 | 1/10 | | 0.11111111  │
│ | 1/9 | | 0.125 | 1/8 | | 0.14285714 | 1/7 | |   │
│ 0.16666667 | 1/6 | | 0.2 | 1/5 | | 0.22222222    │
│ |...                                             │
╰──────────────────────────────────────────────────╯
╭────────────────── Final Answer ──────────────────╮
│ The fraction of Taiwan's population to Japan's   │
│ population as of 2025 is approximately 0.191.    │
╰──────────────────────────────────────────────────╯
────────────────────── Task 2 ──────────────────────
╭────────────────────── User ──────────────────────╮
│ Compare the main display specs of iPhone 15 and  │
│ Samsung S24.                                     │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I need to find the main display         │
│ specifications for both the iPhone 15 and        │
│ Samsung S24 to compare them.                     │
│ Action: Search                                   │
│ Action Input: iPhone 15 display specifications   │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: The iPhone 15        │
│ features a 6.1-inch Super Retina XDR OLED        │
│ display with a resolution of 2556 x 1179 pixels  │
│ and a pixel density of 460 PPI. It supports      │
│ HDR10 and has a max brightness of 2,000 nits.    │
│ The display is protected by Ceramic Shield.      │
│ Top results:                                     │
│ 1. iPhone 15 - Wikipedia score=0.96              │
│ (https://en.wikipedia.org/wiki/IPhone_15)        │
│    ## Hardware  ### Display  The iPhone 15       │
│ features a 6.1-inch (155 mm) display with Super  │
│ Retina XDR OLED technology at a resolution of    │
│ 2556×1179 pixels and a pixel density of about    │
│ 460 PPI with a refresh rate of 60 Hz. The iPhone │
│ 15 Plus features a 6.7-inch (170 mm) display     │
│ wit...                                           │
│ 2. iPhone 15 - Tech Specs score=0.93             │
│ (https://support.apple.com/en-us/111831)         │
│    The iPhone 15 display has rounded corners     │
│ that follow a beautiful curved design, and these │
│ corners are within a standard rectangle. When    │
│ measured as a standard rectangular shape, the    │
│ screen is 6.12 inches diagonally (actual         │
│ viewable area is less).  ### Splash, Water, and  │
│ Dust...                                          │
│ 3. iPhone 15 Screen Sizes - Use Your Loaf        │
│ score=0.92                                       │
│ (https://useyourloaf.com/blog/iphone-15-screen-s │
│ izes/)                                           │
│    ### iPhone 15  The iPhone 15 gains some of    │
│ the features of the now discontinued iPhone 14   │
│ Pro such as the dynamic island, and the A16      │
│ Bionic chip.   A16 Bionic chip (6-core CPU,      │
│ 5-core GPU, 16-core Neural Engine)  Display:     │
│ 6.1" Super Retina XDR OLED  Screen resolution    │
│ (points)...                                      │
│ 4. iPhone 15: viewport, screen size, CSS pixel   │
│ ratio, cross- ... score=0.91                     │
│ (https://blisk.io/devices/details/iphone-15)     │
│    #### Specification (Summary)  |  |  |  --- |  │
│ | Release Date | Friday, September 22, 2023 | |  │
│ Vendor | Apple | | Device Type | phone | |       │
│ Operating System | iOS | | Display | Super       │
│ Retina XDR OLED, 91.3 cm2, 19.5:9, ~86.4%        │
│ screen-to-body ratio | | Screen Size             │
│ (Resolution) Width...                            │
│ 5. Apple iPhone 15 - Full phone specifications - │
│ GSMArena.com score=0.91                          │
│ (https://www.gsmarena.com/apple_iphone_15-12559. │
│ php)                                             │
│    |  |  |  |  ---  | Display | Type | Super     │
│ Retina XDR OLED, HDR10, Dolby Vision, 1000 nits  │
│ (HBM), 2000 nits (peak) | | Size | 6.1 inches,   │
│ 91.3 cm2 (~86.4% screen-to-body ratio) | |       │
│ Resolution | 1179 x 2556 pixels, 19.5:9 ratio    │
│ (~461 ppi density) | | Protection | Ceramic      │
│ Shield...                                        │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: Now I need to find the display          │
│ specifications for the Samsung S24 to complete   │
│ the comparison.                                  │
│ Action: Search                                   │
│ Action Input: Samsung S24 display specifications │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: The Samsung Galaxy   │
│ S24 has a 6.2-inch FHD+ AMOLED display with a    │
│ 120Hz refresh rate. The S24 Plus has a 6.7-inch  │
│ QHD+ AMOLED display. The S24 Ultra has a         │
│ 6.8-inch QHD+ AMOLED display.                    │
│ Top results:                                     │
│ 1. Galaxy S24 | Samsung Mobile Press score=1.00  │
│ (https://www.samsungmobilepress.com/media-assets │
│ /galaxy-s24?tab=specs)                           │
│    |  |  |  |  |  |  ---  ---  | Galaxy S24 | |  │
│ | | | | Display | 6.2-inch FHD+\ Dynamic AMOLED  │
│ 2X Display   Super Smooth 120Hz refresh rate     │
│ (1~120Hz)  Vision booster | | | \Measured        │
│ diagonally, Galaxy S24’s screen size is 6.2-inch │
│ in the full rectangle and 6.0-inch with          │
│ accounti...                                      │
│ 2. Samsung Galaxy S24 - Full phone               │
│ specifications - GSMArena.com score=1.00         │
│ (https://www.gsmarena.com/samsung_galaxy_s24-127 │
│ 73.php)                                          │
│    |  |  |  |  ---  | Display | Type | Dynamic   │
│ LTPO AMOLED 2X, 120Hz, HDR10+, 2600 nits (peak)  │
│ | | Size | 6.2 inches, 94.4 cm2 (~90.9%          │
│ screen-to-body ratio) | | Resolution | 1080 x    │
│ 2340 pixels, 19.5:9 ratio (~416 ppi density) | | │
│ Protection | Corning Gorilla Glass Victus 2 |    │
│ |...                                             │
│ 3. Samsung Galaxy S24 - Wikipedia score=1.00     │
│ (https://en.wikipedia.org/wiki/Samsung_Galaxy_S2 │
│ 4)                                               │
│    ## Specifications    ### Display    The       │
│ Galaxy S24 and S24+ use a "Dynamic AMOLED 2X"    │
│ display with HDR10+ support, 2600 nits of peak   │
│ brightness, LTPO backplane, "dynamic tone        │
│ mapping" technology, and Corning Gorilla Glass   │
│ Victus 2. The Galaxy S24 FE has 1900 nits o...   │
│ 4. Samsung Galaxy S24 screen size for every      │
│ model - TechRadar score=1.00                     │
│ (https://www.techradar.com/phones/samsung-phones │
│ /samsung-galaxy-s24-screen-size)                 │
│    Samsung Galaxy S24 hands on handheld front    │
│ straight  Both the Galaxy S24 and Galaxy S24     │
│ Plus have received a 0.1-inch display size       │
│ upgrade without increasing their respective      │
│ overall sizes; this is all thanks to slimmer     │
│ bezels. So the Galaxy S24 has a 6.2-inch display │
│ and the...                                       │
│ 5. Galaxy S24 Series: Discover all the new and   │
│ exciting features! score=1.00                    │
│ (https://www.samsung.com/au/members/whats-new/ga │
│ laxy-s24-series-discover-all-the-new-and-excitin │
│ g-features/?srsltid=AfmBOopuPEpUuqq1rXAQD16D_3hr │
│ zuvb-D_wRnRscjzaWYvq7iJbVOft)                    │
│    11 Measured diagonally, Galaxy S24 Ultra's    │
│ screen size is 6.8 inches in the full rectangle  │
│ and 6.8 inches accounting for the rounded        │
│ corners, Galaxy S24's screen size is 6.2 inches  │
│ in the full rectangle and 6 inches accounting    │
│ for the rounded corners and Galaxy S24+'s screen │
│ s...                                             │
╰──────────────────────────────────────────────────╯
╭────────────────── Final Answer ──────────────────╮
│ The main display specifications are as follows:  │
│                                                  │
│ **iPhone 15:**                                   │
│ - Display Type: Super Retina XDR OLED            │
│ - Size: 6.1 inches                               │
│ - Resolution: 2556 x 1179 pixels                 │
│ - Pixel Density: 460 PPI                         │
│ - Refresh Rate: 60 Hz                            │
│ - Max Brightness: 2,000 nits                     │
│ - Protection: Ceramic Shield                     │
│                                                  │
│ **Samsung Galaxy S24:**                          │
│ - Display Type: Dynamic AMOLED 2X                │
│ - Size: 6.2 inches                               │
│ - Resolution: 1080 x 2340 pixels                 │
│ - Pixel Density: 416 PPI                         │
│ - Refresh Rate: 120 Hz                           │
│ - Max Brightness: 2,600 nits                     │
│ - Protection: Corning Gorilla Glass Victus 2     │
│                                                  │
│ The iPhone 15 has a slightly smaller display     │
│ with a higher resolution and pixel density,      │
│ while the Samsung S24 features a higher refresh  │
│ rate and peak brightness.                        │
╰──────────────────────────────────────────────────╯
────────────────────── Task 3 ──────────────────────
╭────────────────────── User ──────────────────────╮
│ Who is the CEO of the startup 'Morphic' AI       │
│ search?                                          │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I need to find information about the    │
│ startup 'Morphic' and its CEO.                   │
│ Action: Search                                   │
│ Action Input: Morphic AI search CEO              │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: Weston Baker is the  │
│ CEO of Morphic, an AI-powered web design         │
│ platform. He founded Morphic to help startups    │
│ build professional websites quickly. Morphic     │
│ aims to reduce the time and cost of web design   │
│ for businesses.                                  │
│ Top results:                                     │
│ 1. Morphic holding CEO sells shares worth over   │
│ $1.2 million score=1.00                          │
│ (https://www.investing.com/news/company-news/mor │
│ phic-holding-ceo-sells-shares-worth-over-12-mill │
│ ion-93CH-3514690)                                │
│    The acquisition, anticipated to finalize in   │
│ the third quarter of 2024, is seen as a          │
│ strategic move for Eli Lilly, potentially        │
│ positioning the company to enter the first-line  │
│ ulcerative colitis market. Morphic's lead drug,  │
│ MORF-057, currently under multiple phase 2       │
│ studies for...                                   │
│ 2. Morphic - 2026 Company Profile & Team -       │
│ Tracxn score=1.00                                │
│ (https://tracxn.com/d/companies/morphic/__QREWaD │
│ zuHM-XW-PFwSgyqKupVzTD3aOF5VD9L0I9mSw)           │
│    Jaynti Kanani is the current CEO of Morphic.  │
│ They are also angel investors in 19 startups,    │
│ including Polygon.  Morphicis headquartered in   │
│ San Francisco, United States.  Morphicis a       │
│ funded company,having raised a total of  $\\\\\  │
│ in its 1st and only funding round.  Explore      │
│ our...                                           │
│ 3. Morphic Therapeutic Expands Leadership with   │
│ Key Appointments in ... score=1.00               │
│ (https://www.biospace.com/morphic-therapeutic-ex │
│ pands-leadership-with-key-appointments-in-clinic │
│ al-and-corporate-development)                    │
│    Marc Schegerin, MD, COO and CFO of Morphic    │
│ Therapeutic, stated, “Aaron’s broad experience   │
│ and strategic perspectives will be critical as   │
│ we expand our clinical pipeline. Aaron will      │
│ continue to oversee our partnering efforts,      │
│ commercial planning and integrate seamlessly     │
│ with ou...                                       │
│ 4. Morphic Management Team - CB Insights         │
│ score=0.98                                       │
│ (https://www.cbinsights.com/company/morphic/peop │
│ le)                                              │
│    Founder, Chief Executive Officer  Current  |  │
│ |  |  --- | | Name | Weston Baker | | Work       │
│ History | Skidmore, Owings & Merrill, and Foster │
│ + Partners | | Title | Founder, Chief Executive  │
│ Officer | | Status | Current |  Name  Weston     │
│ Baker  Work History  Skidmore, Owings &          │
│ Merril...                                        │
│ 5. Weston Baker - Morphic - LinkedIn score=0.98  │
│ (https://www.linkedin.com/in/westonbaker)        │
│    # Weston Baker Founder @ Morphic | AI-Powered │
│ Websites for VCs & Growth Firms | Automating     │
│ High-End Design for Startups New York, New York, │
│ United States, US   500 connections, 7515        │
│ followers  ## About 🚀 Helping Startups & Growth │
│ Firms Build Exceptional Websites—Fast  I work    │
│ w...                                             │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I have found conflicting information    │
│ regarding the CEO of Morphic. Some sources       │
│ indicate Weston Baker, while others mention      │
│ Jaynti Kanani. I need to verify which one is     │
│ correct.                                         │
│ Action: Search                                   │
│ Action Input: current CEO of Morphic AI search   │
│ Weston Baker or Jaynti Kanani?                   │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: Jaynti Kanani is the │
│ current CEO of Morphic AI. He previously         │
│ co-founded Polygon. Weston Baker is not          │
│ associated with Morphic AI.                      │
│ Top results:                                     │
│ 1. Jaynti Kanani - Founder CEO at Morphic        │
│ score=0.79                                       │
│ (https://www.getprog.ai/profile/1692593)         │
│    Jaynti Kanani is a founder and CEO with 13    │
│ years of engineering experience, best known as a │
│ co-founder of Polygon (Matic) and currently      │
│ leading Morphic from the UAE. He blends          │
│ protocol-level blockchain engineering—authoring  │
│ changes to the Bor consensus, Heimdall           │
│ validator, and...                                │
│ 2. Jaynti Kanani Email & Phone Number | Morphic  │
│ Founder and CEO Contact Information score=0.72   │
│ (https://rocketreach.co/jaynti-kanani-email_7573 │
│ 2683)                                            │
│    see less    ### Jaynti Kanani Summary  Jaynti │
│ Kanani, based in United Arab Emirates, is        │
│ currently a Founder and CEO at Morphic. Jaynti   │
│ Kanani brings experience from previous roles at  │
│ Polygon Technology, Housing.com and Function     │
│ space. Jaynti Kanani holds a 2007 - 2011         │
│ Bachelor...                                      │
│ 3. Jaynti Kanani - Founder & CEO at Morphic |    │
│ The Org score=0.71                               │
│ (https://theorg.com/org/morphic-1/org-chart/jayn │
│ ti-kanani)                                       │
│    Pricing  Morphic  Unverified  # Jaynti Kanani │
│ ### Founder & CEO  Contact  Jaynti Kanani, a     │
│ seasoned professional in the tech industry, has  │
│ a rich and varied career history. From           │
│ co-founding Polygon Technology and serving as    │
│ the CEO to working as a Data Scientist at        │
│ Housing.co...                                    │
│ 4. Biography of Jaynti Kanani: Co-Founder & CEO  │
│ of Polygon- Entrepreneur score=0.63              │
│ (https://www.werisebyliftingothers.in/2024/08/bi │
│ ography-of-jaynti-kanani-co-founder.html)        │
│    Transitioning Leadership  In October 2023,    │
│ Jaynti Kanani announced his decision to step     │
│ down from his role as CEO of Polygon. He chose   │
│ to focus on new ventures while continuing to     │
│ support Polygon from a distance. His departure   │
│ marked a significant shift in the company’s      │
│ leader...                                        │
│ 5. Jaynti Kanani - 2026 Portfolio & Founded      │
│ Companies - Tracxn score=0.59                    │
│ (https://tracxn.com/d/people/jaynti-kanani/__Uqy │
│ LQxE7Dvy1UH2eKS66_43H7DMHHtGL5CNToE6WqTU)        │
│    Most viewed in 2019  ## About Jaynti Kanani   │
│ Jaynti Kananiis an entrepreneurand an angel      │
│ investorbased out of United Arab Emirates. Their │
│ journey in the startup ecosystem started in 2017 │
│ through Polygon. Jaynti Kanani has founded 2     │
│ companies. They are currently acting as the f... │
╰──────────────────────────────────────────────────╯
╭────────────────── Final Answer ──────────────────╮
│ Jaynti Kanani is the current CEO of Morphic AI.  │
│ He previously co-founded Polygon.                │
╰──────────────────────────────────────────────────╯
```

</details>

## Testing

To run the tests for the project, use the following command:

```bash
uv run pytest tests
```

## Implementation Details

### Implementation Logic

#### 1. System Prompt Strategy

The system prompt is designed to guide the agent's behavior in a structured manner. It emphasizes the importance of generating a Thought, deciding on an Action, and providing an Action Input for each step of the reasoning process. The prompt also instructs the agent to avoid outputting Observations directly and to end each response with a specific marker (`===STEP_END===`) to indicate the completion of a reasoning step.

```plain
You are a single general-purpose ReAct agent.
Respond only in this strict format (no extra text, no Observation lines):
Thought: <brief reasoning step>
Action: Search
Action Input: <search query>
Final Answer: <only when you have enough evidence>

- Do not output Observation; your code will add it.
- End each response with the marker exactly: ===STEP_END===
- If you need another tool call, do another Thought/Action/Action Input.
- If you cannot find enough info in this step, do not output Final Answer.

One-shot example:
User: Who is the CEO of the startup 'Morphic' AI search?
Thought: Search company and CEO.
Action: Search
Action Input: Morphic AI search CEO
===STEP_END===
```

#### 2. The Loop Mechanism

The agent operates in a loop where it generates a Thought, decides on an Action, and provides an Action Input. After each action, the system provides an Observation based on the action taken. The agent continues this process until it determines that it has enough information to provide a Final Answer.

### Benchmark Traces (The Evidence)

#### 1. Task 1: Population Fraction Calculation

The agent successfully navigates through the process of finding the population of Japan and Taiwan in 2025, and then attempts to calculate the fraction. Although it initially struggles with the unsupported "Calculate" action, it eventually finds a way to obtain the fraction through a search query, demonstrating its ability to adapt its strategy based on the tools available.

<details>
<summary>click to expand </summary>
```plain
────────────────────── Task 1 ──────────────────────
╭────────────────────── User ──────────────────────╮
│ What fraction of Japan's population is Taiwan's  │
│ population as of 2025?                           │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I need to find the population of Japan  │
│ and Taiwan as of 2025 to calculate the fraction. │
│ Action: Search                                   │
│ Action Input: Japan population 2025, Taiwan      │
│ population 2025                                  │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: Japan's population   │
│ in 2025 is projected to be around 121.96         │
│ million. Taiwan's population in 2025 is          │
│ estimated to be about 23.3 million.              │
│ Top results:                                     │
│ 1. Country comparison Taiwan vs Japan Population │
│ 2026 score=1.00                                  │
│ (https://countryeconomy.com/countries/compare/ta │
│ iwan/japan?sc=XE23)                              │
│    | 4,578.5 | 2017 | [Remittance received ($M)  │
│ [+]](/demography/migration/remittance/japan      │
│ "Emigrants Remittance received ") | | 2.20% |    │
│ 2020 | [% Immigrant                              │
│ [+]](/demography/migration/immigration/japan     │
│ "International immigrant percent") | | 0.64% |   │
│ 2020 | [% Emigrant [+]](/demog...                │
│ 2. Japan Population (1950-2025) - Macrotrends    │
│ score=1.00                                       │
│ (https://www.macrotrends.net/global-metrics/coun │
│ tries/jpn/japan/population)                      │
│    ## Japan Population (1950-2025)  Population   │
│ Economy Trade Health Education Development Labor │
│ Force Environment Crime Immigration Other        │
│ Population Growth Rate Density Urban Rural Life  │
│ Expectancy Birth Rate Death Rate Infant          │
│ Mortality Rate Fertility Rate  ##### Total       │
│ current po...                                    │
│ 3. Demographics of Japan - Wikipedia score=1.00  │
│ (https://en.wikipedia.org/wiki/Demographics_of_J │
│ apan)                                            │
│    See also: Demographics of the Empire of Japan │
│ and Demographic history of Japan before the      │
│ Meiji Restoration  As of 2025, Japan was the     │
│ world's twelfth-most populous country. Japan's   │
│ population had declined by 0.8 percent from the  │
│ time of the 2012 census, the first time it       │
│ had...                                           │
│ 4. Demographics of Taiwan - Wikipedia score=0.99 │
│ (https://en.wikipedia.org/wiki/Demographics_of_T │
│ aiwan)                                           │
│    | 2023 | 23,420,000 | 135,571 | 205,368 |     │
│ −69,797 | 5.8 | 8.8 | −3.0 | 9.7 | 0.86 | | 2024 │
│ | 23,400,000 | 134,856 | 202,107 | −67,251 | 5.8 │
│ | 8.7 | −2.9 | 2.1 | 0.89 | | 2025 | 23,299,132  │
│ | 107,812 | 200,268 | −92,456 | 4.6 | 8.6 | -4.0 │
│ | −0.4 | 0.72 | [...] | Nationality | 20...      │
│ 5. Taiwan Population (1950-2025) - Macrotrends   │
│ score=0.99                                       │
│ (https://www.macrotrends.net/global-metrics/coun │
│ tries/twn/taiwan/population)                     │
│    ## Taiwan Population (1950-2025)  Population  │
│ Economy Trade Health Education Development Labor │
│ Force Environment Crime Immigration Other        │
│ Population Growth Rate Density Urban Rural Life  │
│ Expectancy Birth Rate Death Rate Infant          │
│ Mortality Rate Fertility Rate  ##### Total       │
│ current p...                                     │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: Now that I have the populations of      │
│ Japan and Taiwan for 2025, I can calculate the   │
│ fraction of Taiwan's population relative to      │
│ Japan's population.                              │
│ Action: Calculate                                │
│ Action Input: Fraction = Taiwan's population /   │
│ Japan's population = 23.3 million / 121.96       │
│ million                                          │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Unsupported action: Calculate       │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I will perform the calculation to find  │
│ the fraction of Taiwan's population relative to  │
│ Japan's population.                              │
│ Action: Calculate                                │
│ Action Input: 23.3 million / 121.96 million      │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Unsupported action: Calculate       │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I need to find the fraction of Taiwan's │
│ population compared to Japan's population using  │
│ the provided numbers.                            │
│ Action: Search                                   │
│ Action Input: Calculate fraction of 23.3 million │
│ to 121.96 million                                │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: The fraction of 23.3 │
│ million to 121.96 million is 23.3/121.96, which  │
│ simplifies to approximately 0.191.               │
│ Top results:                                     │
│ 1. Fraction Calculator score=0.65                │
│ (https://www.calculator.net/fraction-calculator. │
│ html)                                            │
│    Financial Fitness & Health Math Other [...]   │
│ sign in  home / math / fraction calculator  #    │
│ Fraction Calculator  Below are multiple fraction │
│ calculators capable of addition, subtraction,    │
│ multiplication, division, simplification, and    │
│ conversion between fractions and decimals.       │
│ Fie...                                           │
│ 2. How to Calculate ANY Fraction Easily! -       │
│ YouTube score=0.20                               │
│ (https://www.youtube.com/watch?v=EKoI1hYbpA4)    │
│    1590 comments ### Transcript: [...] see what  │
│ I mean. So, let's do this. The way we do this is │
│ as follows. We're going to keep the same bottom  │
│ numbers, the same denominators here. So, we're   │
│ going to have a two and we're going to have a    │
│ three. All right? And we're going to be ad...    │
│ 3. Free Fraction Calculator: Simplify, Add,      │
│ Subtract, Multiply score=0.14                    │
│ (https://www.hackmath.net/en/calculator/fraction │
│ )                                                │
│    ## Fractions in word problems: [...] #        │
│ Fraction Calculator  This fraction calculator    │
│ performs all basic fraction operations –         │
│ addition, subtraction, multiplication, and       │
│ division – and evaluates expressions with        │
│ fractions. Each calculation includes a detailed  │
│ step-by-step expla...                            │
│ 4. Fractions Calculator - Calculator Soup        │
│ score=0.11                                       │
│ (https://www.calculatorsoup.com/calculators/math │
│ /fractions.php)                                  │
│    ## Fraction Formulas  There is a way to add   │
│ or subtract fractions without finding the least  │
│ common denominator (LCD). This method involves   │
│ cross multiplication of the fractions. See the   │
│ formulas below.  You may find that it is easier  │
│ to use these formulas than to do the math t...   │
│ 5. Decimal to fraction converter -               │
│ RapidTables.com score=0.08                       │
│ (https://www.rapidtables.com/convert/number/deci │
│ mal-to-fraction.html)                            │
│    | Decimal | Fraction |  --- | | 0.00001 |     │
│ 1/100000 | | 0.0001 | 1/10000 | | 0.001 | 1/1000 │
│ | | 0.01 | 1/100 | | 0.08333333 | 1/12 | |       │
│ 0.09090909 | 1/11 | | 0.1 | 1/10 | | 0.11111111  │
│ | 1/9 | | 0.125 | 1/8 | | 0.14285714 | 1/7 | |   │
│ 0.16666667 | 1/6 | | 0.2 | 1/5 | | 0.22222222    │
│ |...                                             │
╰──────────────────────────────────────────────────╯
╭────────────────── Final Answer ──────────────────╮
│ The fraction of Taiwan's population to Japan's   │
│ population as of 2025 is approximately 0.191.    │
╰──────────────────────────────────────────────────╯
```

</details>

#### 2. Task 2: Display Specification Comparison

The agent effectively gathers detailed specifications for both the iPhone 15 and Samsung Galaxy S24, demonstrating its ability to extract relevant information from multiple sources. It then synthesizes this information into a clear and concise comparison, highlighting the key differences between the two devices.

<details>
<summary>click to expand </summary>

```plain
────────────────────── Task 2 ──────────────────────
╭────────────────────── User ──────────────────────╮
│ Compare the main display specs of iPhone 15 and  │
│ Samsung S24.                                     │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I need to find the main display         │
│ specifications for both the iPhone 15 and        │
│ Samsung S24 to compare them.                     │
│ Action: Search                                   │
│ Action Input: iPhone 15 display specifications   │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: The iPhone 15        │
│ features a 6.1-inch Super Retina XDR OLED        │
│ display with a resolution of 2556 x 1179 pixels  │
│ and a pixel density of 460 PPI. It supports      │
│ HDR10 and has a max brightness of 2,000 nits.    │
│ The display is protected by Ceramic Shield.      │
│ Top results:                                     │
│ 1. iPhone 15 - Wikipedia score=0.96              │
│ (https://en.wikipedia.org/wiki/IPhone_15)        │
│    ## Hardware  ### Display  The iPhone 15       │
│ features a 6.1-inch (155 mm) display with Super  │
│ Retina XDR OLED technology at a resolution of    │
│ 2556×1179 pixels and a pixel density of about    │
│ 460 PPI with a refresh rate of 60 Hz. The iPhone │
│ 15 Plus features a 6.7-inch (170 mm) display     │
│ wit...                                           │
│ 2. iPhone 15 - Tech Specs score=0.93             │
│ (https://support.apple.com/en-us/111831)         │
│    The iPhone 15 display has rounded corners     │
│ that follow a beautiful curved design, and these │
│ corners are within a standard rectangle. When    │
│ measured as a standard rectangular shape, the    │
│ screen is 6.12 inches diagonally (actual         │
│ viewable area is less).  ### Splash, Water, and  │
│ Dust...                                          │
│ 3. iPhone 15 Screen Sizes - Use Your Loaf        │
│ score=0.92                                       │
│ (https://useyourloaf.com/blog/iphone-15-screen-s │
│ izes/)                                           │
│    ### iPhone 15  The iPhone 15 gains some of    │
│ the features of the now discontinued iPhone 14   │
│ Pro such as the dynamic island, and the A16      │
│ Bionic chip.   A16 Bionic chip (6-core CPU,      │
│ 5-core GPU, 16-core Neural Engine)  Display:     │
│ 6.1" Super Retina XDR OLED  Screen resolution    │
│ (points)...                                      │
│ 4. iPhone 15: viewport, screen size, CSS pixel   │
│ ratio, cross- ... score=0.91                     │
│ (https://blisk.io/devices/details/iphone-15)     │
│    #### Specification (Summary)  |  |  |  --- |  │
│ | Release Date | Friday, September 22, 2023 | |  │
│ Vendor | Apple | | Device Type | phone | |       │
│ Operating System | iOS | | Display | Super       │
│ Retina XDR OLED, 91.3 cm2, 19.5:9, ~86.4%        │
│ screen-to-body ratio | | Screen Size             │
│ (Resolution) Width...                            │
│ 5. Apple iPhone 15 - Full phone specifications - │
│ GSMArena.com score=0.91                          │
│ (https://www.gsmarena.com/apple_iphone_15-12559. │
│ php)                                             │
│    |  |  |  |  ---  | Display | Type | Super     │
│ Retina XDR OLED, HDR10, Dolby Vision, 1000 nits  │
│ (HBM), 2000 nits (peak) | | Size | 6.1 inches,   │
│ 91.3 cm2 (~86.4% screen-to-body ratio) | |       │
│ Resolution | 1179 x 2556 pixels, 19.5:9 ratio    │
│ (~461 ppi density) | | Protection | Ceramic      │
│ Shield...                                        │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: Now I need to find the display          │
│ specifications for the Samsung S24 to complete   │
│ the comparison.                                  │
│ Action: Search                                   │
│ Action Input: Samsung S24 display specifications │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: The Samsung Galaxy   │
│ S24 has a 6.2-inch FHD+ AMOLED display with a    │
│ 120Hz refresh rate. The S24 Plus has a 6.7-inch  │
│ QHD+ AMOLED display. The S24 Ultra has a         │
│ 6.8-inch QHD+ AMOLED display.                    │
│ Top results:                                     │
│ 1. Galaxy S24 | Samsung Mobile Press score=1.00  │
│ (https://www.samsungmobilepress.com/media-assets │
│ /galaxy-s24?tab=specs)                           │
│    |  |  |  |  |  |  ---  ---  | Galaxy S24 | |  │
│ | | | | Display | 6.2-inch FHD+\ Dynamic AMOLED  │
│ 2X Display   Super Smooth 120Hz refresh rate     │
│ (1~120Hz)  Vision booster | | | \Measured        │
│ diagonally, Galaxy S24’s screen size is 6.2-inch │
│ in the full rectangle and 6.0-inch with          │
│ accounti...                                      │
│ 2. Samsung Galaxy S24 - Full phone               │
│ specifications - GSMArena.com score=1.00         │
│ (https://www.gsmarena.com/samsung_galaxy_s24-127 │
│ 73.php)                                          │
│    |  |  |  |  ---  | Display | Type | Dynamic   │
│ LTPO AMOLED 2X, 120Hz, HDR10+, 2600 nits (peak)  │
│ | | Size | 6.2 inches, 94.4 cm2 (~90.9%          │
│ screen-to-body ratio) | | Resolution | 1080 x    │
│ 2340 pixels, 19.5:9 ratio (~416 ppi density) | | │
│ Protection | Corning Gorilla Glass Victus 2 |    │
│ |...                                             │
│ 3. Samsung Galaxy S24 - Wikipedia score=1.00     │
│ (https://en.wikipedia.org/wiki/Samsung_Galaxy_S2 │
│ 4)                                               │
│    ## Specifications    ### Display    The       │
│ Galaxy S24 and S24+ use a "Dynamic AMOLED 2X"    │
│ display with HDR10+ support, 2600 nits of peak   │
│ brightness, LTPO backplane, "dynamic tone        │
│ mapping" technology, and Corning Gorilla Glass   │
│ Victus 2. The Galaxy S24 FE has 1900 nits o...   │
│ 4. Samsung Galaxy S24 screen size for every      │
│ model - TechRadar score=1.00                     │
│ (https://www.techradar.com/phones/samsung-phones │
│ /samsung-galaxy-s24-screen-size)                 │
│    Samsung Galaxy S24 hands on handheld front    │
│ straight  Both the Galaxy S24 and Galaxy S24     │
│ Plus have received a 0.1-inch display size       │
│ upgrade without increasing their respective      │
│ overall sizes; this is all thanks to slimmer     │
│ bezels. So the Galaxy S24 has a 6.2-inch display │
│ and the...                                       │
│ 5. Galaxy S24 Series: Discover all the new and   │
│ exciting features! score=1.00                    │
│ (https://www.samsung.com/au/members/whats-new/ga │
│ laxy-s24-series-discover-all-the-new-and-excitin │
│ g-features/?srsltid=AfmBOopuPEpUuqq1rXAQD16D_3hr │
│ zuvb-D_wRnRscjzaWYvq7iJbVOft)                    │
│    11 Measured diagonally, Galaxy S24 Ultra's    │
│ screen size is 6.8 inches in the full rectangle  │
│ and 6.8 inches accounting for the rounded        │
│ corners, Galaxy S24's screen size is 6.2 inches  │
│ in the full rectangle and 6 inches accounting    │
│ for the rounded corners and Galaxy S24+'s screen │
│ s...                                             │
╰──────────────────────────────────────────────────╯
╭────────────────── Final Answer ──────────────────╮
│ The main display specifications are as follows:  │
│                                                  │
│ **iPhone 15:**                                   │
│ - Display Type: Super Retina XDR OLED            │
│ - Size: 6.1 inches                               │
│ - Resolution: 2556 x 1179 pixels                 │
│ - Pixel Density: 460 PPI                         │
│ - Refresh Rate: 60 Hz                            │
│ - Max Brightness: 2,000 nits                     │
│ - Protection: Ceramic Shield                     │
│                                                  │
│ **Samsung Galaxy S24:**                          │
│ - Display Type: Dynamic AMOLED 2X                │
│ - Size: 6.2 inches                               │
│ - Resolution: 1080 x 2340 pixels                 │
│ - Pixel Density: 416 PPI                         │
│ - Refresh Rate: 120 Hz                           │
│ - Max Brightness: 2,600 nits                     │
│ - Protection: Corning Gorilla Glass Victus 2     │
│                                                  │
│ The iPhone 15 has a slightly smaller display     │
│ with a higher resolution and pixel density,      │
│ while the Samsung S24 features a higher refresh  │
│ rate and peak brightness.                        │
╰──────────────────────────────────────────────────╯
```

</details>

#### 3. Task 3: CEO Identification

The agent encounters conflicting information regarding the CEO of Morphic AI. It identifies the discrepancy and takes the initiative to verify the correct information through additional searches. Ultimately, it successfully determines that Jaynti Kanani is the current CEO, showcasing its ability to handle and resolve conflicting data.

<details>
<summary>click to expand </summary>

```plain
────────────────────── Task 3 ──────────────────────
╭────────────────────── User ──────────────────────╮
│ Who is the CEO of the startup 'Morphic' AI       │
│ search?                                          │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I need to find information about the    │
│ startup 'Morphic' and its CEO.                   │
│ Action: Search                                   │
│ Action Input: Morphic AI search CEO              │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: Weston Baker is the  │
│ CEO of Morphic, an AI-powered web design         │
│ platform. He founded Morphic to help startups    │
│ build professional websites quickly. Morphic     │
│ aims to reduce the time and cost of web design   │
│ for businesses.                                  │
│ Top results:                                     │
│ 1. Morphic holding CEO sells shares worth over   │
│ $1.2 million score=1.00                          │
│ (https://www.investing.com/news/company-news/mor │
│ phic-holding-ceo-sells-shares-worth-over-12-mill │
│ ion-93CH-3514690)                                │
│    The acquisition, anticipated to finalize in   │
│ the third quarter of 2024, is seen as a          │
│ strategic move for Eli Lilly, potentially        │
│ positioning the company to enter the first-line  │
│ ulcerative colitis market. Morphic's lead drug,  │
│ MORF-057, currently under multiple phase 2       │
│ studies for...                                   │
│ 2. Morphic - 2026 Company Profile & Team -       │
│ Tracxn score=1.00                                │
│ (https://tracxn.com/d/companies/morphic/__QREWaD │
│ zuHM-XW-PFwSgyqKupVzTD3aOF5VD9L0I9mSw)           │
│    Jaynti Kanani is the current CEO of Morphic.  │
│ They are also angel investors in 19 startups,    │
│ including Polygon.  Morphicis headquartered in   │
│ San Francisco, United States.  Morphicis a       │
│ funded company,having raised a total of  $\\\\\  │
│ in its 1st and only funding round.  Explore      │
│ our...                                           │
│ 3. Morphic Therapeutic Expands Leadership with   │
│ Key Appointments in ... score=1.00               │
│ (https://www.biospace.com/morphic-therapeutic-ex │
│ pands-leadership-with-key-appointments-in-clinic │
│ al-and-corporate-development)                    │
│    Marc Schegerin, MD, COO and CFO of Morphic    │
│ Therapeutic, stated, “Aaron’s broad experience   │
│ and strategic perspectives will be critical as   │
│ we expand our clinical pipeline. Aaron will      │
│ continue to oversee our partnering efforts,      │
│ commercial planning and integrate seamlessly     │
│ with ou...                                       │
│ 4. Morphic Management Team - CB Insights         │
│ score=0.98                                       │
│ (https://www.cbinsights.com/company/morphic/peop │
│ le)                                              │
│    Founder, Chief Executive Officer  Current  |  │
│ |  |  --- | | Name | Weston Baker | | Work       │
│ History | Skidmore, Owings & Merrill, and Foster │
│ + Partners | | Title | Founder, Chief Executive  │
│ Officer | | Status | Current |  Name  Weston     │
│ Baker  Work History  Skidmore, Owings &          │
│ Merril...                                        │
│ 5. Weston Baker - Morphic - LinkedIn score=0.98  │
│ (https://www.linkedin.com/in/westonbaker)        │
│    # Weston Baker Founder @ Morphic | AI-Powered │
│ Websites for VCs & Growth Firms | Automating     │
│ High-End Design for Startups New York, New York, │
│ United States, US   500 connections, 7515        │
│ followers  ## About 🚀 Helping Startups & Growth │
│ Firms Build Exceptional Websites—Fast  I work    │
│ w...                                             │
╰──────────────────────────────────────────────────╯
╭─────────────────── Agent Plan ───────────────────╮
│ Thought: I have found conflicting information    │
│ regarding the CEO of Morphic. Some sources       │
│ indicate Weston Baker, while others mention      │
│ Jaynti Kanani. I need to verify which one is     │
│ correct.                                         │
│ Action: Search                                   │
│ Action Input: current CEO of Morphic AI search   │
│ Weston Baker or Jaynti Kanani?                   │
╰──────────────────────────────────────────────────╯
╭────────────────── Observation ───────────────────╮
│ Observation: Direct answer: Jaynti Kanani is the │
│ current CEO of Morphic AI. He previously         │
│ co-founded Polygon. Weston Baker is not          │
│ associated with Morphic AI.                      │
│ Top results:                                     │
│ 1. Jaynti Kanani - Founder CEO at Morphic        │
│ score=0.79                                       │
│ (https://www.getprog.ai/profile/1692593)         │
│    Jaynti Kanani is a founder and CEO with 13    │
│ years of engineering experience, best known as a │
│ co-founder of Polygon (Matic) and currently      │
│ leading Morphic from the UAE. He blends          │
│ protocol-level blockchain engineering—authoring  │
│ changes to the Bor consensus, Heimdall           │
│ validator, and...                                │
│ 2. Jaynti Kanani Email & Phone Number | Morphic  │
│ Founder and CEO Contact Information score=0.72   │
│ (https://rocketreach.co/jaynti-kanani-email_7573 │
│ 2683)                                            │
│    see less    ### Jaynti Kanani Summary  Jaynti │
│ Kanani, based in United Arab Emirates, is        │
│ currently a Founder and CEO at Morphic. Jaynti   │
│ Kanani brings experience from previous roles at  │
│ Polygon Technology, Housing.com and Function     │
│ space. Jaynti Kanani holds a 2007 - 2011         │
│ Bachelor...                                      │
│ 3. Jaynti Kanani - Founder & CEO at Morphic |    │
│ The Org score=0.71                               │
│ (https://theorg.com/org/morphic-1/org-chart/jayn │
│ ti-kanani)                                       │
│    Pricing  Morphic  Unverified  # Jaynti Kanani │
│ ### Founder & CEO  Contact  Jaynti Kanani, a     │
│ seasoned professional in the tech industry, has  │
│ a rich and varied career history. From           │
│ co-founding Polygon Technology and serving as    │
│ the CEO to working as a Data Scientist at        │
│ Housing.co...                                    │
│ 4. Biography of Jaynti Kanani: Co-Founder & CEO  │
│ of Polygon- Entrepreneur score=0.63              │
│ (https://www.werisebyliftingothers.in/2024/08/bi │
│ ography-of-jaynti-kanani-co-founder.html)        │
│    Transitioning Leadership  In October 2023,    │
│ Jaynti Kanani announced his decision to step     │
│ down from his role as CEO of Polygon. He chose   │
│ to focus on new ventures while continuing to     │
│ support Polygon from a distance. His departure   │
│ marked a significant shift in the company’s      │
│ leader...                                        │
│ 5. Jaynti Kanani - 2026 Portfolio & Founded      │
│ Companies - Tracxn score=0.59                    │
│ (https://tracxn.com/d/people/jaynti-kanani/__Uqy │
│ LQxE7Dvy1UH2eKS66_43H7DMHHtGL5CNToE6WqTU)        │
│    Most viewed in 2019  ## About Jaynti Kanani   │
│ Jaynti Kananiis an entrepreneurand an angel      │
│ investorbased out of United Arab Emirates. Their │
│ journey in the startup ecosystem started in 2017 │
│ through Polygon. Jaynti Kanani has founded 2     │
│ companies. They are currently acting as the f... │
╰──────────────────────────────────────────────────╯
╭────────────────── Final Answer ──────────────────╮
│ Jaynti Kanani is the current CEO of Morphic AI.  │
│ He previously co-founded Polygon.                │
╰──────────────────────────────────────────────────╯
```

</details>

Apify is one of the most powerful scraping tools out there. It gives you access to thousands of pre-built scrapers — Google Maps, Facebook, LinkedIn, Amazon, you name it — and with the CLI, it's easier than ever to have your AI coding agent set this up for you. Just pass this document to Claude Code, OpenClaw, Hermes or whatever you're using, along with what you want to scrape, and let it handle the rest.

This guide covers what you need to know to get started, how to prompt your agent to build scraping pipelines, and some best practices I learned building one myself.


What Apify actually is

Think of Apify as an app store for scrapers. Each scraper is called an "Actor." There are thousands of them, built by Apify and the community. You don't write scraping code — you pick an Actor, give it inputs (what to search for, where, how many results), and it runs on Apify's cloud and gives you structured data back.

Examples of what you can scrape:
- Google Maps businesses (name, phone, email, reviews, address)
- Facebook pages (contact info, about section, posts)
- LinkedIn profiles and companies
- Amazon products and prices
- Instagram accounts and posts
- Any website with a custom scraper

The CLI lets you do all of this from your terminal — which means any AI coding agent can do it too.


How to prompt your agent to build scraping pipelines

The Apify CLI is a terminal tool, which means Claude Code, OpenClaw, or any agent with terminal access can use it directly. But the key is how you prompt it. Here's the workflow that actually works well, based on how I built a full scraping pipeline in a single session.


Step 1: Start with a plan, not a scrape

Don't jump straight into running commands. Start by telling your agent what you're trying to accomplish and have it create a plan first. Something like:

"I need to scrape all coffee shops in Austin, Texas from Google Maps — name, phone, website, email, and reviews. Create a plan for how we'd do this with Apify."

Your agent will research the right Actors, figure out input parameters, estimate costs, and lay out the pipeline before touching anything. This saves you from burning credits on a scrape that's configured wrong.


Step 2: Give your agent a CLI reference

If you have documentation for the tools you want your agent to use, put it in your project folder. I dropped an Apify CLI reference doc into the project directory so the agent knew every available command — how to run Actors, download results, check run status, abort jobs, etc. Without this, it will figure it out, but with it, it moves faster and doesn't guess.

You can point your agent to the Actor page on apify.com and let it read the input schema, or include the CLI reference at the end of this guide in your project.


Step 3: Test small, then scale

This is the most important part. Tell your agent to do small test runs first — 3 to 5 results max — and inspect the output before scaling up.

Here's what that looks like in practice:

First test: "Run the Google Maps scraper for 'coffee shop' in Austin, Texas, max 3 results. Show me what fields we get back."

Your agent runs it, downloads the results, and shows you the data. You check: are the businesses actually in the right area? Do we get phone numbers? Websites? Is the geolocation correct?

Second test: "Now try it with 2 search terms — 'coffee shop' and 'bakery' — still max 3 each. Make sure multi-query works."

It runs it, confirms both search terms return separate results, and checks for deduplication.

Third test: "Enable contact extraction and run it again. I want to see if we get emails from their websites."

It runs it, and now you can see which businesses have emails pulled directly from their websites. You didn't waste credits on a 5,000-business scrape to find this out.

Each test costs pennies. A full scrape configured wrong costs real money. Always test incrementally.


Step 4: Save the working configuration

Once the tests look right, tell your agent to save the working input as a file and write a reference document. Something like:

"The scrape is working. Save the input config as a JSON file for the full run, and write a reference doc so we can repeat this later."

Now you have:
- A tested input.json you can rerun anytime
- A reference doc explaining what each parameter does, what the output looks like, and how to process results

This is the difference between a one-off experiment and a repeatable pipeline. Next time you (or your agent) need to run this scrape, the reference doc has everything — no re-research needed.


Step 5: Chain and iterate

Once one scrape is working, you can layer on more. For example:
- A Google Maps scrape might get emails for about half the businesses from their websites
- You then run a Facebook page scraper on the ones that were missing emails
- Facebook pages almost always list a contact email, so you fill in most of the gaps

Tell your agent to build each step the same way: small test first, verify output, then scale. Each Actor is a building block. You can chain them together into a full pipeline — the output of one becomes the input for the next.


What to give your agent before you start:
- Make sure your Apify account is logged in (run apify login -t YOUR_TOKEN before starting the session)
- Tell it what you want to scrape and where
- Tell it what output format you need (JSON, CSV, etc.)
- Tell it your budget constraints so it can set appropriate limits
- Drop any relevant docs (CLI reference, Actor documentation) into the project folder


Getting set up

Install:
  brew install apify-cli

Or:
  npm install -g apify-cli

Log in with your API token (get it from console.apify.com under Settings > Integrations):
  apify login -t YOUR_TOKEN

Verify it worked:
  apify info

That's it. You're ready to scrape.


The core workflow

Everything in Apify follows the same pattern:

1. Find an Actor on apify.com/store (or tell your agent what you want to scrape and let it find one)
2. Run it with apify call
3. Get your results with apify datasets get-items

Here's a real example — scraping coffee shops in Austin from Google Maps:

  apify call compass/crawler-google-places -i '{
    "searchStringsArray": ["coffee shop"],
    "countryCode": "us",
    "state": "Texas",
    "city": "Austin",
    "maxCrawledPlacesPerSearch": 100,
    "language": "en",
    "proxyConfig": {"useApifyProxy": true}
  }'

When it finishes, it prints a dataset ID. Grab your results:

  apify datasets get-items DATASET_ID > results.json

Or as CSV:

  apify datasets get-items DATASET_ID --format csv > results.csv

That's the entire workflow. Find actor, call it, download results.


Using input files instead of inline JSON

For anything beyond a simple test, save your inputs to a file. This is easier to read, edit, and reuse:

  apify call compass/crawler-google-places --input-file input.json

Your input.json:

  {
    "searchStringsArray": ["coffee shop", "bakery", "brunch restaurant"],
    "countryCode": "us",
    "state": "Texas",
    "city": "Austin",
    "maxCrawledPlacesPerSearch": 200,
    "language": "en",
    "skipClosedPlaces": true,
    "proxyConfig": {"useApifyProxy": true}
  }

This is also the best way to hand off scraping tasks to your agent — give it the Actor name and let it build the input file for you.


What to watch out for

Pay-per-event pricing can surprise you. Many popular Actors charge per result, not per compute time. At $4/1,000 places for Google Maps, a scrape of 5,000 businesses costs $20. Know the pricing before you run a big job. Always check the Actor's page on apify.com for its pricing model.

Always start small. Test with 3-5 results before running a full scrape. Verify the data looks right and you're getting the fields you need. This applies to every Actor, not just Google Maps.

Read the Actor's input schema. Every Actor has different parameters, required fields, and quirks. Some need proxy configuration, some need specific geolocation settings, some have optional enrichment features that change the output completely. Your agent can read the schema from the Actor's page, but you should understand what's going in.

CSV export is messy for complex data. Actors that return nested objects (arrays, sub-objects) produce CSVs with hundreds of columns. JSON is almost always better for processing. Convert to a clean CSV yourself after picking the fields you actually need.

Runs happen in the cloud. When you run apify call, the Actor runs on Apify's servers, not your machine. You can close your terminal and check on it later with:
  apify runs info RUN_ID

Save your results locally. Apify stores results in datasets on their platform, but those can get cleaned up over time. Always download and save results to your project after a run.


Useful commands beyond the basics

Check what's running:
  apify runs ls

See the logs of a run (useful for debugging):
  apify runs log RUN_ID

Kill a run that's taking too long or looks wrong:
  apify runs abort RUN_ID

List your datasets (past results):
  apify datasets ls

Paginate through large results:
  apify datasets get-items DATASET_ID --limit 100 --offset 200


Chaining Actors together

This is where it gets powerful. You can use the output of one Actor as the input for another.

Example: scrape Google Maps to get business listings with Facebook page URLs, then run a Facebook scraper on those URLs to get emails that weren't on the website.

Step 1 — Google Maps scrape:
  apify call compass/crawler-google-places --input-file google-maps-input.json

Step 2 — Extract Facebook URLs from results and feed them to the Facebook scraper:
  apify call apify/facebook-pages-scraper -i '{
    "startUrls": [
      {"url": "https://www.facebook.com/somebusiness"},
      {"url": "https://www.facebook.com/anotherbusiness"}
    ],
    "scrapeAbout": true,
    "scrapePosts": false,
    "scrapeReviews": false,
    "proxyConfiguration": {"useApifyProxy": true}
  }'

In practice, you'd have your agent extract the Facebook URLs from the first scrape's results and build the input for the second scrape automatically. Then merge the results — emails from Facebook fill in the gaps from the Google Maps scrape.


Popular Actors worth knowing about

Google Maps Scraper (compass/crawler-google-places)
Scrapes business listings from Google Maps. Gets name, address, phone, website, reviews, rating, categories, opening hours. Can also visit websites to extract emails and social links.

Facebook Pages Scraper (apify/facebook-pages-scraper)
Extracts page info including email, phone, website, address, and social links from public Facebook business pages. Can also pull posts and reviews.

Instagram Scraper (apify/instagram-scraper)
Profiles, posts, hashtags, comments, and followers.

LinkedIn Scraper (curious_coder/linkedin-scraper)
Company pages and employee profiles. Use carefully — LinkedIn is aggressive about blocking scrapers.

Amazon Scraper (junglee/amazon-crawler)
Product listings, prices, reviews, seller info.

Website Content Crawler (apify/website-content-crawler)
General-purpose crawler that extracts text content from any website. Good for feeding content to AI or building datasets.


How pricing actually works

There are two layers: your platform plan and what each Actor charges. Everything comes out of one credit pool.

Your plan gives you a monthly usage allowance:
- Free: $5 in credits (no monthly fee)
- Starter: $29/mo, up to $200 in usage
- Scale: $199/mo, up to $1,000 in usage
- Business: $999/mo, up to $5,000 in usage

Most popular Actors charge per result (pay-per-event). The Google Maps scraper costs $0.004 per place ($4/1,000), the Facebook Pages scraper about $0.01 per page. These charges come out of your plan credits — there's no separate bill. Some community-built Actors don't charge per result and just use your compute time instead, but those are harder to predict cost-wise.

The free $5 gets you roughly 1,000-1,200 Google Maps results — enough for testing and one small run. For bigger projects, the Starter plan at $29/mo gives you $200 in usage, which covers a lot of scraping.

You can set a maximum cost per run to prevent a misconfigured scrape from draining your credits. On the free plan you're blocked when credits run out. On paid plans you can go over as overage up to your plan's limit.

---

Hope this helped!

🚀 Want This Set Up for Your Business?

I help businesses set up OpenClaw and build custom AI automations — so you can run more with less. 
Work with me → https://moritzkremb.com

🔥 Join My Community for More Resources

Get more free prompts, guides, and AI automation tips.
Join Prompt Warrior Community → https://www.skool.com/promptwarrior

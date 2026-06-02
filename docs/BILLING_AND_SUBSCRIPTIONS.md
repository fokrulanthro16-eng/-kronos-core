# KRONOS CORE — Billing & Subscriptions

## Plan tiers

| Plan | Price | Reports/day | History | PDF | Team |
|---|---|---|---|---|---|
| Free | $0/mo | 10 | No | No | 1 |
| Starter | $49/mo | 100 | Yes | Yes | 3 |
| Pro | $149/mo | Unlimited | Yes | Yes | 25 |
| Enterprise | Custom | Unlimited | Yes | Yes | Unlimited |

## Environment variables

Add these to your root `.env` (never commit real values):

```env
STRIPE_SECRET_KEY=sk_live_...          # Backend only — NEVER expose to frontend
STRIPE_WEBHOOK_SECRET=whsec_...        # Used to verify Stripe webhook signatures
STRIPE_PRICE_STARTER=price_...         # Stripe Price ID for Starter plan
STRIPE_PRICE_PRO=price_...             # Stripe Price ID for Pro plan
STRIPE_PRICE_ENTERPRISE=price_...      # Stripe Price ID for Enterprise plan
```

Add this to `frontend/.env.local`:

```env
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_live_...   # Safe for browser bundle
```

## Stripe setup steps

1. Create a Stripe account at https://stripe.com
2. Go to **Dashboard → Developers → API keys** — copy Secret key and Publishable key
3. Go to **Products → Add product** — create Starter, Pro, Enterprise products with monthly prices
4. Copy the **Price ID** for each plan (starts with `price_`)
5. Go to **Developers → Webhooks → Add endpoint**:
   - URL: `https://your-api-domain.com/api/v1/billing/webhook`
   - Events: `checkout.session.completed`, `customer.subscription.deleted`, `customer.subscription.updated`
   - Copy the **Signing secret** (`whsec_...`)
6. Add all values to `.env` and restart the backend

## Checkout session flow

```
Frontend → POST /api/v1/billing/create-checkout-session { plan: "pro" }
         ← { checkout_url: "https://checkout.stripe.com/..." }
Frontend → window.location.href = checkout_url
User completes payment on Stripe-hosted page
Stripe → POST /api/v1/billing/webhook (checkout.session.completed)
Backend updates user plan in Supabase
User redirected to /account?upgrade=success
```

## Webhook concept

The webhook endpoint at `POST /api/v1/billing/webhook`:
- Verifies the Stripe signature using `STRIPE_WEBHOOK_SECRET`
- Handles `checkout.session.completed` → activate plan
- Handles `customer.subscription.deleted` → downgrade to Free
- Returns 400 on invalid signatures — never processes unverified payloads

## Local demo mode behaviour

When `STRIPE_SECRET_KEY` is not set:
- `GET /api/v1/billing/status` → `demo_mode: true`
- `GET /api/v1/billing/plans` → returns all plans with `demo_mode: true`
- `POST /api/v1/billing/create-checkout-session` → returns setup instructions, no Stripe call
- `POST /api/v1/billing/webhook` → returns demo-mode message, no processing
- Frontend pricing page shows demo mode warning banner
- Account page shows current plan as "Free (Demo)"

## Security notes

- **Never** expose `STRIPE_SECRET_KEY` to the frontend — it's server-side only
- **Never** commit `.env` to version control (`.gitignore` already protects it)
- **Always** verify webhook signatures in production using `STRIPE_WEBHOOK_SECRET`
- Use Stripe test keys (`sk_test_...`) for development, live keys only in production
- Stripe Checkout handles all PCI-DSS compliance — no card data touches your server

## What remains for production billing

- Store Stripe `customer_id` and subscription status in `subscription_status` table (Supabase)
- Enforce plan limits per user (reports_per_day, history, PDF) based on subscription
- Add upgrade success/cancel pages
- Add invoice download for paid users
- Add plan management (cancel, downgrade) in account page

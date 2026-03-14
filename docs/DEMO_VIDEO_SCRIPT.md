# PriceIntel — Demo Video Script

**Video:** Product Search & Price Comparison Walkthrough  
**Duration:** ~5–8 minutes  
**Recording tool:** OBS Studio / Loom / any screen recorder

---

## Pre-Recording Checklist

- [ ] Backend running: `python manage.py runserver`
- [ ] Frontend running: `npm run dev`
- [ ] Browser is at `http://localhost:5173`
- [ ] Browser window is at 1280×720 or larger
- [ ] Test data ready: have a clear product image (e.g., laptop, headphones, phone)
- [ ] At least 1 wishlist item and 1 price alert already created for the demo
- [ ] Log out so you can show the login flow

---

## Scene-by-Scene Script

---

### Scene 1: Opening (0:00–0:30)

**Screen:** PriceIntel login page

**Narration:**
> "Welcome to PriceIntel — a visual product search and price comparison platform. With PriceIntel, you can take a photo of any product and instantly compare prices across Amazon, eBay, and Walmart. Let me walk you through the main features."

---

### Scene 2: Login & Registration (0:30–1:15)

**Screen:** Login page → Registration page

**Actions:**
1. Show the login form
2. Click "Create Account"  
3. Fill in name, email, password
4. Hit Register — shows Home page
5. Optionally: log out, log back in with email + password

**Narration:**
> "Creating an account is quick. Fill in your details, and you're ready to go. Login uses a secure JWT token system — your session automatically refreshes without you needing to re-enter your password."

---

### Scene 3: Image Upload & Recognition (1:15–2:30)

**Screen:** Home page → Upload page

**Actions:**
1. Click "Upload Image" button
2. Drag a product photo onto the upload zone
3. Show the file being accepted (green checkmark or preview)
4. Watch the loading spinner while AI processes

**Narration:**
> "This is the core feature. I'll upload a photo of wireless headphones. The image is sent to our Django backend, where a CNN model analyzes it and identifies the product category and keywords."

4. Show recognition result: "Wireless Headphones — 89% confidence"

**Narration:**
> "The AI identified this as wireless headphones with 89% confidence. This query is then sent to our scrapers."

---

### Scene 4: Price Comparison Results (2:30–4:00)

**Screen:** Results / Compare page

**Actions:**
1. Results appear (Amazon, eBay, Walmart cards)
2. Point out the "Best Deal" badge
3. Show the price summary bar (lowest, highest, average)
4. Hover over a card to show the hover effect
5. Click "View Deal" — opens retailer page in new tab (close it)
6. Click "❤️" on one card — saves to wishlist
7. Click "⊕ Compare" on two more cards

**Narration:**
> "Here are live prices from all three platforms. The best deal is highlighted — Sony WH-1000XM5 at Walmart for $249.99. I can open any listing directly, save it to my Wishlist, or add it to the comparison basket."

---

### Scene 5: Side-by-Side Comparison (4:00–4:30)

**Screen:** Comparison overlay

**Actions:**
1. Show the floating comparison basket at the bottom
2. Click "Compare Now"
3. Show the side-by-side overlay with 3 products

**Narration:**
> "The comparison overlay lets me view up to 3 products side-by-side — price, rating, shipping, and availability — so I can make an informed decision at a glance."

---

### Scene 6: Wishlist (4:30–5:00)

**Screen:** Wishlist page

**Actions:**
1. Navigate to Wishlist
2. Show saved items with prices
3. Click "View Deal" on one

**Narration:**
> "My saved products are here in the Wishlist. They're preserved between sessions so I can come back and check them later."

---

### Scene 7: Price Alerts (5:00–5:45)

**Screen:** Price Alerts page

**Actions:**
1. Navigate to Alerts
2. Show existing alerts with statuses
3. Click "+ New Alert"
4. Fill: product name "Sony WH-1000XM5", target price "$230"
5. Save it — shows in list with "Active" status

**Narration:**
> "Price Alerts let me set a target price. The system monitors prices automatically and can notify me when the price drops to my target. Active alerts are checked nightly."

---

### Scene 8: Dashboard (5:45–7:00)

**Screen:** Dashboard page

**Actions:**
1. Navigate to Dashboard
2. Show the 4 overview cards (searches, alerts, wishlist count, today's searches)
3. Show the price history chart (line chart)
4. Show the recent searches list
5. Show the recommendations section

**Narration:**
> "The Dashboard gives me a complete overview of my activity. The price history chart shows how prices have changed over time for the products I've searched. I can also see personalized recommendations based on my search patterns."

---

### Scene 9: Profile & Security (7:00–7:30)

**Screen:** Profile page

**Actions:**
1. Navigate to Profile
2. Show the account details section
3. Show "Change Password" option
4. Briefly mention data export and account deletion (GDPR)

**Narration:**
> "In your profile, you can update your information, change your password, and for privacy, you can export all your data as a JSON file or permanently delete your account."

---

### Scene 10: Closing (7:30–8:00)

**Screen:** Home page

**Narration:**
> "PriceIntel brings together AI product recognition, real-time web scraping, and a comprehensive user experience — all in a secure, production-ready package. Thank you for watching!"

---

## Recording Tips

- Speak at a moderate pace
- Pause briefly after each screen transition
- Keep browser zoom at 100%
- Hide browser bookmarks bar for cleaner look
- Use a 4K or 1080p recording resolution
- Add light background music at 10–15% volume in editing

---

## Suggested Recording Software

| Tool | Platform | Free |
|---|---|---|
| OBS Studio | Windows/Mac/Linux | ✅ |
| Loom | Browser extension | ✅ (up to 5 min free) |
| ShareX | Windows | ✅ |
| Camtasia | Windows/Mac | ❌ (trial available) |

---

## Post-Processing

1. Trim start/end silence
2. Add title card: "PriceIntel — Visual Product Search & Price Comparison"
3. Add end card with project details
4. Export as MP4 at 1080p, 30fps
5. Place in `/demo-video/` folder

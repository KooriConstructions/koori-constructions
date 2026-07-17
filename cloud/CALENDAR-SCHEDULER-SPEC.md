# Calendar Scheduler — spec (for the AI admin)

Turns trade/supplier/delivery emails (and texts, once SMS is wired) into colour-coded
calendar events on the **Koori Active Jobs** calendar. Implemented in `koori_admin.py`.

## Colours = Outlook Categories (create these 5 once, Categorize → New Category)
| Category | Colour | Contents |
|---|---|---|
| Quotes | 🔵 Blue | quote site-visits, measures, follow-ups, new leads |
| Trades | 🟢 Green | subbie bookings — **trade invited to the event** |
| Suppliers/Deliveries | 🟠 Orange | material deliveries/pickups, PC items arriving |
| Crew | 🟣 Purple | Koori crew site days (Glenn/Bailey/Adam/Mark) |
| Personal | ⚫ Grey | non-work |

## Rules
- Read inbound mail; an LLM extracts any real date/time + who it's with.
- Create the event on **Koori Active Jobs** calendar, title `Q-ref — scope — who`,
  address + job ref + contact in the body, tagged the right category/colour.
- **If the booking is with a trade, add their email as an attendee** (they get the
  invite + accept — same as the Belmont North events).
- If a date changes, update the existing event (no duplicates).
- Never accept/decline on Brad's behalf; never send.

## Requires
- Graph delegated **Calendars.ReadWrite** (+ Mail.ReadWrite for the reply drafts).
- Texts need the SMS→Zapier bridge; email dates work today.

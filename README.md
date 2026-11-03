
# SIDE B.

**Discover the sound. Explore the artist.**

SIDE B. is a full-stack music discovery and merchandise platform developed for CST150 Web Technologies Project 3 at SAE.

The website combines detailed artist profiles, music discovery and an online shopping experience.

## Project Overview

SIDE B. allows visitors to explore a growing collection of musicians, discover their music and browse artist-related merchandise.

Each artist has a dedicated profile featuring their background, musical identity, releases, Spotify integration and merchandise collection.

The platform is designed to support multiple artists through a database-driven system rather than hardcoded individual artist pages.

### Initial Example Artists

- Tame Impala
- Mac DeMarco
- Sticky Fingers

These artists are initial placeholders. The platform will support additional artists through its database.

## Core Features

- **Homepage:** Featured artists and merchandise collections.
- **Artist Profiles:** Biographies, musical backgrounds, releases and images.
- **Spotify Integration:** Embedded music for artist discovery (planned).
- **Product Catalogue:** At least 10 database-driven products.
- **Shopping Cart:** Add products, update quantities and remove items.
- **Checkout:** Collect customer details and record simulated purchases.
- **Order Confirmation:** Display completed transaction information.
- **Admin Dashboard:** View orders, customers and financial information.
- **Responsive Design:** Support desktop, tablet and mobile devices.

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python Flask, Jinja2 |
| Database | SQLite |
| Music Integration | Spotify Embeds (planned) |

## Merchandise

SIDE B. will support a flexible merchandise catalogue capable of representing:

- Digital products
- Simulated physical products
- A combination of both

The final product format is pending lecturer clarification.

All transactions will be simulated. No real payments will be processed.

## Planned Project Structure

```text
side-b/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   ├── artists.html
│   ├── artist.html
│   ├── product.html
│   ├── cart.html
│   ├── checkout.html
│   └── admin.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── main.js
    └── images/
```

## Development Approach

The website will use a database-driven structure to support multiple artists.

Rather than creating separate HTML files for each artist, SIDE B. will use reusable Flask routes and Jinja2 templates.

Example artist URLs:

- `/artists/tame-impala`
- `/artists/mac-demarco`
- `/artists/sticky-fingers`

New artists can be added to the database without creating additional page templates.

## Project Status

**Planning and initial development.**

## Disclaimer

SIDE B. is an unofficial educational project and is not affiliated with or endorsed by any featured artist or Spotify.

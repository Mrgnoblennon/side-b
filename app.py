# import flask class
from flask import Flask, render_template, url_for, request, abort, session, redirect, flash
import os
import hmac
import secrets
from database import initialise_database, seed_products, load_products, place_order, load_order, list_orders, order_stats, update_product

# initialise flask application
app = Flask(__name__)
# Set SIDE_B_SECRET_KEY in production to keep carts valid across restarts.
app.secret_key = os.environ.get('SIDE_B_SECRET_KEY', 'side-b-local-development-only')


# SIDE B. sample artist catalogue (AUD). Replace sample prices and stock as needed.
artists = [
    {
        "id": 1,
        "name": "Tame Impala",
        "slug": "tame-impala",
        "genre": "Psychedelic Rock",
        "description": "Australian psychedelic music project led by Kevin Parker.",
        "image": "images/artists/tame-impala/heroes/hero 1.jpeg",
        "portrait": "images/artists/tame-impala/portraits/portrait 1.jpeg",
        "biography": "Tame Impala is the psychedelic music project of Australian multi-instrumentalist Kevin Parker. Emerging from Perth, Parker developed a distinctive sound combining psychedelic rock, electronic music, pop and disco. Albums such as Lonerism, Currents and The Slow Rush helped establish Tame Impala as one of the most influential psychedelic acts of the modern era.",
        "gallery": [
            "images/artists/tame-impala/gallery/gallery 1.jpeg",
            "images/artists/tame-impala/gallery/gallery 2.jpeg",
            "images/artists/tame-impala/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 1,
                "artist_id": 1,
                "name": "Tame Impala Graphic T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for Tame Impala.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/tame-impala/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "1-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "1-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "1-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "1-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "1-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 2,
                "artist_id": 1,
                "name": "Tame Impala Run from the Sun Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for Tame Impala.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/tame-impala/merch/hoodies/hoodie.webp",
                "variants": [
                    {"id": "2-V01", "size": "S", "colour": "Grey", "stock": 3},
                    {"id": "2-V02", "size": "M", "colour": "Grey", "stock": 3},
                    {"id": "2-V03", "size": "L", "colour": "Grey", "stock": 3},
                    {"id": "2-V04", "size": "XL", "colour": "Grey", "stock": 3},
                    {"id": "2-V05", "size": "XXL", "colour": "Grey", "stock": 3},
                ],
            },
            {
                "id": 3,
                "artist_id": 1,
                "name": "Tame Impala Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for Tame Impala.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/tame-impala/merch/caps/cap.jpg",
                "variants": [
                    {
                        "id": "3-V01",
                        "colour": "Dark Grey",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 4,
                "artist_id": 1,
                "name": "Tame Impala Currents Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for Tame Impala.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/tame-impala/merch/vinyl/vinyl.jpg",
                "variants": [
                    {
                        "id": "4-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 5,
                "artist_id": 1,
                "name": "Tame Impala Currents Art Print",
                "category": "artwork",
                "description": "Sample artwork merchandise for Tame Impala.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/tame-impala/merch/artwork/art 1.webp",
                "variants": [
                    {"id": "5-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "5-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "5-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 6,
                "artist_id": 1,
                "name": "Tame Impala Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for Tame Impala.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/tame-impala/merch/tote-bags/tote 1.webp",
                "variants": [{"id": "6-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 7,
                "artist_id": 1,
                "name": "Tame Impala Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for Tame Impala.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/tame-impala/merch/sweatshirts/sweatshirt.webp",
                "variants": [
                    {"id": "7-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "7-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "7-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "7-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "7-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 8,
                "artist_id": 1,
                "name": "Tame Impala Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for Tame Impala.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/tame-impala/merch/accessories/stickers.jpg",
                "variants": [{"id": "8-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 2,
        "name": "Mac DeMarco",
        "slug": "mac-demarco",
        "genre": "Indie Rock",
        "description": "Canadian singer-songwriter known for his laid-back indie sound.",
        "image": "images/artists/mac-demarco/heroes/hero 1.jpeg",
        "portrait": "images/artists/mac-demarco/portraits/portrait 1.jpeg",
        "biography": "Mac DeMarco is a Canadian singer-songwriter and multi-instrumentalist known for his relaxed approach to indie rock. His music combines jangly guitars, mellow melodies and personal songwriting with a distinctive sense of humour. Albums such as 2, Salad Days and This Old Dog helped establish his reputation as one of indie music’s most recognisable artists.",
        "gallery": [
            "images/artists/mac-demarco/gallery/gallery 1.jpeg",
            "images/artists/mac-demarco/gallery/gallery 2.jpeg",
            "images/artists/mac-demarco/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 9,
                "artist_id": 2,
                "name": "Mac DeMarco Graphic T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for Mac DeMarco.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/mac-demarco/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "9-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "9-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "9-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "9-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "9-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 10,
                "artist_id": 2,
                "name": "Mac DeMarco Relaxed Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for Mac DeMarco.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/mac-demarco/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "10-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "10-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "10-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "10-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "10-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 11,
                "artist_id": 2,
                "name": "Mac DeMarco Baseball Cap",
                "category": "hats",
                "description": "Sample hats merchandise for Mac DeMarco.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/mac-demarco/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "11-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 12,
                "artist_id": 2,
                "name": "Mac DeMarco Salad Days Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for Mac DeMarco.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/mac-demarco/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "12-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 13,
                "artist_id": 2,
                "name": "Mac DeMarco Salad Days Art Print",
                "category": "artwork",
                "description": "Sample artwork merchandise for Mac DeMarco.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/mac-demarco/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "13-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "13-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "13-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 14,
                "artist_id": 2,
                "name": "Mac DeMarco Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for Mac DeMarco.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/mac-demarco/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "14-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 15,
                "artist_id": 2,
                "name": "Mac DeMarco Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for Mac DeMarco.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/mac-demarco/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "15-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "15-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "15-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "15-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "15-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 16,
                "artist_id": 2,
                "name": "Mac DeMarco Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for Mac DeMarco.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/mac-demarco/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "16-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 3,
        "name": "Sticky Fingers",
        "slug": "sticky-fingers",
        "genre": "Indie Rock / Reggae",
        "description": "Australian band known for blending indie rock, reggae and psychedelic influences.",
        "image": "images/artists/sticky-fingers/heroes/hero 1.jpeg",
        "portrait": "images/artists/sticky-fingers/portraits/portrait 1.jpeg",
        "biography": "Sticky Fingers are an Australian band formed in Sydney, known for combining indie rock, reggae, dub and psychedelic influences. Their relaxed grooves, distinctive vocals and energetic live performances helped them build a dedicated following. Albums such as Caress Your Soul, Land of Pleasure and Westway established their place in Australian alternative music.",
        "gallery": [
            "images/artists/sticky-fingers/gallery/gallery 1.jpeg",
            "images/artists/sticky-fingers/gallery/gallery 2.jpeg",
            "images/artists/sticky-fingers/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 17,
                "artist_id": 3,
                "name": "Sticky Fingers Band T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for Sticky Fingers.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/sticky-fingers/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "17-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "17-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "17-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "17-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "17-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 18,
                "artist_id": 3,
                "name": "Sticky Fingers Band Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for Sticky Fingers.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/sticky-fingers/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "18-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "18-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "18-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "18-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "18-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 19,
                "artist_id": 3,
                "name": "Sticky Fingers Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for Sticky Fingers.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/sticky-fingers/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "19-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 20,
                "artist_id": 3,
                "name": "Sticky Fingers Land of Pleasure Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for Sticky Fingers.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/sticky-fingers/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "20-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 21,
                "artist_id": 3,
                "name": "Sticky Fingers Land of Pleasure Poster",
                "category": "artwork",
                "description": "Sample artwork merchandise for Sticky Fingers.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/sticky-fingers/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "21-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "21-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "21-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 22,
                "artist_id": 3,
                "name": "Sticky Fingers Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for Sticky Fingers.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/sticky-fingers/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "22-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 23,
                "artist_id": 3,
                "name": "Sticky Fingers Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for Sticky Fingers.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/sticky-fingers/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "23-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "23-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "23-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "23-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "23-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 24,
                "artist_id": 3,
                "name": "Sticky Fingers Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for Sticky Fingers.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/sticky-fingers/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "24-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 4,
        "name": "Frank Ocean",
        "slug": "frank-ocean",
        "genre": "Alternative R&B",
        "description": "American singer-songwriter known for his experimental R&B, emotional storytelling and atmospheric production.",
        "image": "images/artists/frank-ocean/heroes/hero 1.jpeg",
        "portrait": "images/artists/frank-ocean/portraits/portrait 1.jpeg",
        "biography": "Frank Ocean is an American singer-songwriter recognised for his emotional storytelling, experimental production and distinctive approach to contemporary R&B. His projects Channel Orange and Blonde received widespread acclaim for their songwriting and exploration of identity, love and personal experience. His influence extends across R&B, alternative pop and modern hip-hop.",
        "gallery": [
            "images/artists/frank-ocean/gallery/gallery 1.jpeg",
            "images/artists/frank-ocean/gallery/gallery 2.jpeg",
            "images/artists/frank-ocean/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 25,
                "artist_id": 4,
                "name": "Frank Ocean Graphic T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for Frank Ocean.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/frank-ocean/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "25-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "25-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "25-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "25-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "25-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 26,
                "artist_id": 4,
                "name": "Frank Ocean Minimal Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for Frank Ocean.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/frank-ocean/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "26-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "26-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "26-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "26-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "26-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 27,
                "artist_id": 4,
                "name": "Frank Ocean Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for Frank Ocean.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/frank-ocean/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "27-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 28,
                "artist_id": 4,
                "name": "Frank Ocean Blonde Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for Frank Ocean.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/frank-ocean/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "28-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 29,
                "artist_id": 4,
                "name": "Frank Ocean Blonde Art Print",
                "category": "artwork",
                "description": "Sample artwork merchandise for Frank Ocean.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/frank-ocean/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "29-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "29-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "29-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 30,
                "artist_id": 4,
                "name": "Frank Ocean Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for Frank Ocean.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/frank-ocean/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "30-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 31,
                "artist_id": 4,
                "name": "Frank Ocean Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for Frank Ocean.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/frank-ocean/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "31-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "31-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "31-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "31-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "31-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 32,
                "artist_id": 4,
                "name": "Frank Ocean Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for Frank Ocean.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/frank-ocean/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "32-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 5,
        "name": "Khruangbin",
        "slug": "khruangbin",
        "genre": "Psychedelic Funk / Soul",
        "description": "American trio blending psychedelic funk, soul, dub and global musical influences.",
        "image": "images/artists/khruangbin/heroes/hero 1.jpeg",
        "portrait": "images/artists/khruangbin/portraits/portrait 1.jpeg",
        "biography": "Khruangbin are an American trio from Houston, Texas, consisting of Laura Lee, Mark Speer and Donald Johnson. Their largely instrumental music blends psychedelic funk, soul, dub and musical influences from around the world. Known for their distinctive guitar tones, smooth basslines and relaxed rhythms, the band has developed an instantly recognisable sound and visual identity.",
        "gallery": [
            "images/artists/khruangbin/gallery/gallery 1.jpeg",
            "images/artists/khruangbin/gallery/gallery 2.jpeg",
            "images/artists/khruangbin/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 33,
                "artist_id": 5,
                "name": "Khruangbin Graphic T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for Khruangbin.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/khruangbin/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "33-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "33-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "33-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "33-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "33-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 34,
                "artist_id": 5,
                "name": "Khruangbin Groove Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for Khruangbin.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/khruangbin/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "34-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "34-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "34-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "34-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "34-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 35,
                "artist_id": 5,
                "name": "Khruangbin Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for Khruangbin.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/khruangbin/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "35-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 36,
                "artist_id": 5,
                "name": "Khruangbin Con Todo El Mundo Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for Khruangbin.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/khruangbin/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "36-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 37,
                "artist_id": 5,
                "name": "Khruangbin Psychedelic Art Print",
                "category": "artwork",
                "description": "Sample artwork merchandise for Khruangbin.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/khruangbin/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "37-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "37-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "37-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 38,
                "artist_id": 5,
                "name": "Khruangbin Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for Khruangbin.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/khruangbin/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "38-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 39,
                "artist_id": 5,
                "name": "Khruangbin Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for Khruangbin.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/khruangbin/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "39-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "39-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "39-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "39-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "39-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 40,
                "artist_id": 5,
                "name": "Khruangbin Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for Khruangbin.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/khruangbin/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "40-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 6,
        "name": "Men I Trust",
        "slug": "men-i-trust",
        "genre": "Dream Pop / Indie",
        "description": "Canadian indie band known for their dreamy melodies, smooth basslines and atmospheric sound.",
        "image": "images/artists/men-i-trust/heroes/hero 1.jpeg",
        "portrait": "images/artists/men-i-trust/portraits/portrait 1.jpeg",
        "biography": "Men I Trust are a Canadian indie band from Quebec, known for their dreamy production, soft vocals and smooth bass-driven melodies. Their music combines dream pop, indie and electronic influences to create a calm, atmospheric sound. Songs such as Show Me How and Lauren helped introduce their music to a wider international audience.",
        "gallery": [
            "images/artists/men-i-trust/gallery/gallery 1.jpeg",
            "images/artists/men-i-trust/gallery/gallery 2.jpeg",
            "images/artists/men-i-trust/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 41,
                "artist_id": 6,
                "name": "Men I Trust Dream Pop T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for Men I Trust.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/men-i-trust/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "41-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "41-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "41-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "41-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "41-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 42,
                "artist_id": 6,
                "name": "Men I Trust Soft Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for Men I Trust.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/men-i-trust/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "42-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "42-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "42-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "42-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "42-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 43,
                "artist_id": 6,
                "name": "Men I Trust Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for Men I Trust.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/men-i-trust/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "43-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 44,
                "artist_id": 6,
                "name": "Men I Trust Untourable Album Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for Men I Trust.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/men-i-trust/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "44-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 45,
                "artist_id": 6,
                "name": "Men I Trust Dreamy Art Print",
                "category": "artwork",
                "description": "Sample artwork merchandise for Men I Trust.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/men-i-trust/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "45-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "45-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "45-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 46,
                "artist_id": 6,
                "name": "Men I Trust Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for Men I Trust.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/men-i-trust/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "46-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 47,
                "artist_id": 6,
                "name": "Men I Trust Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for Men I Trust.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/men-i-trust/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "47-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "47-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "47-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "47-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "47-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 48,
                "artist_id": 6,
                "name": "Men I Trust Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for Men I Trust.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/men-i-trust/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "48-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 7,
        "name": "MF DOOM",
        "slug": "mf-doom",
        "genre": "Alternative Hip-Hop",
        "description": "British-American rapper and producer celebrated for his intricate wordplay, masked persona and underground hip-hop influence.",
        "image": "images/artists/mf-doom/heroes/hero 1.jpeg",
        "portrait": "images/artists/mf-doom/portraits/portrait 1.jpeg",
        "biography": "MF DOOM was a British-American rapper and producer known for his intricate lyricism, comic-book-inspired identity and distinctive metal mask. Born Daniel Dumile, he became one of underground hip-hop’s most influential figures. His music combined unusual samples, complex rhymes and an unmistakable sense of humour.",
        "gallery": [
            "images/artists/mf-doom/gallery/gallery 1.jpeg",
            "images/artists/mf-doom/gallery/gallery 2.jpeg",
            "images/artists/mf-doom/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 49,
                "artist_id": 7,
                "name": "MF DOOM Mask Graphic T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for MF DOOM.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/mf-doom/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "49-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "49-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "49-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "49-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "49-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 50,
                "artist_id": 7,
                "name": "MF DOOM DOOM Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for MF DOOM.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/mf-doom/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "50-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "50-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "50-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "50-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "50-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 51,
                "artist_id": 7,
                "name": "MF DOOM Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for MF DOOM.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/mf-doom/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "51-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 52,
                "artist_id": 7,
                "name": "MF DOOM MM..FOOD Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for MF DOOM.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/mf-doom/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "52-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 53,
                "artist_id": 7,
                "name": "MF DOOM DOOM Art Print",
                "category": "artwork",
                "description": "Sample artwork merchandise for MF DOOM.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/mf-doom/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "53-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "53-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "53-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 54,
                "artist_id": 7,
                "name": "MF DOOM Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for MF DOOM.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/mf-doom/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "54-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 55,
                "artist_id": 7,
                "name": "MF DOOM Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for MF DOOM.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/mf-doom/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "55-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "55-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "55-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "55-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "55-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 56,
                "artist_id": 7,
                "name": "MF DOOM Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for MF DOOM.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/mf-doom/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "56-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 8,
        "name": "PinkPantheress",
        "slug": "pink-pantheress",
        "genre": "UK Garage / Alternative Pop",
        "description": "British singer and producer known for blending UK garage, drum and bass, and nostalgic pop.",
        "image": "images/artists/pink-pantheress/heroes/hero 1.jpeg",
        "portrait": "images/artists/pink-pantheress/portraits/portrait 1.jpeg",
        "biography": "PinkPantheress is a British singer-songwriter and producer known for combining UK garage, drum and bass, bedroom pop and nostalgic electronic sounds. Her short, melodic songs first gained widespread attention online before reaching international audiences. Her distinctive production style and soft vocals have made her an influential voice in modern alternative pop.",
        "gallery": [
            "images/artists/pink-pantheress/gallery/gallery 1.jpeg",
            "images/artists/pink-pantheress/gallery/gallery 2.jpeg",
            "images/artists/pink-pantheress/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 57,
                "artist_id": 8,
                "name": "PinkPantheress Baby Tee",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for PinkPantheress.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/pink-pantheress/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "57-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "57-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "57-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "57-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "57-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 58,
                "artist_id": 8,
                "name": "PinkPantheress Pink Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for PinkPantheress.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/pink-pantheress/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "58-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "58-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "58-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "58-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "58-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 59,
                "artist_id": 8,
                "name": "PinkPantheress Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for PinkPantheress.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/pink-pantheress/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "59-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 60,
                "artist_id": 8,
                "name": "PinkPantheress Heaven Knows Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for PinkPantheress.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/pink-pantheress/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "60-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 61,
                "artist_id": 8,
                "name": "PinkPantheress Nostalgic Poster",
                "category": "artwork",
                "description": "Sample artwork merchandise for PinkPantheress.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/pink-pantheress/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "61-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "61-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "61-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 62,
                "artist_id": 8,
                "name": "PinkPantheress Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for PinkPantheress.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/pink-pantheress/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "62-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 63,
                "artist_id": 8,
                "name": "PinkPantheress Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for PinkPantheress.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/pink-pantheress/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "63-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "63-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "63-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "63-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "63-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 64,
                "artist_id": 8,
                "name": "PinkPantheress Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for PinkPantheress.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/pink-pantheress/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "64-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 9,
        "name": "Dope Lemon",
        "slug": "dope-lemon",
        "genre": "Psychedelic Rock / Indie Folk",
        "description": "Australian psychedelic music project led by Angus Stone, known for its laid-back grooves, dreamy melodies and mellow sound.",
        "image": "images/artists/dope-lemon/heroes/hero 1.jpeg",
        "portrait": "images/artists/dope-lemon/portraits/portrait 1.jpeg",
        "biography": "Dope Lemon is the psychedelic music project of Australian musician Angus Stone. The project combines relaxed guitar melodies, blues influences and hazy psychedelic production to create a distinctive laid-back sound. Albums such as Honey Bones and Smooth Big Cat showcase its dreamy atmosphere, storytelling and mellow grooves.",
        "gallery": [
            "images/artists/dope-lemon/gallery/gallery 1.jpeg",
            "images/artists/dope-lemon/gallery/gallery 2.jpeg",
            "images/artists/dope-lemon/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 65,
                "artist_id": 9,
                "name": "Dope Lemon Graphic T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for Dope Lemon.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/dope-lemon/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "65-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "65-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "65-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "65-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "65-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 66,
                "artist_id": 9,
                "name": "Dope Lemon Psychedelic Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for Dope Lemon.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/dope-lemon/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "66-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "66-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "66-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "66-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "66-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 67,
                "artist_id": 9,
                "name": "Dope Lemon Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for Dope Lemon.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/dope-lemon/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "67-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 68,
                "artist_id": 9,
                "name": "Dope Lemon Honey Bones Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for Dope Lemon.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/dope-lemon/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "68-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 69,
                "artist_id": 9,
                "name": "Dope Lemon Dope Lemon Art Print",
                "category": "artwork",
                "description": "Sample artwork merchandise for Dope Lemon.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/dope-lemon/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "69-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "69-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "69-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 70,
                "artist_id": 9,
                "name": "Dope Lemon Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for Dope Lemon.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/dope-lemon/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "70-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 71,
                "artist_id": 9,
                "name": "Dope Lemon Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for Dope Lemon.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/dope-lemon/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "71-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "71-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "71-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "71-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "71-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 72,
                "artist_id": 9,
                "name": "Dope Lemon Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for Dope Lemon.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/dope-lemon/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "72-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 10,
        "name": "Kaytranada",
        "slug": "kaytranada",
        "genre": "Electronic / House / Hip-Hop",
        "description": "Haitian-Canadian producer and DJ known for his distinctive blend of house, funk, hip-hop and R&B.",
        "image": "images/artists/kaytranada/heroes/hero 1.jpeg",
        "portrait": "images/artists/kaytranada/portraits/portrait 1.jpeg",
        "biography": "Kaytranada is a Haitian-Canadian producer and DJ recognised for his distinctive combination of house, funk, hip-hop and R&B. His rhythmic production style features energetic drum patterns, soulful samples and smooth basslines. Albums such as 99.9% and Bubba helped establish him as one of contemporary electronic music’s most recognisable producers.",
        "gallery": [
            "images/artists/kaytranada/gallery/gallery 1.jpeg",
            "images/artists/kaytranada/gallery/gallery 2.jpeg",
            "images/artists/kaytranada/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 73,
                "artist_id": 10,
                "name": "Kaytranada Graphic T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for Kaytranada.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/kaytranada/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "73-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "73-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "73-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "73-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "73-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 74,
                "artist_id": 10,
                "name": "Kaytranada Club Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for Kaytranada.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/kaytranada/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "74-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "74-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "74-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "74-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "74-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 75,
                "artist_id": 10,
                "name": "Kaytranada Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for Kaytranada.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/kaytranada/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "75-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 76,
                "artist_id": 10,
                "name": "Kaytranada Bubba Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for Kaytranada.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/kaytranada/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "76-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 77,
                "artist_id": 10,
                "name": "Kaytranada Electronic Art Print",
                "category": "artwork",
                "description": "Sample artwork merchandise for Kaytranada.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/kaytranada/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "77-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "77-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "77-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 78,
                "artist_id": 10,
                "name": "Kaytranada Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for Kaytranada.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/kaytranada/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "78-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 79,
                "artist_id": 10,
                "name": "Kaytranada Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for Kaytranada.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/kaytranada/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "79-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "79-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "79-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "79-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "79-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 80,
                "artist_id": 10,
                "name": "Kaytranada Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for Kaytranada.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/kaytranada/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "80-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 11,
        "name": "Tyler, the Creator",
        "slug": "tyler-the-creator",
        "genre": "Alternative Hip-Hop / R&B",
        "description": "American rapper, producer and creative artist known for his genre-blending albums, distinctive production and visual style.",
        "image": "images/artists/tyler-the-creator/heroes/hero 1.jpeg",
        "portrait": "images/artists/tyler-the-creator/portraits/portrait 1.jpeg",
        "biography": "Tyler, the Creator is an American rapper, producer and creative artist known for his constantly evolving musical and visual identity. Emerging as a founding member of Odd Future, he developed a solo career combining hip-hop, jazz, soul and alternative R&B. Albums such as Flower Boy, Igor and Call Me If You Get Lost demonstrate his distinctive production and storytelling.",
        "gallery": [
            "images/artists/tyler-the-creator/gallery/gallery 1.jpeg",
            "images/artists/tyler-the-creator/gallery/gallery 2.jpeg",
            "images/artists/tyler-the-creator/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 81,
                "artist_id": 11,
                "name": "Tyler, the Creator Graphic T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for Tyler, the Creator.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/tyler-the-creator/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "81-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "81-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "81-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "81-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "81-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 82,
                "artist_id": 11,
                "name": "Tyler, the Creator Colourblock Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for Tyler, the Creator.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/tyler-the-creator/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "82-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "82-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "82-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "82-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "82-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 83,
                "artist_id": 11,
                "name": "Tyler, the Creator Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for Tyler, the Creator.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/tyler-the-creator/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "83-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 84,
                "artist_id": 11,
                "name": "Tyler, the Creator IGOR Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for Tyler, the Creator.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/tyler-the-creator/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "84-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 85,
                "artist_id": 11,
                "name": "Tyler, the Creator Flower Boy Art Print",
                "category": "artwork",
                "description": "Sample artwork merchandise for Tyler, the Creator.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/tyler-the-creator/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "85-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "85-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "85-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 86,
                "artist_id": 11,
                "name": "Tyler, the Creator Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for Tyler, the Creator.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/tyler-the-creator/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "86-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 87,
                "artist_id": 11,
                "name": "Tyler, the Creator Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for Tyler, the Creator.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/tyler-the-creator/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "87-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "87-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "87-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "87-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "87-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 88,
                "artist_id": 11,
                "name": "Tyler, the Creator Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for Tyler, the Creator.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/tyler-the-creator/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "88-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
    {
        "id": 12,
        "name": "Lorde",
        "slug": "lorde",
        "genre": "Alternative Pop / Art Pop",
        "description": "New Zealand singer-songwriter known for her distinctive vocals, introspective lyrics and atmospheric pop production.",
        "image": "images/artists/lorde/heroes/hero 1.jpeg",
        "portrait": "images/artists/lorde/portraits/portrait 1.jpeg",
        "biography": "Lorde is a New Zealand singer-songwriter known for her distinctive vocals, introspective songwriting and atmospheric approach to pop music. She gained international recognition with Royals and her debut album Pure Heroine. Later projects including Melodrama and Solar Power explored personal growth, relationships and changing perspectives through inventive pop production.",
        "gallery": [
            "images/artists/lorde/gallery/gallery 1.jpeg",
            "images/artists/lorde/gallery/gallery 2.jpeg",
            "images/artists/lorde/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 89,
                "artist_id": 12,
                "name": "Lorde Graphic T-Shirt",
                "category": "t-shirts",
                "description": "Sample t shirts merchandise for Lorde.",
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/lorde/merch/t-shirts/t-shirt 1.jpeg",
                "variants": [
                    {"id": "89-V01", "size": "S", "colour": "Black", "stock": 4},
                    {"id": "89-V02", "size": "M", "colour": "Black", "stock": 4},
                    {"id": "89-V03", "size": "L", "colour": "Black", "stock": 4},
                    {"id": "89-V04", "size": "XL", "colour": "Black", "stock": 4},
                    {"id": "89-V05", "size": "XXL", "colour": "Black", "stock": 4},
                ],
            },
            {
                "id": 90,
                "artist_id": 12,
                "name": "Lorde Tour Hoodie",
                "category": "hoodies",
                "description": "Sample hoodies merchandise for Lorde.",
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/lorde/merch/hoodies/hoodie 1.jpeg",
                "variants": [
                    {"id": "90-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "90-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "90-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "90-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "90-V05", "size": "XXL", "colour": "Black", "stock": 3},
                ],
            },
            {
                "id": 91,
                "artist_id": 12,
                "name": "Lorde Embroidered Cap",
                "category": "hats",
                "description": "Sample hats merchandise for Lorde.",
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/lorde/merch/hats/hat 1.jpeg",
                "variants": [
                    {
                        "id": "91-V01",
                        "colour": "Black",
                        "fit": "Adjustable",
                        "stock": 12,
                    }
                ],
            },
            {
                "id": 92,
                "artist_id": 12,
                "name": "Lorde Melodrama Vinyl",
                "category": "vinyl",
                "description": "Sample vinyl merchandise for Lorde.",
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/lorde/merch/vinyl/vinyl 1.jpeg",
                "variants": [
                    {
                        "id": "92-V01",
                        "edition": "Standard",
                        "colour": "Black",
                        "stock": 10,
                    }
                ],
            },
            {
                "id": 93,
                "artist_id": 12,
                "name": "Lorde Melodrama Art Print",
                "category": "artwork",
                "description": "Sample artwork merchandise for Lorde.",
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/lorde/merch/artwork/art 1.jpeg",
                "variants": [
                    {"id": "93-V01", "size": "A4", "finish": "Unframed", "stock": 9},
                    {"id": "93-V02", "size": "A3", "finish": "Unframed", "stock": 8},
                    {"id": "93-V03", "size": "A2", "finish": "Unframed", "stock": 8},
                ],
            },
            {
                "id": 94,
                "artist_id": 12,
                "name": "Lorde Canvas Tote Bag",
                "category": "tote-bags",
                "description": "Sample tote bags merchandise for Lorde.",
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/lorde/merch/tote-bags/tote 1.jpeg",
                "variants": [{"id": "94-V01", "colour": "Natural", "stock": 18}],
            },
            {
                "id": 95,
                "artist_id": 12,
                "name": "Lorde Crewneck Sweatshirt",
                "category": "sweatshirts",
                "description": "Sample sweatshirts merchandise for Lorde.",
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/lorde/merch/sweatshirts/sweatshirt 1.jpeg",
                "variants": [
                    {"id": "95-V01", "size": "S", "colour": "Black", "stock": 3},
                    {"id": "95-V02", "size": "M", "colour": "Black", "stock": 3},
                    {"id": "95-V03", "size": "L", "colour": "Black", "stock": 3},
                    {"id": "95-V04", "size": "XL", "colour": "Black", "stock": 3},
                    {"id": "95-V05", "size": "XXL", "colour": "Black", "stock": 2},
                ],
            },
            {
                "id": 96,
                "artist_id": 12,
                "name": "Lorde Sticker Pack",
                "category": "accessories",
                "description": "Sample accessories merchandise for Lorde.",
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/lorde/merch/accessories/stickers 1.jpeg",
                "variants": [{"id": "96-V01", "option": "Sticker pack", "stock": 40}],
            },
        ],
    },
]


# home route for sending recieving requests, connects the homepage url
@app.route("/")
# define route function that will handle reququests
def home():
    # sends a response back to the browser
    return render_template("index.html", artists=artists)


@app.route("/artists")
def artists_page():
    return render_template("artists.html", artists=artists)


@app.route("/artists/<slug>")
def artist_page(slug):

    # Find the artist matching the URL slug
    for artist in artists:
        if artist["slug"] == slug:
            return render_template("artist.html", artist=artist)

    return "Artist not found", 404


# Initialise and seed the SQLite catalogue on first startup only.
initialise_database()
seed_products(artists)


def get_products():
    products = load_products()
    artist_names = {artist["id"]: artist["name"] for artist in artists}
    for product in products:
        product["artist"] = artist_names.get(product["artist_id"], "Unknown Artist")
    return products


# merch shop page
@app.route("/shop")
def merch_shop():
    products = get_products()
    categories = sorted(set(p["category"] for p in products))
    artist_names = sorted(set(p["artist"] for p in products))
    selected_category = request.args.get("category", "All")
    selected_artist = request.args.get("artist", "All")
    selected_sort = request.args.get("sort", "default")

    if selected_category not in categories:
        selected_category = "All"
    if selected_artist not in artist_names:
        selected_artist = "All"
    if selected_sort not in ("default", "price_asc", "price_desc", "name_asc"):
        selected_sort = "default"

    if selected_category != "All":
        products = [p for p in products if p["category"] == selected_category]
    if selected_artist != "All":
        products = [p for p in products if p["artist"] == selected_artist]

    if selected_sort == "price_asc":
        products.sort(key=lambda p: float(p["price"]))
    elif selected_sort == "price_desc":
        products.sort(key=lambda p: float(p["price"]), reverse=True)
    elif selected_sort == "name_asc":
        products.sort(key=lambda p: p["name"].casefold())

    return render_template("shop.html", products=products, categories=categories,
                           artist_names=artist_names, selected_category=selected_category,
                           selected_artist=selected_artist, selected_sort=selected_sort)

# individual product page
@app.route("/shop/<int:product_id>")
def product_detail(product_id):
    products = get_products()

    # find the product using its id
    product = next(
        (product for product in products if str(product.get("id")) == str(product_id)),
        None,
    )

    print("PRODUCT IDS:", [product.get("id") for product in products])

    if product is None:
        abort(404)

    # get other products from the same artist
    related_products = [
        item
        for item in products
        if item["artist"] == product["artist"]
        and str(item.get("id")) != str(product_id)
    ][:4]

    return render_template(
        "product.html",
        product=product,
        related_products=related_products
    )


# Cart stores only IDs and quantities; product details come from the catalogue.
def cart_details():
    catalogue = {str(p["id"]): p for p in get_products()}
    items = []
    subtotal = 0.0
    for entry in session.get("cart", []):
        product = catalogue.get(str(entry.get("product_id")))
        if not product:
            continue
        variant = next((v for v in product.get("variants", []) if str(v["id"]) == str(entry.get("variant_id"))), None)
        if product.get("variants") and variant is None:
            continue
        stock = int(variant["stock"] if variant else product.get("stock", 0))
        quantity = min(max(1, int(entry.get("quantity", 1))), stock)
        if stock <= 0:
            continue
        price = float(product["price"])
        subtotal += price * quantity
        label = " · ".join(str(variant[k]) for k in ("size", "colour", "edition", "fit", "finish", "option") if variant and variant.get(k))
        items.append({"product": product, "variant": variant, "variant_label": label,
                      "quantity": quantity, "stock": stock, "line_total": price * quantity,
                      "variant_id": entry.get("variant_id", "")})
    return items, round(subtotal, 2)


@app.route("/cart")
def view_cart():
    items, subtotal = cart_details()
    return render_template("cart.html", items=items, subtotal=subtotal)


@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    product_id = request.form.get("product_id", "")
    variant_id = request.form.get("variant", "")
    product = next((p for p in get_products() if str(p["id"]) == product_id), None)
    if not product:
        abort(404)
    variant = next((v for v in product.get("variants", []) if str(v["id"]) == variant_id), None)
    if product.get("variants") and variant is None:
        flash("Please select a valid option.")
        return redirect(url_for("product_detail", product_id=product["id"]))
    try:
        quantity = int(request.form.get("quantity", "1"))
    except ValueError:
        quantity = 0
    stock = int(variant["stock"] if variant else product.get("stock", 0))
    cart = list(session.get("cart", []))
    existing = next((item for item in cart if str(item["product_id"]) == product_id and str(item.get("variant_id", "")) == variant_id), None)
    current = int(existing["quantity"]) if existing else 0
    if quantity < 1 or current + quantity > stock:
        flash("Invalid quantity or not enough stock available.")
        return redirect(url_for("product_detail", product_id=product["id"]))
    if existing:
        existing["quantity"] += quantity
    else:
        cart.append({"product_id": product_id, "variant_id": variant_id, "quantity": quantity})
    session["cart"] = cart
    flash("Added to cart.")
    return redirect(url_for("view_cart"))


@app.route("/cart/update", methods=["POST"])
def update_cart():
    product_id = request.form.get("product_id", "")
    variant_id = request.form.get("variant_id", "")
    product = next((p for p in get_products() if str(p["id"]) == product_id), None)
    if not product:
        abort(404)
    variant = next((v for v in product.get("variants", []) if str(v["id"]) == variant_id), None)
    if product.get("variants") and variant is None:
        abort(400)
    try:
        quantity = int(request.form.get("quantity", "0"))
    except ValueError:
        quantity = -1
    stock = int(variant["stock"] if variant else product.get("stock", 0))
    cart = list(session.get("cart", []))
    matching = [item for item in cart if str(item["product_id"]) == product_id and str(item.get("variant_id", "")) == variant_id]
    if not matching:
        abort(404)
    if quantity == 0:
        cart = [item for item in cart if item not in matching]
    elif 1 <= quantity <= stock:
        matching[0]["quantity"] = quantity
    else:
        flash("Quantity must be between 1 and available stock.")
        return redirect(url_for("view_cart"))
    session["cart"] = cart
    return redirect(url_for("view_cart"))


# Simulated checkout: no payment details are collected.
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    items, subtotal = cart_details()
    if not session.get("cart") or not items:
        flash("Add something to your cart before checking out.")
        return redirect(url_for("view_cart"))
    if request.method == "POST":
        customer = {key: request.form.get(key, "").strip() for key in ("name", "email", "phone", "suburb")}
        if any(not value or len(value) > 200 for value in customer.values()) or "@" not in customer["email"]:
            flash("Please enter valid contact details.")
        else:
            try:
                order_id = place_order(customer, session["cart"])
            except ValueError as exc:
                flash(str(exc))
                return redirect(url_for("view_cart"))
            session.pop("cart", None)
            session["last_order_id"] = order_id
            return redirect(url_for("order_confirmation", order_id=order_id))
    return render_template("checkout.html", items=items, subtotal=subtotal)


@app.route("/order/<int:order_id>")
def order_confirmation(order_id):
    if session.get("last_order_id") != order_id:
        abort(404)
    order, items = load_order(order_id)
    if not order:
        abort(404)
    return render_template("order_confirmation.html", order=order, items=items)



# Admin access is disabled until SIDE_B_ADMIN_PASSWORD is configured.
def admin_authenticated():
    return bool(os.environ.get("SIDE_B_ADMIN_PASSWORD")) and session.get("admin_authenticated") is True


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if admin_authenticated():
        return redirect(url_for("admin_orders"))
    configured_password = os.environ.get("SIDE_B_ADMIN_PASSWORD", "")
    if request.method == "POST":
        supplied = request.form.get("password", "")
        if configured_password and hmac.compare_digest(supplied, configured_password):
            session.clear()
            session["admin_authenticated"] = True
            session["admin_csrf"] = secrets.token_urlsafe(32)
            return redirect(url_for("admin_orders"))
        flash("Incorrect password, or admin access has not been configured.")
    return render_template("admin_login.html", configured=bool(configured_password))


@app.route("/admin/logout", methods=["POST"])
def admin_logout():
    if not admin_authenticated():
        abort(403)
    if not hmac.compare_digest(request.form.get("csrf_token", ""), session.get("admin_csrf", "")):
        abort(403)
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin/orders")
def admin_orders():
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    return render_template("admin_orders.html", orders=list_orders(), stats=order_stats())


@app.route("/admin/orders/<int:order_id>")
def admin_order_detail(order_id):
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    order, items = load_order(order_id)
    if not order:
        abort(404)
    return render_template("admin_order_detail.html", order=order, items=items)



@app.route("/admin/products")
def admin_products():
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    products = get_products()
    for product in products:
        product["available_stock"] = sum(int(v["stock"]) for v in product["variants"]) if product["variants"] else int(product["stock"])
    query = request.args.get("q", "").strip()
    if query:
        products = [p for p in products if query.casefold() in p["name"].casefold() or query.casefold() in p["artist"].casefold()]
    return render_template("admin_products.html", products=products, query=query)


@app.route("/admin/products/<int:product_id>/edit", methods=["GET", "POST"])
def admin_edit_product(product_id):
    if not admin_authenticated():
        return redirect(url_for("admin_login"))
    product = next((p for p in get_products() if p["id"] == product_id), None)
    if product is None:
        abort(404)
    if request.method == "POST":
        if not hmac.compare_digest(request.form.get("csrf_token", ""), session.get("admin_csrf", "")):
            abort(403)
        fields = {key: request.form.get(key, "") for key in ("name", "colour", "price", "stock")}
        variant_stock = {str(v["id"]): request.form.get("stock_" + str(v["id"]), "") for v in product["variants"]}
        try:
            update_product(product_id, fields, variant_stock)
        except ValueError as exc:
            flash(str(exc))
        else:
            flash("Product updated successfully.")
            return redirect(url_for("admin_edit_product", product_id=product_id))
    return render_template("admin_edit_product.html", product=product)


# runs when everything before it is correct
if __name__ == "__main__":
    # starts the server
    app.run(debug=True, port=5001)

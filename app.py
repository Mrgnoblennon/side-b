# import flask class
from flask import Flask, render_template, url_for
import os

# initialise flask application
app = Flask(__name__)


# SIDE B. sample artist catalogue (AUD). Replace sample prices and stock as needed.
artists = [
    {
        "id": 1,
        "name": 'Tame Impala',
        "slug": 'tame-impala',
        "genre": 'Psychedelic Rock',
        "description": 'Australian psychedelic music project led by Kevin Parker.',
        "image": "images/artists/tame-impala/heroes/hero 1.jpeg",
        "portrait": "images/artists/tame-impala/portraits/portrait 1.jpeg",
        "biography": 'Tame Impala is the psychedelic music project of Australian multi-instrumentalist Kevin Parker. Emerging from Perth, Parker developed a distinctive sound combining psychedelic rock, electronic music, pop and disco. Albums such as Lonerism, Currents and The Slow Rush helped establish Tame Impala as one of the most influential psychedelic acts of the modern era.',
        "gallery": [
            "images/artists/tame-impala/gallery/gallery 1.jpeg",
            "images/artists/tame-impala/gallery/gallery 2.jpeg",
            "images/artists/tame-impala/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 1,
                "artist_id": 1,
                "name": 'Tame Impala Graphic T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for Tame Impala.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/tame-impala/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 2,
                "artist_id": 1,
                "name": 'Tame Impala Psychedelic Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for Tame Impala.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/tame-impala/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 3,
                "artist_id": 1,
                "name": 'Tame Impala Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for Tame Impala.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/tame-impala/merch/hats/hat 1.jpeg"
            },
            {
                "id": 4,
                "artist_id": 1,
                "name": 'Tame Impala Currents Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for Tame Impala.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/tame-impala/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 5,
                "artist_id": 1,
                "name": 'Tame Impala Currents Art Print',
                "category": "artwork",
                "description": 'Sample artwork merchandise for Tame Impala.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/tame-impala/merch/artwork/art 1.jpeg"
            },
            {
                "id": 6,
                "artist_id": 1,
                "name": 'Tame Impala Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for Tame Impala.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/tame-impala/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 7,
                "artist_id": 1,
                "name": 'Tame Impala Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for Tame Impala.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/tame-impala/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 8,
                "artist_id": 1,
                "name": 'Tame Impala Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for Tame Impala.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/tame-impala/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 2,
        "name": 'Mac DeMarco',
        "slug": 'mac-demarco',
        "genre": 'Indie Rock',
        "description": 'Canadian singer-songwriter known for his laid-back indie sound.',
        "image": "images/artists/mac-demarco/heroes/hero 1.jpeg",
        "portrait": "images/artists/mac-demarco/portraits/portrait 1.jpeg",
        "biography": 'Mac DeMarco is a Canadian singer-songwriter and multi-instrumentalist known for his relaxed approach to indie rock. His music combines jangly guitars, mellow melodies and personal songwriting with a distinctive sense of humour. Albums such as 2, Salad Days and This Old Dog helped establish his reputation as one of indie music’s most recognisable artists.',
        "gallery": [
            "images/artists/mac-demarco/gallery/gallery 1.jpeg",
            "images/artists/mac-demarco/gallery/gallery 2.jpeg",
            "images/artists/mac-demarco/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 9,
                "artist_id": 2,
                "name": 'Mac DeMarco Graphic T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for Mac DeMarco.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/mac-demarco/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 10,
                "artist_id": 2,
                "name": 'Mac DeMarco Relaxed Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for Mac DeMarco.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/mac-demarco/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 11,
                "artist_id": 2,
                "name": 'Mac DeMarco Baseball Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for Mac DeMarco.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/mac-demarco/merch/hats/hat 1.jpeg"
            },
            {
                "id": 12,
                "artist_id": 2,
                "name": 'Mac DeMarco Salad Days Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for Mac DeMarco.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/mac-demarco/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 13,
                "artist_id": 2,
                "name": 'Mac DeMarco Salad Days Art Print',
                "category": "artwork",
                "description": 'Sample artwork merchandise for Mac DeMarco.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/mac-demarco/merch/artwork/art 1.jpeg"
            },
            {
                "id": 14,
                "artist_id": 2,
                "name": 'Mac DeMarco Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for Mac DeMarco.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/mac-demarco/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 15,
                "artist_id": 2,
                "name": 'Mac DeMarco Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for Mac DeMarco.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/mac-demarco/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 16,
                "artist_id": 2,
                "name": 'Mac DeMarco Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for Mac DeMarco.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/mac-demarco/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 3,
        "name": 'Sticky Fingers',
        "slug": 'sticky-fingers',
        "genre": 'Indie Rock / Reggae',
        "description": 'Australian band known for blending indie rock, reggae and psychedelic influences.',
        "image": "images/artists/sticky-fingers/heroes/hero 1.jpeg",
        "portrait": "images/artists/sticky-fingers/portraits/portrait 1.jpeg",
        "biography": 'Sticky Fingers are an Australian band formed in Sydney, known for combining indie rock, reggae, dub and psychedelic influences. Their relaxed grooves, distinctive vocals and energetic live performances helped them build a dedicated following. Albums such as Caress Your Soul, Land of Pleasure and Westway established their place in Australian alternative music.',
        "gallery": [
            "images/artists/sticky-fingers/gallery/gallery 1.jpeg",
            "images/artists/sticky-fingers/gallery/gallery 2.jpeg",
            "images/artists/sticky-fingers/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 17,
                "artist_id": 3,
                "name": 'Sticky Fingers Band T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for Sticky Fingers.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/sticky-fingers/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 18,
                "artist_id": 3,
                "name": 'Sticky Fingers Band Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for Sticky Fingers.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/sticky-fingers/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 19,
                "artist_id": 3,
                "name": 'Sticky Fingers Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for Sticky Fingers.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/sticky-fingers/merch/hats/hat 1.jpeg"
            },
            {
                "id": 20,
                "artist_id": 3,
                "name": 'Sticky Fingers Land of Pleasure Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for Sticky Fingers.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/sticky-fingers/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 21,
                "artist_id": 3,
                "name": 'Sticky Fingers Land of Pleasure Poster',
                "category": "artwork",
                "description": 'Sample artwork merchandise for Sticky Fingers.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/sticky-fingers/merch/artwork/art 1.jpeg"
            },
            {
                "id": 22,
                "artist_id": 3,
                "name": 'Sticky Fingers Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for Sticky Fingers.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/sticky-fingers/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 23,
                "artist_id": 3,
                "name": 'Sticky Fingers Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for Sticky Fingers.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/sticky-fingers/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 24,
                "artist_id": 3,
                "name": 'Sticky Fingers Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for Sticky Fingers.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/sticky-fingers/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 4,
        "name": 'Frank Ocean',
        "slug": 'frank-ocean',
        "genre": 'Alternative R&B',
        "description": 'American singer-songwriter known for his experimental R&B, emotional storytelling and atmospheric production.',
        "image": "images/artists/frank-ocean/heroes/hero 1.jpeg",
        "portrait": "images/artists/frank-ocean/portraits/portrait 1.jpeg",
        "biography": 'Frank Ocean is an American singer-songwriter recognised for his emotional storytelling, experimental production and distinctive approach to contemporary R&B. His projects Channel Orange and Blonde received widespread acclaim for their songwriting and exploration of identity, love and personal experience. His influence extends across R&B, alternative pop and modern hip-hop.',
        "gallery": [
            "images/artists/frank-ocean/gallery/gallery 1.jpeg",
            "images/artists/frank-ocean/gallery/gallery 2.jpeg",
            "images/artists/frank-ocean/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 25,
                "artist_id": 4,
                "name": 'Frank Ocean Graphic T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for Frank Ocean.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/frank-ocean/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 26,
                "artist_id": 4,
                "name": 'Frank Ocean Minimal Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for Frank Ocean.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/frank-ocean/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 27,
                "artist_id": 4,
                "name": 'Frank Ocean Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for Frank Ocean.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/frank-ocean/merch/hats/hat 1.jpeg"
            },
            {
                "id": 28,
                "artist_id": 4,
                "name": 'Frank Ocean Blonde Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for Frank Ocean.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/frank-ocean/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 29,
                "artist_id": 4,
                "name": 'Frank Ocean Blonde Art Print',
                "category": "artwork",
                "description": 'Sample artwork merchandise for Frank Ocean.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/frank-ocean/merch/artwork/art 1.jpeg"
            },
            {
                "id": 30,
                "artist_id": 4,
                "name": 'Frank Ocean Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for Frank Ocean.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/frank-ocean/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 31,
                "artist_id": 4,
                "name": 'Frank Ocean Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for Frank Ocean.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/frank-ocean/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 32,
                "artist_id": 4,
                "name": 'Frank Ocean Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for Frank Ocean.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/frank-ocean/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 5,
        "name": 'Khruangbin',
        "slug": 'khruangbin',
        "genre": 'Psychedelic Funk / Soul',
        "description": 'American trio blending psychedelic funk, soul, dub and global musical influences.',
        "image": "images/artists/khruangbin/heroes/hero 1.jpeg",
        "portrait": "images/artists/khruangbin/portraits/portrait 1.jpeg",
        "biography": 'Khruangbin are an American trio from Houston, Texas, consisting of Laura Lee, Mark Speer and Donald Johnson. Their largely instrumental music blends psychedelic funk, soul, dub and musical influences from around the world. Known for their distinctive guitar tones, smooth basslines and relaxed rhythms, the band has developed an instantly recognisable sound and visual identity.',
        "gallery": [
            "images/artists/khruangbin/gallery/gallery 1.jpeg",
            "images/artists/khruangbin/gallery/gallery 2.jpeg",
            "images/artists/khruangbin/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 33,
                "artist_id": 5,
                "name": 'Khruangbin Graphic T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for Khruangbin.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/khruangbin/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 34,
                "artist_id": 5,
                "name": 'Khruangbin Groove Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for Khruangbin.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/khruangbin/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 35,
                "artist_id": 5,
                "name": 'Khruangbin Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for Khruangbin.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/khruangbin/merch/hats/hat 1.jpeg"
            },
            {
                "id": 36,
                "artist_id": 5,
                "name": 'Khruangbin Con Todo El Mundo Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for Khruangbin.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/khruangbin/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 37,
                "artist_id": 5,
                "name": 'Khruangbin Psychedelic Art Print',
                "category": "artwork",
                "description": 'Sample artwork merchandise for Khruangbin.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/khruangbin/merch/artwork/art 1.jpeg"
            },
            {
                "id": 38,
                "artist_id": 5,
                "name": 'Khruangbin Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for Khruangbin.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/khruangbin/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 39,
                "artist_id": 5,
                "name": 'Khruangbin Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for Khruangbin.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/khruangbin/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 40,
                "artist_id": 5,
                "name": 'Khruangbin Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for Khruangbin.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/khruangbin/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 6,
        "name": 'Men I Trust',
        "slug": 'men-i-trust',
        "genre": 'Dream Pop / Indie',
        "description": 'Canadian indie band known for their dreamy melodies, smooth basslines and atmospheric sound.',
        "image": "images/artists/men-i-trust/heroes/hero 1.jpeg",
        "portrait": "images/artists/men-i-trust/portraits/portrait 1.jpeg",
        "biography": 'Men I Trust are a Canadian indie band from Quebec, known for their dreamy production, soft vocals and smooth bass-driven melodies. Their music combines dream pop, indie and electronic influences to create a calm, atmospheric sound. Songs such as Show Me How and Lauren helped introduce their music to a wider international audience.',
        "gallery": [
            "images/artists/men-i-trust/gallery/gallery 1.jpeg",
            "images/artists/men-i-trust/gallery/gallery 2.jpeg",
            "images/artists/men-i-trust/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 41,
                "artist_id": 6,
                "name": 'Men I Trust Dream Pop T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for Men I Trust.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/men-i-trust/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 42,
                "artist_id": 6,
                "name": 'Men I Trust Soft Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for Men I Trust.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/men-i-trust/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 43,
                "artist_id": 6,
                "name": 'Men I Trust Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for Men I Trust.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/men-i-trust/merch/hats/hat 1.jpeg"
            },
            {
                "id": 44,
                "artist_id": 6,
                "name": 'Men I Trust Untourable Album Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for Men I Trust.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/men-i-trust/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 45,
                "artist_id": 6,
                "name": 'Men I Trust Dreamy Art Print',
                "category": "artwork",
                "description": 'Sample artwork merchandise for Men I Trust.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/men-i-trust/merch/artwork/art 1.jpeg"
            },
            {
                "id": 46,
                "artist_id": 6,
                "name": 'Men I Trust Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for Men I Trust.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/men-i-trust/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 47,
                "artist_id": 6,
                "name": 'Men I Trust Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for Men I Trust.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/men-i-trust/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 48,
                "artist_id": 6,
                "name": 'Men I Trust Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for Men I Trust.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/men-i-trust/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 7,
        "name": 'MF DOOM',
        "slug": 'mf-doom',
        "genre": 'Alternative Hip-Hop',
        "description": 'British-American rapper and producer celebrated for his intricate wordplay, masked persona and underground hip-hop influence.',
        "image": "images/artists/mf-doom/heroes/hero 1.jpeg",
        "portrait": "images/artists/mf-doom/portraits/portrait 1.jpeg",
        "biography": 'MF DOOM was a British-American rapper and producer known for his intricate lyricism, comic-book-inspired identity and distinctive metal mask. Born Daniel Dumile, he became one of underground hip-hop’s most influential figures. His music combined unusual samples, complex rhymes and an unmistakable sense of humour.',
        "gallery": [
            "images/artists/mf-doom/gallery/gallery 1.jpeg",
            "images/artists/mf-doom/gallery/gallery 2.jpeg",
            "images/artists/mf-doom/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 49,
                "artist_id": 7,
                "name": 'MF DOOM Mask Graphic T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for MF DOOM.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/mf-doom/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 50,
                "artist_id": 7,
                "name": 'MF DOOM DOOM Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for MF DOOM.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/mf-doom/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 51,
                "artist_id": 7,
                "name": 'MF DOOM Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for MF DOOM.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/mf-doom/merch/hats/hat 1.jpeg"
            },
            {
                "id": 52,
                "artist_id": 7,
                "name": 'MF DOOM MM..FOOD Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for MF DOOM.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/mf-doom/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 53,
                "artist_id": 7,
                "name": 'MF DOOM DOOM Art Print',
                "category": "artwork",
                "description": 'Sample artwork merchandise for MF DOOM.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/mf-doom/merch/artwork/art 1.jpeg"
            },
            {
                "id": 54,
                "artist_id": 7,
                "name": 'MF DOOM Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for MF DOOM.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/mf-doom/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 55,
                "artist_id": 7,
                "name": 'MF DOOM Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for MF DOOM.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/mf-doom/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 56,
                "artist_id": 7,
                "name": 'MF DOOM Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for MF DOOM.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/mf-doom/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 8,
        "name": 'PinkPantheress',
        "slug": 'pink-pantheress',
        "genre": 'UK Garage / Alternative Pop',
        "description": 'British singer and producer known for blending UK garage, drum and bass, and nostalgic pop.',
        "image": "images/artists/pink-pantheress/heroes/hero 1.jpeg",
        "portrait": "images/artists/pink-pantheress/portraits/portrait 1.jpeg",
        "biography": 'PinkPantheress is a British singer-songwriter and producer known for combining UK garage, drum and bass, bedroom pop and nostalgic electronic sounds. Her short, melodic songs first gained widespread attention online before reaching international audiences. Her distinctive production style and soft vocals have made her an influential voice in modern alternative pop.',
        "gallery": [
            "images/artists/pink-pantheress/gallery/gallery 1.jpeg",
            "images/artists/pink-pantheress/gallery/gallery 2.jpeg",
            "images/artists/pink-pantheress/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 57,
                "artist_id": 8,
                "name": 'PinkPantheress Baby Tee',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for PinkPantheress.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/pink-pantheress/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 58,
                "artist_id": 8,
                "name": 'PinkPantheress Pink Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for PinkPantheress.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/pink-pantheress/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 59,
                "artist_id": 8,
                "name": 'PinkPantheress Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for PinkPantheress.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/pink-pantheress/merch/hats/hat 1.jpeg"
            },
            {
                "id": 60,
                "artist_id": 8,
                "name": 'PinkPantheress Heaven Knows Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for PinkPantheress.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/pink-pantheress/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 61,
                "artist_id": 8,
                "name": 'PinkPantheress Nostalgic Poster',
                "category": "artwork",
                "description": 'Sample artwork merchandise for PinkPantheress.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/pink-pantheress/merch/artwork/art 1.jpeg"
            },
            {
                "id": 62,
                "artist_id": 8,
                "name": 'PinkPantheress Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for PinkPantheress.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/pink-pantheress/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 63,
                "artist_id": 8,
                "name": 'PinkPantheress Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for PinkPantheress.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/pink-pantheress/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 64,
                "artist_id": 8,
                "name": 'PinkPantheress Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for PinkPantheress.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/pink-pantheress/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 9,
        "name": 'Dope Lemon',
        "slug": 'dope-lemon',
        "genre": 'Psychedelic Rock / Indie Folk',
        "description": 'Australian psychedelic music project led by Angus Stone, known for its laid-back grooves, dreamy melodies and mellow sound.',
        "image": "images/artists/dope-lemon/heroes/hero 1.jpeg",
        "portrait": "images/artists/dope-lemon/portraits/portrait 1.jpeg",
        "biography": 'Dope Lemon is the psychedelic music project of Australian musician Angus Stone. The project combines relaxed guitar melodies, blues influences and hazy psychedelic production to create a distinctive laid-back sound. Albums such as Honey Bones and Smooth Big Cat showcase its dreamy atmosphere, storytelling and mellow grooves.',
        "gallery": [
            "images/artists/dope-lemon/gallery/gallery 1.jpeg",
            "images/artists/dope-lemon/gallery/gallery 2.jpeg",
            "images/artists/dope-lemon/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 65,
                "artist_id": 9,
                "name": 'Dope Lemon Graphic T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for Dope Lemon.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/dope-lemon/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 66,
                "artist_id": 9,
                "name": 'Dope Lemon Psychedelic Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for Dope Lemon.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/dope-lemon/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 67,
                "artist_id": 9,
                "name": 'Dope Lemon Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for Dope Lemon.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/dope-lemon/merch/hats/hat 1.jpeg"
            },
            {
                "id": 68,
                "artist_id": 9,
                "name": 'Dope Lemon Honey Bones Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for Dope Lemon.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/dope-lemon/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 69,
                "artist_id": 9,
                "name": 'Dope Lemon Dope Lemon Art Print',
                "category": "artwork",
                "description": 'Sample artwork merchandise for Dope Lemon.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/dope-lemon/merch/artwork/art 1.jpeg"
            },
            {
                "id": 70,
                "artist_id": 9,
                "name": 'Dope Lemon Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for Dope Lemon.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/dope-lemon/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 71,
                "artist_id": 9,
                "name": 'Dope Lemon Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for Dope Lemon.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/dope-lemon/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 72,
                "artist_id": 9,
                "name": 'Dope Lemon Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for Dope Lemon.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/dope-lemon/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 10,
        "name": 'Kaytranada',
        "slug": 'kaytranada',
        "genre": 'Electronic / House / Hip-Hop',
        "description": 'Haitian-Canadian producer and DJ known for his distinctive blend of house, funk, hip-hop and R&B.',
        "image": "images/artists/kaytranada/heroes/hero 1.jpeg",
        "portrait": "images/artists/kaytranada/portraits/portrait 1.jpeg",
        "biography": 'Kaytranada is a Haitian-Canadian producer and DJ recognised for his distinctive combination of house, funk, hip-hop and R&B. His rhythmic production style features energetic drum patterns, soulful samples and smooth basslines. Albums such as 99.9% and Bubba helped establish him as one of contemporary electronic music’s most recognisable producers.',
        "gallery": [
            "images/artists/kaytranada/gallery/gallery 1.jpeg",
            "images/artists/kaytranada/gallery/gallery 2.jpeg",
            "images/artists/kaytranada/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 73,
                "artist_id": 10,
                "name": 'Kaytranada Graphic T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for Kaytranada.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/kaytranada/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 74,
                "artist_id": 10,
                "name": 'Kaytranada Club Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for Kaytranada.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/kaytranada/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 75,
                "artist_id": 10,
                "name": 'Kaytranada Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for Kaytranada.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/kaytranada/merch/hats/hat 1.jpeg"
            },
            {
                "id": 76,
                "artist_id": 10,
                "name": 'Kaytranada Bubba Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for Kaytranada.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/kaytranada/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 77,
                "artist_id": 10,
                "name": 'Kaytranada Electronic Art Print',
                "category": "artwork",
                "description": 'Sample artwork merchandise for Kaytranada.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/kaytranada/merch/artwork/art 1.jpeg"
            },
            {
                "id": 78,
                "artist_id": 10,
                "name": 'Kaytranada Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for Kaytranada.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/kaytranada/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 79,
                "artist_id": 10,
                "name": 'Kaytranada Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for Kaytranada.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/kaytranada/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 80,
                "artist_id": 10,
                "name": 'Kaytranada Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for Kaytranada.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/kaytranada/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 11,
        "name": 'Tyler, the Creator',
        "slug": 'tyler-the-creator',
        "genre": 'Alternative Hip-Hop / R&B',
        "description": 'American rapper, producer and creative artist known for his genre-blending albums, distinctive production and visual style.',
        "image": "images/artists/tyler-the-creator/heroes/hero 1.jpeg",
        "portrait": "images/artists/tyler-the-creator/portraits/portrait 1.jpeg",
        "biography": 'Tyler, the Creator is an American rapper, producer and creative artist known for his constantly evolving musical and visual identity. Emerging as a founding member of Odd Future, he developed a solo career combining hip-hop, jazz, soul and alternative R&B. Albums such as Flower Boy, Igor and Call Me If You Get Lost demonstrate his distinctive production and storytelling.',
        "gallery": [
            "images/artists/tyler-the-creator/gallery/gallery 1.jpeg",
            "images/artists/tyler-the-creator/gallery/gallery 2.jpeg",
            "images/artists/tyler-the-creator/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 81,
                "artist_id": 11,
                "name": 'Tyler, the Creator Graphic T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for Tyler, the Creator.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/tyler-the-creator/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 82,
                "artist_id": 11,
                "name": 'Tyler, the Creator Colourblock Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for Tyler, the Creator.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/tyler-the-creator/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 83,
                "artist_id": 11,
                "name": 'Tyler, the Creator Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for Tyler, the Creator.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/tyler-the-creator/merch/hats/hat 1.jpeg"
            },
            {
                "id": 84,
                "artist_id": 11,
                "name": 'Tyler, the Creator IGOR Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for Tyler, the Creator.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/tyler-the-creator/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 85,
                "artist_id": 11,
                "name": 'Tyler, the Creator Flower Boy Art Print',
                "category": "artwork",
                "description": 'Sample artwork merchandise for Tyler, the Creator.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/tyler-the-creator/merch/artwork/art 1.jpeg"
            },
            {
                "id": 86,
                "artist_id": 11,
                "name": 'Tyler, the Creator Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for Tyler, the Creator.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/tyler-the-creator/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 87,
                "artist_id": 11,
                "name": 'Tyler, the Creator Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for Tyler, the Creator.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/tyler-the-creator/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 88,
                "artist_id": 11,
                "name": 'Tyler, the Creator Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for Tyler, the Creator.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/tyler-the-creator/merch/accessories/stickers 1.jpeg"
            },
        ]
    },
    {
        "id": 12,
        "name": 'Lorde',
        "slug": 'lorde',
        "genre": 'Alternative Pop / Art Pop',
        "description": 'New Zealand singer-songwriter known for her distinctive vocals, introspective lyrics and atmospheric pop production.',
        "image": "images/artists/lorde/heroes/hero 1.jpeg",
        "portrait": "images/artists/lorde/portraits/portrait 1.jpeg",
        "biography": 'Lorde is a New Zealand singer-songwriter known for her distinctive vocals, introspective songwriting and atmospheric approach to pop music. She gained international recognition with Royals and her debut album Pure Heroine. Later projects including Melodrama and Solar Power explored personal growth, relationships and changing perspectives through inventive pop production.',
        "gallery": [
            "images/artists/lorde/gallery/gallery 1.jpeg",
            "images/artists/lorde/gallery/gallery 2.jpeg",
            "images/artists/lorde/gallery/gallery 3.jpeg",
        ],
        "merch": [
            {
                "id": 89,
                "artist_id": 12,
                "name": 'Lorde Graphic T-Shirt',
                "category": "t-shirts",
                "description": 'Sample t shirts merchandise for Lorde.',
                "price": 39.99,
                "stock": 20,
                "image": "images/artists/lorde/merch/t-shirts/shirt 1.jpeg"
            },
            {
                "id": 90,
                "artist_id": 12,
                "name": 'Lorde Tour Hoodie',
                "category": "hoodies",
                "description": 'Sample hoodies merchandise for Lorde.',
                "price": 79.99,
                "stock": 15,
                "image": "images/artists/lorde/merch/hoodies/hoodie 1.jpeg"
            },
            {
                "id": 91,
                "artist_id": 12,
                "name": 'Lorde Embroidered Cap',
                "category": "hats",
                "description": 'Sample hats merchandise for Lorde.',
                "price": 29.99,
                "stock": 12,
                "image": "images/artists/lorde/merch/hats/hat 1.jpeg"
            },
            {
                "id": 92,
                "artist_id": 12,
                "name": 'Lorde Melodrama Vinyl',
                "category": "vinyl",
                "description": 'Sample vinyl merchandise for Lorde.',
                "price": 49.99,
                "stock": 10,
                "image": "images/artists/lorde/merch/vinyl/vinyl 1.jpeg"
            },
            {
                "id": 93,
                "artist_id": 12,
                "name": 'Lorde Melodrama Art Print',
                "category": "artwork",
                "description": 'Sample artwork merchandise for Lorde.',
                "price": 24.99,
                "stock": 25,
                "image": "images/artists/lorde/merch/artwork/art 1.jpeg"
            },
            {
                "id": 94,
                "artist_id": 12,
                "name": 'Lorde Canvas Tote Bag',
                "category": "tote-bags",
                "description": 'Sample tote bags merchandise for Lorde.',
                "price": 24.99,
                "stock": 18,
                "image": "images/artists/lorde/merch/tote-bags/tote 1.jpeg"
            },
            {
                "id": 95,
                "artist_id": 12,
                "name": 'Lorde Crewneck Sweatshirt',
                "category": "sweatshirts",
                "description": 'Sample sweatshirts merchandise for Lorde.',
                "price": 64.99,
                "stock": 14,
                "image": "images/artists/lorde/merch/sweatshirts/sweatshirt 1.jpeg"
            },
            {
                "id": 96,
                "artist_id": 12,
                "name": 'Lorde Sticker Pack',
                "category": "accessories",
                "description": 'Sample accessories merchandise for Lorde.',
                "price": 9.99,
                "stock": 40,
                "image": "images/artists/lorde/merch/accessories/stickers 1.jpeg"
            },
        ]
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

# runs when everything before it is correct
if __name__ == "__main__":
  # starts the server
    app.run(debug=True, port=5001)
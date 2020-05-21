import json, copy, re
from flask import Flask
from flask import render_template
from flask import Response, request, jsonify

app = Flask(__name__)

current_id = 30
result = []
search_key = None

venues = [
    {
        "name": "Bowery Ballroom",
        "is_deleted": False,
        "id": 0,

        "image": "https://assets3.thrillist.com/v1/image/2812852/size/tl-horizontal_main.jpg",
        "description": "A decently sized bar and lounge downstairs and stairs at both the front and the back of the 575-person capacity performance space help keep crowd movement fluid -- or the place’s knack for catching acts just as they are beginning to have their moment, there’s a special alchemy that makes a show at the Bowery great. It also doesn’t hurt that Bowery Ballroom is smack in the middle of the food and drink hub of the Lower East Side, providing fantastic options for pre- and post- show fun.",
        "rating": 4.6,
        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Penny Pennell",
                "review": "when we discovered our favourite band was touring and playing at the Bowery we decided it would be a perfect reason to go to NYC for the weekend.  As a Canadian, I've heard of this venue over the years and thought it would be great to check out. It did not disappoint. We stood at the back bar and had fantastic sight lines. The hype is real! This is a fantastic live music venue."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Carol Campion",
                "review": "Saw Shannon Lay who performed with Ty Seagull and I was blown away! The show was very well liked by everyone in the balcony and on the floor. It was fantastic. I met people who traveled from Canada 🇨🇦 just to see Shannon . Ty’s wife also gave me a CD . Thanks Great Place/ Show/ People who work here are All fabulous!!!"
            },
            {
                "id": 2,
                "user": "Candypie 2010",
                "review": "The place is nice and spacious for a good crowd of 568 people only wish the bar had better choices from drinks mostly all they have are beer drinks. my friend also said the sound system need to be a little better when they sing and be a little creative with the background settings other than that I enjoyed myself and the performance"
            },
        ],
    },
    {
        "name": "Mercury Lounge",
        "is_deleted": False,
        "id": 1,

        "image": "https://assets3.thrillist.com/v1/image/2813014/size/tl-horizontal_main.jpg",

        "description": "Best spot for up and coming artists The 250 capacity room at Mercury Lounge solidified its reputation as a hotspot for up and coming artists when the Strokes were discovered here in 2000. It’s somehow maintained this cred despite ditching its independence in 2017 to team up with promoter Live Nation under the Mercury East banner (which also includes the Bowery Ballroom). Fantastic programming and cheap ticket prices still draw fans to the small, barebones room, show after show",

        "rating": 4.4,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Keri Clearwater",
                "review": "My first Red Party! I had so much fun. This was a great venue for a decent sized gathering."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Christopher Moscatelli",
                "review": "Great little venue, intimate atmosphere. Lauren the bartender took great care of me. Will definitely catch another show here on a future visit."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Candypie 2010",
                "review": "Classic NYC bar to see bands. Maybe legendary... Decent space, good sound and lighting. While they do have an $11 beer and shot special, $9 drafts does seem high. They don't sell food here and unlike other venues that don't, they don't allow outside food??? Cool space and location but docked a star for the too-cool-for-school staff (guys you're not, you're a late night bouncer or Monday night bartender). Manager should explain that it doesn't cost extra to be nice and btw they're in a service business - oh, and it could help tips..."
            },
        ],
    },
    {
        "name": "Market Hotel",
        "is_deleted": False,
        "id": 2,

        "image": "http://www.brooklynvegan.com/files/img/ah/sleater-kinney/market-hotel/sleater-kinney-58.jpg",

        "description": "Best spot for small shows. Hidden inside an old building facing the elevated JMZ train, Market Hotel could be easy to miss if it weren’t for the gaggle of concert-goers smoking out front. Originally an artists-in-residence space when it opened in 2008, Market Hotel endured a shutdown and renovations before reopening as a concert hall in 2015. Its unique history and commitment to curating talent with cult-like followings helps the smaller spot retain its underground vibe. The room’s odd V shape doesn’t hinder dancing or crowd surfing, and it’s a feeling like no other when the rickety floor shakes from both the bass and the trains passing through the nearby Myrtle-Broadway station.",

        "rating": 4.4,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Kelsey Brow",
                "review": "Super cool look, particularly before it heats up  and fogs the window! You can see the subway go by behind the performers. Such an iconic NYC look 🤩 AND! The only metal bar in town with multiple toilets for the ladies/stall users. An important detail because they are also the metal bar with the best beer selection!! And very solid hard liquor selection as well. One caveat is if you like to be front and center like me... the acoustics aren’t so hot. Move back a bit for a better sound. Fun venue!! RIP my left earring that was kicked out of my ear by a crowd surfer! Woo! 🤘"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Ben Holzwarth",
                "review": "Very Brooklyn. Cool space. Backdrop is the subway and you watch the world go by. You can't actually hear the subway though thankfully. Good bar."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Moondy Abel",
                "review": "A bit difficult to find, save for one small sign. The venue is on the 2nd floor and has a more intimate feel to it. The stage has a nice view of the subway station as a backdrop. If you don't mind the dive bar appearance, Market Hotel is one of Brooklyn's better kept secrets."
            },
        ],
    },
    {
        "name": "Barclays Center",
        "is_deleted": False,
        "id": 3,

        "image": "https://assets3.thrillist.com/v1/image/2812830/size/tl-horizontal_main.jpg",

        "description": "Best venue for an actually enjoyable arena experience. Manhattan’s iconic Madison Square Garden may be NYC’s most famous arena, but Brooklyn’s Barclays Center is an upgrade. First opened in 2012, Barclay’s has a clean, modern aesthetic, and it was designed with an eye toward the future of entertainment, featuring featuring improved acoustics and seating that make even the nosebleed seats worth the price of admission. And unlike MSG, it’s a world away from Midtown, meaning the massive concert crowds don’t have to compete with droves of tourists. -- SB",

        "rating": 4.5,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Gene Yu",
                "review": "New stadium that has pretty much all of the expected amenities you would come to expect, though I did appreciate the fact that they had multiple carts that also sold alcohol to alleviate long lines. Lot of foot traffic right around the stadium due its placement being surrounded by shops and restaurants. I sat in the lower 200s section for a Nets game and still found them to be really good seats to watch the game."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Melissa Caldero",
                "review": "Can't go wrong at Barclays! Nice big space hosting a variety of events. My son had his college graduation here. There were 14,000 in attendance! Sound quality was really nice. As for food and drinks, as usual, as in any stadium, pricey but good."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Alex",
                "review": "Awesome venue for a basketball game! Love the grey and black color scheme and the bright lights and architecture of the arena. A wide variety of food options and an entertaining in-game experience. The court looks very nice as well, especially with the new grey colors. The angling of the upper level provides a clear view of the action, even from the highest rows. Overall, a clean, modern arena that felt like a lounge from the moment I walked inside. Convenient subway exit right in front of the arena too. My primary critique would be the incredibly small distance between rows of seats on the upper level, it was difficult to maneuver even with people standing out of the way. I understand the need to hold more people, but a little more room would be nice. Otherwise, I definitely look forward to returning to Barclays Center in the future for another basketball game, maybe even making it a yearly tradition."
            },
        ]
    },
    {
        "name": "Brooklyn Steel",
        "is_deleted": False,
        "id": 4,

        "image": "https://assets3.thrillist.com/v1/image/2813013/size/tl-horizontal_main.jpg",

        "description": "Terminal 5 enjoyed a long reign as the city’s de rigueur few-thousand capacity venue. But Terminal 5 is... bad. Its Hell’s Kitchen location is inconvenient, and the layout lends itself to gridlock. It’s enough to make New Yorkers miss the subway. Luckily, since Brooklyn Steel opened in 2017 the Greenpoint sister venue -- both are owned by Bowery Presents -- has been cutting into Terminal 5’s share of mid-sized bookings. It isn’t perfect, but ample space and adequate sightlines make it the best of its kind in New York. -- AG",

        "rating": 4.6,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Michael Mortensen",
                "review": "Saw Tove Lo here on 2/13.  Really great venue, nice and big, multiple bars, and two levels. Super large bathrooms so there was never a wait.Easy security. Only downside is that it’s not really by the subway (15 minutes walking from the L). Great time!"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Shawn The Sheep",
                "review": "A great venue! Large and spacious! After a terrible experience at another venue this weekend I had to come show this place some love because every time I’ve been here has been a good experience! This is absolutely my go-to for concerts in NYC, always happy when my fave artists perform here."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Jeremy Christian",
                "review": "Hands down the best music venue in NYC. I was here for their first ever show, LCD Soundsystem. The sound was flawless, as were the sight lines. Imagine a refined and perfected Terminal 5 and you get the vibe for Brooklyn Steel. Since then I've returned for multiple shows (including a brilliant performance by Phoenix) because nowhere else in the city compares. Every experience here is utter perfection."
            },
        ]
    },
    {
        "name": "The Apollo Theater",
        "is_deleted": False,
        "id": 5,

        "image": "https://assets3.thrillist.com/v1/image/2813015/size/tl-horizontal_main.jpg",

        "description": "Nothing tops showtime at the legendary Apollo Theater for a traditional experience amid Old New York ambiance and ornate design. The neo-classical theater is a cathedral of African American cultural history that made or broke stars of yore. Ella Fitzgerald debuted here, James Brown recorded one of the greatest albums of all time here, and a young Jimi Hendrix won an amateur night contest here in 1964. Greatness permeates the landmark building. Plus, a show at the Apollo is an excellent occasion to take advantage of Harlem’s excellent restaurant scene, including soul food classics like Amy Ruth’s and Sylvia’s and newer spots like Clay, ROKC, and Marcus Samuelsson’s Red Rooster. -- AG",

        "rating": 4.6,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Elvin Rodriguez",
                "review": "Went to Apollo.to buy my mother and aunt some jazz tickets. My mother loves Apollo and Red lobsters next door. It's a landmark. Lots of history walked through those doors. Comedy nights is the best for me but mommy loves jazz"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Allen Fields",
                "review": "Amazing venue!  The Apollo Theater is a must visit concert site for any music fan.  Opeth was incredible, and the sound mix was stellar.  A treasure in the heart of Harlem.  I felt safe, welcome, and the staff went out of their way to accommodate my mobility issues.  Hats off to them!"
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "bernard Greene",
                "review": "First of all, I have been going to the Apollo Theater since I was a kid.I have seen a variety of singers & musicians over the years and have never been disappointed.This Holiday Gospel Celebration with Donald Lawrence & Yolanda Adams was no exception. The music was very inspirational, enjoyable and caused you to get involved in some way, whether singing along, patting your feet, clapping your hands, dancing in or out of your seat and even.....SHOUTING!"
            },
        ]
    },
    {
        "name": "Lehman Center for the Performing Arts",
        "is_deleted": False,
        "id": 6,

        "image": "https://assets3.thrillist.com/v1/image/2812947/size/tl-horizontal_main.jpg",

        "description": "Lincoln Center might seem the obvious choice here, but the not-for-profit Lehman Center gets credit for bringing the fine arts beyond Manhattan. With venues like the Paradise Theater and the Olympic Theater Concert Hall shutting down over the years, the Bronx has had bad luck holding onto large performance spaces. But year after year, the 2,278-seat Lehman Center brings acts like Janelle Monáe, ballet performances, world dance and Salsa groups, and tributes to David Bowie to its stage. -- AG",

        "rating": 4.5,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Ihor Strutynsky",
                "review": "Good value for Your hard earned dollar. Clean. Comfortable seats. Clean bathrooms. Appropriate temperature. Good selection of talented, varied, national and international artists and company's. Easily accessible via Mass Transit. Problems resolved relatively well. Recommended."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Nancy J",
                "review": "Concerts are awesome Doesn't matter where you sit all good . Reasonable  ticket prices."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Arleen Castillo",
                "review": "Went to see Elvis Crespo in concert and it was amazing. The Lehman Center was spacious, clean and the staff who were working were top notch 👍 They had a lot for parking and the $10 was worth not looking for a spot and it was close to the entrance of the campus. Overall a great experience and can't wait for the next concert there"
            },
        ]
    },
    {
        "name": "Elsewhere",
        "is_deleted": False,
        "id": 7,

        "image": "https://assets3.thrillist.com/v1/image/2812870/size/tl-horizontal_main.jpg",

        "description": "From the team behind the former Williamsburg club Glasslands Gallery, Elsewhere is an arts space/venue housed in a converted warehouse in Bushwick. The multi-room neighborhood staple is able to host two separate bills every night, and its trendy upper-level/rooftop bar is always open for business after the show. An eclectic lighting set up and large open floor make Elsewhere’s main room particularly great for the DJs and electronic musicians who spin sets there late on Friday and Saturday nights. The industrial atmosphere feels like an art scene rave. -- SB",

        "rating": 4.6,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Yael Weiss",
                "review": "First time going to an event here. Really liked the multiple floors. They have 3 different places to hear music any given night, with the loft even providing food and places to sit. Multiple gender neutral bathrooms that were relatively clean, even had some nice art installations. As for the music and acoustics, I thought The Hall was wonderful. Went to see a DJ set and we were able to hear it loud and clear and find space where people weren't on top of each other. Would definitely recommend!!!!"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Fabrício Kury",
                "review": "Great club for finding real club culture as opposed to a commercial music venue. The parties I've been here were not too crowded, folks do sway into the groove and dance, and I always have like a workout of a dancing night. The passage to the second stage is fun in itself as it across to the other side literally via the restrooms. The toilets are decently clean."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Andre Gribble",
                "review": "First time at this place and it was great. Went to see Deerhoof live, which would have been awesome anywhere, but this space was perfect for it: the sound is great, it's not hard to get a good spot if you get on time (and even return to it if you have to go to the bathroom or the bar), it gets crowded but not uncomfortably so. Standing room only, but I don't see why you'd want to sit at a show like this."
            },
        ]
    },
    {
        "name": "H0L0",
        "is_deleted": False,
        "id": 8,

        "image": "https://66.media.tumblr.com/0f967efe1c68eddd3da9cd5b6af8ffd6/tumblr_p9tv3hSi3B1u3zgyoo8_500.jpg",

        "description": "H0L0’s entrance is almost as obscure as its minimal online presence, giving your stop here a twinge of hush-hush cool. Inside, the industrial, intimate, gallery-like space is equally fit for DJs, pop acts, and rappers. Technicolor lights and visuals further the artsy air. Here, you’ll get up close and personal with emerging artists and you’re likely to catch the next underground great. -- SB",

        "rating": 4.3,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Jamekia Swepson",
                "review": "Great place for new artists to try music. Crowd is eclectic"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "DJ Transaction",
                "review": "I give extra star because I played there and I like it personally. The problem with this place is that it's in the middle of no where and I can't see anyone going here unless there is a big promoted event."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Thiago DeMoura",
                "review": "The team at dub day has made a place where progressive thoughts and sounds could be accepted. HOLO was the space in which that idea was able to come alive and we thank the staff and venue for letting us use it on a weekely basis."
            },
        ]
    },
    {
        "name": "Rough Trade",
        "is_deleted": False,
        "id": 9,

        "image": "https://assets3.thrillist.com/v1/image/2813012/size/tl-horizontal_main.jpg",

        "description": "Originally a British music label and chain of record stores, the sole Rough Trade on this side of the Atlantic features the same vibe as London’s Rough Trade East: a duel record store/music venue combo. The back performance area is tiny, but its retail adjacency has its perks. In addition to concerts, artists also often sign records before or after shows, there a few free, acoustic sets on weekend afternoons, and fans can score invites to exclusive listening parties ahead of album releases. -- SB",

        "rating": 4.7,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "warren huberman",
                "review": "For those of you who can remember, this is as close to Tower and Virgin that you can get in 2020. Great selection, nicely laid out and with several listening stations (!) for the latest releases. Prices are fair as well. Mostly for new releases but there is some used stuff too. Worth the trip!"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "John J",
                "review": "Amazing store. I could spend all day in here. Great selection, carefully curated displays. Large and welcoming. Very good vibes"
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Brian Ferdman",
                "review": "Half record store and half performance space, Rough Trade was built from old ship containers, giving it a cool vibe (which can also lead to some cool drafts in winter). The record store is spacious, and the performance venue is excellent, affording patrons with very good sound and mostly good sight lines. While the balcony railing can occasionally get in the line of sight for those patrons, the balcony itself is fairly spacious and offers limited bench seating. A downstairs bar keeps customers sated."
            },
        ]
    },
    {
        "name": "Trans-Pecos",
        "is_deleted": False,
        "id": 10,

        "image": "https://assets3.thrillist.com/v1/image/2812862/size/tl-horizontal_main.jpg",

        "description": "Trans-Pecos, one of the area’s few standing, all-ages DIY venues, hosts some of the most exciting emerging artists in the city. Some small tours pass through, but you’ll typically see Brooklyn bands and local students on Trans-Pecos’ humble stage. The small space is adorned with house plants and frequently features kaleidoscopic projections on its walls like it’s an art school dorm room -- appropriate for its younger-leaning crowd. Check your scenester proclivities at the door, no matter how cool its underground patrons seem, Trans-Pecos regulars are just looking to enjoy new music and dance (or mosh) on the floor. -- SB",

        "rating": 4.6,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Michael C. Antonino",
                "review": "I saw Jeff Rosenstock play here on the 23rd of December and it was fantastic. This place let him play every Monday in December for Black Lives Matter when h I think is really cool. The venue was PACKED (I cannot stress that enough.) It was shoulder-to-shoulder in there. I'm not sure what it's like when an artist without that big of a draw plays there. What I'm trying to say basically is it's cool that they didn't seem to turn anyone away due to capacity. I heard from (I think) locals that Trans Pecos serves food during the day time and it appears they serve higher end coffee as well which would've been nice to have."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Alf Lenni Erlandsen",
                "review": "I cannot stay away from this place. A great spot for those with curious ears, eyes and minds. Staff is the best and crowd varies a lot. Not alot of venues likes these left in this city."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Patrick Finnen",
                "review": "Cool small space to see a show. Big expansive backyard area with tables."
            },
        ]
    },
    {
        "name": "LunÀtico",
        "is_deleted": False,
        "id": 11,

        "image": "https://assets3.thrillist.com/v1/image/2812832/size/tl-horizontal_main.jpg",

        "description": "Many NYC music venues are attached to a bar, but here we mean a place where the music and the bartending happen in same space. There is no better spot than Bar LunÀtico. The Bed-Stuy restaurant and bar sports a live act every single night from an impressive range of global, jazz, blues, and rock acts -- Daptone soul singer Naomi Shelton regularly performs at the Sunday gospel brunch. The hyper-intimate space, mostly occupied by small café tables, and first-come-first-served policy makes for a truly unique neighborhood vibe. Coming for a drink, meal or coffee is like listening to music at a friend’s house. -- AG",

        "rating": 4.7,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Karen Glenn",
                "review": "Went to the Sunday Gospel brunch - what an experience! Beverly Crosby on vocals and Greg Monk on the organ. Such an emotional and beautiful performance. Beverly has  a powerful and moving voice in such an intimate setting-really something special. Loved the bar staff and cocktails- this place has a real appreciation for musicians. Would highly recommend- and will definitely be coming back"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Brad Klein",
                "review": "Solid neighborhood bar. Packed when there's funky live music in the back. Menu looks delicious - will be back!"
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Dan Calladine",
                "review": "A great local bar.  We went for the weekend brunch (inc live music on a Sunday) and could not have had a better time.  Great food, excellent iced coffee, and a wonderful vibe"
            },
        ]
    },
    {
        "name": "The Bitter End",
        "is_deleted": False,
        "id": 12,

        "image": "https://lh5.googleusercontent.com/p/AF1QipMMQp_hGADGyjgbmampZIhmKNM_lRqiU1aRezRO=w408-h306-k-no",

        "description": "The Bitter End is a 230-person capacity nightclub, coffeehouse and folk music venue in New York City's Greenwich Village. It opened in 1961 at 147 Bleecker Street under the auspices of owner Fred Weintraub. The club changed its name to The Other End in June 1975. However, after a few years the owners changed the club's name back to the more recognizable The Bitter End. It remains open under new ownership.",

        "rating": 4.3,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "J Droid Dennis",
                "review": "Great music every night! The service is exceptional, especially Ann our waitress. Checks drinks if empty, but not intrusive. Remembered all drinks and prompt service. (Tip generously!) This place has introduced some greats and still has unique and talented acts to this day. Can anyone say Robert Zimmerman?"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Rick Culleton",
                "review": "Good music and a good time. Twice I've seen great cover bands here. Last night they closed with a very good Zeppelin song. Well worth the $10 cover. There are a handful of live music venues on Bleaker and a couple good places to eat. This part of town makes for a great night out."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Sarah Lee",
                "review": "Wow, such a cool bar! I highly recommend this place if you enjoy live music, drinking, and love to meet weird people. Great staff and super hip interior. It's a small bar, but it's definitely a great place to listen to amazing music and just have a great time. Also keep in mind that you will have to order 2 drinks per band/show that performs."
            },
        ]
    },
    {
        "name": "Forest Hills Stadium",
        "is_deleted": False,
        "id": 13,

        "image": "https://media.timeout.com/images/102626829/380/285/image.jpg",

        "description": "After extensive renovation, this storied tennis stadium—home to memorable matches and concerts from the ’20s through the ’80s (including the Beatles, Stones and others)—reopened its doors in 2013 with a rowdy Mumford & Sons gig. These days, the venue regularly hosts a wide variety of artists ranging from Chainsmokers to Van Morrison.",

        "rating": 4.5,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Seth Ayers",
                "review": "Forest Hills Stadium is one of the nicest music venues I've been to.  It's got a tiny music festival vibe to it;  Great drinks, plenty of options for food, and almost no lines for the restrooms.  The show itself was wonderful, great acoustics."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Arthur Shatz",
                "review": "Great venue. Easy to get to by public transit. Superb sound system.  Beautiful clean brand new restrooms. Outstanding and varied food court. Bleacher seats have no seat backs, but not a big deal unless you have back problems."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Julissa Herrera",
                "review": "Public transportation commute to the stadium was not complicated. The security line was smooth and quick. Staff was incredibly friendly. And space itself provided great seating options and view. I didn't used restroom or buy any food or drinks but there seems to be plenty of those. Be sure to dress accordingly as it's outdoor and can get breezy and cool up on the top tiers. Enjoy the experience I'd highly recommend."
            },
        ]
    },
    {
        "name": "Rockwood Music Hall",
        "is_deleted": False,
        "id": 14,

        "image": "https://media.timeout.com/images/101206475/750/422/image.jpg",

        "description": "This LES haunt started as a tiny, cramped storefront space and has expanded into a multistage downtown fixture. Rockwood books an endless parade of aspirants, some of whom (such Chris Thile, Gabriel Kahane) have gone on to become stars of the singer-songwriter and Americana realms.",

        "rating": 4.5,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Boris Lemeshev",
                "review": "Great place if you want to see local bands perform. The acoustics are incredible and the sound system they use is top notch. Always great programs, covers, musicians, and the price is very reasonable. In total 3 stages for one music hall. Always nice to bring your friends to see a good concert and have a good time, and they have an open bar too, which is a plus."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Russell Wustenberg",
                "review": "We came here with a friend to see a local artist perform a set. The venue is cozy and ideal for small music events. The artist was high-quality, and she had worked with major artists and labels so we were getting a bargain for the cost of the event. We didn’t drink, but there were waiters running around serving directly to the clients at their tables. Overall it was a wonderful evening and I would go back anytime I’m in the village!"
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Nathan Drapela",
                "review": "I really want to like this place, but I have some frustrations. I went to in stage 2 to see two solo singer/songwriter folk singers, one of whom I was familiar with and the other I had never heard before. Both singers were amazing and am very glad there are venues for performers like these. However, I was less impressed with the venue itself. While very cozy, it seems to operate more as a bar, where there happens to be live music than a performance space where they serve alcohol. There's apparently a 2 drink minimum for sitting and 1 drink minimum for standing."
            },
        ]
    },
    {
        "name": "Music Hall of Williamsburg",
        "is_deleted": False,
        "id": 15,

        "image": "https://media.timeout.com/images/100108711/380/285/image.jpg",

        "description": "Run by local promoter Bowery Presents, this Williamsburg outpost is basically a mirror image of similarly sized Bowery Ballroom, one upping its Manhattan counterpart with improved sightlights—including elevated areas on either side of the room—and a bit more breathing room. With booking that ranges from indie-rock bands to hip-hop acts, it's one of the best rooms in New York to see a show.",
        "rating": 4.5,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Chris Meyer",
                "review": "Venue has very good sound quality and a cool vibe. It took ages to get in due to security. Very happy to feels safe but wish there was a more streamlined system. I'd definitely see other shows here but would suggest you arrive early."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Leifur Björnsson",
                "review": "Love this venue. Size is good and it always sounds nice. I've seen and played a number of shows here. The area around it is nice, walk a few steps to get a great view of Manhattan and the river, good restaurants and etc. The area has gotten gentrified a lot these past few years, used to be better, more authentic, but still it's a nice spot."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Harpy Monet",
                "review": "Very efficient security and ticketing process! Had lots of fun. Very convenient bar and restroom downstairs of the main music hall. Awesome time!"
            },
        ]
    },
    {
        "name": "Beacon Theatre",
        "is_deleted": False,
        "id": 16,

        "image": "https://media.timeout.com/images/100262465/380/285/image.jpg",

        "description": "This spacious former vaudeville theater, resplendent after a recent renovation, hosts a variety of popular acts, from Steely Dan to Ryan Adams. While the vastness can seem daunting for performers and audience members alike, the gaudy interior and uptown location make you feel as though you’re having a real night out on the town. ",

        "rating": 4.7,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Paul faria",
                "review": "Beautiful theater.  The seats are a little tight for wider guys like myself but I still found them comfortable.  They also had plenty of beverage stations on each floor to keep the lines short. We saw Seinfeld there and the acoustics were great. I would definitely recommend going just to see the interior.  It is a style that would be hard to replicate today."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Chris Becker",
                "review": "Love this venue. The architecture is historic. The bar and bathroom lines are long but what's new. Definitely a great place to see a show whether you're on the floor or the balcony"
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "C P",
                "review": "First time going there located in the Upper Westside. Absolutely love the elegant, classy exterior. Very tastefully decorated, three tiered theatre, seats over 2000, the stage is well designed you can get a great view wherever you are sitting."
            },
        ]
    },
    {
        "name": "The Iridium",
        "is_deleted": False,
        "id": 17,

        "image": "https://media.timeout.com/images/105486614/380/285/image.jpg",

        "description": "Live music seven days a week? We'll take it. The Iridium, a musical landmark centered in the heart of Times Square, has been serving New York City concert...",

        "rating": 4.5,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Bogdan Iordachita",
                "review": "Excellent experience. Very nice place to disconnect from all the rush outside and enter the wonderful world of jazz. Very good service even if the place was crowded."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "c g",
                "review": "Great place. Amazing food. Amazing night of Sharon Klein Productions particularly Boys of the Bandstand. They were absolutely amazing had the whole house rocking hope that they are permanent member of the iridium.  Great time"
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "THE GOLDEN PIE .",
                "review": "Event itself was amazing and I will admit it’s a lovely little venue. But I have literally never and I mean never had such an appalling experience when it came to a simple overcharge on my card. Don’t bother trying to call them. Won’t happen. Maybe an email to say? Doesn’t work. As for the way the Facebook page acts it’s both shocking and laughable. 55 dollars down and I get offered t shirts. That most likely cost very very little. The other offer was 2 tickets to a show which I admit is admirable and were I still there I would have taken them up on the offer. "
            },
        ]
    },
    {
        "name": "Radio City Music Hall",
        "is_deleted": False,
        "id": 18,

        "image": "https://media.timeout.com/images/100559627/380/285/image.jpg",

        "description": "One heralded as the Showplace of the World, this famed Rockefeller Center venue has razzle-dazzled patrons since the 1930s with its elaborate Art Deco details, massive stage and theatrics. Though best known as the home of the Christmas Spectacular, which stars the high-kicking Rockettes and a full cast of nativity animals, many musicians consider the 6,000-seat theater a dream stage to perform on, including a recent extended stay from Lady Gaga and Tony Bennett.",

        "rating": 4.7,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Zebby Clark",
                "review": "I went around Christmas time for my girlfriends birthday. We had a wonderful time and the winter spectacular was amazing. We had such a great time. The staff was very friendly and helpful. I’ve to a lot of shows in New York radio city has the best staff. Get any seat, they all have wonderful views of the stage. Definitely will be back!"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "K. West",
                "review": "I had great seats for the Jill Scott concert. But what was most amazing about this experience was the effective handling of long line to the women's bathroom. It went by quickly because an employee directed people to a stall when it became available. I know it seems crazy for that to stand out but for such a crowded facility this was an amazing experience."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Amber Evans",
                "review": "Radio City Music Hall is absolutely breathtaking, especially during Christmas time! We've taken the tour before which was a really amazing experience. The coolest part of that was being in the light/ sound area and looking down on the performance on stage. The year after, we got the pleasure of seeing The Christmas Spectacular with the Rockettes. Not only were the dancers phenomenal, but the entire show was mesmerizing to watch. They even had live animals (camels, a sheep, and a donkey) which was so cool to see! I had no idea going into it. Highly recommend this show, it was absolutely amazing!"
            },
        ]
    },
    {
        "name": "Saint Vitus",
        "is_deleted": False,
        "id": 19,

        "image": "https://media.timeout.com/images/100316543/380/285/image.jpg",

        "description": "This Greenpoint club—moodily decorated with all-black walls and dead roses hanging above the bar—is one of the best places in the city to see metal, rock and more experimental heavy music, with reliably loud bands typically booked seven nights a week.",

        "rating": 4.7,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Monica Hernandes",
                "review": "Amazing times at Saint Vitus. Awesome bartenders and friendly crowd. Great place to chill and have a few drinks. Alcohol prices are good. When Big name bands play at the venue it can get extremely packed, but overall bar is a great place."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Alejandro4891 .",
                "review": "I've been going to metal shows since 2008 and this bar since 2012. Throughout the years and various venues I've been to, this is without a doubt one of or my absolute favorite venue for metal shows. "
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Steve M.",
                "review": "the first time that I was trying to looking for this bar was very tough but the second that you know where it is you always want to come back to it. The interior in the bar itself was out-of-this-world I've never seen before. I went here for a small rock concert that they were holding and it was really awesome time listen to the bands at their venue. "
            },
        ]
    },
    {
        "name": "Village Vanguard",
        "is_deleted": False,
        "id": 20,

        "image": "https://media.timeout.com/images/100206113/380/285/image.jpg",

        "description": "After more than 80 years, this basement club’s stage still hosts the crème de la crème of mainstream jazz talent. Plenty of history has been made here—John Coltrane, Miles Davis and Bill Evans have grooved in this hallowed hall—and the 16-piece Vanguard Jazz Orchestra has been the Monday-night regular since 1966. Thanks to the venue's strict no cell phone policy, seeing a show here feels like stepping back and time. It's just you and the music. ",

        "rating": 4.7,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Ritesh Poddar",
                "review": "The vanguard's music set was exquisite. The 16 piece jazz group had everything. It is a cosy place and if you want the best seats, it is best to arrive early. We reached at 10 pm for a 10:30 pm show and all we got was seats at the back. We probably should have arrived 45 minutes before to get better seats but the jazz was great."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Agata Petromilli",
                "review": "Cool drinks, cool vibe. If you're a jazz lover, you gotta come here and give this place a chance. You'll also find great artists and performers."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Scott Sperling",
                "review": "One of the world's great jazz clubs. Literally, a hole in the wall. Actually, literally a hole in the ground, but that doesn't matter: great atmosphere, great music, always full to the gills. Get there early to get a seat with decent sight lines."
            },
        ]
    },
    {
        "name": "Blue Note",
        "is_deleted": False,
        "id": 21,

        "image": "https://media.timeout.com/images/100433851/380/285/image.jpg",

        "description": "The Blue Note prides itself on being the jazz capital of the world. Bona fide musical titans (Chick Corea, Ron Carter) rub against hot young talents, while the close-set tables in the club get patrons rubbing up against each other. Arrive early to secure a good spot—and we recommend shelling out for a table seat.",

        "rating": 4.4,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Scott Sperling",
                "review": "One of the great jazz clubs. What more can I say? Get here early to get a good seat. Warning: you are packed in! You'll get to know your neighbor well. Thus, the importance of getting here early: in order to get an end seat. As for the music, well you already know it's the best..."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Sol ,",
                "review": "Great venue, but you might wanna avoid sitting nearby the piano as the seats are very close to the bar. It gets a bit noisy at the start even though all the employees are very nice and trying hard not to make unnecessary noises. But Blue Note is one of my favourite jazz venue for sure!"
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Sagy Langer",
                "review": "Went to see the Dizzy Gillespie All Stars. Really enjoyed it. Sound was good, atmosphere is cozy and food was okay. Even though it was an \"All star\" show, it was very enjoyable. Every performer on stage was really gifted, and the pianist is a prodigy! He \"stole\" the show."
            },
        ]
    },
    {
        "name": "Kings Theatre",
        "is_deleted": False,
        "id": 22,

        "image": "https://media.timeout.com/images/101898503/380/285/image.jpg",

        "description": "Once one of Brooklyn’s most elegant movie theaters, the Loew’s Kings Theatre opened in Flatbush as a movie and live performance space in 1929. When multiplex cinemas became popular in the 1950s, the theater lost traction with audiences. It eventually closed in 1977 and the stunning interior fell into disrepair. After an elaborate $95 million restoration, the 3,074-seat theater reopened in 2015 in all its original glory. Catch classic acts and rising stars alike at the ornate theater.",

        "rating": 4.6,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Brian Kaplan",
                "review": "I'm old enough that I choose concerts based on the quality of the venue and I love Kings Theatre. The acoustics and sound system alone should make you want to see shows here but the quantity, variety and distribution of bars, the friendly staff, and all housed in a gorgeously renovated historic theater make it a superb venue. Only drawback is the less than ideal restroom situation but that only dings the score one star."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Heather Owen",
                "review": "Seating was comfortable and not cramped, but the way they allowed ticketholders in leaves something to be desired. We showed up before doors opened and walked for several blocks to reach the end of the entry line. By the time we entered the venue doors, the show had been going on for 20 minutes already. Also, one of the employees asked my partner why they were using a cane. That seemed a little insensitive."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Everlina - Whynter Thomas",
                "review": "The Hiphop Nutcracker was simply AMAZING. The cast outdid themselves. Mr. Curtis Blow was an awesome host who had the crowd going. Can't wait to see what else they have in store for future performances."
            },
        ]
    },
    {
        "name": "Brooklyn Bazaar",
        "is_deleted": False,
        "id": 23,

        "image": "https://media.timeout.com/images/103504033/380/285/image.jpg",

        "description": "After being ousted from its Greenpoint warehouse home in June of 2015, the crowd-pleasing pop-up market reopened inside a sprawling banquet hall in the same nabe the following summer. Modeled after eclectic Asian street markets, the flea features a locally-focused lineup of craftspeople, food vendors and, yes, indie-rock talent and DJs in its second-floor music space. ",

        "rating": 4.2,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Raven Black",
                "review": "I really was so impressed by this music venue the food and drinks are amazing too.   Top notch security is a class act they surely have everything under control and organized. I like the fact that when the music show was over people left accordingly and didn't linger. It was easy to exit the venue without a hassle. That was because of the serious security they have there.  Great place for music, drinks and dinner."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Rich Zumpano",
                "review": "I have seen a few shows here. It's a strange place with the performance space upstairs and a diner type eating area downstairs. Liquor prices were reasonable."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Brittany Caceres",
                "review": "Came here for the RAW Artist showcase to support a friend! great space for events with multiple floors in this case to showcase live art and other other pieces. The bathrooms were really nice and there were a lot of food options nearby! The space also had a bar with some arcade games and a lot of places to take some nice pictures for the gram! Definitely would recommend checking them out to see what live shows may be coming up that will interest you."
            },
        ]
    },
    {
        "name": "Le Poisson Rouge",
        "is_deleted": False,
        "id": 24,

        "image": "https://media.timeout.com/images/100202089/380/285/image.jpg",

        "description": "Situated in the basement of the long-gone Village Gate—a legendary performance space that hosted everyone from Miles Davis to Jimi Hendrix—Le Poisson Rouge was opened in 2008 by a group of young music enthusiasts with ties to both the classical and indie-rock worlds. With a top-notch sound system and modular stage that can be set up for in-the-round performances, LPR sounds great whatever the genre is.",

        "rating": 4.4,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "William Polito",
                "review": "Awesome place to see a band. Felt comfortable in the space provided. Not too big not too small. Great cornered stage layout. Staff was inviting. Drinks a bit pricey but I'm sure their rent is too. Great location."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "ZayP The IAm",
                "review": "It's a decent sized dance floor.... And a lil side gallery for seating away from the crowd... Great party space... Open yet intimateWay overpriced drinks... Wasn't even giving straws... But besides that was cool🤷🏾‍♂"
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Brian Ferdman",
                "review": "The former home of the historic Village Gate Theater, where the likes of Bob Dylan and Janis Joplin once graced the stage, this subterranean venue generally features very good sound. Seated shows tend to suffer from the typical \"jazz seating\" arrangement, i.e. patrons are crammed into place and may have to contort their head in strange angles to see the stage. General Admission shows tend to be a nicer experience, although sold out shows can be jam-packed. The VIP section is tucked into a back corner on a platform. The bar offers a decent selection of cocktails and has solid food. Be forewarned that your phone will likely have minimal service this far underground."
            },
        ]
    },
    {
        "name": "Pianos",
        "is_deleted": False,
        "id": 25,

        "image": "http://www.brooklynvegan.com/files/img/music/jackpenate/pianos/1.jpg",

        "description": "In recent years, a lot of the cooler bookings have moved from Pianos to Brooklyn or down the block to venues such as Cake Shop. Still, while sound is often lousy and the room can get uncomfortably mobbed, there are always good reasons to go back—very often the under-the-radar emerging rock bands that make local music scenes tick.",

        "rating": 4.0,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Courtney Burstion",
                "review": "Came through to see @Lambrabbit rock the 1s and 2s.... Phenomenal. She's knowledgeable and immensely talented with a diverse range of genres✨✨✨ But from what I gather this is a generally dope spot for music. Check it out, and bring your State Issued ID! They don't accept IDNYC"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Alberto",
                "review": "This is the place to be! You party for cheap and actually have fun! It's super packed but the line to get in moves relatively fast. You will be dancing all night with a college crowd that's super diverse"
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Raymond R-Mcnaught",
                "review": "Great place to play. Downstairs has a great PA for bands. Upstairs has decent sound. The Dj upstairs on Wednesday is fire. "
            },
        ]
    },
    {
        "name": "The Town Hall",
        "is_deleted": False,
        "id": 26,

        "image": "https://media.timeout.com/images/100292137/380/285/image.jpg",

        "description": "Acoustics at the 1921 people’s auditorium are superb, and there’s no doubting the gravitas of the Town Hall’s surroundings. The building was originally designed by illustrious architects McKim, Mead & White as a meeting house for the League for Political Education, a suffragist organisation. George Benson, Grizzly Bear and Lindsey Buckingham have performed here in recent times, and smart indie songwriters such as the Magnetic Fields have set up shop for a number of nights.",

        "rating": 4.5,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "shanikka white",
                "review": "Nice intimate place. Seats space a bit small but manageable. The Mockingbird project was excellent very insightful and informative. I think everyone should watch this. I wish more of my coworkers attended due to dealing directly with mass incarceration."
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Erica Loberg",
                "review": "I saw City and Colour here, and the acoustics in this venue where phenomenal. It’s the perfect sized theater to maintain an intimate feeling while also enabling the excited energy of a large enough crowd. It’s kind of an old building, which adds interesting character (since I didn’t experience any problems because of that)."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Adam Ford",
                "review": "This is such a quintessential New York institution. The seats are comfortable in the view lines are all good. I love the historical information posted on the walls upstairs. I wish I could have been there for the Margaret Sanger riot in 1921."
            },
        ]
    },
    {
        "name": "United Palace Theatre",
        "is_deleted": False,
        "id": 27,

        "image": "https://media.timeout.com/images/101304621/380/285/image.jpg",

        "description": "This renovated movie house, which was once a vaudeville theater, dates from the 1930s. It really does feel as if you’ve entered a palace here, with the shimmering chandeliers, ornate ceiling and gold-drenched corridors. Over the past few years, the venue’s bookings have ranged from popular young acts such as Adele, Vampire Weekend and Bon Iver to stalwarts of the music world like Bob Dylan and the Allman Brothers Band. Though it's located at the top end of Manhattan, far beyond the traditional nightlife or tourist zone, the theater is nevertheless easily accessible by subway.",

        "rating": 4.5,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "U-roy Felix Agboli",
                "review": "My church held a Sunday service is this magnificent edifice today and my experience was inexplicable. The place is ginormous and colorful with gold finish. The interior is an architectural marvel; the creativity, the layout, the distinctiveness is ethereal. This spellbinding theatre was built in 1930 with a seating capacity of 3,327. It’s pretty close to the road and can be easily noticed from a vehicle in normal traffic. There’s also wheelchair accessible for the differently able"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Sandra",
                "review": "This is a beautiful large venue. It fits a little less than 3,400 people. The interior is stunning and awesome for some aesthetic Instagram photos. It is far up, but it is magical venue. My church was here for a field trip service and now meets here regularly every Sunday. Everyone loves the venue."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Michelle H",
                "review": "This building is exquisite. It is majestic. There are 2 bars, one on each level."
            },
        ]
    },
    {
        "name": "Carnegie Hall",
        "is_deleted": False,
        "id": 28,

        "image": "https://media.timeout.com/images/100202927/380/285/image.jpg",

        "description": "Since it first opened its doors in 1891, Carnegie Hall has been a mainstay of the New York music scene. George Gershwin, Louis Armstrong and the Beatles have all performed here, and to this day, artistic diector Clive Gillinson continues to put his stamp on the renowned concert hall. Whether you catch a show in the Isaac Stern Auditorium, Zankel Hall or the Weill Recital Hall, you're sure to be dazzled by the history and ambiance of the place.",

        "rating": 4.7,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Jennifer Bondurant-Magnone",
                "review": "I so enjoyed joining my cousin Rain Worthington for an orchestra performance featuring one of her composed pieces. It was a beautiful evening with my family and friends! So proud of Rain & how far her NYC journey has come! Carnegie hall is a wonderful experience!"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "George Gregoriou",
                "review": "The legendary venue is a must see, whether you're in Manhattan for an evening or have been for a lifetime. If legroom is a priority, book seats on the Parquet or First Tier, as the rest of the levels (especially the second tier) are a \"cozy\" fit. As far as acoustics go, there isn't a single bad seat in the house."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "redwillow ",
                "review": "Place was cool. I had a balcony seat and felt I could see the stage fairly well. Sound was a bit stained but that could just be my hearing. The elevator was not publicized very well and the walk up was an exercise but not the end of the world. Atmosphere wasn't stuffy - at least not in the balcony. A wonderful experience overall."
            },
        ]
    },
    {
        "name": "Webster Hall",
        "is_deleted": False,
        "id": 29,

        "image": "https://media.timeout.com/images/101216599/380/285/image.jpg",

        "description": "Built in 1886, Webster Hall has been through several iterations (and names) before settling into its tenure as a high-caliber concert venue. In the 1950s, performers like Tito Puente and Woody Guthrie graced the stage, and when it was known as The Ritz in the '80s, the same venue hosted rock legends like U2, Eric Clapton and Guns N' Roses. These days, you can expect to find indie acts like Animal Collective and The Maine, as well as hip-hop artists like Wiz Khalifa and Mobb Deep. Just be sure to show up early if you want a decent view.",

        "rating": 4.1,

        "reviews": [
            {
                "id": 0,
                "is_deleted": False,
                "user": "Courtneay Fitts",
                "review": "I love Webster Hall!  Huge venue and the staff there are cool and laid back while still being very attentive. They have a nice lounge area near the entrance/exit where you can enjoy some drinks and snacks at the bar before heading upstairs to the main stage areas.  There are bars scattered everywhere throughout so you will never go thirsty ;)"
            },
            {
                "id": 1,
                "is_deleted": False,
                "user": "Megan Eiswerth",
                "review": "Mixed feelings about this place. Pros: Large venue with freedom to roam the floor or the balcony. Lounge/ bar area downstairs by the bathrooms where you can still hear the music and watch from screens. Average beer prices. Good sound and light production. Security thoroughness is average. Good location, easy to get to.Cons: Excruciating lines. I have been stuck in entry lines that wrap around the block, even an hour+ after doors opened. THEN once inside, I had to wait almost 40 minutes to check my coat. It seems like their staff/ organization is just really sloppy. I've also had experiences where staff is very short-tempered and rude, either yelling or pushing past, unprovoked."
            },
            {
                "id": 2,
                "is_deleted": False,
                "user": "Sean Murray",
                "review": "One of the best concert venues in New York because they truly customize the experience to each artist and bring in the best acts. The entire place is newly renovated and easy to navigate. I'm tall, so I don't mind the standing room only, but I have seen shorter people get annoyed when they have to jockey for space to see the stage. Will be going back soon!"
            },
        ]
    },
]
# =======================================================================


@app.route('/')
def home():
    global venues
    showcase = []
    lastIdx = len(venues)
    startIdx = lastIdx - 12

    for i in range(startIdx, lastIdx):
        showcase.insert(0,venues[i])

    return render_template('home.html', data=showcase)


@app.route('/autoComplete')
def autoComplete():
    names = []

    for i in range(0, len(venues)):
        names.append(venues[i]['name'])

    return jsonify(names)


@app.route('/view/<venue_id>')
def view_result(venue_id):
    global venues
    view_id = int(venue_id)
    # data = []
    name = None
    img = None
    description = None
    rating = None
    reviews = [None,None,None]

    for i in range(0, len(venues)):
        if venues[i]['id'] == view_id:
            name = venues[i]['name']
            img = venues[i]['image']
            description = venues[i]['description']
            rating = venues[i]['rating']
            reviews = venues[i]['reviews']
            # data = venues[i]

    return render_template('view.html', name=name, img=img, venue_id=view_id, 
         description=description, rating=rating, reviews=reviews)


@app.route('/search_process', methods=['POST'])
def search_process():
    global venues
    global search_key
    global result
    result.clear()

    target = request.form['target'].lower()
    search_key = target

    for i in range(0, len(venues)):
        name = venues[i]['name'].lower()
        description = venues[i]['description'].lower()
        if target in name or target in description:
            result.append(venues[i])

    return jsonify(result)


@app.route('/search')
def search():
    global search_key
    global result
    highlighted = copy.deepcopy(result)
    search_str = str(search_key)
    
    for i in range(0, len(highlighted)):
        
        desc = highlighted[i]['description']
        desc = re.sub(search_str, r"<span class='hl'>\g<0></span>", desc, flags=re.IGNORECASE)
        highlighted[i]['description'] = desc 
        
        name = highlighted[i]['name']
        name = re.sub(search_str, r"<span class='hl'>\g<0></span>", name, flags=re.IGNORECASE)
        highlighted[i]['name'] = name

    return render_template('search.html', result=highlighted, key=search_key)


@app.route('/edits', methods=['POST'])
def addReview():
    global venues
    id = int(request.form['id'])

    new_user = request.form['new_user']
    new_review = request.form['new_review']
    reviews = venues[id]['reviews']

    if new_user and new_review:
        new_data = {
            "id": len(reviews),
            "is_deleted": False,
            "user": new_user,
            "review": new_review
        }

    reviews.insert(0, new_data)
    
    return jsonify(reviews)


@app.route('/edits2', methods=['POST'])
def eidtDescription():
    global venues
    id = int(request.form['id'])

    new_description = request.form['new_description']
    new_rating= request.form['new_rating']

    if new_description:
        venues[id]['description'] = new_description

    if new_rating:
        venues[id]['rating'] = new_rating

    return jsonify({"new_desc":new_description, "new_rating":new_rating})


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    global venues
    venue_id = int(request.form['venue_id'])
    deleted_id = int(request.form['delete_id'])
    is_undo = int(request.form['is_undo'])
    flagged = None
    idx = None

    for i in range (0, len(venues)):
        if venues[i]['id'] == venue_id:
            idx=i
            break

    reviews = venues[idx]['reviews']

    for j in range (0, len(reviews)):
        if reviews[j]['id'] == deleted_id:
            # jdx = j
            flagged = reviews[j]
            
            if is_undo == 0:
                reviews[j]['is_deleted'] = True
            if is_undo == 1:
                reviews[j]['is_deleted'] = False

    return jsonify({"deleted":flagged, "is_undo":is_undo}) 


@app.route('/create')
def create():

    return render_template('create.html')
    

@app.route('/create_process', methods=['POST'])
def create_process():
    global venues
    global current_id

    new_entry = current_id
    new_data = request.get_json()
    venues.append(new_data)
    venues[new_entry]['id'] = current_id

    current_id += 1

    return jsonify(venues[new_entry])


if __name__ == '__main__':
    app.run(debug=True)

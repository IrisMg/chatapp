# db_population_custom.py
import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "questions.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# --- Tables ---
# --- User Background Questions ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS userbackground_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    type TEXT CHECK(type IN ('single','multiple')) DEFAULT 'single'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS userbackground_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY(question_id) REFERENCES userbackground_questions(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS concern_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    area_of_concern TEXT NOT NULL,
    specific_concern TEXT NOT NULL,
    text TEXT NOT NULL,
    type TEXT CHECK(type IN ('single')) NOT NULL DEFAULT 'single'
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS concern_answer_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    explanation TEXT,
    FOREIGN KEY (question_id) REFERENCES concern_questions(id)
)
""")

# --- Learn More Content Table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS learn_more (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    specific_concern TEXT UNIQUE NOT NULL,
    what_is_it TEXT,
    why_it_matters TEXT,
    dos TEXT,
    donts TEXT
)
""")

#----- User PET Recommendations Table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_pets_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    selected_concern TEXT,
    awareness_level TEXT,
    device TEXT,
    os TEXT,
    country TEXT,
    pet_name TEXT,
    pet_price TEXT,
    pet_description TEXT,
    pet_company TEXT,
    pet_link TEXT,
    logo_link TEXT,
    why_use TEXT,
    popularity INTEGER
)
"""
)


# --- Sample User Background Questions ---
background_questions = [
    {
        "text": "On which device do you want to increase your online privacy?",
        "type": "single",
        "options": ["Desktop", "Mobile"]
    },
    {
        "text": "Which operating system do you primarily use?",
        "type": "single",
        "options": ["Windows", "macOS", "Linux", "Android", "iOS"]
    },
    {
        "text": 'Which country are you located in?',
        "type": "single",
        "options": ["Europe", "USA", "Asia", "Other"]
    },
    {
        "text": "Would you prefer free or paid privacy tools?",
        "type": "single",
        "options": ["Free", "Paid"]
    },
    {
        "text": "Where do you want to improve your privacy?",
        "type": "single",
        "options": ["Website browsing", "Mobile apps", "Network", "Cloud"]
    },

]

for q in background_questions:
    cursor.execute(
        "INSERT INTO userbackground_questions (text, type) VALUES (?, ?)",
        (q["text"], q["type"])
    )
    question_id = cursor.lastrowid
    for opt in q["options"]:
        cursor.execute(
            "INSERT INTO userbackground_options (question_id, text) VALUES (?, ?)",
            (question_id, opt)
        )

questions_data = {
    "Web Browsing": {
        "Browser Fingerprinting": [
            {
                "text": "Q1. Which of the following best describes browser fingerprinting?",
                "options": [
                    ("Using cookies to track logins", False),
                    ("Storing files on your computer", False),
                    ("Identifying your device through its unique settings and configuration", True),
                    ("Scanning for malware", False)
                ]
            },
            {
                "text": "Q2. What kind of data can be used to create a browser fingerprint?",
                "options": [
                    ("Screen resolution", False),
                    ("Browser type", False),
                    ("Installed fonts", False),
                    ("All of the above", True)
                ]
            },
            {
                "text": "Q3. Why can’t fingerprinting be easily blocked like cookies?",
                "options": [
                    ("It doesn’t store anything on your device", True),
                    ("It’s encrypted", False),
                    ("It collects data actively from your browser settings", False),
                    ("It only works with cookies", False)
                ]
            },
            {
                "text": "Q4. You use “Private/Incognito” mode and clear cookies often. A website still recognizes you on the next visit. Why?",
                "options": [
                    ("Fingerprinting can identify you even without cookies", True),
                    ("Your cookies weren’t cleared properly", False),
                    ("The site stored a backup cookie", False),
                    ("It’s using your IP address only", False)
                ]
            },
            {
                "text": "Q5. You open the same website on two different browsers from the same computer, and it still knows it’s you. What does that suggest?",
                "options": [
                    ("The site uses fingerprinting based on device characteristics", True),
                    ("Your browser is synced", False),
                    ("Your IP address didn’t change", False),
                    ("You forgot to log out", False)
                ]
            },
            {
                "text": "Q6. You’re using a VPN, but a website still seems to know it’s you. Why could that be?",
                "options": [
                    ("The VPN is not working", False),
                    ("Your browser setup hasn’t changed", True),
                    ("You used the same password", False),
                    ("Your IP address didn’t change", False)
                ]
            },
            {
                "text": "Q7. You install multiple browser extensions to improve privacy. What’s one potential downside?",
                "options": [
                    ("Extensions always make you harder to track", False),
                    ("Too many extensions can make your fingerprint more unique", True),
                    ("Extensions block all fingerprinting", False),
                    ("No downside at all", False)
                ]
            },
            {
                "text": "Q8. Which of the following changes could slightly reduce how unique your device looks online?",
                "options": [
                    ("Using a browser that hides details like fonts and plugins", True),
                    ("Using a bigger monitor", False),
                    ("Changing your password", False),
                    ("Keeping more tabs open", False)
                ]
            },
            {
                "text": "Q9. You visit a site that asks for permission to access your camera and microphone. What might this have to do with fingerprinting?",
                "options": [
                    ("It helps you to connect faster", False),
                    ("It can give the site more information about your device setup", True),
                    ("It’s required for all websites", False),
                    ("It protects your privacy", False)
                ]
            },
            {
                "text": "Q10. You install new fonts and themes on your browser. How might this affect your online privacy?",
                "options": [
                    ("It has no effect", False),
                    ("It can make your device more unique and easier to recognize", True),
                    ("It improves privacy", False),
                    ("It blocks ads automatically", False)
                ]
            }
        ],
        "Targeted Ads and Online tracking": [
            {
                "text": "Q1. Why do advertisers track your online activity?",
                "options": [
                    ("To randomly display ads to users", False),
                    ("To serve ads that are more likely to match your interests", True),
                    ("To reduce internet speed", False),
                    ("To comply with government regulations", False)
                ]
            },
            {
                "text": "Q2. What causes you to see ads for things you recently searched online?",
                "options": [
                    ("Your computer is constantly listening through the microphone", False),
                    ("Websites and apps share data through trackers and cookies", True),
                    ("Ads are chosen randomly", False),
                    ("It’s controlled solely by your internet provider", False)
                ]
            },
            {
                "text": "Q3. Which of the following is a common method used by advertisers to personalize ads?",
                "options": [
                    ("Random selection of ad content", False),
                    ("Using demographic information and browsing history", True),
                    ("Displaying the same ad to all users", False),
                    ("Ignoring user data", False)
                ]
            },
            {
                "text": "Q4. What does “personalized advertising” mean?",
                "options": [
                    ("Ads based on your recent searches, interests, or location", True),
                    ("Ads chosen by government regulations", False),
                    ("Ads displayed randomly", False),
                    ("Ads that require your explicit payment", False)
                ]
            },
            {
                "text": "Q5. Which of the following can help to reduce online tracking?",
                "options": [
                    ("Using incognito mode", False),
                    ("Using a VPN and a privacy-focused browser", True),
                    ("Keeping cookies always enabled", False),
                    ("Allowing all website permissions", False)
                ]
            },
            {
                "text": "Q6. You search for a product on a shopping site, then you see ads for it on social media. Why is that?",
                "options": [
                    ("Social media and websites share tracking data through ad-networks", True),
                    ("Your friends mentioned it online so it shows up", False),
                    ("Your IP address was publicly posted", False),
                    ("It’s just a coincidence", False)
                ]
            },
            {
                "text": "Q7. You visit a free news site and click “Accept All” on the cookie consent popup. What happens next?",
                "options": [
                    ("The site can share your browsing data with advertisers", True),
                    ("You automatically block all trackers", False),
                    ("You begin browsing in total privacy", False),
                    ("The site deletes your previous cookies", False)
                ]
            },
            {
                "text": "Q8. You install an ad-blocker and notice fewer ads, but some websites stop working properly. Why?",
                "options": [
                    ("The ad blocker may also block essential website scripts", True),
                    ("Your browser has been hacked", False),
                    ("The website detects a VPN", False),
                    ("The ads were essential for the content", False)
                ]
            },
            {
                "text": "Q9. You delete cookies and browsing history, but personalized ads continue to appear. Why?",
                "options": [
                    ("Tracking also happens through your logged-in accounts and device IDs", True),
                    ("Your cookies weren’t properly deleted", False),
                    ("VPNs cause this behaviour", False),
                    ("The ads are random again", False)
                ]
            },
            {
                "text": "Q10. You get an ad about something you only discussed verbally near your phone. Is that considered possible as tracking?",
                "options": [
                    ("Probably not—more likely due to your search or social media behaviour", True),
                    ("Yes, your phone was secretly recording audio", False),
                    ("Only Apple does this", False),
                    ("It’s illegal everywhere", False)
                ]
            }
        ],
        "Public Wi-Fi browsing risks": [
            {
                "text": "Q1. What is one of the main risks when connecting to a public Wi-Fi network at a café or airport?",
                "options": [
                    ("The network always filters malware automatically", False),
                    ("Your device’s battery will drain faster", False),
                    ("Your data may be intercepted because the Wi-Fi may lack proper encryption", True),
                    ("The internet speed will be slower than home Wi-Fi", False)
                ]
            },
            {
                "text": "Q2. What is a common trick attackers use on public Wi-Fi?",
                "options": [
                    ("Creating fake networks that look legitimate to steal user data", True),
                    ("Slowing down the internet for everyone", False),
                    ("Automatically installing apps that improve security", False),
                    ("Blocking websites randomly", False)
                ]
            },
            {
                "text": "Q3. What is an “evil twin” Wi-Fi network?",
                "options": [
                    ("A backup network provided by your ISP", False),
                    ("A router inside your home with same SSID as your neighbour’s", False),
                    ("A fake public Wi-Fi hotspot set up by an attacker imitating a legitimate one", True),
                    ("A WPA3-secured network in public", False)
                ]
            },
            {
                "text": "Q4. Why can using public Wi-Fi be risky even if you just browse the web and don’t log in anywhere?",
                "options": [
                    ("Public Wi-Fi automatically blocks all risks", False),
                    ("Attackers could still view your online activity if the network is not secure", True),
                    ("Cookies are the only danger", False),
                    ("Your device automatically blocks all unsafe websites", False)
                ]
            },
            {
                "text": "Q5. Which precaution helps mitigate risks when using public Wi-Fi?",
                "options": [
                    ("Always connecting automatically to any “Free WiFi” network", False),
                    ("Disabling a VPN because it slows down browsing", False),
                    ("Using a VPN or ensuring websites use HTTPS when connected to public Wi-Fi", True),
                    ("Sharing your printer over the network so you don’t lose files", False)
                ]
            },
            {
                "text": "Q6. Which activity is least safe on public Wi-Fi?",
                "options": [
                    ("Checking weather updates", False),
                    ("Streaming a public news article", False),
                    ("Logging into your online banking account without any encryption", True),
                    ("Sending a message using an end-to-end encrypted chat app", False)
                ]
            },
            {
                "text": "Q7. You connect to “Cafe_FreeWiFi” at a coffee shop, check your email, and later notice someone gained access to your bank account. Which one might be the cause?",
                "options": [
                    ("The cafe’s Wi-Fi was secure and nothing went wrong", False),
                    ("You had too many browser tabs open", False),
                    ("You connected to a rogue network or your data was intercepted because the Wi-Fi lacked proper encryption", True),
                    ("Your bank password expired and auto-renewed", False)
                ]
            },
            {
                "text": "Q8. You download a free app using a public Wi-Fi connection at the airport. Later your device is infected with malware. What risk does this illustrate?",
                "options": [
                    ("Free games never contain malware", False),
                    ("Public Wi-Fi can be used as a delivery vector for malware because attackers can exploit unprotected networks", True),
                    ("The airport Wi-Fi is always secure by government law", False),
                    ("Only USB charging stations are dangerous, not Wi-Fi", False)
                ]
            },
            {
                "text": "Q9. You log into your bank using public Wi-Fi that seems password-protected, but you don’t use a VPN. Is this completely safe?",
                "options": [
                    ("Yes, protected Wi-Fi always keeps you safe", False),
                    ("No, attackers could still intercept your data; extra protections like VPNs or HTTPS are recommended", True),
                    ("Only safe if your phone is new", False),
                    ("Switching to mobile data afterward removes all risk", False)
                ]
            },
            {
                "text": "Q10. You connect your phone to public Wi-Fi and share a document with someone on the same network. Later, the file is leaked. What is the most likely reason?",
                "options": [
                    ("Sharing files is always safe on public Wi-Fi", False),
                    ("The network may be unsecured, allowing attackers to access shared files", True),
                    ("The leak must be from your email provider, not Wi-Fi", False),
                    ("Public Wi-Fi automatically encrypts all file transfers", False)
                ]
            }
        ],
        "Auto-Saved Passwords and Autofill Data": [
            {
                "text": "Q1. What is the risk of using the browser’s “save password or autofill” feature for many websites?",
                "options": [
                    ("There is no risk — it is fully secure.", False),
                    ("Your device may fill saved credentials into malicious or hidden form fields without your noticing.", True),
                    ("The passwords will automatically change every month.", False),
                    ("You will never have to log in again and thus no password theft is possible.", False)
                ]
            },
            {
                "text": "Q2. Why should you avoid using autofill on shared or public computers?",
                "options": [
                    ("Autofill uses too much memory.", False),
                    ("Other users could access saved login details or autofilled fields.", True),
                    ("Public computers automatically delete autofill data.", False),
                    ("The Wi-Fi connection will be slower.", False)
                ]
            },
            {
                "text": "Q3. What threat does auto-saved password data pose if your device is lost or compromised?",
                "options": [
                    ("None — auto-saved passwords cannot be accessed without the original password.", False),
                    ("The attacker might access your browser or password manager vault and use the saved credentials to impersonate you.", True),
                    ("Only cloud-syncing passwords are at risk — local ones are safe.", False),
                    ("Saved passwords automatically expire after 24 hours.", False)
                ]
            },
            {
                "text": "Q4. Why is using the same saved password across multiple sites risky?",
                "options": [
                    ("It makes browsing faster.", False),
                    ("If one site is hacked, attackers can try the same password elsewhere.", True),
                    ("Password managers prevent this automatically.", False),
                    ("Websites can’t read saved passwords.", False)
                ]
            },
            {
                "text": "Q5. What are good practices of mitigation when using password managers with autofill?",
                "options": [
                    ("Always enable autofill on all sites including iframes.", False),
                    ("Use strong master password, enable 2FA, disable automatic autofill on page load, and verify domain before filling.", True),
                    ("Use one weak password for all sites, and rely on autofill everywhere.", False),
                    ("Never use password managers or autofill — always write passwords on paper.", False)
                ]
            },
            {
                "text": "Q6. You fill in only your name and email in a site’s form, then your browser autofills your address and phone number into hidden fields which you didn’t see. What risk can this cause?",
                "options": [
                    ("Your browser is only filling visible fields, so no risk.", False),
                    ("The hidden fields could capture additional personal data without your awareness.", True),
                    ("Hidden fields make autofill impossible, so you’re safe.", False),
                    ("It only matters if you manually click “autofill”, not when it happens automatically.", False)
                ]
            },
            {
                "text": "Q7. Your password manager syncs across your laptop and phone through the cloud. After your phone is stolen, the thief can still access your synced accounts. Which risk may happen?",
                "options": [
                    ("Cloud-synced password managers without strong master passwords and 2FA may make stolen devices vulnerable.", True),
                    ("Cloud syncing prevents password theft completely.", False),
                    ("Cloud syncing works only on Wi-Fi, so data is safe.", False),
                    ("The stolen phone cannot access passwords once it’s offline.", False)
                ]
            },
            {
                "text": "Q8. You notice that your browser autofills your home address and card details on a “prize giveaway” website that looks legitimate. What could attackers exploit in this case?",
                "options": [
                    ("Form data autofill can reveal personal or payment details on deceptive or malicious sites.", True),
                    ("Autofill automatically verifies website authenticity before filling.", False),
                    ("Autofill never works on unknown sites.", False),
                    ("The browser requires your fingerprint for all autofill actions.", False)
                ]
            },
            {
                "text": "Q9. You lend your laptop to a friend to login into his email account. What should you do first?",
                "options": [
                    ("Log out of your browser or use a guest profile to prevent autofill from revealing your logins.", True),
                    ("Turn off Wi-Fi only.", False),
                    ("Close all tabs but keep the browser open.", False),
                    ("Nothing — browsers hide autofill from others.", False)
                ]
            },
            {
                "text": "Q10. What’s a safer way to store passwords if you often forget them?",
                "options": [
                    ("Write them on sticky notes near your computer.", False),
                    ("Use a reputable password manager protected by a strong master password.", True),
                    ("Save them in a text file on your desktop.", False),
                    ("Reuse one password for all accounts.", False)
                ]
            }
        ]
    },
    "Mobile Apps": {
        "Location Tracking by Apps": [
            {
            "text": "Q1. If an app collects your location continuously, what kind of personal details can it reveal?",
            "options": [
                ("Just the last location you visited", False),
                ("Your routines, favorite places, and possible home or workplace", True),
                ("Only the Wi-Fi networks you connect to", False),
                ("Your phone’s battery status", False)
            ]
        },
        {
            "text": "Q2. Which of the following is a risk when an app has “Always” location access (i.e., background tracking) rather than just “While using the app”?",
            "options": [
                ("It reduces battery life", False),
                ("It allows the app to collect location data even when you’re not actively using it", True),
                ("It restricts the app to only whenever you open it", False),
                ("It automatically disables network access", False)
            ]
        },
        {
            "text": "Q3. Many apps asked for your location more often than people expected. What do you think the percentage can be?",
            "options": [
                ("Less than 5%", False),
                ("Around 20%", False),
                ("Over 70%", True),
                ("None — users were well aware", False)
            ]
        },
        {
            "text": "Q4. What should you check before giving an app permission to access your location?",
            "options": [
                ("Whether the app’s developer name looks legitimate", False),
                ("If the app clearly explains why it needs your location", True),
                ("If your friends use the app too", False),
                ("If your phone battery is full", False)
            ]
        },
        {
            "text": "Q5. Why might some free apps often request your location data even though it’s not needed for the app’s main function?",
            "options": [
                ("To make your phone faster", False),
                ("Because location data can be sold or used for targeted ads", True),
                ("Because it improves your battery", False),
                ("To help you back up your contacts", False)
            ]
        },
        {
            "text": "Q6. What should you check before giving an app permission to access your location?",
            "options": [
                ("Whether the app’s developer name looks legitimate", False),
                ("If the app clearly explains why it needs your location", True),
                ("If your phone can install safely", False),
                ("If your phone battery is full", False)
            ]
        },
        {
            "text": "Q7. If you grant an app location access “only once,” what is the benefit compared to “always”?",
            "options": [
                ("It lets the app use location only for a short time, reducing unnecessary tracking", True),
                ("It increases app speed permanently", False),
                ("It disables GPS completely", False),
                ("It automatically deletes the app later", False)
            ]
        },
        {
            "text": "Q8. A ridesharing app asks for location “While using the app” but you leave it open in background for hours. During that time it logs your drivers and routes you take to multiple places. What is the concern here?",
            "options": [
                ("This is expected and safe", False),
                ("The app effectively tracks you beyond the intended session, building a detailed history of your movements", True),
                ("Background tracking doesn’t matter for rideshare", False),
                ("It only tracks your battery level", False)
            ]
        },
        {
            "text": "Q9. You download a free route-tracking app for walking, which asks for “Always” location access. You grant it. Later you notice it tracks you when you’re at home, not just when you’re walking. What risk does this illustrate?",
            "options": [
                ("No risk — the app is harmless", False),
                ("The app has background location access and may collect data outside the expected usage: walking, possibly creating a profile of sensitive places (home, work)", True),
                ("The app only collects battery usage", False),
                ("It shows you local weather instead", False)
            ]
        },
        {
            "text": "Q10. You are a user of many social media apps. Many of them request your device’s location seemingly to “improve experience.” You realize you never checked whether they shared your location with advertisers. What do you think they may use it for?",
            "options": [
                ("They never share your data", False),
                ("They may share precise location or location-derived profiles with ad networks, giving them insight into your movements and habits", True),
                ("Location data is useless for advertising", False),
                ("You can’t change the permission later", False)
            ]
        }
        ],
        "Data Sharing with Third Parties": [
            
        {
            "text": "Q1. Which of the following best describes “third-party data sharing” by apps or websites?",
            "options": [
                ("Only sharing data with internal teams of the app", False),
                ("Sharing user data with external companies, such as advertisers, analytics providers, or partners", True),
                ("Sharing data with your friends on social media", False),
                ("Only storing data locally on your device", False)
            ]
        },
        {
            "text": "Q2. What kind of personal information might commonly be shared with third parties?",
            "options": [
                ("Only your app username", False),
                ("Contact information, browsing habits, location, purchase history, and app usage patterns", True),
                ("Just your device battery level", False),
                ("None — third parties don’t get real data", False)
            ]
        },
        {
            "text": "Q3. What risk arises from apps or websites sharing your data with advertising networks?",
            "options": [
                ("Better personalized content without privacy concerns", False),
                ("Targeted advertising, profiling, potential identity leaks, and cross-site tracking", True),
                ("Increased device battery life", False),
                ("Automatic software updates", False)
            ]
        },
        {
            "text": "Q4. Why might a free app be more likely to share your data with third parties?",
            "options": [
                ("Free apps have unlimited funding and don’t need ads", False),
                ("They use it to share with advertisers or analytics companies to make money", True),
                ("Free apps are legally forbidden from sharing data", False),
                ("Free apps never request any permissions", False)
            ]
        },
        {
            "text": "Q5. You notice that a shopping app shows ads for items you recently looked at on another website. What does this likely mean?",
            "options": [
                ("Your phone is broken", False),
                ("The app shared or accessed your browsing info via advertising networks", True),
                ("The items magically appeared", False),
                ("Your Wi-Fi is slow", False)
            ]
        },
        {
            "text": "Q6. A free music streaming app requests access to your contacts and microphone. You decline, but the app still shares anonymized usage data with analytics providers. What concern does this raise?",
            "options": [
                ("No concern — anonymized data is harmless", False),
                ("Even limited or anonymized data can be combined with other sources to reidentify users", True),
                ("Apps cannot share any data if you decline permissions", False),
                ("Only your microphone is affected", False)
            ]
        },
        {
            "text": "Q7. You notice that multiple apps from different developers show similar ads after you searched for a product online. What does this indicate?",
            "options": [
                ("Third-party tracking and data sharing between apps or advertising networks is occurring, enabling cross-app profiling", True),
                ("Your device is malfunctioning", False),
                ("Apps are communicating directly with each other", False),
                ("Ads are randomly assigned", False)
            ]
        },
        {
            "text": "Q8. A social media platform shares your in-app activity with partner advertisers. Later, a breach exposes partner databases. What can be the main privacy risk?",
            "options": [
                ("Minimal risk — only partners see data", False),
                ("Third-party sharing increases exposure, making your personal data more vulnerable to leaks", True),
                ("Social media never shares activity", False),
                ("Only app crashes are affected", False)
            ]
        },
        {
            "text": "Q9. A social media app shows you products you never searched for, but your friends have searched for them. What is happening?",
            "options": [
                ("The app is sharing your friends’ search data with you", False),
                ("Ads are always random", False),
                ("Advertising networks may be combining data from multiple sources to target users with age range", True),
                ("Your account data is linked to other websites searches", False)
            ]
        },
        {
            "text": "Q10. Which of the following is a good practice to reduce how much your apps share your data?",
            "options": [
                ("Tap “Allow” on every permission", False),
                ("Review and limit permissions, turn off ad tracking, and only share what’s necessary", True),
                ("Share your data with all apps", False),
                ("Turn off your device permanently", False)
            ]
        }
        ],
        "Hidden Background Activity": [
           
        {
            "text": "Q1. Which of the following can be an example of hidden background activity?",
            "options": [
                ("An email app syncing new messages while you’re not using it", False),
                ("A game app collecting usage data when it’s closed", False),
                ("A social media app tracking your location in the background", False),
                ("All of the above", True)
            ]
        },
        {
            "text": "Q2. You notice your phone battery drains quickly even when you haven’t used it much. What could that be happening?",
            "options": [
                ("Your phone battery is broken", False),
                ("Some apps may be running in the background without your knowledge, using power and data", True),
                ("Your phone randomly loses charge", False),
                ("The Wi-Fi router drains your battery", False)
            ]
        },
        {
            "text": "Q3. Why hidden background activity can be considered as a privacy concern?",
            "options": [
                ("It’s only a minor annoyance", False),
                ("It makes apps run faster", False),
                ("Apps may collect personal data (location, contacts, browsing habits) without your knowledge", True),
                ("It improves battery life", False)
            ]
        },
        {
            "text": "Q4. You notice your mobile data usage is higher than expected even though you haven’t streamed or downloaded anything. What might be happening?",
            "options": [
                ("Your phone randomly consumes data", False),
                ("Your Wi-Fi is leaking data", False),
                ("Some apps are syncing or uploading data in the background", True),
                ("Data usage is always exactly what you expect", False)
            ]
        },
        {
            "text": "Q5. A free game app keeps sending notifications and collecting scores while you are not playing. Why could this be a concern?",
            "options": [
                ("It improves game performance", False),
                ("The app may be tracking game playing patterns or other data for advertisers", True),
                ("It helps your battery last longer", False),
                ("It’s required by law", False)
            ]
        },
        {
            "text": "Q6. Which is a good practice to detect hidden background activity?",
            "options": [
                ("Check battery and data usage statistics regularly; uninstall or restrict apps that use excessive resources in the background", True),
                ("Always leave apps open", False),
                ("Never update apps", False),
                ("Enable all permissions for all apps", False)
            ]
        },
        {
            "text": "Q7. A social media app keeps syncing your activity even when closed. Later, you see ads for topics you discussed privately. Why?",
            "options": [
                ("Background activity allows apps to collect and share data with advertisers", True),
                ("Ads are random", False),
                ("Friends sent the ads to you", False),
                ("The app is broken", False)
            ]
        },
        {
            "text": "Q8. After installing several free apps, you notice slower performance and higher data usage. What might be happening?",
            "options": [
                ("Apps are secretly running tasks in the background", True),
                ("Your phone is broken", False),
                ("The internet provider is slowing you down", False),
                ("It’s impossible; apps cannot run in the background", False)
            ]
        },
        {
            "text": "Q9. A music streaming app continues downloading recommendations overnight even though you haven’t opened it. Why could this be risky?",
            "options": [
                ("Nothing — downloading songs is harmless", False),
                ("The app may use your data plan or collect listening habits for third-party analytics and ads performance", True),
                ("It improves battery life", False),
                ("It deletes other apps automatically", False)
            ]
        },
        {
            "text": "Q10. You logged into a social media app and leave it logged in all day. Later, you see ads on other platforms related to your private messages or posts. Why?",
            "options": [
                ("Background activity allows the app to send metadata to advertising networks for cross-platform profiling", True),
                ("Ads are random coincidences", False),
                ("Other apps are malfunctioning", False),
                ("Only system apps share data", False)
            ]
        }

        ],
        
    "Malicious or Scam Apps": [
        {
            "text": "Q1. You find a banking app with very few downloads and glowing reviews, but it requests full access to your contacts, photos, files and camera. What can be the main risk?",
            "options": [
                ("It might improve your bank security", False),
                ("It could be a malicious app designed to steal personal information", True),
                ("Nothing; all banking apps ask for everything", False),
                ("The app will only track battery usage", False)
            ]
        },
        {
            "text": "Q2. Why should users be cautious when installing apps from unknown or unofficial app stores?",
            "options": [
                ("Apps may contain malware, spyware, or phishing mechanisms", True),
                ("The apps always run faster", False),
                ("Your phone automatically encrypts all data", False),
                ("It is recommended by all OS developers", False)
            ]
        },
        {
            "text": "Q3. Which of the following can be an indication of a scam app?",
            "options": [
                ("App description matches the screenshots", False),
                ("Excessive permissions unrelated to app function", True),
                ("Verified developer listed", False),
                ("Many positive reviews from verified users", False)
            ]
        },
        {
            "text": "Q4. What can happen if a malicious app gains access to your contacts?",
            "options": [
                ("The app can send spam or phishing messages to your friends", True),
                ("Nothing happens", False),
                ("Contacts automatically delete themselves", False),
                ("It improves your social networking experience", False)
            ]
        },
        {
            "text": "Q5. Which practice helps reduce the risk of installing scam apps?",
            "options": [
                ("Install only apps from verified publishers and check app permissions before giving", True),
                ("Always accept all requested permissions", False),
                ("Download apps from any link in social media", False),
                ("Ignore app reviews", False)
            ]
        },
        {
            "text": "Q6. You install a free random app (e.g., QR scanner) and give contact permission. Soon after, your friends report receiving strange promotional messages from you. What likely happened?",
            "options": [
                ("The app misused permissions to access your contacts and send spam", True),
                ("Your contacts were hacked randomly", False),
                ("Nothing; QR scanner apps cannot send messages", False),
                ("Your phone automatically sent messages", False)
            ]
        },
        {
            "text": "Q7. You install a free ‘photo editor’ app that requests full storage and camera access. Later, ads on other apps show images from your gallery. What happened?",
            "options": [
                ("The app misused permissions to collect sensitive files for advertising", True),
                ("Ads appear randomly", False),
                ("Your phone automatically shares photos", False),
                ("Nothing; apps cannot access photos", False)
            ]
        },
        {
            "text": "Q8. A messaging app asks for microphone access to enhance calls, but you notice unusual battery drain and high data usage. What could this indicate?",
            "options": [
                ("Background data collection or eavesdropping by a malicious app", True),
                ("Normal battery usage", False),
                ("The app deletes other apps", False),
                ("Nothing; microphones don’t use data", False)
            ]
        },
        {
            "text": "Q9. You receive an email claiming your free game account is suspended and asks you to download an updated version app. What is the safest action?",
            "options": [
                ("Ignore the email and download apps only from official stores", True),
                ("Click the link and install", False),
                ("Reply with your password", False),
                ("Forward it to friends", False)
            ]
        },
        {
            "text": "Q10. You download a free “clean storage” app from an unknown source. After installing it, your phone starts showing random pop-ups, redirects your browser to suspicious sites, and some new unknown apps appear automatically. What is the most likely explanation?",
            "options": [
                ("Your phone is malfunctioning", False),
                ("The app contains malware and is compromising your device", True),
                ("Battery optimizer apps always change browser settings", False),
                ("Nothing; apps cannot affect other apps or the browser", False)
            ]
        }
        ]
    },
    'Cloud': {
        'Unprotected File Sharing Links': [
       {
            "text": "Q1. What is a primary risk associated with sharing cloud files via unprotected links?",
            "options": [
                ("Unauthorized access to sensitive data", True),
                ("Increased file storage costs", False),
                ("Enhanced collaboration efficiency", False),
                ("Improved data encryption", False)
            ]
        },
        {
            "text": "Q2. Which of the following is a recommended practice to secure shared cloud files?",
            "options": [
                ("Share links with 'anyone with the link' setting", False),
                ("Use password protection and set expiration dates for links", True),
                ("Disable all sharing features", False),
                ("Share links via public forums", False)
            ]
        },
        {
            "text": "Q3. Why is it important to set expiration dates for shared cloud links?",
            "options": [
                ("To limit the duration of access to the shared file", True),
                ("To increase the file's visibility", False),
                ("To allow unlimited access", False),
                ("To reduce file storage size", False)
            ]
        },
        {
            "text": "Q4. Which method is considered safest for sharing sensitive files in the cloud?",
            "options": [
                ("Public link with 'anyone with the link'", False),
                ("Email attachment to intended recipient only", True),
                ("Posting the link in a public forum", False),
                ("Using a link with no expiration date", False)
            ]
        },
        {
            "text": "Q5. Which feature can improve security when sharing cloud files?",
            "options": [
                ("Password-protected links", False),
                ("Link expiration dates", False),
                ("Restricting access to specific users", False),
                ("All of the above", True)
            ]
        },
        {
            "text": "Q6. You share a confidential report via a cloud link without setting any access restrictions. Later, the link is forwarded to unauthorized individuals. What will be the concern/risk?",
            "options": [
                ("Unauthorized access to sensitive information", True),
                ("Increased storage costs", False),
                ("Enhanced collaboration efficiency", False),
                ("Improved data encryption", False)
            ]
        },
        {
            "text": "Q7. You share a cloud link with sensitive data to a colleague, setting the link to expire in 30 days. However, the colleague forwards the link to a third party before it expires, and the third party accesses the data after the expiration date. What could have prevented this?",
            "options": [
                ("Setting a shorter expiration date", False),
                ("Using a password-protected link", False),
                ("Restricting access to specific individuals", False),
                ("All of the above", True)
            ]
        },
        {
            "text": "Q8. You accidentally share a sensitive document via a cloud link without restrictions. What is the immediate action to mitigate potential risks?",
            "options": [
                ("Inform the receiver to delete the link", False),
                ("Change the link's access settings or expiration date", True),
                ("Ignore the issue; the damage is already done", False),
                ("Notify all receivers to avoid sharing links", False)
            ]
        },
        {
            "text": "Q9. You notice some old shared cloud links you created years ago are still active. Why is this risky?",
            "options": [
                ("They may still provide public access to sensitive files", True),
                ("Old links automatically expire, so there is no risk", False),
                ("Only people who saved the link can access it", False),
                ("Old links are automatically encrypted", False)
            ]
        },
        {
            "text": "Q10. You want to collaborate on a confidential document with multiple colleagues. Which is the safest way to share the file?",
            "options": [
                ("Public link with edit permissions", False),
                ("Email invitations to specific colleagues with edit permissions", True),
                ("Post link in internal chat without restrictions", False),
                ("Share via social media private message", False)
            ]
        },
    
    ],
    "Weak or Shared Passwords": [
        {
            "text": "Q1. Which of the following is an example of a weak password?",
            "options": [
                ("QwErT!29#xZ", False),
                ("123456", True),
                ("7&nPz4!fL9", False),
                ("G@7tYx9*", False)
            ]
        },
        {
            "text": "Q2. What is a risk of reusing the same password across multiple accounts?",
            "options": [
                ("Easier account recovery", False),
                ("If one account is leaked, all accounts using that password are at risk", True),
                ("Passwords become encrypted automatically", False),
                ("Faster login across services", False)
            ]
        },
        {
            "text": "Q3. Sharing your password with friends or coworkers can lead to:",
            "options": [
                ("Unauthorized account access", False),
                ("Data leaks or privacy violations", False),
                ("Compromised online reputation", False),
                ("All of the above", True)
            ]
        },
        {
            "text": "Q4. What is the safest way to manage multiple strong passwords?",
            "options": [
                ("Writing them on a notebook", False),
                ("Using the same password for all accounts", False),
                ("Using a password manager to generate and store passwords", True),
                ("Memorizing all passwords", False)
            ]
        },
        {
            "text": "Q5. Which additional measure enhances password security even if the password is leaked?",
            "options": [
                ("Two-factor authentication (2FA)", True),
                ("Using a password hint", False),
                ("Sharing with a trusted friend", False),
                ("Using a weak password", False)
            ]
        },
        {
            "text": "Q6. You use the same password for your email and online banking. Your email account is hacked. What is the risk?",
            "options": [
                ("Only the email account is affected", False),
                ("Your banking account may also be at risk", True),
                ("Nothing happens; passwords are separate", False),
                ("Only social media accounts are affected", False)
            ]
        },
        {
            "text": "Q7. You create a password for your banking account with your birthday. Why is this risky?",
            "options": [
                ("It’s easy for attackers to guess using personal information", True),
                ("It automatically encrypts your account", False),
                ("It makes login faster", False),
                ("It prevents phishing attacks", False)
            ]
        },
        {
            "text": "Q8. You create passwords using predictable patterns like “January2025,” “February2025,” etc., for multiple accounts. What is the main risk?",
            "options": [
                ("Easy for attackers to guess using pattern recognition", True),
                ("Passwords are automatically encrypted", False),
                ("Faster login", False),
                ("No risk if accounts are different websites", False)
            ]
        },
        {
            "text": "Q9. You send your work account password to a colleague via email so they can log in while you’re on leave. What is the main risk?",
            "options": [
                ("Unauthorized access if the email is intercepted", True),
                ("Email automatically encrypts the password", False),
                ("No risk because it’s shared with a colleague", False),
                ("Only affects low-priority accounts", False)
            ]
        },
        {
            "text": "Q10. You set up password recovery questions like “What is your favorite color?” or “Your pet’s name?” for multiple accounts. What is the primary concern?",
            "options": [
                ("Easy for attackers to guess using publicly available information", True),
                ("Strengthens password security", False),
                ("Automatically triggers 2FA", False),
                ("Makes accounts inaccessible", False)
            ]
        }, 
    ],
    "Automatic Photo Backup Without Consent": [
        {
            "text": "Q1. What is the main privacy risk of automatic photo backup without user consent?",
            "options": [
                ("Reduced image resolution", False),
                ("Uploading personal or sensitive images to the cloud without awareness", True),
                ("Increased phone storage capacity", False),
                ("Improved device performance", False)
            ]
        },
        {
            "text": "Q2. If your cloud app automatically uploads all photos—including screenshots and documents—to the server, what is a potential outcome?",
            "options": [
                ("Easier organization of your gallery", False),
                ("Exposure of confidential work-related or sensitive personal information", True),
                ("Better phone performance", False),
                ("Automatic deletion of duplicates", False)
            ]
        },
        {
            "text": "Q3. What hidden data in photos can create additional privacy risks when automatically backed up?",
            "options": [
                ("The file name", False),
                ("Metadata such as GPS location, timestamp, and device information", True),
                ("The image size only", False),
                ("The app’s name", False)
            ]
        },
        {
            "text": "Q4. What is the most privacy-friendly setting when using cloud photo backup services?",
            "options": [
                ("Automatic and continuous upload", False),
                ("Manual upload only with permission prompt each time", True),
                ("Sync over mobile data", False),
                ("Share all albums by default", False)
            ]
        },
        {
            "text": "Q5. Which of the following represents informed consent for cloud photo backups?",
            "options": [
                ("The app clearly explains what will be backed up and allows the user to give permission before uploading any photos", True),
                ("Backup starts automatically after installation", False),
                ("The user is notified only after upload", False),
                ("The app assumes all users want full sync", False)
            ]
        },
        {
            "text": "Q6. You use a messaging app that quietly backs up all received photos to its cloud servers. Later, you notice they appear in another device logged into your account. What privacy issue is this?",
            "options": [
                ("Cross-device syncing without informed consent", True),
                ("Hardware malfunction", False),
                ("Internet connection issue", False),
                ("Encrypted file recovery", False)
            ]
        },
        {
            "text": "Q7. Your friend logs into their cloud account on your phone to transfer photos. Later, all your photos start appearing on their account. What privacy control could have prevented this?",
            "options": [
                ("Revoking account access and disabling auto-backup immediately", True),
                ("Keeping Bluetooth turned off", False),
                ("Restarting your phone", False),
                ("Delete the app", False)
            ]
        },
        {
            "text": "Q8. After reinstalling a cloud storage app, you notice all your old photos—including deleted ones—reappear in the gallery. What likely happened?",
            "options": [
                ("Automatic cloud restore re-synced previously deleted photos", True),
                ("Your storage got corrupted", False),
                ("The app installed incorrectly", False),
                ("Photos were saved in a local hidden folder", False)
            ]
        },
        {
            "text": "Q9. You grant an app permission to access your camera for one photo. Days later, you learn it uploaded your entire gallery. What should have been the correct app behavior?",
            "options": [
                ("Enable option to request permission again before uploading any file", True),
                ("Automatically back up everything", False),
                ("Share only compressed images", False),
                ("Encrypt images without notice", False)
            ]
        },
        {
            "text": "Q10. A user switches to a new phone and signs into their old cloud account. Without any prompt, the new phone starts uploading all photos automatically. What privacy issue does this represent?",
            "options": [
                ("Automatic synchronization without renewed consent", True),
                ("Device malfunction", False),
                ("Manual upload error", False),
                ("Network configuration problem", False)
            ]
        }
    ],
    "Data Stored in Unknown Locations": [
    {
        "text": "Q1. Why is it a privacy risk if your cloud-stored data is saved in unknown or multiple countries?",
        "options": [
            ("It makes access faster globally", False),
            ("Different countries have different data protection laws and may allow government access", True),
            ("It reduces storage costs", False),
            ("It prevents backups from working", False)
        ]
    },
    {
        "text": "Q2. Have you heard of “data sovereignty”? What do you think it refers to in the context of cloud storage?",
        "options": [
            ("Users’ ability to encrypt their files", False),
            ("The principle that data is subject to the laws of the country where it is stored", True),
            ("The number of cloud servers used", False),
            ("The speed of network connection", False)
        ]
    },
    {
        "text": "Q3. Why might users lose control over their personal data when it’s stored across multiple international data centers?",
        "options": [
            ("Each center follows identical global privacy laws", False),
            ("Different data centers may follow different legal and retention policies", True),
            ("Cloud providers delete all data immediately after transfer", False),
            ("Users can manually manage each data center location", False)
        ]
    },
    {
        "text": "Q4. How can unknown data storage locations affect user trust in cloud providers?",
        "options": [
            ("It reduces trust due to uncertainty about who can access or process their data", True),
            ("It increases transparency and confidence", False),
            ("It guarantees higher encryption", False),
            ("It ensures faster retrieval times", False)
        ]
    },
    {
        "text": "Q5. Why is knowing your data’s physical storage location important for data deletion requests?",
        "options": [
            ("It determines how long the data stays accessible and whether local regulations require retention", True),
            ("It changes how files are encrypted", False),
            ("It improves device compatibility", False),
            ("It speeds up your uploads", False)
        ]
    },
    {
        "text": "Q6. What is a key challenge with deleting data from cloud services that store copies in multiple countries?",
        "options": [
            ("Backup copies in other locations may not be removed immediately or may follow different local rules", True),
            ("Files are automatically encrypted", False),
            ("The internet speed slows down deletion", False),
            ("Your device storage increases", False)
        ]
    },
    {
        "text": "Q7. You request a cloud service to delete your files, but later discover that copies of your data still exist on backup servers in another country. Why could this happen?",
        "options": [
            ("The cloud service keeps extra copies in different places for backup, and it’s not always clear where they are", True),
            ("The cloud servers stopped working", False),
            ("You didn’t click “delete” correctly", False),
            ("The internet connection was too slow", False)
        ]
    },
    {
        "text": "Q8. You save your personal photos and documents to a cloud service. Later, you find out some of your data is stored in a different country you didn’t know about. Why is this risky?",
        "options": [
            ("Your data may be subject to other countries’ privacy rules", True),
            ("The upload will take longer", False),
            ("You can’t share your files with friends", False),
            ("Your phone storage will increase", False)
        ]
    },
    {
        "text": "Q9. You move to a new phone and log into your cloud account. You notice all your old photos appear on the new device automatically, even those you thought were deleted. What happened?",
        "options": [
            ("The cloud synced all backup copies from unknown locations without asking again", True),
            ("The phone automatically created duplicates", False),
            ("The camera malfunctioned", False),
            ("Your internet connection caused a glitch", False)
        ]
    },
    {
        "text": "Q10. Which practice can help reduce privacy risks when using cloud services in multiple countries?",
        "options": [
            ("Choosing providers that let you select or restrict the data storage region", True),
            ("Uploading all files at once", False),
            ("Using free services without checking privacy policies", False),
            ("Disabling encryption", False)
        ]
    },
    ],
    },
    "Network": {
    "Using Public Wi-Fi Without Protection": [
        {
            "text": "Q1. What is the main risk of connecting to public Wi-Fi without protection?",
            "options": [
                ("Faster browsing speed", False),
                ("Other users can intercept your data, including passwords and personal information", True),
                ("Your device will automatically encrypt data", False),
                ("Free Wi-Fi always protects your privacy", False)
            ]
        },
        {
            "text": "Q2. What does “man-in-the-middle” (MITM) attack mean in the context of public Wi-Fi?",
            "options": [
                ("Someone sitting physically between two people", False),
                ("An attacker secretly intercepts and possibly alters communication between your device and the internet", True),
                ("Your device automatically connects to the nearest network", False),
                ("The router speeds up your connection", False)
            ]
        },
        {
            "text": "Q3. Which type of data is most at risk when using an open public Wi-Fi network?",
            "options": [
                ("Only photos", False),
                ("Passwords, emails, credit card details, photos and other sensitive data", True),
                ("Device battery level", False),
                ("Screen brightness settings", False)
            ]
        },
        {
            "text": "Q4. Why is public Wi-Fi particularly risky in places like airports and cafes?",
            "options": [
                ("Networks are typically open and unencrypted, making it easy for attackers to intercept data", True),
                ("They always block internet access", False),
                ("They provide slow connections", False),
                ("Devices automatically update without consent", False)
            ]
        },
        {
            "text": "Q5. What is the safest way to use public Wi-Fi?",
            "options": [
                ("Connect freely without protection", False),
                ("Use a Virtual Private Network (VPN) or HTTPS connections", True),
                ("Disable antivirus software", False),
                ("Share your files over the network", False)
            ]
        },
        {
            "text": "Q6. You log into your online banking account using a free coffee shop Wi-Fi without using a VPN. What could happen?",
            "options": [
                ("An attacker on the same Wi-Fi could capture your login credentials", True),
                ("Your balance automatically increases", False),
                ("Your connection becomes faster", False),
                ("Nothing, public Wi-Fi is always safe", False)
            ]
        },
        {
            "text": "Q7. You are checking emails at an airport Wi-Fi. Later, you notice strange login attempts on your account. What likely caused this?",
            "options": [
                ("Man-in-the-middle attacks capturing credentials over unsecured Wi-Fi", True),
                ("Your email provider slowed down", False),
                ("Your device battery is low", False),
                ("Emails got deleted automatically", False)
            ]
        },
        {
            "text": "Q8. You connect your smartphone to a public Wi-Fi that asks you to install a “security certificate” to access the internet. Why could this be dangerous?",
            "options": [
                ("It could be a malicious certificate allowing attackers to decrypt your traffic", True),
                ("It makes browsing faster", False),
                ("It automatically encrypts your device", False),
                ("It improves Wi-Fi signal", False)
            ]
        },
        {
            "text": "Q9. You use public Wi-Fi in a library to browse social media. Later, you notice ads for things you searched for on other devices. What might explain this?",
            "options": [
                ("Data captured on unsecured networks could be linked across sessions", True),
                ("Your browser crashed", False),
                ("Ads appear randomly", False),
                ("Your Wi-Fi speeds are low", False)
            ]
        },
        {
            "text": "Q10. You need to work on sensitive documents using public WiFi. Which practice best protects your data?",
            "options": [
                ("Use a VPN, ensure sites are HTTPS, and avoid sharing files over public Wi-Fi", True),
                ("Connect without restrictions", False),
                ("Disable all app notifications", False),
                ("Share your device hotspot with others", False)
            ]
        }
    ],
    "ISP Tracking and Data Logging": [
        {
            "text": "Q1. Which of these can your internet provider see about your online activity?",
            "options": [
                ("Websites you visit and when you visit them", True),
                ("Your phone’s battery level", False),
                ("Messages inside encrypted apps", False),
                ("Your photos", False)
            ]
        },
        {
            "text": "Q2. Why is it a privacy concern if your internet provider keeps records of your online activity?",
            "options": [
                ("They could use it to show you targeted ads or share with other companies or authorities", True),
                ("It makes your internet slower", False),
                ("Records delete themselves automatically", False),
                ("It increases battery life", False)
            ]
        },
        {
            "text": "Q3. Why might your ISP keep records of your activity even if you try to delete history?",
            "options": [
                ("They often save backup copies on other servers that may not be deleted immediately", True),
                ("The internet slows down", False),
                ("You didn’t press delete enough", False),
                ("They never collected it in the first place", False)
            ]
        },
        {
            "text": "Q4. Why might your ISP keep records of your activity even if you try to delete history?",
            "options": [
                ("The internet slows down", False),
                ("They never collected it in the first place", False),
                ("You didn’t press delete enough", False),
                ("They often save backup copies on other servers that may not be deleted immediately", True)
            ]
        },
        {
            "text": "Q5. Which of the following is true about using a VPN to protect your online activity from your ISP?",
            "options": [
                ("A VPN hides the websites you visit from your ISP by encrypting your internet traffic", True),
                ("A VPN makes your ISP delete all previous records automatically", False),
                ("A VPN allows your ISP to see everything faster", False),
                ("A VPN prevents your device from connecting to Wi-Fi", False)
            ]
        },
        {
            "text": "Q6. Which statement best describes modern ISP practices?",
            "options": [
                ("All ISPs only provide connectivity and never use customer data", False),
                ("Some ISPs collect extra data (beyond what’s needed for routing) and may combine it with other services for business uses", True),
                ("ISPs always destroy logs immediately and never share them", False),
                ("ISPs are legally banned everywhere from logging any metadata", False)
            ]
        },
        {
            "text": "Q7. You use your home ISP for browsing and notice targeted ads in your ISP’s TV service for websites you visited privately. What likely happened?",
            "options": [
                ("Your modem sped up", False),
                ("Ads appear by pure coincidence", False),
                ("Your browser crashed", False),
                ("Your browsing activity was recorded and linked to other services", True)
            ]
        },
        {
            "text": "Q8. You want to prevent your ISP from seeing which websites you visit. What should you do?",
            "options": [
                ("Use a VPN so all your internet traffic is encrypted and routed through a private server", True),
                ("Only use your ISP’s network at night", False),
                ("Turn off your device for a day", False),
                ("Visit fewer websites", False)
            ]
        },
        {
            "text": "Q9. You ask your ISP to delete your browsing history, but later learn that copies still exist on backup servers. Why?",
            "options": [
                ("ISPs keep backup copies for safety, which may not be deleted immediately", True),
                ("The internet refused deletion", False),
                ("You didn’t press delete correctly", False),
                ("The records never existed", False)
            ]
        },
        {
            "text": "Q10. Your ISP offers a “free” service in exchange for letting them see some of your browsing activity. What should you consider?",
            "options": [
                ("They could use your data for ads or profiling; consider opting out if possible", True),
                ("Your device will run faster", False),
                ("The service deletes your history automatically", False),
                ("It guarantees privacy", False)
            ]
        }
    ],
    "Unencrypted Network Traffic": [
        {
            "text": "Q1. What do you think 'unencrypted network traffic' mean?",
            "options": [
                ("The information you send over the internet (like passwords, messages, or emails) can be seen by others on the same network", True),
                ("Your device battery is hidden", False),
                ("Your apps will never update", False),
                ("It makes your internet faster", False)
            ]
        },
        {
            "text": "Q2. Why should you avoid sending sensitive information (like passwords or bank details) over websites that don’t use HTTPS?",
            "options": [
                ("Because unencrypted traffic can be intercepted by attackers on the same network", True),
                ("Because the websites will crash", False),
                ("Because it will slow down your device battery", False),
                ("Because it makes your Wi-Fi stronger", False)
            ]
        },
        {
            "text": "Q3. Why is unencrypted network traffic especially risky on public Wi-Fi?",
            "options": [
                ("Anyone nearby on the same Wi-Fi can potentially capture what you send or receive", True),
                ("The Wi-Fi will automatically disconnect", False),
                ("Your device battery will drain faster", False),
                ("Your Wi-Fi will become slower", False)
            ]
        },
        {
            "text": "Q4. Which practice helps keep your internet traffic private?",
            "options": [
                ("Using a VPN or accessing only HTTPS websites", True),
                ("Sharing your Wi-Fi password with neighbors", False),
                ("Leaving Bluetooth always on", False),
                ("Downloading apps from unknown websites", False)
            ]
        },
        {
            "text": "Q5. Which of the following is NOT a secure way to send sensitive information online?",
            "options": [
                ("Using websites without HTTPS or apps that don’t encrypt messages", True),
                ("Using a VPN over a public network", False),
                ("Using end-to-end encrypted messaging apps", False),
                ("Using a trusted home network with WPA2/WPA3", False)
            ]
        },
        {
            "text": "Q6. You are at a coffee shop using their free Wi-Fi and log into your bank account. The site doesn’t show a lock symbol (HTTPS). What could happen?",
            "options": [
                ("Someone else on the same Wi-Fi could capture your login and access your account", True),
                ("Your phone will automatically block ads", False),
                ("Your device will never need updates", False),
                ("Nothing — social media accounts are always safe", False)
            ]
        },
        {
            "text": "Q7. You use a messaging app that doesn’t encrypt messages. What’s a potential risk?",
            "options": [
                ("Anyone monitoring your network could read your messages", True),
                ("The messages will be faster", False),
                ("The app automatically deletes messages", False),
                ("Messages cannot be sent", False)
            ]
        },
        {
            "text": "Q8. You browse websites that start with 'http://' instead of 'https://' on your home Wi-Fi. Should you worry?",
            "options": [
                ("Yes, because even on home Wi-Fi, unencrypted traffic can be intercepted by malware or anyone with access to your network", True),
                ("No, home Wi-Fi is always secure", False),
                ("Only if your Wi-Fi is hidden", False),
                ("It’s only risky on mobile devices", False)
            ]
        },
        {
            "text": "Q9. You want to send a confidential report over the internet. Which is the safest method?",
            "options": [
                ("Use an unverified app from the app store", False),
                ("Send it over email on a public network without encryption", False),
                ("Use a website with HTTPS or a VPN, or a secure cloud storage link with encryption", True),
                ("Post it on social media", False)
            ]
        },
        {
            "text": "Q10. While traveling, you use hotel Wi-Fi to log in to multiple apps that don’t encrypt traffic. What is the risk?",
            "options": [
                ("Your login credentials, messages, or personal info could be intercepted by attackers on the same Wi-Fi", True),
                ("Your apps will run faster", False),
                ("Hotel Wi-Fi automatically protects all traffic", False),
                ("Nothing — hotels always secure Wi-Fi", False)
            ]
        }
    ],
    "Unsecured Bluetooth / Hotspot Sharing": [
        {
            "text": "Q1. What is the main risk of leaving your Bluetooth always 'discoverable'?",
            "options": [
                ("Strangers nearby could connect to your device, access files, or send malware", True),
                ("Your battery will charge faster", False),
                ("Your phone will automatically delete apps", False),
                ("Nothing — Bluetooth is always safe", False)
            ]
        },
        {
            "text": "Q2. Which of these is a safer practice for using Bluetooth?",
            "options": [
                ("Turn on Bluetooth only when needed and set it to non-discoverable", True),
                ("Leave it on all the time for convenience", False),
                ("Share your Bluetooth password publicly", False),
                ("Pair with any device that requests connection automatically", False)
            ]
        },
        {
            "text": "Q3. What is the risk of sharing a mobile hotspot without a password or with a weak password?",
            "options": [
                ("Nothing — open hotspots are safe", False),
                ("Your phone will become faster", False),
                ("The hotspot will automatically encrypt itself", False),
                ("Anyone nearby could use your internet and access your device or network", True)
            ]
        },
        {
            "text": "Q4. Which of these is the safest way to share your mobile hotspot?",
            "options": [
                ("Use a strong password and limit the number of devices that can connect", True),
                ("Leave it open so anyone can connect", False),
                ("Use your hotspot as a public Wi-Fi network for everyone in the area", False),
                ("Share your device admin credentials along with the hotspot", False)
            ]
        },
        {
            "text": "Q5. You share your mobile hotspot with friends but do not set a password. Later, you notice unusual internet activity. What likely happened?",
            "options": [
                ("Your friends’ devices created malware", False),
                ("The phone automatically blocks intruders", False),
                ("Strangers nearby connected to your hotspot and used your internet or tried to access your device", True),
                ("Nothing — open hotspot is safe", False)
            ]
        },
        {
            "text": "Q6. You want to share your mobile hotspot with friends in public. Which approach reduces risk?",
            "options": [
                ("Set a strong password and monitor the devices that connect", True),
                ("Leave it open without a password", False),
                ("Share your admin credentials for convenience", False),
                ("Enable hotspot and leave it discoverable to everyone nearby", False)
            ]
        },
        {
            "text": "Q7. You pair your phone with a public device’s Bluetooth (like a smart printer or display) without checking the connection. What is the main risk?",
            "options": [
                ("Malware or unauthorized access could spread to your device", True),
                ("The printer will automatically delete your files", False),
                ("Your battery will increase", False),
                ("Nothing — public devices are always safe", False)
            ]
        },
        {
            "text": "Q8. You occasionally connect your phone via Bluetooth to devices you don’t own, like public displays or printers. What is a safer approach?",
            "options": [
                ("Accept all incoming pairing requests automatically", False),
                ("Leave all devices paired forever for convenience", False),
                ("Only pair with trusted devices and remove old or unused pairings regularly", True),
                ("Share your hotspot password with them", False)
            ]
        },
        {
            "text": "Q9. Some apps can access your mobile hotspot or Bluetooth connections without you realizing it. What is a potential risk?",
            "options": [
                ("Apps could share your location or data with others without permission", True),
                ("The hotspot will automatically turn off", False),
                ("Your phone will become faster", False),
                ("Nothing — apps cannot misuse connections", False)
            ]
        },
        {
            "text": "Q10. Leaving your Bluetooth or hotspot on all day when you are not using it can also cause:",
            "options": [
                ("Increased battery drain and potential exposure to attacks", True),
                ("Automatic encryption of all files", False),
                ("Faster internet speed", False),
                ("Nothing — it only affects convenience", False)
            ]
        }
    ]

    },
}
 

#------- Learn More Content Data ---
learn_more_data = [
    {
        "specific_concern": "Browser Fingerprinting",
        "what_is_it": (
            "Browser fingerprinting is a technique websites use to track user behavior by "
            "collecting unique details from your device and browser. Unlike cookies, it does "
            "not store data on your device.\n\n"
            "Examples include:\n"
            "- Screen resolution\n"
            "- Browser type and version\n"
            "- Installed fonts and plugins\n"
            "- Time zone and language"
        ),
        "why_it_matters": (
            "• Enhances security: Fingerprinting can help websites recognize your device, making it "
            "harder for attackers to impersonate you.\n"
            "• Fraud prevention: Banks, payment services, and secure apps use fingerprinting to "
            "detect unusual logins or suspicious activity.\n"
            "• Custom experiences: Websites can remember your device settings and preferences "
            "without relying on cookies.\n"
            "• Safer authentication: Fingerprinting can add an extra layer of protection when "
            "combined with passwords or multi-factor authentication."
        ),
        "dos": (
            "• Use privacy-focused browsers such as Tor or Firefox with anti-tracking features when you want anonymity.\n"
            "• Be aware of fingerprinting: Know when websites may be tracking your device.\n"
            "• Balance privacy and security: Consider when fingerprinting can be beneficial (e.g., banking apps) "
            "versus when it may be a privacy concern."
        ),
        "donts": (
            "• Assuming all fingerprinting is bad: Not all fingerprinting is malicious; some enhances "
            "security and user experience.\n"
            "• Ignoring privacy settings: Adjust browser and app settings to control what data is shared.\n"
            "• Using unverified anti-fingerprinting tools indiscriminately, which may break useful security features."
        )
    },
    {
        "specific_concern": "Targeted Ads and Online tracking",
        "what_is_it": (
            "Targeted advertising involves delivering personalized ads to users based on their "
            "online behavior and interests.\n"
            "Online tracking refers to the methods used by websites and advertisers to monitor users' "
            "activities across the internet, with or without explicit consent."
        ),
        "why_it_matters": (
            "• Enhanced user experience: Personalized ads can make online content more relevant and engaging.\n"
            "• Improved product discovery: Targeted ads can help users discover products and services "
            "that align with their interests and needs."
        ),
        "dos": (
            "• Adjust privacy settings: Use browser settings and extensions to control ad tracking and personalization.\n"
            "• Review ad preferences: Regularly check and update ad preferences to prevent tracking.\n"
            "• Use privacy-focused tools: Consider using ad blockers or privacy browsers to limit tracking."
        ),
        "donts": (
            "• Ignoring privacy settings: Not adjusting ad preferences can lead to unwanted tracking and irrelevant ads.\n"
            "• Over-sharing personal information: Providing excessive personal details can increase the amount of data "
            "available for ad targeting.\n"
            "• Using unverified privacy tools: Some tools may not effectively block ads or could compromise security."
        )
    },
    {
        "specific_concern": "Public Wi-Fi browsing risks",
        "what_is_it": (
            "Public Wi-Fi networks are often unsecured, where data transmission over them "
            "can be intercepted by malicious actors."
        ),
        "why_it_matters": (
            "• Data interception: Without encryption, sensitive information like passwords and "
            "credit card numbers can be easily captured by attackers.\n"
            "• Man-in-the-middle attacks: Cybercriminals can position themselves between you and "
            "the connection point, potentially altering communications.\n"
            "• Malware distribution: Hackers can exploit vulnerabilities in the network to distribute "
            "malware to connected devices.\n"
            "• Session hijacking: Attackers can steal session cookies to impersonate users and gain "
            "unauthorized access to accounts."
        ),
        "dos": (
            "• Use a Virtual Private Network (VPN): Encrypts your internet connection, protecting your "
            "data from attackers.\n"
            "• Connect to secured networks: Prefer networks that require a password or have WPA3 "
            "(Wi-Fi Protected Access 3) encryption.\n"
            "• Disable sharing settings: Turn off file and printer sharing when connected to public Wi-Fi.\n"
            "• Use HTTPS websites: Ensure the websites you visit use HTTPS, indicating encrypted "
            "communication.\n"
            "• Enable two-factor authentication: Adds an extra layer of security to your online accounts."
        ),
        "donts": (
            "• Accessing sensitive information: Avoid online banking or shopping on public Wi-Fi networks.\n"
            "• Connecting to unknown networks: Refrain from joining networks with generic names like 'Free Wi-Fi.'\n"
            "• Disabling firewalls or antivirus software: These tools help protect your device from potential threats."
        )
    },
    {
        "specific_concern": "Auto-Saved Passwords and Autofill Data",
        "what_is_it": (
            "Auto-saved passwords are credentials that your browser or password manager stores "
            "to automatically log you into websites.\n"
            "Autofill data includes saved information such as names, addresses, phone numbers, "
            "credit card details, and email addresses, which can be automatically filled into forms."
        ),
        "why_it_matters": (
            "• Convenience: Auto-fill and saved passwords save time and reduce errors when logging "
            "into accounts or completing forms.\n"
            "• Risk of unauthorized access: If your device is lost, stolen, or compromised, attackers "
            "may access saved credentials and personal information.\n"
            "• Phishing vulnerability: Malicious websites can trick browsers into auto-filling sensitive "
            "data on fake forms."
        ),
        "dos": (
            "• Use a trusted password manager: Prefer reputable password managers over browser "
            "auto-save for stronger encryption.\n"
            "• Enable device authentication: Require biometrics or a strong master password before "
            "autofill is accessed.\n"
            "• Limit autofill of sensitive data: Disable autofill for payment cards or sensitive personal "
            "information when possible.\n"
            "• Keep devices secure: Regularly update software, use strong passwords, and enable device "
            "encryption."
        ),
        "donts": (
            "• Storing all passwords in the browser without additional protection.\n"
            "• Using public or shared devices to save passwords or autofill data.\n"
            "• Clicking unknown links that trigger autofill forms on untrusted websites.\n"
            "• Ignoring software updates, which may cause vulnerabilities in autofill systems."
        )
    },
    {
        "specific_concern": "Location Tracking by Apps",
        "what_is_it": (
            "Location tracking by mobile applications involves the collection of a user's geographical "
            "position through various means such as GPS, Wi-Fi networks, Bluetooth, or cellular data. "
            "This tracking can occur while the app is in use or in background activity."
        ),
        "why_it_matters": (
            "• Privacy Concerns: Continuous location tracking can reveal sensitive information about "
            "a user's daily routines, frequent locations, and personal habits.\n"
            "• Targeted Advertising: Many free applications monetize user location data with advertisers, "
            "for delivering the targeted advertisements based on the user's movements and behaviors.\n"
            "• Security Risks: Leaked location data can expose users to various security threats, including "
            "stalking, burglary, etc. if the data reveals patterns such as home addresses or daily routines.\n"
            "• Battery Performance: Apps that continuously track location can drain device battery life "
            "and consume data, affecting the overall performance of the device."
        ),
        "dos": (
            "• Review App Permissions: Regularly check which apps have access to your location data and "
            "adjust permissions as necessary to limit access to only those apps that truly require it.\n"
            "• Use Temporary or One-Time Permissions: When possible, grant location access only for the "
            "duration of the app's use or on a one-time basis, rather than allowing continuous background access.\n"
            "• Understand App Privacy Policies: Before granting location access, read the app's privacy "
            "policy to understand how your location data will be used, stored, and shared."
        ),
        "donts": (
            "• Grant Unnecessary Permissions: Avoid granting location access to apps that do not require it "
            "for their core functionality.\n"
            "• Ignore Background Tracking: Be cautious of apps that request background location access, "
            "as they can track your movements even when the app is not actively in use.\n"
            "• Neglect Device Settings: Regularly review and adjust your device's location settings to ensure "
            "that apps are not accessing your location without your knowledge."
        )
    },
    {
        "specific_concern": "Data Sharing with Third Parties",
        "what_is_it": (
            "Third-party data sharing occurs when apps or websites send information collected from users "
            "to external companies, such as advertisers, analytics providers, or business partners. "
            "This is different from data that stays within the app’s own system/company. Third parties may "
            "use this information for targeted advertising, analytics, or other commercial purposes.\n"
            "Example of demanding user data shared with third parties: contact information, location data, "
            "browsing history, app usage habits, purchase behavior, etc."
        ),
        "why_it_matters": (
            "• Targeted Advertising & Profiling: Sharing data allows advertisers to build detailed profiles "
            "of users across apps and websites, enabling highly personalized advertising.\n"
            "• Privacy & Security Risks: Third-party sharing increases the number of entities holding your data, "
            "raising the risk of leaks, breaches, or misuse.\n"
            "• Re-identification Risk: Even “anonymized” data can sometimes be combined with other datasets "
            "which can possibly identify users.\n"
            "• Monetization of Free Apps: Many free apps rely on third-party advertising and analytics to generate "
            "revenue, which is why they often share user data externally."
        ),
        "dos": (
            "• Review Permissions Carefully: Only grant the permissions necessary for the app to function.\n"
            "• Limit Ad Tracking: Enable settings like “Limit Ad Tracking” or equivalent privacy controls on your device.\n"
            "• Understand App Policies: Check whether apps disclose sharing with third parties in their privacy policies.\n"
            "• Use Privacy Tools: Browser extensions or operating system settings can reduce the amount of data visible to advertisers."
        ),
        "donts": (
            "• Do Not Accept All Permissions by Default: Granting all requested permissions can unnecessarily expose your data.\n"
            "• Do Not Assume Anonymized Data is Safe: Third-party data, even if anonymized, can sometimes be re-identified.\n"
            "• Do Not Ignore App Privacy Practices: Be skeptical of free apps that request more permissions than necessary."
        )
    },
    {
        "specific_concern": "Hidden Background Activity",
        "what_is_it": (
            "Hidden background activity occurs when apps continue to run tasks, collect data, or communicate with servers "
            "even when you are not actively using them. While some background activity is legitimate (e.g., health apps), "
            "many apps use this opportunity to collect personal data without your knowledge.\n"
            "Examples of Hidden Background Activity:\n"
            "• A social media app syncing your activity or messages while closed\n"
            "• A game app collecting usage patterns or device information in the background\n"
            "• Apps uploading location, contacts, or browsing habits without user interaction (e.g., walking tracking app)"
        ),
        "why_it_matters": (
            "• Privacy Risks: Apps can collect sensitive data such as location, contacts, browsing habits, and app usage "
            "patterns without your explicit consent.\n"
            "• Data Monetization: Background activity allows apps to send collected data to advertisers and analytics "
            "companies for profiling and targeted advertising.\n"
            "• Battery and Data Consumption: Apps running unseen in the background can drain battery life and consume "
            "significant mobile data, affecting device performance. (Zhang et al., 2014)"
        ),
        "dos": (
            "• Check Battery & Data Usage: Regularly monitor which apps consume high resources in the background.\n"
            "• Restrict Background Activity: Use OS-level settings to restrict background data or force-stop unnecessary apps.\n"
            "• Review App Permissions: Limit permissions for apps that don’t need constant access to sensitive data.\n"
            "• Uninstall Suspicious Apps: Remove apps that run tasks in the background without clear justification."
        ),
        "donts": (
            "• Do Not Ignore High Resource Usage: High battery or data usage can indicate hidden background activity.\n"
            "• Do Not Grant All Permissions by Default: Excess permissions enable apps to perform background operations unnecessarily.\n"
            "• Do Not Neglect Updates: Some apps fix background data collection issues in updates; outdated apps may continue risky behavior."
        )
    },
    {
        "specific_concern": "Malicious or Scam Apps",
        "what_is_it": (
            "Malicious or scam apps are misleading applications designed to steal personal information, display intrusive ads, "
            "install malware, or perform unauthorized actions on your device. These apps often impersonate themselves as legitimate apps "
            "but contain hidden code to exploit user trust.\n"
            "Examples include: fake banking or payment apps that steal credentials, free “utility” apps (QR scanners, storage cleaners) "
            "that collect private data, etc."
        ),
        "why_it_matters": (
            "• Data Theft and Identity Fraud: Malicious apps can collect sensitive data like passwords, photos, contacts, and location, "
            "then transmit it to attackers.\n"
            "• Financial and Credential Theft: Fake banking apps often impersonate legitimate applications to steal user logins or "
            "initiate unauthorized transactions.\n"
            "• Unauthorized Surveillance: Some malicious apps secretly record audio, take photos, or collect keystrokes through unknowingly granted permissions."
        ),
        "dos": (
            "• Install Only from Official Stores: Use Google Play, Apple App Store, or official repositories with verified publishers.\n"
            "• Check Developer and Permissions: Avoid apps requesting unnecessary permissions (e.g., a weather app asking for contacts).\n"
            "• Read Authentic Reviews: Look for detailed feedback from verified users; fake reviews often sound repetitive or vague.\n"
            "• Use Mobile Security Tools: Consider using reputable mobile antivirus that flag known malicious software.\n"
            "• Keep Software Updated: Updates often fix security vulnerabilities that malicious apps exploit."
        ),
        "donts": (
            "• Do Not Download from Unknown Links: Avoid downloading apps from emails, ads, or social media links.\n"
            "• Do Not Ignore Permissions: If an app asks for access unrelated to its purpose (camera, contacts, etc), don’t allow it.\n"
            "• Do Not Store Sensitive Info in Unverified Apps: Never enter personal or banking data in unfamiliar apps.\n"
            "• Do Not Click on “Too Good to Be True” Offers: Free premium features, instant cash rewards, etc are dangerous."
        )
    }, 
    {
    "specific_concern": "Unprotected File Sharing Links",
        "what_is_it": (
            "Unprotected file sharing links refer to cloud-based file access URLs that grant access to files without authentication, "
            "user verification, or expiration settings. While convenient for collaboration, such links can accidentally expose "
            "confidential or personal information to unauthorized individuals or the public."
        ),
        "why_it_matters": (
            "• Unauthorized Access to Sensitive Data: Files shared via unrestricted links may be accessed by anyone who discovers or receives the link.\n"
            "• Data Leakage via Link Forwarding: Unprotected URLs can be shared beyond intended users, creating persistent exposure risks.\n"
            "• Inadequate Expiration Controls: Many cloud services lack robust expiration management, where old links may remain active indefinitely unless manually revoked."
        ),
        "dos": (
            "• Use Password-Protected Links: Require a password or authentication to access files. Most major providers (Google Drive, OneDrive, Dropbox) support this feature.\n"
            "• Set Expiration Dates: Expiration ensures shared access ends automatically after a defined period — a key control against long-term exposure.\n"
            "• Restrict Access to Specific Users: Limit sharing to named collaborators’ accounts rather than “anyone with the link.”\n"
            "• Review Old Shared Links: Regularly audit cloud storage permissions and revoke inactive or unused links.\n"
            "• Monitor Access Logs: Use cloud activity logs to track who accessed or downloaded shared files."
        ),
        "donts": (
            "• Select “Anyone with the Link” Settings for Sensitive Data: This effectively makes the file public — anyone with the link can access it, even unintentionally.\n"
            "• Do Not Share Links via Public Platforms: Posting links on forums, chats, or social media can lead to massive uncontrolled distribution.\n"
            "• Don’t Assume Links Expire Automatically: Many services leave links active until manually revoked."
        )
    },
    {
        "specific_concern": "Weak or Shared Passwords",
        "what_is_it": (
            "Weak or shared passwords refer to login credentials that are easily guessable, reused across multiple services, or shared between individuals. "
            "Such passwords often rely on personal information (e.g., birthdays, names, or simple patterns like “123456”). "
            "Even though passwords remain the most common form of authentication, research consistently shows that users tend to select weak or reused passwords, "
            "increasing the likelihood of large-scale data breaches and identity theft."
        ),
        "why_it_matters": (
            "• Password Reuse Increases Breach Impact: Using the same password across multiple platforms means a single data breach can compromise all linked accounts — a phenomenon known as credential stuffing.\n"
            "• Weak Passwords Are Easily Guessable: Simple or predictable passwords (e.g., “password123,” “birthday”) can be cracked within seconds using automated tools. Attackers often exploit common patterns derived from password leaks.\n"
            "• Shared Passwords Lead to Accountability Risks: Sharing credentials undermines access control and traceability, making it impossible to determine who performed specific actions within a system.\n"
            "• Weak Recovery Questions Are Exploitable: Password recovery mechanisms using personal or guessable questions (“mother’s maiden name,” “pet’s name”) are often publicly discoverable, especially through social media.\n"
            "• Multi-Factor Authentication (MFA) Reduces Risk: Even if a password is compromised, MFA provides a critical secondary barrier (e.g., one-time codes or biometric verification)."
        ),
        "dos": (
            "• Use a Password Manager: Generate and store complex, unique passwords securely for every account.\n"
            "• Enable Multi-Factor Authentication (2FA/MFA): Adds an extra layer of defense even if passwords are compromised.\n"
            "• Create Strong, Random Passwords: Use at least 12 characters combining letters, numbers, and symbols.\n"
            "• Change Passwords After a Breach: Regularly update passwords if any service you use is affected by a data leak.\n"
            "• Educate Team Members: Enforce security awareness to prevent password sharing or unsafe recovery practices."
        ),
        "donts": (
            "• Avoid Reusing Passwords Across Sites: Prevent attackers from accessing multiple accounts after one breach.\n"
            "• Never Share Passwords: Even trusted colleagues or friends can unintentionally expose credentials.\n"
            "• Don’t Use Personal Info: Birthdays, names, and common words are easy for attackers to guess.\n"
            "• Don’t Rely on Security Questions Alone: Use 2FA instead of predictable recovery answers."
        )
    },
    {
        "specific_concern": "Automatic Photo Backup Without Consent",
        "what_is_it": (
            "Images and videos are being backed up automatically from the user’s device to a cloud without explicit user permission or knowledge of data being transferred. "
            "These data can include sensitive personal information and this backup raises serious privacy protection and consent violations."
        ),
        "why_it_matters": (
            "• Unintentional Exposure of Sensitive Images: Photos may include personal identifiers, family members, or private contexts not meant to be stored online. Automatic upload might accidentally expose such images to service providers, hackers, or unintended recipients.\n"
            "• Metadata Leakage (Hidden Information in Photos): Modern photos often store EXIF metadata, such as GPS coordinates, timestamps, and device identifiers. When backed up automatically, this hidden data can reveal location history or behavioral patterns.\n"
            "• Cross-Device Synchronization Without User Awareness: When a user logs into multiple devices, photos may sync across all of them automatically, causing unintended disclosure or co-mingling of data among different users or devices.\n"
            "• Deleted Files May Persist in Cloud Copies: Cloud storage systems often maintain redundant copies of user data across multiple servers or data centers. Even after deletion from visible cloud folders, replicated versions may continue to exist for a certain retention period, extending potential exposure of sensitive information."
        ),
        "dos": (
            "• Review Backup Settings Before Enabling Cloud Sync: Manually confirm which folders or media types are being uploaded.\n"
            "• Use “Manual Upload” Mode: Set the settings that prompt you each time before uploading photos.\n"
            "• Regularly Audit Cloud Accounts: Review stored media and delete files manually you no longer wish to keep online.\n"
            "• Disable Metadata Upload: Exclude GPS and device data from photos before cloud upload.\n"
            "• Revoke Unused Device Access: Check all linked devices and sign out of any you no longer use."
        ),
        "donts": (
            "• Don’t Assume Backup Consent is Required by Default: Some apps auto-enable uploads without clear prompts so always check initial setup options.\n"
            "• Avoid Logging into Cloud Apps on Shared Devices: Auto-sync may transfer private media to others’ accounts.\n"
            "• Don’t Ignore Permissions Requests: Carefully read what access the app requests.\n"
            "• Avoid Using Unknown or Unverified Cloud Apps or Services: Stick to providers with transparent privacy and security policies."
        )
    },
    {
        'specific_concern': "Data Stored in Unknown Locations",
        'what_is_it': (
            """Data stored in unknown locations refers to information that users upload to cloud services without knowing the exact country or data center where it will reside. Many cloud providers replicate files across multiple locations for redundancy, performance, or legal purposes, which means your data may travel internationally without your knowledge."""
        ),
        "why_it_matters":(
             """• Data Sovereignty & Legal Risks: Different countries have different data protection laws. Data stored abroad may be subject to local government access or regulatory requirements that differ from your home country.\n'
                • Loss of Control: Storing data across multiple jurisdictions can make it harder to ensure proper deletion, privacy compliance, or enforcement of user rights.\n'
                • Reduced Trust: Users may lose confidence in cloud providers when storage locations are unclear, potentially exposing sensitive personal or business information.\n'
                • Backup & Retention Challenges: Copies in unknown locations may not be deleted promptly or may follow different retention policies, increasing the risk of unintended access."""
        ),
        "dos": (
                "Check Data Location Options: Choose cloud providers that allow you to select or restrict the region where your data is stored.\n"
                "Read Privacy & Security Policies: Understand how your cloud provider handles international replication and legal access requests.\n"
                "Enable Strong Encryption: Use end-to-end encryption to ensure that even if data is stored in an unknown country, only you can access it.\n"
                "Regularly Audit Cloud Data: Verify where your data resides, and review backup copies and sharing settings."
        ),
        "donts": (
                "Don’t Assume Global Storage Is Safe: Replication for convenience may expose data to foreign jurisdictions with weaker privacy protections.\n"
                "Don’t Ignore Provider Transparency: Avoid using services that don’t clearly state where your data is stored or replicated.\n"
                "Don’t Skip Encryption or Access Controls: Leaving files unencrypted or broadly shared increases the risk if they reside in unknown or multiple countries.\n"
                "Don’t Rely Solely on Automatic Deletion: Backup copies may persist in other locations, so always confirm deletion policies and procedures."
        )
    },
    {
        'specific_concern': "Using Public Wi-Fi Without Protection",
        'what_is_it': (
            """Public Wi-Fi is a wireless network available in places like cafes, airports, hotels, and libraries. These networks are often open and do not require a password, making them easy to access but also easy for attackers to exploit."""
        ),
        "why_it_matters":(
             """• Attackers can intercept your communications, including emails, passwords, and banking information.\n'
                • Man-in-the-middle attacks allow attackers to modify or capture your data without your knowledge.\n'
                • Even casual browsing activity can be tracked and linked across devices or accounts.\n'
                • Cybercriminals can use these networks to commit identity theft, fraud, or gain unauthorized access to your accounts."""
        ),
        "dos": (
                "Use a VPN to encrypt your internet traffic.\n"
                "Prefer HTTPS websites to ensure secure connections.\n"
                "Keep your device’s firewall and antivirus software active.\n"
                "Log out of accounts when finished and disable automatic network connections."
        ),
        "donts": (
                "Don’t access sensitive accounts (banking, work files) on unsecured Wi-Fi.\n"
                "Don’t accept or install unknown security certificates.\n"
                "Don’t share files or folders over public networks.\n"
                "Don’t assume all free Wi-Fi is safe; attackers can create fake networks."
        )
    },
    {
        'specific_concern': "ISP Tracking and Data Logging",
        'what_is_it': (
            """Your Internet Service Provider (ISP) is the company that gives you access to the internet. While providing connectivity, ISPs can monitor certain aspects of your online activity, such as the websites you visit, the time you spend online, and other metadata. Even if content is encrypted, your ISP can often see patterns in your traffic."""
        ),
        "why_it_matters":(
             """• ISPs can record your browsing history and link it to your identity.\n'
                • Backup copies of your activity may exist even after deletion, meaning records are rarely fully erased immediately.\n'
                • Some ISPs combine browsing data with other services they provide, increasing exposure.\n'
                • Your online activity could be correlated across devices or accounts, reducing anonymity."""
        ),
        "dos": (
                "Use a VPN to encrypt your internet traffic and hide visited websites from your ISP.\n"
                "Enable HTTPS connections to secure your communication with websites.\n"
                "Consider privacy-focused ISPs or services that minimize data collection.\n"
                "Review your ISP’s privacy policy to understand what data they collect and how it’s used."
        ),
        "donts": (
                "Don’t assume your ISP cannot see your online activity.\n"
                "Don’t rely solely on deleting browser history; backups may still exist.\n"
                "Don’t share sensitive data without using encryption or privacy safeguards.\n"
                "Don’t ignore “free” ISP services that require data access that they may track or monetize your activity."
        )
    },
    {
        'specific_concern': "Unencrypted Network Traffic",
        'what_is_it': (
            """Unencrypted network traffic is data sent over the internet that is not protected by encryption, meaning anyone on the same network or in some cases even farther away which can potentially see it. This includes passwords, emails, messages, banking information, and other sensitive data. Websites that use “HTTP” instead of “HTTPS” or apps without encryption send information in plain text."""
        ),
        "why_it_matters":(
             """• Passwords and login credentials can be intercepted and stolen.\n'
                • Financial or sensitive personal data could be captured, leading to fraud or identity theft.\n'
                • Messages sent through unencrypted apps can be read by attackers.\n'
                • Lack of encryption reduces trust in the services you use and exposes you to unnecessary risks."""
        ),
        "dos": (
                "Use HTTPS websites whenever possible (look for the lock symbol in the browser).\n"
                "Use a VPN when on public networks to encrypt all your traffic.\n"
                "Prefer end-to-end encrypted apps for messaging and file sharing.\n"
                "Regularly update apps and devices to benefit from security improvements.."
        ),
        "donts": (
                "Don’t send passwords, bank info, or sensitive files over HTTP websites or unencrypted apps.\n"
                "Don’t use untrusted public networks for confidential tasks without a VPN.\n"
                "Don’t ignore security warnings or missing HTTPS indicators on websites.\n"
                "Don’t assume encryption is unnecessary on home WiFi malware or misconfigured routers can intercept traffic."
        )
    }
]

#------- Pet Recommendation Data ---
pet_data = [
    {
        "selected_concern": "Browser Fingerprinting",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "DuckDuckGo Privacy Browser",
        "pet_price": "Free",
        "pet_description": "The DuckDuckGo app provides the most comprehensive online privacy protection with the push of a button. With one free download, you get an everyday private Internet browser that offers seamless protection while you search and browse, and access to tracking protection for emails you receive and apps you use. Many of these protections are not offered in most popular web browsers by default.",
        "pet_company": "DuckDuckGo",
        "pet_link": "https://duckduckgo.com",
        "why_use": "Block Tracking Cookies While Browsing, Automatically Enforce Encryption, Block Email Trackers,Escape Fingerprinting",
        "popularity": 4
    },
    {
        "selected_concern": "Browser Fingerprinting",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "DuckDuckGo Privacy Browser",
        "pet_price": "Free",
        "pet_description": "The DuckDuckGo app provides the most comprehensive online privacy protection with the push of a button. With one free download, you get an everyday private Internet browser that offers seamless protection while you search and browse, and access to tracking protection for emails you receive and apps you use. Many of these protections are not offered in most popular web browsers by default.",
        "pet_company": "DuckDuckGo",
        "pet_link": "https://duckduckgo.com",
        "why_use": "Block Tracking Cookies While Browsing, Automatically Enforce Encryption, Block Email Trackers,Escape Fingerprinting",
        "popularity": 4
    },
    {
        "selected_concern": "Browser Fingerprinting",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Firefox Browser",
        "pet_price": "Free",
        "pet_description": "Get Firefox so your passwords, browsing history and ad blocker extensions — and the privacy and security you rely on.",
        "pet_company": "Mozilla",
        "pet_link": "https://www.firefox.com/en-US/",
        "why_use": " Automatic tracker blocking, Enhanced tracking protection, Ad blocker extensions",
        "popularity": 4
    },
    {
        "selected_concern": "Browser Fingerprinting",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Tor Browser",
        "pet_price": "Free",
        "pet_description": "The Tor Project, Inc., is a 501(c)(3) organization developing free and open source software for privacy and freedom online, protecting people from tracking, surveillance, and censorship. The Tor Project’s mission is to advance human rights and freedoms by creating and deploying free and open source anonymity and privacy technologies, support their unrestricted availability and use, and further their scientific and popular understanding.",
        "pet_company": "The Tor Project",
        "pet_link": "https://www.torproject.org/download/",
        "why_use": "BLOCK TRACKERS, DEFEND AGAINST SURVEILLANCE, RESIST FINGERPRINTING, MULTI-LAYERED ENCRYPTION",
        "popularity": 4
    },
    {
        "selected_concern": "Browser Fingerprinting",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "Tor Browser",
        "pet_price": "Free",
        "pet_description": "The Tor Project, Inc., is a 501(c)(3) organization developing free and open source software for privacy and freedom online, protecting people from tracking, surveillance, and censorship. The Tor Project’s mission is to advance human rights and freedoms by creating and deploying free and open source anonymity and privacy technologies, support their unrestricted availability and use, and further their scientific and popular understanding.",
        "pet_company": "The Tor Project",
        "pet_link": "https://www.torproject.org/download/",
        "why_use": "BLOCK TRACKERS, DEFEND AGAINST SURVEILLANCE, RESIST FINGERPRINTING, MULTI-LAYERED ENCRYPTION",
        "popularity": 4
    },
    {
        "selected_concern": "Browser Fingerprinting",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "CanvasBlocker",
        "pet_price": "Free",
        "pet_description": "This add-on allows users to prevent websites from using some Javascript APIs to fingerprint them. Users can choose to block the APIs entirely on some or all websites (which may break some websites) or fake its fingerprinting-friendly readout API.",
        "pet_company": "kkapsner",
        "pet_link": "https://addons.mozilla.org/en-US/firefox/addon/canvasblocker/",
        "why_use": " If a website is not listed on the white list or black list, the user will be asked if the website should be allowed to use the protected APIs each time they are called.Ignore all lists and block the protected APIs on all websites.",
        "popularity": 4
    },
    {
        "selected_concern": "Browser Fingerprinting",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "CanvasBlocker",
        "pet_price": "Free",
        "pet_description": "This add-on allows users to prevent websites from using some Javascript APIs to fingerprint them. Users can choose to block the APIs entirely on some or all websites (which may break some websites) or fake its fingerprinting-friendly readout API.",
        "pet_company": "kkapsner",
        "pet_link": "https://addons.mozilla.org/en-US/firefox/addon/canvasblocker/",
        "why_use": " If a website is not listed on the white list or black list, the user will be asked if the website should be allowed to use the protected APIs each time they are called.Ignore all lists and block the protected APIs on all websites.",
        "popularity": 4
    },
    {
        "selected_concern": "Browser Fingerprinting",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Tor Browser",
        "pet_price": "Free",
        "pet_description": "The Tor Project, Inc., is a 501(c)(3) organization developing free and open source software for privacy and freedom online, protecting people from tracking, surveillance, and censorship. The Tor Project’s mission is to advance human rights and freedoms by creating and deploying free and open source anonymity and privacy technologies, support their unrestricted availability and use, and further their scientific and popular understanding.",
        "pet_company": "The Tor Project",
        "pet_link": "https://www.torproject.org/download/",
        "why_use": "BLOCK TRACKERS, DEFEND AGAINST SURVEILLANCE, RESIST FINGERPRINTING, MULTI-LAYERED ENCRYPTION",
        "popularity": 4
    },
    {
        "selected_concern": "Browser Fingerprinting",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Tor Browser",
        "pet_price": "Free",
        "pet_description": "The Tor Project, Inc., is a 501(c)(3) organization developing free and open source software for privacy and freedom online, protecting people from tracking, surveillance, and censorship. The Tor Project’s mission is to advance human rights and freedoms by creating and deploying free and open source anonymity and privacy technologies, support their unrestricted availability and use, and further their scientific and popular understanding.",
        "pet_company": "The Tor Project",
        "pet_link": "https://www.torproject.org/download/",
        "why_use": "BLOCK TRACKERS, DEFEND AGAINST SURVEILLANCE, RESIST FINGERPRINTING, MULTI-LAYERED ENCRYPTION",
        "popularity": 4
    },
    {
        "selected_concern": "Browser Fingerprinting",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "FPRandom or FPGuard",
        "pet_price": "Paid",
        "pet_description": "",
        "pet_company": "The Tor Project",
        "pet_link": "https://inria.hal.science/hal-01527580/document",
        "why_use": "Please refer to the literature for more information.",
        "popularity": 4
    },
    {
        "selected_concern": "Targeted Ads and online tracking",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "DuckDuckGo Privacy Browser",
        "pet_price": "Free",
        "pet_description": "The DuckDuckGo app provides the most comprehensive online privacy protection with the push of a button. With one free download, you get an everyday private Internet browser that offers seamless protection while you search and browse, and access to tracking protection for emails you receive and apps you use. Many of these protections are not offered in most popular web browsers by default.",
        "pet_company": "DuckDuckGo",
        "pet_link": "https://duckduckgo.com",
        "why_use": "Block Tracking Cookies While Browsing, Automatically Enforce Encryption, Block Email Trackers,Escape Fingerprinting",
        "popularity": 4
    },
    {
        "selected_concern": "Targeted Ads and online tracking",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Firefox Browser",
        "pet_price": "Free",
        "pet_description": "Get Firefox so your passwords, browsing history and ad blocker extensions — and the privacy and security you rely on.",
        "pet_company": "Mozilla",
        "pet_link": "https://www.firefox.com/en-US/",
        "why_use": " Automatic tracker blocking, Enhanced tracking protection, Ad blocker extensions",
        "popularity": 4
    },
    {
        "selected_concern": "Targeted Ads and online tracking",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "Android",
        "country": "Global",
        "pet_name": "DuckDuckGo Privacy Browser",
        "pet_price": "Free",
        "pet_description": "The DuckDuckGo app provides the most comprehensive online privacy protection with the push of a button. With one free download, you get an everyday private Internet browser that offers seamless protection while you search and browse, and access to tracking protection for emails you receive and apps you use. Many of these protections are not offered in most popular web browsers by default.",
        "pet_company": "DuckDuckGo",
        "pet_link": "https://duckduckgo.com",
        "why_use": "Block Tracking Cookies While Browsing, Automatically Enforce Encryption, Block Email Trackers,Escape Fingerprinting",
        "popularity": 4
    },
    {
        "selected_concern": "Targeted Ads and online tracking",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Brave Browser",
        "pet_price": "Free",
        "pet_description": "The new Brave browser blocks ads and trackers that slow you down and invade your privacy",
        "pet_company": "Brave Software",
        "pet_link": "https://brave.com",
        "why_use": "AI ASSISTANT, Brave Search, Private Browsing, Browse Faster, Privacy Protection",
        "popularity": 4
    },
    {
        "selected_concern": "Targeted Ads and online tracking",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Ghostery Plus",
        "pet_price": "Free",
        "pet_description": "Ghostery provides several applications that work together to ensure optimal privacy protection. Whether you need an ad blocker, a tracker neutralizer, or a private search engine, Ghostery has you covered.",
        "pet_company": "Brave Software",
        "pet_link": "https://www.ghostery.com",
        "why_use": "Block all ads on websites, including YouTube and Facebook, to focus on the information that matters.Automatically remove intrusive cookie pop-ups and express dissent to online tracking.Preview tracker information on search engine result pages to make informed choices.",
        "popularity": 4
    },
    {
        "selected_concern": "Targeted Ads and online tracking",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "Window",
        "country": "Global",
        "pet_name": "Tor Browser",
        "pet_price": "Free",
        "pet_description": "The Tor Project, Inc., is a 501(c)(3) organization developing free and open source software for privacy and freedom online, protecting people from tracking, surveillance, and censorship. The Tor Project’s mission is to advance human rights and freedoms by creating and deploying free and open source anonymity and privacy technologies, support their unrestricted availability and use, and further their scientific and popular understanding.",
        "pet_company": "The Tor Project",
        "pet_link": "https://www.torproject.org/download/",
        "why_use": "BLOCK TRACKERS, DEFEND AGAINST SURVEILLANCE, RESIST FINGERPRINTING, MULTI-LAYERED ENCRYPTION",
        "popularity": 4
    },
    {
        "selected_concern": "Targeted Ads and online tracking",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "Window",
        "country": "Global",
        "pet_name": "NextDNS ",
        "pet_price": "€1.99",
        "pet_description": "NextDNS is a cloud-based DNS filter and firewall designed to protect your home, family, and online privacy. With NextDNS Manager, you can effortlessly control your NextDNS settings to ensure a safer, more secure digital experience. ",
        "pet_company": "DoubleAngels",
        "pet_link": "https://nextdns.io",
        "why_use": "Easily manage your NextDNS settings including filtering modes, blocklists, and whitelists.Benefit from NextDNS' robust filtering capabilities to safeguard your online activities. An app lock using biometrics or a PIN code secures your settings from prying eyes.",
        "popularity": 4
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "HTTPs extensions",
        "pet_price": "Free",
        "pet_description": "Automatically redirect to HTTPS version of websites.Navigate the web with confidence! HTTPS Everywhere is a Chrome extension designed to enhance your internet security with a simple yet powerful action: it automatically redirects you to the HTTPS version of websites whenever possible. ",
        "pet_company": "Chrome",
        "pet_link": "https://chromewebstore.google.com/detail/https-everywhere/ikclbgejgcbdlhjmckecmdljlpbhmbmf?hl=en",
        "why_use": "Seamlessly switches your connection from HTTP to HTTPS, ensuring that your browsing is encrypted and more resistant to eavesdropping.Protect your sensitive information from prying eyes, especially on public Wi-Fi networks.",
        "popularity": 3
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Mullvad",
        "pet_price": "5$/month",
        "pet_description": "With Mullvad VPN, your traffic travels through an encrypted tunnel to one of our VPN servers and then onward to the website you are visiting. In this way, websites will only see our server’s identity instead of yours. Same goes for your ISP (internet service provider); they’ll see that you’re connected to Mullvad, but not your activity. ",
        "pet_company": "Mullvad VPN AB",
        "pet_link": "https://mullvad.net/en",
        "logo_link": "assets/logos/wifisafe.png",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 3
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "HTTPs extensions",
        "pet_price": "Free",
        "pet_description": "Automatically redirect to HTTPS version of websites.Navigate the web with confidence! HTTPS Everywhere is a Chrome extension designed to enhance your internet security with a simple yet powerful action: it automatically redirects you to the HTTPS version of websites whenever possible. ",
        "pet_company": "Chrome",
        "pet_link": "https://chromewebstore.google.com/detail/https-everywhere/ikclbgejgcbdlhjmckecmdljlpbhmbmf?hl=en",
        "why_use": "Seamlessly switches your connection from HTTP to HTTPS, ensuring that your browsing is encrypted and more resistant to eavesdropping.Protect your sensitive information from prying eyes, especially on public Wi-Fi networks.",
        "popularity": 3
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "HTTPs extensions",
        "pet_price": "Free",
        "pet_description": "Automatically redirect to HTTPS version of websites.Navigate the web with confidence! HTTPS Everywhere is a Chrome extension designed to enhance your internet security with a simple yet powerful action: it automatically redirects you to the HTTPS version of websites whenever possible. ",
        "pet_company": "Chrome",
        "pet_link": "https://chromewebstore.google.com/detail/https-everywhere/ikclbgejgcbdlhjmckecmdljlpbhmbmf?hl=en",
        "why_use": "Seamlessly switches your connection from HTTP to HTTPS, ensuring that your browsing is encrypted and more resistant to eavesdropping.Protect your sensitive information from prying eyes, especially on public Wi-Fi networks.",
        "popularity": 3
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "NordVPN",
        "pet_price": "2.99$/month",
        "pet_description": "It’s an easy-to-use VPN app for Android smartphones, tablets.",
        "pet_company": "Nord Security",
        "pet_link": "https://nordvpn.com",
        "why_use": "When you’re connected to a VPN, no one can see what websites you visit or files you download. You can surf the web with confidence with Threat Protection. And NordVPN protects you from traffic-based bandwidth throttling.",
        "popularity": 4
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Surfshark",
        "pet_price": "1.99$/month",
        "pet_description": "Surfshark is a VPN service that encrypts your internet connection, hides your IP address, and protects your online activity across various devices. It is known for its strong security features, fast speeds, unlimited device connections, and user-friendly apps.",
        "pet_company": "Surfshark B.V.",
        "pet_link": "https://surfshark.com/?coupon=onedeal&transaction_id=1022baf5d013694e448d73ab95f88d&offer_id=1526&affiliate_id=2221&source=&aff_sub=15426&utm_source=Affiliates&utm_medium=2221&utm_campaign=affiliate&recurring_goal_id=1517&gad_source=1&gad_campaignid=23260470611&gbraid=0AAAAA-960t7qFCN26src6eAykclF-WVyJ&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNIyHna-1i12HOjnzoXEzA6TDB44YYo3GUoU82lcGPRDF3FGK5ynEosaAp7EEALw_wcB",
        "why_use": "Surfshark helps keep your data safe on public Wi-Fi networks by encrypting all traffic and preventing snooping, tracking, and man-in-the-middle attacks. It also allows secure browsing, streaming, and access to geo-restricted content.",
        "popularity": 4
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "ExpressVPN",
        "pet_price": "2.99$/month",
        "pet_description": "ExpressVPN is a high-security VPN service that creates an encrypted tunnel for all your internet traffic, protecting you from snooping, man-in-the-middle attacks, and IP exposure — especially useful on public Wi-Fi.",
        "pet_company": "ExpressVPN",
        "pet_link": "https://www.expressvpn.com/start/best-vpn?cq_acc=6395056203&cq_adg=187941571853&keyword=expressvpn&geo=9042871&device=&cq_src=google_ads&utm_campaign=%7Bcampaignname%7D&cq_cmp=23224358563&cq_term=expressvpn&cq_plac=&cq_net=g&cq_plt=gp&gad_source=1&gad_campaignid=23224358563&gbraid=0AAAAACmOeQpuPrxCpxNYOgnE4ofLuNHd5&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNJUaVlHrRuOvWD5_6v_fY8Hl7SWrZTJzsV08X0yQmTbDhsuMZ_4A50aAvR-EALw_wcB",
        "why_use": "On public Wi-Fi, ExpressVPN encrypts your connection with AES-256 and masks your real IP, making it very hard for attackers on the same network to spy on your data. It also offers a “Network Lock” kill switch, leak protection (DNS, IPv6), and is no-logs — ensuring that even if someone tried to track you, your traffic isn’t recorded. Additionally, its Lightway protocol is optimized for reliability and speed.",
        "popularity": 4
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Cisco AnyConnect",
        "pet_price": "€1.99 / year",
        "pet_description": "Cisco AnyConnect (Secure Mobility Client) is a corporate-grade VPN client that provides secure network access, endpoint protection, and module-based security (web security, posture, visibility) across desktop and mobile platforms.",
        "pet_company": "Cisco Systems, Inc.",
        "pet_link": "https://www.cisco.com/c/en/us/support/security/anyconnect-secure-mobility-client-v4-x/model.html",
        "why_use": "Using AnyConnect on public Wi-Fi helps establish a secure, encrypted VPN tunnel back to your company’s network, protecting sensitive data from snooping or man-in-the-middle attacks. It supports SSL and IPsec (IKEv2), and modules like Web Security lets you route web traffic via Cisco’s secure proxy.  Because licensing is based on unique users (not just concurrent), you can use it on multiple devices without buying for each session.",
        "popularity": 3
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "FPRandom or FPGuard",
        "pet_price": "Paid",
        "pet_description": "",
        "pet_company": "The Tor Project",
        "pet_link": "https://inria.hal.science/hal-01527580/document",
        "why_use": "Please refer to the literature for more information.",
        "popularity": 4
    },{
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Lockdown Privacy",
        "pet_price": "8.49$/month",
        "pet_description": "Lockdown is a privacy app that combines an on device, open-source firewall with a “Secure Tunnel” VPN. The firewall blocks trackers, ads, and malicious connections, while the VPN encrypts your connection to hide your IP and protect your data on untrusted networks.",
        "pet_company": "Celestian Golden Apps SL",
        "pet_link": "https://lockdownprivacy.com",
        "why_use": "On public Wi‑Fi, Lockdown’s Secure Tunnel VPN encrypts your traffic, preventing eavesdroppers from seeing what you're doing. At the same time, its firewall stops in-app trackers and malicious domains locally, offering a double layer of protection. It is fully audited and open source, giving strong transparency.",
        "popularity": 4
    },
    {
        "selected_concern": "Public Wi-Fi Browsing Risks",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Blokada",
        "pet_price": "Paid",
        "pet_description": "Blokada is a privacy tool that blocks ads, trackers, and malicious domains. It supports encrypted DNS (via Blokada Cloud) and, with the Plus plan, provides a full VPN (Blokada Tunnel) to encrypt all your traffic.",
        "pet_company": "Blocka AB",
        "pet_link": "https://blokada.org",
        "why_use": "When on public Wi‑Fi, upgrading to Blokada Plus gives you a real VPN tunnel via WireGuard or similar, protecting your data from snooping and ensuring that your DNS traffic is encrypted. Even without the VPN, Blokada’s DNS‑based blocking reduces your exposure to tracking and malicious sites.",
        "popularity": 3
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "Low",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Bitwarden",
        "pet_price": "4$/month",
        "pet_description": "Bitwarden is a secure, open-source password manager. It offers a fully encrypted vault for passwords, secure notes, identities, credit cards, and more. You can self-host or use their cloud, and it supports browser extensions, desktop apps, mobile apps, and CLI.",
        "pet_company": "Bitwarden Vault Buddy",
        "pet_link": "https://bitwarden.com",
        "why_use": "Bitwarden encrypts your data locally before it is ever sent to the cloud (end-to-end, zero‑knowledge), so only you can decrypt it. It's open source, so its security model can be publicly audited. :contentReference[oaicite:1]{index=1} With the premium plan, you get extra features like an integrated authenticator (TOTP), encrypted file attachments, emergency access, and more. It’s very cost-effective, especially compared to many proprietary password managers.",
        "popularity": 5
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "Low",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Proton Pass",
        "pet_price": "Free",
        "pet_description": "Proton Pass is a secure, end‑to‑end encrypted password manager from Proton. It lets you store passwords, credit cards, notes, and identities. It also supports passkeys, email aliases, and built-in 2FA, all with strong privacy protections under Swiss law.",
        "pet_company": "Proton AG",
        "pet_link": "https://proton.me/pass",
        "why_use": 'Proton Pass gives you strong encryption and a zero-knowledge model — even metadata like URLs and usernames are encrypted. With its alias feature, you can protect your identity by using a different email for each service. It’s open source and audited, giving transparency to its security. Because Proton is based in Switzerland, data is protected under very strong privacy laws. :contentReference[oaicite:3]{index=3} The paid Plus-plan adds useful features like dark‑web monitoring, emergency access, secure vault sharing, and unlimited aliases.',
        "popularity": 4
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Proton Pass",
        "pet_price": "Free",
        "pet_description": "Proton Pass is a secure, end‑to‑end encrypted password manager from Proton. It lets you store passwords, credit cards, notes, and identities. It also supports passkeys, email aliases, and built-in 2FA, all with strong privacy protections under Swiss law.",
        "pet_company": "Proton AG",
        "pet_link": "https://proton.me/pass",
        "why_use": 'Proton Pass gives you strong encryption and a zero-knowledge model — even metadata like URLs and usernames are encrypted. With its alias feature, you can protect your identity by using a different email for each service. It’s open source and audited, giving transparency to its security. Because Proton is based in Switzerland, data is protected under very strong privacy laws. :contentReference[oaicite:3]{index=3} The paid Plus-plan adds useful features like dark‑web monitoring, emergency access, secure vault sharing, and unlimited aliases.',
        "popularity": 4
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "Proton Pass",
        "pet_price": "Free",
        "pet_description": "Proton Pass is a secure, end‑to‑end encrypted password manager from Proton. It lets you store passwords, credit cards, notes, and identities. It also supports passkeys, email aliases, and built-in 2FA, all with strong privacy protections under Swiss law.",
        "pet_company": "Proton AG",
        "pet_link": "https://proton.me/pass",
        "why_use": 'Proton Pass gives you strong encryption and a zero-knowledge model — even metadata like URLs and usernames are encrypted. With its alias feature, you can protect your identity by using a different email for each service. It’s open source and audited, giving transparency to its security. Because Proton is based in Switzerland, data is protected under very strong privacy laws. :contentReference[oaicite:3]{index=3} The paid Plus-plan adds useful features like dark‑web monitoring, emergency access, secure vault sharing, and unlimited aliases.',
        "popularity": 4
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "1password",
        "pet_price": "2.99",
        "pet_description": '1Password is a mature, feature-rich password manager that provides end‑to‑end encryption, cross-device sync, secure vaults for passwords, notes, credit cards, identities, and even passkeys. It supports multiple vaults, secure sharing, and advanced security features like Travel Mode and Watchtower breach alerts.',
        "pet_company": "AgileBits, Inc.",
        "pet_link": "https://1password.com",
        "why_use": "1Password protects your data using a zero‑knowledge model: only you have the keys (your master password + a Secret Key) so even 1Password can’t decrypt your vault. Their security model uses **256-bit AES‑GCM** encryption. It also supports strong authentication (you need both the master password and the secret key), using the SRP (Secure Remote Password) protocol to avoid sending those secrets over the network.On top of that, 1Password offers features like auto‑locking, clipboard clearing, and phishing protection. For sharing, you can create shared vaults for family or team use. Their “Watchtower” alerts warn you if a site has been breached, or if you have weak or reused passwords and this check happens locally, not on their servers.",
        "popularity": 5
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Dashlane",
        "pet_price": "8$/month",
        "pet_description": 'Dashlane is a full-featured password manager with zero knowledge encryption, secure sharing, dark web monitoring, passkey support, and even a built-in VPN. It’s designed to protect and manage all your credentials, notes, and sensitive data across devices.',
        "pet_company": "Dashlane, Inc.",
        "pet_link": "https://www.dashlane.com",
        "why_use": "Dashlane encrypts everything locally using AES-256 before syncing — meaning they can’t read your data. It supports strong security features and provides a Security Dashboard to highlight weak, reused, or compromised passwords. Premium users also get dark‑web breach alerts and a VPN for safer browsing on public Wi‑Fi. For businesses, Dashlane uses confidential computing so even cloud-based operations keep user data private.",
        "popularity": 4
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Keeper",
        "pet_price": "3.97$/month",
        "pet_description": "Keeper is a zero‑knowledge password manager that stores your logins, credit cards, secure notes, and even files in a fully encrypted vault. It supports strong sharing, passkeys, 2FA, and has dark‑web monitoring via its BreachWatch add‑on.",
        "pet_company": "Keeper Security, Inc.",
        "pet_link": "https://www.keepersecurity.com",
          "why_use": "Keeper encrypts all vault data locally using AES‑256-GCM before it ever goes to their servers. The BreachWatch feature constantly scans the dark web for your credentials, alerting you if something is compromised — and it does this while preserving Keeper’s zero‑knowledge architecture. Keeper also supports passkeys, 2FA, device approval, and secure sharing with public-key cryptography. ",
        "popularity": 4
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Keeper",
        "pet_price": "3.97$/month",
        "pet_description": "Keeper is a zero‑knowledge password manager that stores your logins, credit cards, secure notes, and even files in a fully encrypted vault. It supports strong sharing, passkeys, 2FA, and has dark‑web monitoring via its BreachWatch add‑on.",
        "pet_company": "Keeper Security, Inc.",
        "pet_link": "https://www.keepersecurity.com",
          "why_use": "Keeper encrypts all vault data locally using AES‑256-GCM before it ever goes to their servers. The BreachWatch feature constantly scans the dark web for your credentials, alerting you if something is compromised — and it does this while preserving Keeper’s zero‑knowledge architecture. Keeper also supports passkeys, 2FA, device approval, and secure sharing with public-key cryptography. ",
        "popularity": 4
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "LastPass",
        "pet_price": "Free",
        "pet_description": "LastPass is a widely‑used password manager that provides a secure, encrypted vault to store passwords, secure notes, and form data. It supports syncing across devices, automatic form filling, secure password sharing, and dark‑web monitoring (depending on plan).",
        "pet_company": "LastPass",
        "pet_link": "https://www.lastpass.com/?cp=LP2025-11-50P-A&utm_source=google&utm_medium=cpc&utm_campaign=21421183099&utm_term=lastpass&utm_content=164416837576&gad_source=1&gad_campaignid=21421183099&gbraid=0AAAAADhAijfq29BUeIu7et2Nw9Y-E8eDu&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNLCKmbd1q30TQZ53GymAo1jDCtfNb2OI4wWTD3d7OGEm78hotUUarQaAlXrEALw_wcB",
        "why_use": "LastPass uses a **zero-knowledge** model: only you can decrypt your vault because encryption happens locally on your device. The Premium plan gives you features like emergency access, 1 GB encrypted file storage, and advanced multi-factor authentication. ",
        "popularity": 4
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "LastPass",
        "pet_price": "Free",
        "pet_description": "LastPass is a widely‑used password manager that provides a secure, encrypted vault to store passwords, secure notes, and form data. It supports syncing across devices, automatic form filling, secure password sharing, and dark‑web monitoring (depending on plan).",
        "pet_company": "LastPass",
        "pet_link": "https://www.lastpass.com/?cp=LP2025-11-50P-A&utm_source=google&utm_medium=cpc&utm_campaign=21421183099&utm_term=lastpass&utm_content=164416837576&gad_source=1&gad_campaignid=21421183099&gbraid=0AAAAADhAijfq29BUeIu7et2Nw9Y-E8eDu&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNLCKmbd1q30TQZ53GymAo1jDCtfNb2OI4wWTD3d7OGEm78hotUUarQaAlXrEALw_wcB",
        "why_use": "LastPass uses a **zero-knowledge** model: only you can decrypt your vault because encryption happens locally on your device.  The Premium plan gives you features like emergency access, 1 GB encrypted file storage, and advanced multi-factor authentication. ",
        "popularity": 4
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "StrongBox",
        "pet_price": "2.99$/month",
        "pet_description": "Strongbox is a highly secure KeePass / Password Safe compatible password manager for iPhone, iPad, and Mac. It supports local or cloud‑stored databases, hardware tokens like YubiKey, duress PINs, passkeys, 2FA codes, and more.",
        "pet_company": "LastPass",
        "pet_link": 'https://strongboxsafe.com',
        "why_use": "With Strongbox, your password database is just a file (KeePass `.kdbx` or Password Safe), so **you control where it’s stored** — your own local device, iCloud, Dropbox, SFTP, WebDAV, etc. :contentReference[oaicite:1]{index=1} It supports strong cryptography (AES, TwoFish, ChaCha20) and modern KDFs (Argon2) to protect against brute‑force. :contentReference[oaicite:2]{index=2} It’s very flexible and doesn’t lock you into a proprietary cloud or subscription model unless you choose Pro. :contentReference[oaicite:3]{index=3}",
        "popularity": 3
    },
    {
        "selected_concern": "Location Tracking",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Lockdown Privacy",
        "pet_price": "8.49$/month",
        "pet_description": "Lockdown is a privacy app that combines an on device, open-source firewall with a “Secure Tunnel” VPN. The firewall blocks trackers, ads, and malicious connections, while the VPN encrypts your connection to hide your IP and protect your data on untrusted networks.",
        "pet_company": "Celestian Golden Apps SL",
        "pet_link": "https://lockdownprivacy.com",
        "why_use": "On public Wi‑Fi, Lockdown’s Secure Tunnel VPN encrypts your traffic, preventing eavesdroppers from seeing what you're doing. At the same time, its firewall stops in-app trackers and malicious domains locally, offering a double layer of protection. It is fully audited and open source, giving strong transparency.",
        "popularity": 4
    },
    {
        "selected_concern": "Location Tracking",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "Lockdown Privacy",
        "pet_price": "8.49$/month",
        "pet_description": "Lockdown is a privacy app that combines an on device, open-source firewall with a “Secure Tunnel” VPN. The firewall blocks trackers, ads, and malicious connections, while the VPN encrypts your connection to hide your IP and protect your data on untrusted networks.",
        "pet_company": "Celestian Golden Apps SL",
        "pet_link": "https://lockdownprivacy.com",
        "why_use": "On public Wi‑Fi, Lockdown’s Secure Tunnel VPN encrypts your traffic, preventing eavesdroppers from seeing what you're doing. At the same time, its firewall stops in-app trackers and malicious domains locally, offering a double layer of protection. It is fully audited and open source, giving strong transparency.",
        "popularity": 4
    },
    {
        "selected_concern": "Location Tracking",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "Guardian firewall",
        "pet_price": "9.99$/month",
        "pet_description": "Guardian Firewall is a privacy app that combines a smart firewall with a VPN. It filters out trackers (location, mail, data) using its firewall, while sending all internet traffic through an encrypted VPN tunnel to mask your IP and identity.",
        "pet_company": "Guardian Team",
        "pet_link": "https://guardianapp.com",
        "why_use": "Guardian protects your online activity by blocking tracker connections *before* they leave apps or web pages. Its VPN encrypts everything, and your IP is masked with a randomly generated identity without needing to register or provide personal info.It also supports DNS leak protection and can use DNSFilter resolvers for added safety.",
        "popularity": 4
    },
    {
        "selected_concern": "Location Tracking",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Guardian firewall",
        "pet_price": "9.99$/month",
        "pet_description": "Guardian Firewall is a privacy app that combines a smart firewall with a VPN. It filters out trackers (location, mail, data) using its firewall, while sending all internet traffic through an encrypted VPN tunnel to mask your IP and identity.",
        "pet_company": "Guardian Team",
        "pet_link": "https://guardianapp.com",
        "why_use": "Guardian protects your online activity by blocking tracker connections *before* they leave apps or web pages. Its VPN encrypts everything, and your IP is masked with a randomly generated identity without needing to register or provide personal info. It also supports DNS leak protection and can use DNSFilter resolvers for added safety.",
        "popularity": 4
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "SimpleLogin",
        "pet_price": "Free",
        "pet_description": "SimpleLogin is an open‑source email‑alias service. It lets you create different email addresses that forward to your real inbox, so you can mask your identity, reduce spam, and protect your real address. Aliases can receive and send mail, and you can use your own domain with the paid plan.",
        "pet_company": "Guardian Team",
        "pet_link": "https://simplelogin.io/pricing/",
        "why_use": "By using aliases instead of your real email, you reduce the risk of spam, phishing, and cross‑site tracking. SimpleLogin lets you reply from the alias so your true inbox stays hidden. It’s open source, supports PGP encryption, and can even be self-hosted. It also supports 2FA (TOTP / WebAuthn) for account security.",
        "popularity": 3
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "SimpleLogin",
        "pet_price": "Free",
        "pet_description": "SimpleLogin is an open‑source email‑alias service. It lets you create different email addresses that forward to your real inbox, so you can mask your identity, reduce spam, and protect your real address. Aliases can receive and send mail, and you can use your own domain with the paid plan.",
        "pet_company": "Guardian Team",
        "pet_link": "https://simplelogin.io/pricing/",
        "why_use": "By using aliases instead of your real email, you reduce the risk of spam, phishing, and cross‑site tracking. SimpleLogin lets you reply from the alias so your true inbox stays hidden. It’s open source, supports PGP encryption, and can even be self-hosted. It also supports 2FA for account security.",
        "popularity": 3
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "AdGuard",
        "pet_price": "Paid",
        "pet_description": "AdGuard is a privacy tool that blocks ads and trackers at different levels — app‑level, browser‑level, or DNS‑level. It provides system‑wide ad filtering, DNS privacy, firewall-like control on apps (on mobile), and even malicious‑site blocking.",
        "pet_company": "AdGuard Software Limited",
        "pet_link": "https://adguard.com/en/welcome.html",
        "why_use": "With AdGuard, you block ads not just in browsers but in *apps* as well. Its DNS‑filtering features (using encrypted DNS) let you block unwanted domains before they even resolve. On Android, it has a firewall to control which apps can access the internet. Plus, it protects you from phishing and malicious sites. ",
        "popularity": 4
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "AdGuard",
        "pet_price": "Paid",
        "pet_description": "AdGuard is a privacy tool that blocks ads and trackers at different levels — app‑level, browser‑level, or DNS‑level. It provides system‑wide ad filtering, DNS privacy, firewall-like control on apps (on mobile), and even malicious‑site blocking.",
        "pet_company": "AdGuard Software Limited",
        "pet_link": "https://adguard.com/en/welcome.html",
        "why_use": "With AdGuard, you block ads not just in browsers but in *apps* as well. Its DNS‑filtering features (using encrypted DNS) let you block unwanted domains before they even resolve. On Android, it has a firewall to control which apps can access the internet. Plus, it protects you from phishing and malicious sites. ",
        "popularity": 4
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "AdGuard",
        "pet_price": "Paid",
        "pet_description": "AdGuard is a privacy tool that blocks ads and trackers at different levels — app‑level, browser‑level, or DNS‑level. It provides system‑wide ad filtering, DNS privacy, firewall-like control on apps (on mobile), and even malicious‑site blocking.",
        "pet_company": "AdGuard Software Limited",
        "pet_link": "https://adguard.com/en/welcome.html",
        "why_use": "With AdGuard, you block ads not just in browsers but in *apps* as well. Its DNS‑filtering features (using encrypted DNS) let you block unwanted domains before they even resolve. On Android, it has a firewall to control which apps can access the internet. Plus, it protects you from phishing and malicious sites. ",
        "popularity": 4
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "SimpleLogin",
        "pet_price": "Free",
        "pet_description": "SimpleLogin is an open‑source email‑alias service. It lets you create different email addresses (“aliases”) that forward to your real inbox, so you can mask your identity, reduce spam, and protect your real address. Aliases can receive and send mail, and you can use your own domain with the paid plan.",
        "pet_company": "Guardian Team",
        "pet_link": "https://simplelogin.io/pricing/",
        "why_use": "By using aliases instead of your real email, you reduce the risk of spam, phishing, and cross‑site tracking. SimpleLogin lets you reply from the alias so your true inbox stays hidden. It’s open source, supports PGP encryption, and can even be self-hosted. It also supports 2FA (TOTP / WebAuthn) for account security.",
        "popularity": 3
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Cryptomator",
        "pet_price": "Free",
        "pet_description": "Cryptomator is a client‑side encryption tool that lets you create encrypted “vaults” for your files. You can then sync these vaults with any cloud service (Dropbox, OneDrive, Google Drive, etc.) without risking unencrypted data being exposed.",
        "pet_company": "Skymatic GmbH",
        "pet_link": "https://cryptomator.org/pricing/#for-individuals",
          "why_use": "With Cryptomator, all encryption happens on your device before files go to the cloud. It encrypts both file contents *and* filenames using AES-256, so even your cloud provider can’t read anything. It’s fully open source, so its security can be audited.",
        "popularity": 4
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Cryptomator",
        "pet_price": "Free",
        "pet_description": "Cryptomator is a client‑side encryption tool that lets you create encrypted “vaults” for your files. You can then sync these vaults with any cloud service (Dropbox, OneDrive, Google Drive, etc.) without risking unencrypted data being exposed.",
        "pet_company": "Skymatic GmbH",
        "pet_link": "https://cryptomator.org/pricing/#for-individuals",
          "why_use": "With Cryptomator, all encryption happens on your device before files go to the cloud. It encrypts both file contents *and* filenames using AES-256, so even your cloud provider can’t read anything. It’s fully open source, so its security can be audited.",
        "popularity": 4
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "Signal",
        "pet_price": "$6.99/month",
        "pet_description": "Signal is a non‑profit, open‑source messaging app that provides end‑to‑end encryption for texts, voice calls, video calls, and file sharing. It’s designed for maximal privacy: even Signal’s servers can’t read your messages.",
        "pet_company": "Signal Technology Foundation",
        "pet_link": "https://www.cloudsecure.com/cloudshield",
        "logo_link": "assets/logos/wifisafe.png",
        "why_use": "Signal uses the Signal Protocol — a strong, peer-reviewed cryptographic protocol — to encrypt everything by default. It minimizes metadata collection, supports features like disappearing messages, sealed sender (hides who is sending), and is developed by a non‑profit. It’s widely trusted by security professionals.",
        "popularity": 4
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Signal",
        "pet_price": "$6.99/month",
        "pet_description": "Signal is a non‑profit, open‑source messaging app that provides end‑to‑end encryption for texts, voice calls, video calls, and file sharing. It’s designed for maximal privacy: even Signal’s servers can’t read your messages.",
        "pet_company": "Signal Technology Foundation",
        "pet_link": "https://www.cloudsecure.com/cloudshield",
        "logo_link": "assets/logos/wifisafe.png",
        "why_use": "Signal uses the Signal Protocol — a strong, peer-reviewed cryptographic protocol — to encrypt everything by default. It minimizes metadata collection, supports features like disappearing messages, sealed sender (hides who is sending), and is developed by a non‑profit. It’s widely trusted by security professionals.",
        "popularity": 4
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Mullvad",
        "pet_price": "5$/month",
        "pet_description": "With Mullvad VPN, your traffic travels through an encrypted tunnel to one of our VPN servers and then onward to the website you are visiting. In this way, websites will only see our server’s identity instead of yours. Same goes for your ISP (internet service provider); they’ll see that you’re connected to Mullvad, but not your activity. ",
        "pet_company": "Mullvad VPN AB",
        "pet_link": "https://mullvad.net/en",
        "logo_link": "assets/logos/wifisafe.png",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 3
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Hidden Background Activity",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Malicious or Scam Apps",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "Bitwarden",
        "pet_price": "4$/month",
        "pet_description": "Bitwarden is a secure, open-source password manager. It offers a fully encrypted vault for passwords, secure notes, identities, credit cards, and more. You can self-host or use their cloud, and it supports browser extensions, desktop apps, mobile apps, and CLI.",
        "pet_company": "Bitwarden Vault Buddy",
        "pet_link": "https://bitwarden.com",
        "why_use": "Bitwarden encrypts your data locally before it is ever sent to the cloud (end-to-end, zero‑knowledge), so only you can decrypt it. It's open source, so its security model can be publicly audited. :contentReference[oaicite:1]{index=1} With the premium plan, you get extra features like an integrated authenticator (TOTP), encrypted file attachments, emergency access, and more. It’s very cost-effective, especially compared to many proprietary password managers.",
        "popularity": 5
    },
    {
        "selected_concern": "Malicious or Scam Apps",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Bitwarden",
        "pet_price": "4$/month",
        "pet_description": "Bitwarden is a secure, open-source password manager. It offers a fully encrypted vault for passwords, secure notes, identities, credit cards, and more. You can self-host or use their cloud, and it supports browser extensions, desktop apps, mobile apps, and CLI.",
        "pet_company": "Bitwarden Vault Buddy",
        "pet_link": "https://bitwarden.com",
        "why_use": "Bitwarden encrypts your data locally before it is ever sent to the cloud (end-to-end, zero‑knowledge), so only you can decrypt it. It's open source, so its security model can be publicly audited. :contentReference[oaicite:1]{index=1} With the premium plan, you get extra features like an integrated authenticator (TOTP), encrypted file attachments, emergency access, and more. It’s very cost-effective, especially compared to many proprietary password managers.",
        "popularity": 5
    },
    {
        "selected_concern": "Malicious or Scam Apps",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Blokada",
        "pet_price": "Paid",
        "pet_description": "Blokada is a privacy tool that blocks ads, trackers, and malicious domains. It supports encrypted DNS (via Blokada Cloud) and, with the Plus plan, provides a full VPN (Blokada Tunnel) to encrypt all your traffic.",
        "pet_company": "Blocka AB",
        "pet_link": "https://blokada.org",
        "why_use": "When on public Wi‑Fi, upgrading to Blokada Plus gives you a real VPN tunnel via WireGuard or similar, protecting your data from snooping and ensuring that your DNS traffic is encrypted. Even without the VPN, Blokada’s DNS‑based blocking reduces your exposure to tracking and malicious sites.",
        "popularity": 3
    },
    {
        "selected_concern": "Malicious or Scam Apps",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Cryptomator",
        "pet_price": "Free",
        "pet_description": "Cryptomator is a client‑side encryption tool that lets you create encrypted “vaults” for your files. You can then sync these vaults with any cloud service (Dropbox, OneDrive, Google Drive, etc.) without risking unencrypted data being exposed.",
        "pet_company": "Skymatic GmbH",
        "pet_link": "https://cryptomator.org/pricing/#for-individuals",
          "why_use": "With Cryptomator, all encryption happens on your device before files go to the cloud. It encrypts both file contents *and* filenames using AES-256, so even your cloud provider can’t read anything. It’s fully open source, so its security can be audited.",
        "popularity": 4
    },
    {
        "selected_concern": "Malicious or Scam Apps",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "AdGuard",
        "pet_price": "Paid",
        "pet_description": "AdGuard is a privacy tool that blocks ads and trackers at different levels — app‑level, browser‑level, or DNS‑level. It provides system‑wide ad filtering, DNS privacy, firewall-like control on apps (on mobile), and even malicious‑site blocking.",
        "pet_company": "AdGuard Software Limited",
        "pet_link": "https://adguard.com/en/welcome.html",
        "why_use": "With AdGuard, you block ads not just in browsers but in *apps* as well. Its DNS‑filtering features (using encrypted DNS) let you block unwanted domains before they even resolve. On Android, it has a firewall to control which apps can access the internet. Plus, it protects you from phishing and malicious sites. ",
        "popularity": 4
    },
    {
        "selected_concern": "Malicious or Scam Apps",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "AdGuard",
        "pet_price": "Paid",
        "pet_description": "AdGuard is a privacy tool that blocks ads and trackers at different levels — app‑level, browser‑level, or DNS‑level. It provides system‑wide ad filtering, DNS privacy, firewall-like control on apps (on mobile), and even malicious‑site blocking.",
        "pet_company": "AdGuard Software Limited",
        "pet_link": "https://adguard.com/en/welcome.html",
        "why_use": "With AdGuard, you block ads not just in browsers but in *apps* as well. Its DNS‑filtering features (using encrypted DNS) let you block unwanted domains before they even resolve. On Android, it has a firewall to control which apps can access the internet. Plus, it protects you from phishing and malicious sites. ",
        "popularity": 4
    },
    {
        "selected_concern": "Malicious or Scam Apps",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Signal",
        "pet_price": "$6.99/month",
        "pet_description": "Signal is a non‑profit, open‑source messaging app that provides end‑to‑end encryption for texts, voice calls, video calls, and file sharing. It’s designed for maximal privacy: even Signal’s servers can’t read your messages.",
        "pet_company": "Signal Technology Foundation",
        "pet_link": "https://www.cloudsecure.com/cloudshield",
        "logo_link": "assets/logos/wifisafe.png",
        "why_use": "Signal uses the Signal Protocol — a strong, peer-reviewed cryptographic protocol — to encrypt everything by default. It minimizes metadata collection, supports features like disappearing messages, sealed sender (hides who is sending), and is developed by a non‑profit. It’s widely trusted by security professionals.",
        "popularity": 4
    },
    {
        "selected_concern": "Malicious or Scam Apps",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Malicious or Scam Apps",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Unprotected File Sharing Links",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "SimpleLogin",
        "pet_price": "Free",
        "pet_description": "SimpleLogin is an open‑source email‑alias service. It lets you create different email addresses that forward to your real inbox, so you can mask your identity, reduce spam, and protect your real address. Aliases can receive and send mail, and you can use your own domain with the paid plan.",
        "pet_company": "Guardian Team",
        "pet_link": "https://simplelogin.io/pricing/",
        "why_use": "By using aliases instead of your real email, you reduce the risk of spam, phishing, and cross‑site tracking. SimpleLogin lets you reply from the alias so your true inbox stays hidden. It’s open source, supports PGP encryption, and can even be self-hosted. It also supports 2FA (TOTP / WebAuthn) for account security.",
        "popularity": 3
    },
    {
        "selected_concern": "Unprotected File Sharing Links",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "SimpleLogin",
        "pet_price": "Free",
        "pet_description": "SimpleLogin is an open‑source email‑alias service. It lets you create different email addresses that forward to your real inbox, so you can mask your identity, reduce spam, and protect your real address. Aliases can receive and send mail, and you can use your own domain with the paid plan.",
        "pet_company": "Guardian Team",
        "pet_link": "https://simplelogin.io/pricing/",
        "why_use": "By using aliases instead of your real email, you reduce the risk of spam, phishing, and cross‑site tracking. SimpleLogin lets you reply from the alias so your true inbox stays hidden. It’s open source, supports PGP encryption, and can even be self-hosted. It also supports 2FA (TOTP / WebAuthn) for account security.",
        "popularity": 3
    },
    {
        "selected_concern": "Unprotected File Sharing Links",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Cryptomator",
        "pet_price": "Free",
        "pet_description": "Cryptomator is a client‑side encryption tool that lets you create encrypted “vaults” for your files. You can then sync these vaults with any cloud service (Dropbox, OneDrive, Google Drive, etc.) without risking unencrypted data being exposed.",
        "pet_company": "Skymatic GmbH",
        "pet_link": "https://cryptomator.org/pricing/#for-individuals",
          "why_use": "With Cryptomator, all encryption happens on your device before files go to the cloud. It encrypts both file contents and filenames using AES-256, so even your cloud provider can’t read anything. It’s fully open source, so its security can be audited.",
        "popularity": 4
    },
    {
        "selected_concern": "Unprotected File Sharing Links",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Cryptomator",
        "pet_price": "Free",
        "pet_description": "Cryptomator is a client‑side encryption tool that lets you create encrypted “vaults” for your files. You can then sync these vaults with any cloud service (Dropbox, OneDrive, Google Drive, etc.) without risking unencrypted data being exposed.",
        "pet_company": "Skymatic GmbH",
        "pet_link": "https://cryptomator.org/pricing/#for-individuals",
          "why_use": "With Cryptomator, all encryption happens on your device before files go to the cloud. It encrypts both file contents and filenames using AES-256, so even your cloud provider can’t read anything. It’s fully open source, so its security can be audited.",
        "popularity": 4
    },
    {
        "selected_concern": "Unprotected File Sharing Links",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Boxcryptor",
        "pet_price": "Free",
        "pet_description": "Boxcryptor is a client‑side encryption tool that encrypts your files locally before they go to cloud storage services like Dropbox, Google Drive, OneDrive, and more. It gives you end‑to‑‑end, zero‑knowledge encryption so that even your cloud provider can’t read your data.",
        "pet_company": "Secomba GmbH",
        "pet_link": "https://wf.boxcryptor.com",
        "why_use": "With Boxcryptor, all your cloud‑stored files are encrypted on your device using strong encryption  before being uploaded. You maintain control of your keys, so the cloud provider never has access to unencrypted data. It supports many major cloud services and allows sharing of encrypted files safely. ",
        "popularity": 3
    },
    {
        "selected_concern": "Unprotected File Sharing Links",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "Boxcryptor",
        "pet_price": "Free",
        "pet_description": "Boxcryptor is a client‑side encryption tool that encrypts your files locally before they go to cloud storage services like Dropbox, Google Drive, OneDrive, and more. It gives you end‑to‑‑end, zero‑knowledge encryption so that even your cloud provider can’t read your data.",
        "pet_company": "Secomba GmbH",
        "pet_link": "https://wf.boxcryptor.com",
        "why_use": "With Boxcryptor, all your cloud‑stored files are encrypted on your device using strong encryption (e.g. AES‑256) before being uploaded. You maintain control of your keys, so the cloud provider never has access to unencrypted data. It supports many major cloud services and allows sharing of encrypted files safely.",
        "popularity": 3
    },
    {
        "selected_concern": "Unprotected File Sharing Links",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Tresorit",
        "pet_price": "Free",
        "pet_description": "Tresorit is a highly secure, zero‑knowledge cloud storage and collaboration platform. Files are encrypted on your device before upload, and only you (and people you explicitly share with) can decrypt them. It supports secure sharing, versioning, and collaboration in encrypted ‘tresors’.",
        "pet_company": "Secomba GmbH",
        "pet_link": "https://tresorit.com/de?gad_source=1&gad_campaignid=21618907595&gbraid=0AAAAACUlux-2uR66nAVqUcxRGBnA382uG&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNIocAtTk07eWtz1VD9nd11jzHYyxXloPOlVkAlq3e3CAkIKduvnZ1caAgyeEALw_wcB",
        "why_use": "Tresorit provides **client‑side end-to-end encryption**, meaning no unencrypted data or keys are ever sent to their servers.  It uses strong cryptographic algorithms  and ensures integrity with HMACs.  Tresorit is under Swiss jurisdiction (strong privacy laws), supports compliance (ISO 27001, GDPR, HIPAA), and lets you choose data residency in the EU or Switzerland. ",
        "popularity": 4
    },
    {
        "selected_concern": "Unprotected File Sharing Links",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Tresorit",
        "pet_price": "Free",
        "pet_description": "Tresorit is a highly secure, zero‑knowledge cloud storage and collaboration platform. Files are encrypted on your device before upload, and only you (and people you explicitly share with) can decrypt them. It supports secure sharing, versioning, and collaboration in encrypted ‘tresors’.",
        "pet_company": "Secomba GmbH",
        "pet_link": "https://tresorit.com/de?gad_source=1&gad_campaignid=21618907595&gbraid=0AAAAACUlux-2uR66nAVqUcxRGBnA382uG&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNIocAtTk07eWtz1VD9nd11jzHYyxXloPOlVkAlq3e3CAkIKduvnZ1caAgyeEALw_wcB",
        "why_use": "Tresorit provides **client‑side end-to-end encryption**, meaning no unencrypted data or keys are ever sent to their servers. It uses strong cryptographic algorithms and ensures integrity with HMACs.  Tresorit is under Swiss jurisdiction (strong privacy laws), supports compliance (ISO 27001, GDPR, HIPAA), and lets you choose data residency in the EU or Switzerland. ",
        "popularity": 4
    },
    {
        "selected_concern": "Unprotected File Sharing Links",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Microsoft purview DLP",
        "pet_price": "11,20$/month",
        "pet_description": "Microsoft Purview DLP is a cloud-native solution to detect, monitor, and prevent accidental or malicious exposure of sensitive data across endpoints, cloud apps, and Microsoft 365 workloads. It integrates with labels and classification to enforce rules on email, Teams, SharePoint, OneDrive, and local devices.",
        "pet_company": "Microsoft",
        "pet_link": "https://www.microsoft.com/de-de/security/business/information-protection/microsoft-purview-data-loss-prevention?market=de",
        "why_use": "Purview DLP allows organizations to enforce policies that protect sensitive information, prevent data leaks, and ensure compliance. It supports endpoint DLP, policy enforcement in cloud apps, classification integration, and adaptive/risk-based controls. Alerts and logs are centralized for auditing and investigation, and policies can block, warn, or encrypt data according to rules.",
        "popularity": 4
    },
    {
        "selected_concern": "Unprotected File Sharing Links",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Microsoft purview DLP",
        "pet_price": "11,20$/month",
        "pet_description": "Microsoft Purview DLP is a cloud-native solution to detect, monitor, and prevent accidental or malicious exposure of sensitive data across endpoints, cloud apps, and Microsoft 365 workloads. It integrates with labels and classification to enforce rules on email, Teams, SharePoint, OneDrive, and local devices.",
        "pet_company": "Microsoft",
        "pet_link": "https://www.microsoft.com/de-de/security/business/information-protection/microsoft-purview-data-loss-prevention?market=de",
        "why_use": "Purview DLP allows organizations to enforce policies that protect sensitive information, prevent data leaks, and ensure compliance. It supports endpoint DLP, policy enforcement in cloud apps, classification integration, and adaptive/risk-based controls. Alerts and logs are centralized for auditing and investigation, and policies can block, warn, or encrypt data according to rules.",
        "popularity": 4
    },
    {
        "selected_concern": "Weak or Shared Passwords",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "SimpleLogin",
        "pet_price": "Free",
        "pet_description": "SimpleLogin is an open‑source email‑alias service. It lets you create different email addresses that forward to your real inbox, so you can mask your identity, reduce spam, and protect your real address. Aliases can receive and send mail, and you can use your own domain with the paid plan.",
        "pet_company": "Guardian Team",
        "pet_link": "https://simplelogin.io/pricing/",
        "why_use": "By using aliases instead of your real email, you reduce the risk of spam, phishing, and cross‑site tracking. SimpleLogin lets you reply from the alias so your true inbox stays hidden. It’s open source, supports PGP encryption, and can even be self-hosted. It also supports 2FA (TOTP / WebAuthn) for account security.",
        "popularity": 3
    },
    {
        "selected_concern": "Weak or Shared Passwords",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "SimpleLogin",
        "pet_price": "Free",
        "pet_description": "SimpleLogin is an open‑source email‑alias service. It lets you create different email addresses that forward to your real inbox, so you can mask your identity, reduce spam, and protect your real address. Aliases can receive and send mail, and you can use your own domain with the paid plan.",
        "pet_company": "Guardian Team",
        "pet_link": "https://simplelogin.io/pricing/",
        "why_use": "By using aliases instead of your real email, you reduce the risk of spam, phishing, and cross‑site tracking. SimpleLogin lets you reply from the alias so your true inbox stays hidden. It’s open source, supports PGP encryption, and can even be self-hosted. It also supports 2FA (TOTP / WebAuthn) for account security.",
        "popularity": 3
    },
    {
        "selected_concern": "Weak or Shared Passwords",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Bitwarden",
        "pet_price": "4$/month",
        "pet_description": "Bitwarden is a secure, open-source password manager. It offers a fully encrypted vault for passwords, secure notes, identities, credit cards, and more. You can self-host or use their cloud, and it supports browser extensions, desktop apps, mobile apps, and CLI.",
        "pet_company": "Bitwarden Vault Buddy",
        "pet_link": "https://bitwarden.com",
        "why_use": "Bitwarden encrypts your data locally before it is ever sent to the cloud (end-to-end, zero‑knowledge), so only you can decrypt it. It's open source, so its security model can be publicly audited. :contentReference[oaicite:1]{index=1} With the premium plan, you get extra features like an integrated authenticator (TOTP), encrypted file attachments, emergency access, and more. It’s very cost-effective, especially compared to many proprietary password managers.",
        "popularity": 5
    },
    {
        "selected_concern": "Weak or Shared Passwords",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Bitwarden",
        "pet_price": "4$/month",
        "pet_description": "Bitwarden is a secure, open-source password manager. It offers a fully encrypted vault for passwords, secure notes, identities, credit cards, and more. You can self-host or use their cloud, and it supports browser extensions, desktop apps, mobile apps, and CLI.",
        "pet_company": "Bitwarden Vault Buddy",
        "pet_link": "https://bitwarden.com",
        "why_use": "Bitwarden encrypts your data locally before it is ever sent to the cloud (end-to-end, zero‑knowledge), so only you can decrypt it. It's open source, so its security model can be publicly audited. :contentReference[oaicite:1]{index=1} With the premium plan, you get extra features like an integrated authenticator (TOTP), encrypted file attachments, emergency access, and more. It’s very cost-effective, especially compared to many proprietary password managers.",
        "popularity": 5
    },
    {
        "selected_concern": "Weak or Shared Passwords",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "LastPass",
        "pet_price": "Free",
        "pet_description": "LastPass is a widely‑used password manager that provides a secure, encrypted vault to store passwords, secure notes, and form data. It supports syncing across devices, automatic form filling, secure password sharing, and dark‑web monitoring (depending on plan).",
        "pet_company": "LastPass",
        "pet_link": "https://www.lastpass.com/?cp=LP2025-11-50P-A&utm_source=google&utm_medium=cpc&utm_campaign=21421183099&utm_term=lastpass&utm_content=164416837576&gad_source=1&gad_campaignid=21421183099&gbraid=0AAAAADhAijfq29BUeIu7et2Nw9Y-E8eDu&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNLCKmbd1q30TQZ53GymAo1jDCtfNb2OI4wWTD3d7OGEm78hotUUarQaAlXrEALw_wcB",
        "why_use": "LastPass uses a **zero-knowledge** model: only you can decrypt your vault because encryption happens locally on your device. The Premium plan gives you features like emergency access, 1 GB encrypted file storage, and advanced multi-factor authentication. ",
        "popularity": 4
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "1password",
        "pet_price": "2.99",
        "pet_description": '1Password is a mature, feature-rich password manager that provides end‑to‑end encryption, cross-device sync, secure vaults for passwords, notes, credit cards, identities, and even passkeys. It supports multiple vaults, secure sharing, and advanced security features like Travel Mode and Watchtower breach alerts.',
        "pet_company": "AgileBits, Inc.",
        "pet_link": "https://1password.com",
        "why_use": "1Password protects your data using a zero‑knowledge model: only you have the keys (your master password + a Secret Key) so even 1Password can’t decrypt your vault. Their security model uses **256-bit AES‑GCM** encryption. It also supports strong authentication (you need both the master password and the secret key), using the SRP (Secure Remote Password) protocol to avoid sending those secrets over the network.On top of that, 1Password offers features like auto‑locking, clipboard clearing, and phishing protection. For sharing, you can create shared vaults for family or team use. Their “Watchtower” alerts warn you if a site has been breached, or if you have weak or reused passwords and this check happens locally, not on their servers.",
        "popularity": 5
    },
    {
        "selected_concern": "Auto-Saved Passwords & Autofill Data",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Dashlane",
        "pet_price": "8$/month",
        "pet_description": 'Dashlane is a full-featured password manager with zero knowledge encryption, secure sharing, dark web monitoring, passkey support, and even a built-in VPN. It’s designed to protect and manage all your credentials, notes, and sensitive data across devices.',
        "pet_company": "Dashlane, Inc.",
        "pet_link": "https://www.dashlane.com",
        "why_use": "Dashlane encrypts everything locally using AES-256 before syncing — meaning they can’t read your data. It supports strong security features and provides a Security Dashboard to highlight weak, reused, or compromised passwords. Premium users also get dark‑web breach alerts and a VPN for safer browsing on public Wi‑Fi. For businesses, Dashlane uses confidential computing so even cloud-based operations keep user data private.",
        "popularity": 4
    },
    {
        "selected_concern": "Automatic Photo Backup Without Consent",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Cryptomator",
        "pet_price": "Free",
        "pet_description": "Cryptomator is a client‑side encryption tool that lets you create encrypted “vaults” for your files. You can then sync these vaults with any cloud service (Dropbox, OneDrive, Google Drive, etc.) without risking unencrypted data being exposed.",
        "pet_company": "Skymatic GmbH",
        "pet_link": "https://cryptomator.org/pricing/#for-individuals",
          "why_use": "With Cryptomator, all encryption happens on your device before files go to the cloud. It encrypts both file contents and filenames using AES-256, so even your cloud provider can’t read anything. It’s fully open source, so its security can be audited.",
        "popularity": 4
    },
    {
        "selected_concern": "Automatic Photo Backup Without Consent",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Cryptomator",
        "pet_price": "Free",
        "pet_description": "Cryptomator is a client‑side encryption tool that lets you create encrypted “vaults” for your files. You can then sync these vaults with any cloud service (Dropbox, OneDrive, Google Drive, etc.) without risking unencrypted data being exposed.",
        "pet_company": "Skymatic GmbH",
        "pet_link": "https://cryptomator.org/pricing/#for-individuals",
          "why_use": "With Cryptomator, all encryption happens on your device before files go to the cloud. It encrypts both file contents and filenames using AES-256, so even your cloud provider can’t read anything. It’s fully open source, so its security can be audited.",
        "popularity": 4
    },
    {
        "selected_concern": "Automatic Photo Backup Without Consent",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Tresorit",
        "pet_price": "Free",
        "pet_description": "Tresorit is a highly secure, zero‑knowledge cloud storage and collaboration platform. Files are encrypted on your device before upload, and only you (and people you explicitly share with) can decrypt them. It supports secure sharing, versioning, and collaboration in encrypted ‘tresors’.",
        "pet_company": "Secomba GmbH",
        "pet_link": "https://tresorit.com/de?gad_source=1&gad_campaignid=21618907595&gbraid=0AAAAACUlux-2uR66nAVqUcxRGBnA382uG&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNIocAtTk07eWtz1VD9nd11jzHYyxXloPOlVkAlq3e3CAkIKduvnZ1caAgyeEALw_wcB",
        "why_use": "Tresorit provides client‑side end-to-end encryption, meaning no unencrypted data or keys are ever sent to their servers. It uses strong cryptographic algorithms and ensures integrity with HMACs.  Tresorit is under Swiss jurisdiction (strong privacy laws), supports compliance (ISO 27001, GDPR, HIPAA), and lets you choose data residency in the EU or Switzerland. ",
        "popularity": 4
    },
    {
        "selected_concern": "Automatic Photo Backup Without Consent",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Tresorit",
        "pet_price": "Free",
        "pet_description": "Tresorit is a highly secure, zero‑knowledge cloud storage and collaboration platform. Files are encrypted on your device before upload, and only you (and people you explicitly share with) can decrypt them. It supports secure sharing, versioning, and collaboration in encrypted ‘tresors’.",
        "pet_company": "Secomba GmbH",
        "pet_link": "https://tresorit.com/de?gad_source=1&gad_campaignid=21618907595&gbraid=0AAAAACUlux-2uR66nAVqUcxRGBnA382uG&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNIocAtTk07eWtz1VD9nd11jzHYyxXloPOlVkAlq3e3CAkIKduvnZ1caAgyeEALw_wcB",
        "why_use": "Tresorit provides client‑side end-to-end encryption, meaning no unencrypted data or keys are ever sent to their servers. It uses strong cryptographic algorithms and ensures integrity with HMACs.  Tresorit is under Swiss jurisdiction (strong privacy laws), supports compliance (ISO 27001, GDPR, HIPAA), and lets you choose data residency in the EU or Switzerland. ",
        "popularity": 4
    },
    {
        "selected_concern": "Data Stored in Unknown Locations",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Cryptomator",
        "pet_price": "Free",
        "pet_description": "Cryptomator is a client‑side encryption tool that lets you create encrypted “vaults” for your files. You can then sync these vaults with any cloud service (Dropbox, OneDrive, Google Drive, etc.) without risking unencrypted data being exposed.",
        "pet_company": "Skymatic GmbH",
        "pet_link": "https://cryptomator.org/pricing/#for-individuals",
          "why_use": "With Cryptomator, all encryption happens on your device before files go to the cloud. It encrypts both file contents and filenames using AES-256, so even your cloud provider can’t read anything. It’s fully open source, so its security can be audited.",
        "popularity": 4
    },
    {
        "selected_concern": "Data Stored in Unknown Locations",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Cryptomator",
        "pet_price": "Free",
        "pet_description": "Cryptomator is a client‑side encryption tool that lets you create encrypted “vaults” for your files. You can then sync these vaults with any cloud service (Dropbox, OneDrive, Google Drive, etc.) without risking unencrypted data being exposed.",
        "pet_company": "Skymatic GmbH",
        "pet_link": "https://cryptomator.org/pricing/#for-individuals",
        "why_use": "With Cryptomator, all encryption happens on your device before files go to the cloud. It encrypts both file contents and filenames using AES-256, so even your cloud provider can’t read anything. It’s fully open source, so its security can be audited.",
        "popularity": 4
    },
    {
        "selected_concern": "Data Stored in Unknown Locations",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Tresorit",
        "pet_price": "Free",
        "pet_description": "Tresorit is a highly secure, zero‑knowledge cloud storage and collaboration platform. Files are encrypted on your device before upload, and only you (and people you explicitly share with) can decrypt them. It supports secure sharing, versioning, and collaboration in encrypted ‘tresors’.",
        "pet_company": "Secomba GmbH",
        "pet_link": "https://tresorit.com/de?gad_source=1&gad_campaignid=21618907595&gbraid=0AAAAACUlux-2uR66nAVqUcxRGBnA382uG&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNIocAtTk07eWtz1VD9nd11jzHYyxXloPOlVkAlq3e3CAkIKduvnZ1caAgyeEALw_wcB",
        "why_use": "Tresorit provides client‑side end-to-end encryption, meaning no unencrypted data or keys are ever sent to their servers. It uses strong cryptographic algorithms and ensures integrity with HMACs.  Tresorit is under Swiss jurisdiction (strong privacy laws), supports compliance (ISO 27001, GDPR, HIPAA), and lets you choose data residency in the EU or Switzerland. ",
        "popularity": 4
    },
    {
        "selected_concern": "Data Stored in Unknown Locations",
        "awareness_level": "High",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Tresorit",
        "pet_price": "Free",
        "pet_description": "Tresorit is a highly secure, zero‑knowledge cloud storage and collaboration platform. Files are encrypted on your device before upload, and only you (and people you explicitly share with) can decrypt them. It supports secure sharing, versioning, and collaboration in encrypted ‘tresors’.",
        "pet_company": "Secomba GmbH",
        "pet_link": "https://tresorit.com/de?gad_source=1&gad_campaignid=21618907595&gbraid=0AAAAACUlux-2uR66nAVqUcxRGBnA382uG&gclid=Cj0KCQiAiebIBhDmARIsAE8PGNIocAtTk07eWtz1VD9nd11jzHYyxXloPOlVkAlq3e3CAkIKduvnZ1caAgyeEALw_wcB",
        "why_use": "Tresorit provides client‑side end-to-end encryption, meaning no unencrypted data or keys are ever sent to their servers. It uses strong cryptographic algorithms and ensures integrity with HMACs.  Tresorit is under Swiss jurisdiction (strong privacy laws), supports compliance (ISO 27001, GDPR, HIPAA), and lets you choose data residency in the EU or Switzerland. ",
        "popularity": 4
    },
    {
        "selected_concern": "Data Stored in Unknown Locations",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Google Drive",
        "pet_price": "Free",
        "pet_description": "Google Drive is a widely used cloud storage service that integrates deeply with Google Workspace (Docs, Sheets, Slides, Gmail). It offers file storage, sharing, collaboration, and syncing across devices.",
        "pet_company": "Google",
        "pet_link": "https://workspace.google.com/products/drive/",
        "why_use": "Use Google Drive for seamless cloud storage and collaboration that your data is encrypted in transit and at rest, making it relatively secure.",
        "popularity": 4
    },
    {
        "selected_concern": "Data Stored in Unknown Locations",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Google Drive",
        "pet_price": "Free",
        "pet_description": "Google Drive is a widely used cloud storage service that integrates deeply with Google Workspace (Docs, Sheets, Slides, Gmail). It offers file storage, sharing, collaboration, and syncing across devices.",
        "pet_company": "Google",
        "pet_link": "https://workspace.google.com/products/drive/",
        "why_use": "Use Google Drive for seamless cloud storage and collaboration that your data is encrypted in transit and at rest, making it relatively secure.",
        "popularity": 4
    },
    {
        "selected_concern": "Data Stored in Unknown Locations",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "Google Drive",
        "pet_price": "Free",
        "pet_description": "Google Drive is a widely used cloud storage service that integrates deeply with Google Workspace (Docs, Sheets, Slides, Gmail). It offers file storage, sharing, collaboration, and syncing across devices.",
        "pet_company": "Google",
        "pet_link": "https://workspace.google.com/products/drive/",
        "why_use": "Use Google Drive for seamless cloud storage and collaboration that your data is encrypted in transit and at rest, making it relatively secure.",
        "popularity": 4
    },
    {
        "selected_concern": "Data Stored in Unknown Locations",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Google Drive",
        "pet_price": "Free",
        "pet_description": "Google Drive is a widely used cloud storage service that integrates deeply with Google Workspace (Docs, Sheets, Slides, Gmail). It offers file storage, sharing, collaboration, and syncing across devices.",
        "pet_company": "Google",
        "pet_link": "https://workspace.google.com/products/drive/",
        "why_use": "Use Google Drive for seamless cloud storage and collaboration that your data is encrypted in transit and at rest, making it relatively secure.",
        "popularity": 4
    },
    {
        "selected_concern": "Using Public Wi-Fi Without Protection",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "Avira Phantom VPN",
        "pet_price": "Free",
         "pet_description": "Avira Phantom VPN is a VPN service from Avira that encrypts your internet traffic, hides your IP address, and protects you on public WiFi. It claims a no logs policy and uses encryption to secure your data.",
        "pet_company": "Avira Operations GmbH & Co",
        "pet_link": "https://www.avira.com/en/free-vpn?srsltid=AfmBOop5hGnFo5lNma661_7nSKSD5G6SEwooOMTFP5jmYDZNlgvfdKUQ",
         "why_use": "Use Phantom VPN when you want simple, reliable VPN protection from a reputable security company. It hides your IP, protects your data with strong encryption, and is useful in public WiFi scenarios. Since Avira is based in Germany, it's run by a well-known security vendor. The Pro version supports unlimited simultaneous devices. ",
        "popularity": 3
    },
    {
        "selected_concern": "Using Public Wi-Fi Without Protection",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "Avira Phantom VPN",
        "pet_price": "Free",
         "pet_description": "Avira Phantom VPN is a VPN service from Avira that encrypts your internet traffic, hides your IP address, and protects you on public Wi‑Fi. It claims a no‑logs policy and uses AES‑256 encryption to secure your data.",
        "pet_company": "Avira Operations GmbH & Co",
        "pet_link": "https://www.avira.com/en/free-vpn?srsltid=AfmBOop5hGnFo5lNma661_7nSKSD5G6SEwooOMTFP5jmYDZNlgvfdKUQ",
         "why_use": "Use Phantom VPN when you want simple, reliable VPN protection from a reputable security company. It hides your IP, protects your data with strong encryption, and is useful in public Wi‑Fi scenarios. Since Avira is based in Germany, it's run by a well-known security vendor. The Pro version supports unlimited simultaneous devices. ",
        "popularity": 3
    },
    {
        "selected_concern": "Using Public Wi-Fi Without Protection",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Windscribe",
        "pet_price": "9$/month",
         "pet_description": "Avira Phantom VPN is a VPN service from Avira that encrypts your internet traffic, hides your IP address, and protects you on public Wi‑Fi. It claims a no‑logs policy and uses AES‑256 encryption to secure your data.",
        "pet_company": "Avira Operations GmbH & Co",
        "pet_link": "https://windscribe.com",
         "why_use": "Use Phantom VPN when you want simple, reliable VPN protection from a reputable security company. It hides your IP, protects your data with strong encryption, and is useful in public Wi‑Fi scenarios. Since Avira is based in Germany, it's run by a well-known security vendor. The Pro version supports unlimited simultaneous devices. ",
        "popularity": 3
    },
    {
        "selected_concern": "Using Public Wi-Fi Without Protection",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Using Public Wi-Fi Without Protection",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Little Snitch",
        "pet_price": "Free",
        "pet_description": "Little Snitch is a host‑based application firewall for macOS that monitors and controls outgoing network connections. Whenever an app tries to connect to the Internet, you can decide whether to allow or block it, permanently or just once, and even define rules (which domain, which port, etc.). ",
        "pet_company": "Objective Development Software",
        "pet_link": "https://www.obdev.at/products/littlesnitch",
        "why_use": "Use Little Snitch to gain visibility and control over what your Mac is ‘phoning home’ to. It's especially useful for catching background apps or system processes that connect to servers you didn’t expect. The Network Monitor gives a real‑time map of connections, and you can set detailed, bidirectional firewall rules. ",
        "popularity": 4
    },
    {
        "selected_concern": "Using Public Wi-Fi Without Protection",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Cisco AnyConnect",
        "pet_price": "€1.99 / year",
        "pet_description": "Cisco AnyConnect (Secure Mobility Client) is a corporate-grade VPN client that provides secure network access, endpoint protection, and module-based security (web security, posture, visibility) across desktop and mobile platforms.",
        "pet_company": "Cisco Systems, Inc.",
        "pet_link": "https://www.cisco.com/c/en/us/support/security/anyconnect-secure-mobility-client-v4-x/model.html",
        "why_use": "Using AnyConnect on public Wi-Fi helps establish a secure, encrypted VPN tunnel back to your company’s network, protecting sensitive data from snooping or man-in-the-middle attacks. It supports SSL and IPsec (IKEv2), and modules like Web Security lets you route web traffic via Cisco’s secure proxy.  Because licensing is based on unique users (not just concurrent), you can use it on multiple devices without buying for each session.",
        "popularity": 3
    },
    {
        "selected_concern": "Using Public Wi-Fi Without Protection",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "NetGuard",
        "pet_price": "Free",
        "pet_description": "NetGuard is a no‑root firewall for Android that uses a local VPN to filter traffic. You can block Internet access per app (Wi‑Fi / mobile) or even per address, helping reduce data usage, improve privacy, and control which apps can connect to the network.",
        "pet_company": "FairCode (open‑source community)",
        "pet_link": "https://netguard.me/",
        "why_use": "Use NetGuard if you want granular control over your apps’ network access without rooting your device. Because it’s open source, privacy-focused (no tracking, no ads), and doesn’t call home, it’s a strong choice for people who want to limit which apps can send data out. You also get optional logs, filtering, and advanced per-address blocking in the Pro version. ([netguard.me](https://netguard.me/))",
        "popularity": 4
    },
    {
        "selected_concern": "ISP Tracking and Data Logging",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Brave Browser",
        "pet_price": "Free",
        "pet_description": "The new Brave browser blocks ads and trackers that slow you down and invade your privacy",
        "pet_company": "Brave Software",
        "pet_link": "https://brave.com",
        "why_use": "AI ASSISTANT, Brave Search, Private Browsing, Browse Faster, Privacy Protection",
        "popularity": 4
    },
    {
        "selected_concern": "ISP Tracking and Data Logging",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Brave Browser",
        "pet_price": "Free",
        "pet_description": "The new Brave browser blocks ads and trackers that slow you down and invade your privacy",
        "pet_company": "Brave Software",
        "pet_link": "https://brave.com",
        "why_use": "AI ASSISTANT, Brave Search, Private Browsing, Browse Faster, Privacy Protection",
        "popularity": 4
    },
    {
        "selected_concern": "ISP Tracking and Data Logging",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "DuckDuckGo Browser",
        "pet_price": "Free",
        "pet_description": "DuckDuckGo Browser is a privacy-oriented web browser that blocks trackers, enforces HTTPS connections, and integrates a privacy search engine. It provides automatic tracker blocking, private search, and simplified cookie consent management.",
        "pet_company": "DuckDuckGo, Inc",
        "pet_link": "https://duckduckgo.com/app",
        "why_use": "Use DuckDuckGo Browser when you want a simple, privacy-first browsing experience. It prevents third-party trackers from following you across websites, forces encrypted connections where possible, and clears browsing data automatically when you exit. Its built-in search engine doesn’t track you, and the app provides privacy ratings for websites. ([duckduckgo.com](https://duckduckgo.com/app))",
        "popularity": 4
    },
    {
        "selected_concern": "ISP Tracking and Data Logging",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "DuckDuckGo Browser",
        "pet_price": "Free",
        "pet_description": "DuckDuckGo Browser is a privacy-oriented web browser that blocks trackers, enforces HTTPS connections, and integrates a privacy search engine. It provides automatic tracker blocking, private search, and simplified cookie consent management.",
        "pet_company": "DuckDuckGo, Inc",
        "pet_link": "https://duckduckgo.com/app",
        "why_use": "Use DuckDuckGo Browser when you want a simple, privacy-first browsing experience. It prevents third-party trackers from following you across websites, forces encrypted connections where possible, and clears browsing data automatically when you exit. Its built-in search engine doesn’t track you, and the app provides privacy ratings for websites. ([duckduckgo.com](https://duckduckgo.com/app))",
        "popularity": 4
    },
    {
        "selected_concern": "ISP Tracking and Data Logging",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "NordVPN",
        "pet_price": "2.99$/month",
        "pet_description": "It’s an easy-to-use VPN app for Android smartphones, tablets.",
        "pet_company": "Nord Security",
        "pet_link": "https://nordvpn.com",
        "why_use": "When you’re connected to a VPN, no one can see what websites you visit or files you download. You can surf the web with confidence with Threat Protection. And NordVPN protects you from traffic-based bandwidth throttling.",
        "popularity": 4
    },
    {
        "selected_concern": "ISP Tracking and Data Logging",
        "awareness_level": "Moderate",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "NordVPN",
        "pet_price": "2.99$/month",
        "pet_description": "It’s an easy-to-use VPN app for Android smartphones, tablets.",
        "pet_company": "Nord Security",
        "pet_link": "https://nordvpn.com",
        "why_use": "When you’re connected to a VPN, no one can see what websites you visit or files you download. You can surf the web with confidence with Threat Protection. And NordVPN protects you from traffic-based bandwidth throttling.",
        "popularity": 4
    },
    {
        "selected_concern": "ISP Tracking and Data Logging",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Tor Browser",
        "pet_price": "Free",
        "pet_description": "The Tor Project, Inc., is a organization developing free and open source software for privacy and freedom online, protecting people from tracking, surveillance, and censorship. The Tor Project’s mission is to advance human rights and freedoms by creating and deploying free and open source anonymity and privacy technologies, support their unrestricted availability and use, and further their scientific and popular understanding.",
        "pet_company": "The Tor Project",
        "pet_link": "https://www.torproject.org/download/",
        "why_use": "BLOCK TRACKERS, DEFEND AGAINST SURVEILLANCE, RESIST FINGERPRINTING, MULTI-LAYERED ENCRYPTION",
        "popularity": 4
    },
    {
        "selected_concern": "ISP Tracking and Data Logging",
        "awareness_level": "Moderate",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Tor Browser",
        "pet_price": "Free",
        "pet_description": "The Tor Project, Inc., is a organization developing free and open source software for privacy and freedom online, protecting people from tracking, surveillance, and censorship. The Tor Project’s mission is to advance human rights and freedoms by creating and deploying free and open source anonymity and privacy technologies, support their unrestricted availability and use, and further their scientific and popular understanding.",
        "pet_company": "The Tor Project",
        "pet_link": "https://www.torproject.org/download/",
        "why_use": "BLOCK TRACKERS, DEFEND AGAINST SURVEILLANCE, RESIST FINGERPRINTING, MULTI-LAYERED ENCRYPTION",
        "popularity": 4
    },
    {
        "selected_concern": "ISP Tracking and Data Logging",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Cisco AnyConnect",
        "pet_price": "€1.99 / year",
        "pet_description": "Cisco AnyConnect (Secure Mobility Client) is a corporate-grade VPN client that provides secure network access, endpoint protection, and module-based security (web security, posture, visibility) across desktop and mobile platforms.",
        "pet_company": "Cisco Systems, Inc.",
        "pet_link": "https://www.cisco.com/c/en/us/support/security/anyconnect-secure-mobility-client-v4-x/model.html",
        "why_use": "Using AnyConnect on public Wi-Fi helps establish a secure, encrypted VPN tunnel back to your company’s network, protecting sensitive data from snooping or man-in-the-middle attacks. It supports SSL and IPsec (IKEv2), and modules like Web Security lets you route web traffic via Cisco’s secure proxy.  Because licensing is based on unique users (not just concurrent), you can use it on multiple devices without buying for each session.",
        "popularity": 3
    },
    {
        "selected_concern": "Unencrypted Network Traffic",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "Brave Browser",
        "pet_price": "Free",
        "pet_description": "The new Brave browser blocks ads and trackers that slow you down and invade your privacy",
        "pet_company": "Brave Software",
        "pet_link": "https://brave.com",
        "why_use": "AI ASSISTANT, Brave Search, Private Browsing, Browse Faster, Privacy Protection",
        "popularity": 4
    },
    {
        "selected_concern": "Unencrypted Network Traffic",
        "awareness_level": "Low",
        "device": "Desktop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "Brave Browser",
        "pet_price": "Free",
        "pet_description": "The new Brave browser blocks ads and trackers that slow you down and invade your privacy",
        "pet_company": "Brave Software",
        "pet_link": "https://brave.com",
        "why_use": "AI ASSISTANT, Brave Search, Private Browsing, Browse Faster, Privacy Protection",
        "popularity": 4
    },
    {
        "selected_concern": "Unencrypted Network Traffic",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "DuckDuckGo Browser",
        "pet_price": "Free",
        "pet_description": "DuckDuckGo Browser is a privacy-oriented web browser that blocks trackers, enforces HTTPS connections, and integrates a privacy search engine. It provides automatic tracker blocking, private search, and simplified cookie consent management.",
        "pet_company": "DuckDuckGo, Inc",
        "pet_link": "https://duckduckgo.com/app",
        "why_use": "Use DuckDuckGo Browser when you want a simple, privacy-first browsing experience. It prevents third-party trackers from following you across websites, forces encrypted connections where possible, and clears browsing data automatically when you exit. Its built-in search engine doesn’t track you, and the app provides privacy ratings for websites. ([duckduckgo.com](https://duckduckgo.com/app))",
        "popularity": 4
    },
    {
        "selected_concern": "Unencrypted Network Traffic",
        "awareness_level": "Low",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "DuckDuckGo Browser",
        "pet_price": "Free",
        "pet_description": "DuckDuckGo Browser is a privacy-oriented web browser that blocks trackers, enforces HTTPS connections, and integrates a privacy search engine. It provides automatic tracker blocking, private search, and simplified cookie consent management.",
        "pet_company": "DuckDuckGo, Inc",
        "pet_link": "https://duckduckgo.com/app",
        "why_use": "Use DuckDuckGo Browser when you want a simple, privacy-first browsing experience. It prevents third-party trackers from following you across websites, forces encrypted connections where possible, and clears browsing data automatically when you exit. Its built-in search engine doesn’t track you, and the app provides privacy ratings for websites. ([duckduckgo.com](https://duckduckgo.com/app))",
        "popularity": 4
    },
    {
        "selected_concern": "Unencrypted Network Traffic",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Unencrypted Network Traffic",
        "awareness_level": "Moderate",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "ProtonVPN",
        "pet_price": "Free",
        "pet_description": "Proton VPN is the world's only free VPN app that is safe to use and respects your privacy. Proton VPN is created by the CERN scientists behind Proton Mail - the world's largest encrypted email service. Our fast VPN offers secure, private, encrypted, and unlimited internet access with advanced privacy and security features. ",
        "pet_company": "Proton AG",
        "pet_link": "https://protonvpn.com",
        "why_use": "Full-disk encrypted servers protect your data privacy, DNS leak protection: we encrypt DNS queries to ensure that your browsing activity cannot be exposed through DNS leaks, No personal data required to sign up",
        "popularity": 4
    },
    {
        "selected_concern": "Unencrypted Network Traffic",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "MacOS",
        "country": "Global",
        "pet_name": "NextDNS",
        "pet_price": "Free",
        "pet_description": "NextDNS is a modern, cloud-based DNS resolver that offers encrypted DNS (DoH, DoT), threat protection, tracker/ad blocking, parental controls, and highly customizable filtering rules. It acts like a “DNS firewall” that protects everything on your network or device.",
        "pet_company": "NextDNS Inc.",
        "pet_link": "https://nextdns.io",
        "why_use": "Use NextDNS when you want to filter and monitor DNS traffic at a very granular level: block malware, phishing, trackers, ads — *and* choose how long logs are kept, or disable them entirely. It also supports encrypted DNS, protecting your DNS queries from eavesdroppers.",
        "popularity": 4
    },
    {
        "selected_concern": "Unencrypted Network Traffic",
        "awareness_level": "High",
        "device": "Dektop",
        "os": "Windows",
        "country": "Global",
        "pet_name": "NextDNS",
        "pet_price": "Free",
        "pet_description": "NextDNS is a modern, cloud-based DNS resolver that offers encrypted DNS (DoH, DoT), threat protection, tracker/ad blocking, parental controls, and highly customizable filtering rules. It acts like a “DNS firewall” that protects everything on your network or device.",
        "pet_company": "NextDNS Inc.",
        "pet_link": "https://nextdns.io",
        "why_use": "Use NextDNS when you want to filter and monitor DNS traffic at a very granular level: block malware, phishing, trackers, ads — *and* choose how long logs are kept, or disable them entirely. It also supports encrypted DNS, protecting your DNS queries from eavesdroppers.",
        "popularity": 4
    },
    {
        "selected_concern": "Unencrypted Network Traffic",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "iOS",
        "country": "Global",
        "pet_name": "NextDNS",
        "pet_price": "Free",
        "pet_description": "NextDNS is a modern, cloud-based DNS resolver that offers encrypted DNS (DoH, DoT), threat protection, tracker/ad blocking, parental controls, and highly customizable filtering rules. It acts like a “DNS firewall” that protects everything on your network or device.",
        "pet_company": "NextDNS Inc.",
        "pet_link": "https://nextdns.io",
        "why_use": "Use NextDNS when you want to filter and monitor DNS traffic at a very granular level: block malware, phishing, trackers, ads — *and* choose how long logs are kept, or disable them entirely. It also supports encrypted DNS, protecting your DNS queries from eavesdroppers.",
        "popularity": 4
    },
    {
        "selected_concern": "Unencrypted Network Traffic",
        "awareness_level": "High",
        "device": "Mobile",
        "os": "Android",
        "country": "Global",
        "pet_name": "NextDNS",
        "pet_price": "Free",
        "pet_description": "NextDNS is a modern, cloud-based DNS resolver that offers encrypted DNS (DoH, DoT), threat protection, tracker/ad blocking, parental controls, and highly customizable filtering rules. It acts like a “DNS firewall” that protects everything on your network or device.",
        "pet_company": "NextDNS Inc.",
        "pet_link": "https://nextdns.io",
        "why_use": "Use NextDNS when you want to filter and monitor DNS traffic at a very granular level: block malware, phishing, trackers, ads — *and* choose how long logs are kept, or disable them entirely. It also supports encrypted DNS, protecting your DNS queries from eavesdroppers.",
        "popularity": 4
    }

]


# --- Insert into DB ---
for area, concerns in questions_data.items():
    for concern, questions in concerns.items():
        for q in questions:
            cursor.execute(
                "INSERT INTO concern_questions (area_of_concern, specific_concern, text, type) VALUES (?, ?, ?, ?)",
                (area, concern, q["text"], "single")
            )
            question_id = cursor.lastrowid
            for opt_text, is_correct in q["options"]:
                cursor.execute(
                    "INSERT INTO concern_answer_options (question_id, option_text, is_correct, explanation) VALUES (?, ?, ?, ?)",
                    (question_id, opt_text, int(is_correct), "")
                )

# --- Insert Learn More Content ---
for item in learn_more_data:
    cursor.execute(
        """
        INSERT OR IGNORE INTO learn_more
        (specific_concern, what_is_it, why_it_matters, dos, donts)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            item["specific_concern"],
            item["what_is_it"],
            item["why_it_matters"],
            item["dos"],
            item["donts"]
        )
    )

# Insert pets recommendation 
for pet in pet_data:
    cursor.execute("""
        INSERT INTO user_pets_recommendations 
        (selected_concern, awareness_level, device, os, country,
         pet_name, pet_price, pet_description, pet_company, pet_link,
         logo_link, why_use, popularity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        pet["selected_concern"],
        pet["awareness_level"],
        pet["device"],
        pet["os"],
        pet["country"],
        pet["pet_name"],
        pet["pet_price"],
        pet["pet_description"],
        pet["pet_company"],
        pet["pet_link"],
        pet.get("logo_link", ""),    
        pet.get("why_use", ""),
        pet.get("popularity", 0)
    ))


conn.commit()

conn.close()
print("✅ Database populated with data successfully!")

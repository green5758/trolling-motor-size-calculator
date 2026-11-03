import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "MarineThrustPro"
SITE_TAGLINE = "Trolling Motor Thrust, Shaft Length, Marine Battery & Fish Finder Sizing Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e"

# Cumulative Daily Review Engine: Adds +3 brand-new unique product review articles EVERY SINGLE DAY
LAUNCH_EPOCH = datetime.date(2026, 11, 1)
REVIEWS_PER_DAY = 3

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/marinethrustpro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "marinethrustpro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Minn Kota Terrova 55 / 80 / 112 Lb Thrust Bow-Mount GPS Trolling Motor w/ Spot-Lock",
        "category": "GPS Bow-Mount Trolling Motor",
        "rating": "4.8 ★ (3,850+ reviews)",
        "badge": "#1 GPS Spot-Lock Motor",
        "specs": "12V (55 lb) / 24V (80 lb) / 36V (112 lb) | 45\"–72\" Shaft | Wireless GPS Anchor & Humminbird Link",
        "keyword": "Minn+Kota+Terrova+Bow+Mount+GPS+Trolling+Motor+Spot+Lock"
    },
    {
        "title": "Garmin ECHOMAP UHD2 93sv 9-Inch Touch Fish Finder with GT56UHD-TM Transducer",
        "category": "SideVü & ClearVü Chartplotter",
        "rating": "4.8 ★ (4,600+ reviews)",
        "badge": "#1 9-Inch Sonar Chartplotter",
        "specs": "1,000 kHz Ultra High-Definition SideVü/ClearVü | Preloaded Garmin Navionics+ Maps | LiveScope Ready",
        "keyword": "Garmin+ECHOMAP+UHD2+93sv+9+Inch+Fish+Finder+GT56UHD"
    },
    {
        "title": "NOCO Genius GENPRO10X3 3-Bank 30A (10A/Bank) Waterproof Onboard Marine Battery Charger",
        "category": "Onboard Marine Battery Charger",
        "rating": "4.9 ★ (14,900+ reviews)",
        "badge": "#1 Waterproof Marine Charger",
        "specs": "IP68 Submersible Waterproof | Charges LiFePO4, AGM & Lead-Acid Independently | Thermal Sensor",
        "keyword": "NOCO+Genius+GENPRO10X3+3+Bank+30A+Onboard+Marine+Battery+Charger"
    },
    {
        "title": "Humminbird HELIX 9 / HELIX 10 CHIRP MEGA SI+ GPS G4N Fish Finder & Chartplotter",
        "category": "MEGA Side Imaging+ Sonar",
        "rating": "4.8 ★ (3,400+ reviews)",
        "badge": "Best Structure Side-Imaging",
        "specs": "MEGA Side & Down Imaging+ (200 Ft Range) | Dual Spectrum CHIRP | One-Boat Network i-Pilot Link",
        "keyword": "Humminbird+HELIX+9+10+CHIRP+MEGA+SI+GPS+G4N+Fish+Finder"
    },
    {
        "title": "Newport Vessels NV-Series & Kayak Series 55 Lb / 86 Lb Saltwater Transom Trolling Motor",
        "category": "Transom & Kayak Trolling Motor",
        "rating": "4.7 ★ (12,300+ reviews)",
        "badge": "#1 Transom & Kayak Motor",
        "specs": "12V (55 lb) or 24V (86 lb) | 30\"/36\"/40\" Fiberglass Shaft | Saltwater Stainless Hardware",
        "keyword": "Newport+Vessels+55+lb+86+lb+Saltwater+Transom+Trolling+Motor"
    },
    {
        "title": "LiTime 12V 100Ah TM & 24V / 36V Trolling Motor LiFePO4 Lithium Marine Battery",
        "category": "Deep-Cycle Trolling Battery",
        "rating": "4.8 ★ (7,200+ reviews)",
        "badge": "Best Lithium Trolling Battery",
        "specs": "Low-Temp Cut-Off Protection | 200A Surge BMS for Spot-Lock | 50% Lighter Than Lead-Acid",
        "keyword": "LiTime+Trolling+Motor+LiFePO4+Lithium+Marine+Battery+12V+24V+36V"
    },
    {
        "title": "Lowrance Elite FS 9 with Active Imaging 3-in-1 Transducer & C-MAP Contour+ Charts",
        "category": "Tournament Touch Sonar",
        "rating": "4.7 ★ (2,900+ reviews)",
        "badge": "Top Tournament Bass Sonar",
        "specs": "CHIRP + SideScan + DownScan + FishReveal | ActiveTarget 2 Live Sonar Compatible | NMEA 2000",
        "keyword": "Lowrance+Elite+FS+9+Active+Imaging+3+in+1+Fish+Finder"
    },
    {
        "title": "Minn Kota Endura Max 55 Lb Thrust Transom-Mount Trolling Motor w/ Digital Maximizer",
        "category": "5x Runtime Transom Motor",
        "rating": "4.8 ★ (8,100+ reviews)",
        "badge": "Up to 5x Longer Battery Run",
        "specs": "Variable Speed Digital Maximizer | 36\" or 42\" Indestructible Composite Shaft | 6\" Telescoping Tiller",
        "keyword": "Minn+Kota+Endura+Max+55+lb+Transom+Trolling+Motor+Digital+Maximizer"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Minn Kota Terrova 80 Lb (24V)",
        "type": "Bow-Mount GPS Spot-Lock",
        "thrust_spec": "80 Lbs Thrust (24V System)",
        "shaft_options": "45\", 54\", 60\", 72\" Composite",
        "highlight": "Industry #1 GPS Spot-Lock Anchor",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Minn+Kota+Terrova+80+lb+24V+GPS+Trolling+Motor"
    },
    {
        "model": "Garmin Force Kraken / Force (24V/36V)",
        "type": "Brushless Wireless Bow Motor",
        "thrust_spec": "80 Lbs (24V) / 100 Lbs (36V)",
        "shaft_options": "48\", 57\", 63\", 75\" Brushless",
        "highlight": "30% More Efficient Brushless Motor",
        "rating": "4.9 / 5.0 ★",
        "keyword": "Garmin+Force+Brushless+Trolling+Motor+57+Inch"
    },
    {
        "model": "Minn Kota Endura Max 55 (12V)",
        "type": "Transom-Mount Digital PWM",
        "thrust_spec": "55 Lbs Thrust (12V System)",
        "shaft_options": "36\" & 42\" Composite Shaft",
        "highlight": "Digital Maximizer (5x Battery Runtime)",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Minn+Kota+Endura+Max+55+lb+Transom+Trolling+Motor"
    },
    {
        "model": "Garmin ECHOMAP UHD2 93sv",
        "type": "9\" Touch Chartplotter + GT56",
        "thrust_spec": "1,000 kHz UHD SideVü / ClearVü",
        "shaft_options": "Supports Panoptix LiveScope Plus",
        "highlight": "Fastest Touch UI + Navionics+ Maps",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Garmin+ECHOMAP+UHD2+93sv+9+Inch+Fish+Finder+GT56UHD"
    },
    {
        "model": "Humminbird HELIX 9 MEGA SI+ G4N",
        "type": "9\" MEGA Side Imaging+ Sonar",
        "thrust_spec": "1.2 MHz MEGA SI+ / DI+ Sonar",
        "shaft_options": "Links Directly to Minn Kota Motors",
        "highlight": "Clearest Underwater Timber & Structure",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Humminbird+HELIX+9+CHIRP+MEGA+SI+GPS+G4N+Fish+Finder"
    },
    {
        "model": "NOCO Genius GENPRO10X3 (30A)",
        "type": "3-Bank Onboard Marine Charger",
        "thrust_spec": "30 Amps Total (10A × 3 Banks)",
        "shaft_options": "12V LiFePO4, AGM & Flooded Modes",
        "highlight": "IP68 Submersible + Dead-Battery Force Mode",
        "rating": "4.9 / 5.0 ★",
        "keyword": "NOCO+Genius+GENPRO10X3+3+Bank+30A+Onboard+Marine+Battery+Charger"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-minn-kota-terrova-vs-ultrex-bow-mount-trolling-motor",
        "title": "Minn Kota Terrova vs. Ultrex: Electric Steer vs. Cable-Assisted Power Steering Compared",
        "product_a": "Minn Kota Terrova (GPS Spot-Lock)",
        "product_b": "Minn Kota Ultrex / QUEST",
        "winner_badge": "Best Open-Deck Versatility vs. Best Tournament Bass Foot Pedal",
        "keyword_a": "Minn+Kota+Terrova+80+lb+24V+GPS+Trolling+Motor",
        "keyword_b": "Minn+Kota+Ultrex+80+lb+112+lb+Trolling+Motor",
        "summary": "Compare foot pedal responsiveness, stow/deploy mechanisms, shaft length availability (up to 72\"), and deck footprint between the Minn Kota Terrova and Ultrex.",
        "metrics": [
            {"feature": "Steering Architecture", "val_a": "100% Electric Servo Steering (Flat Low-Profile Pedal + Remote)", "val_b": "Power-Assisted Cable-Steer Heel-Toe Foot Pedal + Remote"},
            {"feature": "Stow & Deploy Mechanism", "val_a": "Fall-Away Ramp Release Lever (Zero Pull-Cord Effort)", "val_b": "Scissors-Mount Lift-Assist Pull Cable (Instant Shallow Stowing)"},
            {"feature": "Shaft Length Options", "val_a": "45\", 54\", 60\", and 72\" (Fits Deep-V, Pontoons & Bay Boats)", "val_b": "45\", 52\", and 60\" (Optimized for Low-Bow Bass Boats)"},
            {"feature": "GPS Spot-Lock Accuracy", "val_a": "Identical Advanced GPS Spot-Lock & Jog-5-Feet Feature", "val_b": "Identical Advanced GPS Spot-Lock & Jog-5-Feet Feature"},
            {"feature": "Price & Weight", "val_a": "$500–$800 Less Expensive & Lighter on the Bow", "val_b": "Premium Tournament Tier"}
        ],
        "verdict_text": "Choose the Minn Kota Terrova if you own a Deep-V walleye boat, pontoon, multi-species aluminum boat, or center console that needs a 54\" to 72\" shaft and an uncluttered front deck (you can run it solely from the wireless neck remote). Choose the Minn Kota Ultrex if you fish shallow docks and heavy timber from a fiberglass bass boat and demand instant heel-toe cable foot pedal feedback."
    },
    {
        "slug": "compare-garmin-echomap-uhd2-93sv-vs-humminbird-helix-9-mega-si",
        "title": "Garmin ECHOMAP UHD2 93sv vs. Humminbird HELIX 9 MEGA SI+ G4N: Which 9-Inch Fish Finder Wins?",
        "product_a": "Garmin ECHOMAP UHD2 93sv (GT56)",
        "product_b": "Humminbird HELIX 9 MEGA SI+ G4N",
        "winner_badge": "Best Touchscreen & LiveScope Path vs. Best Side-Imaging & Minn Kota Link",
        "keyword_a": "Garmin+ECHOMAP+UHD2+93sv+9+Inch+Fish+Finder+GT56UHD",
        "keyword_b": "Humminbird+HELIX+9+CHIRP+MEGA+SI+GPS+G4N+Fish+Finder",
        "summary": "Compare 1,000 kHz GT56UHD vs. 1.2 MHz MEGA Side Imaging+, touchscreen vs. keypad controls, and forward-facing sonar expansion.",
        "metrics": [
            {"feature": "Screen Control Interface", "val_a": "Hybrid Touchscreen + Physical Key Assist + Quick-Release Cradle", "val_b": "Physical Keypad & Rotary Joystick Only (No Touchscreen on HELIX)"},
            {"feature": "Side-Scan Resolution", "val_a": "GT56UHD-TM (455 / 800 / 1,000 kHz Ultra High-Def)", "val_b": "XM 9 HW MSI+ T (455 / 800 kHz & 1.2 MHz MEGA Imaging+)"},
            {"feature": "Forward-Facing Live Sonar", "val_a": "Plug-and-Play Ready for Garmin Panoptix LiveScope Plus LVS34", "val_b": "Supports Humminbird MEGA Live Imaging Transducer"},
            {"feature": "Trolling Motor Integration", "val_a": "Wireless Sync with Garmin Force & Kraken Motors", "val_b": "One-Boat Network Syncs w/ Minn Kota Terrova/Ultrex to Follow Contours"},
            {"feature": "Preloaded Lake Maps", "val_a": "Built-In Garmin Navionics+ Inland & Coastal Charts", "val_b": " Humminbird Basemap (Lakemaster VX Card Optional)"}
        ],
        "verdict_text": "Choose the Garmin ECHOMAP UHD2 93sv if you want a fast smartphone-like touchscreen, a quick-release bail mount that unclips in 2 seconds for security, and a direct upgrade path to Garmin LiveScope Plus. Choose the Humminbird HELIX 9 MEGA SI+ G4N if you run a Minn Kota trolling motor and want your boat to automatically steer along Lakemaster depth contours."
    },
    {
        "slug": "compare-12v-vs-24v-vs-36v-trolling-motor-battery-system",
        "title": "12V vs. 24V vs. 36V Trolling Motor Systems: Thrust Lbs, Amp Draw & LiFePO4 Weight Compared",
        "product_a": "12V Trolling System (30–55 Lb Thrust)",
        "product_b": "24V (80 Lb) & 36V (112 Lb) Systems",
        "winner_badge": "Lightest Single-Battery Setup vs. All-Day Current & Wind Authority",
        "keyword_a": "Minn+Kota+Endura+Max+55+lb+Transom+Trolling+Motor",
        "keyword_b": "LiTime+Trolling+Motor+LiFePO4+Lithium+Marine+Battery+12V+24V+36V",
        "summary": "See why doubling or tripling voltage cuts amp draw, prevents trolling motor wiring heat, and keeps heavy boats locked in wind and river current.",
        "metrics": [
            {"feature": "Max Available Thrust", "val_a": "55 Lbs Max (Physical 50A Limit on 12V Wiring)", "val_b": "80 Lbs on 24V | 100–115 Lbs on 36V"},
            {"feature": "Boat Weight Capacity", "val_a": "Kayaks, Jon Boats & Skiffs Up to 2,200 Lbs Loaded", "val_b": "24V: Up to 4,000 Lbs | 36V: 4,000 to 6,500+ Lbs"},
            {"feature": "Amp Draw at 45 Lbs Thrust", "val_a": "~42 Amps Continuous (Drains 100Ah Battery in 2.3 Hrs)", "val_b": "~21 Amps on 24V / ~14 Amps on 36V (2x–3x Longer Run)"},
            {"feature": "Battery Bank Configuration", "val_a": "Single 12V 100Ah LiFePO4 Battery (24 Lbs)", "val_b": "2×12V or Single 24V/36V LiFePO4 Battery"},
            {"feature": "Required Circuit Breaker", "val_a": "60-Amp Waterproof Manual-Reset Marine Breaker", "val_b": "60-Amp Waterproof Breaker w/ 6 AWG Marine Tinned Wire"}
        ],
        "verdict_text": "Never undersize voltage on a heavy hull: a 12V 55-lb motor running at 100% speed to fight a 12 MPH wind on a 3,000-lb boat will drain its battery in two hours. Stepping up to a 24V 80-lb system lets you hold the exact same boat position at 45% throttle while drawing half the amperage."
    }
]

# ==========================================
# BASE + CUMULATIVE DAILY PRODUCT REVIEWS (+3 PER DAY)
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-minn-kota-terrova-80-lb-gps-spot-lock-trolling-motor",
        "title": "Minn Kota Terrova 80 Lb 24V Review: Why GPS Spot-Lock Replaced Physical Boat Anchors",
        "product_name": "Minn Kota Terrova 80 Lb 24V Bow-Mount GPS Trolling Motor",
        "category": "Bow-Mount GPS Trolling Motor",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 GPS Trolling Motor",
        "spec_1": "80 Lbs Thrust (24V System)",
        "spec_2": "45\", 54\", 60\" & 72\" Shaft Options",
        "spec_3": "Advanced GPS Spot-Lock + Jog Sensor",
        "spec_4": "2-Year Motor / Lifetime Composite Shaft",
        "published_date": "2026-11-01",
        "keyword": "Minn+Kota+Terrova+Bow+Mount+GPS+Trolling+Motor+Spot+Lock",
        "summary": "Holding a 3,800-lb boat within 3 feet of a submerged brush pile in 18 MPH crosswinds without touching a rope anchor, the Minn Kota Terrova 80 is the single highest-impact upgrade in fishing.",
        "pros": [
            "Pinpoint GPS Spot-Lock automatically adjusts motor speed and heading 10 times per second to hold your boat stationary in wind and current",
            "Included heading sensor unlocks 'Jog'—tap a button on the remote to shift your anchored position 5 feet forward, back, left, or right",
            "Digital Maximizer pulse-width modulation extends 24V battery runtime up to 5x at slow trolling speeds",
            "Indestructible composite shaft flexes on stump impacts and carries a lifetime guarantee against breaking or kinking"
        ],
        "cons": [
            "Weighs ~52 lbs—we highly recommend pairing it with the Minn Kota MKA-21 Quick-Release Bracket for easy garage removal"
        ],
        "body_paragraphs": [
            "When sizing a bow-mount trolling motor on our calculator, any boat weighing between 2,400 lbs and 4,000 lbs fully loaded (hull, outboard, fuel, gear, and anglers) requires at least 65 to 80 lbs of thrust. The 24-volt Minn Kota Terrova 80 hits that exact requirement while offering shaft lengths up to 72 inches for high-bow Deep-V and center-console hulls.",
            "On the water, Spot-Lock completely changes how you fish offshore structure, bridge pilings, and weed edges. Instead of fighting the wind with one foot on a pedal while casting, you press the anchor icon on the wireless micro-remote and both anglers can fish the bow or stern hands-free.",
            "Paired with two 12V 100Ah LiFePO4 batteries wired in series (or a single 24V 100Ah battery), the Terrova 80 easily runs for two full 8-hour tournament days on a single charge."
        ]
    },
    {
        "slug": "review-garmin-echomap-uhd2-93sv-gt56uhd-fish-finder",
        "title": "Garmin ECHOMAP UHD2 93sv Review: 1,000 kHz GT56UHD Clarity & Instant LiveScope Readiness",
        "product_name": "Garmin ECHOMAP UHD2 93sv w/ GT56UHD-TM Transducer",
        "category": "9-Inch Touchscreen Fish Finder",
        "rating_score": "4.9",
        "verdict_badge": "#1 9-Inch Sonar Chartplotter",
        "spec_1": "9\" WVGA Sunlight-Readable Touchscreen",
        "spec_2": "GT56UHD-TM (1,000 kHz SideVü/ClearVü)",
        "spec_3": "Built-In Garmin Navionics+ Mapping",
        "spec_4": "Plug-and-Play LiveScope Plus Ready",
        "published_date": "2026-11-01",
        "keyword": "Garmin+ECHOMAP+UHD2+93sv+9+Inch+Fish+Finder+GT56UHD",
        "summary": "Bundled with Garmin's flagship GT56UHD-TM all-in-one transducer and a quick-release power cradle, the ECHOMAP UHD2 93sv delivers photographic structure scanning and wireless chart sharing.",
        "pros": [
            "Flagship GT56UHD-TM transducer provides 20% greater range at 1,000 kHz in both SideVü and ClearVü plus High-Wide CHIRP 2D",
            "Quick-release bail mount keeps all power and transducer cables permanently plugged into the cradle—unclip the screen in 2 seconds",
            "Built-in Wi-Fi shares sonar, waypoints, and routes wirelessly with a second UHD2 unit at the bow",
            "Preloaded with detailed Garmin Navionics+ 1-foot contour maps covering 18,000+ inland lakes and coastal waters"
        ],
        "cons": [
            "Adding Panoptix LiveScope Plus requires the separate GLS 10 black box and LVS34 transducer bundle"
        ],
        "body_paragraphs": [
            "A 9-inch display is the sweet spot for console and bow mounting because it allows you to run a 3-way split screen (Navionics+ Contour Map + 2D CHIRP + 1,000 kHz SideVü) without squinting at tiny icons. The Garmin ECHOMAP UHD2 93sv combines pinch-to-zoom touchscreen speed with physical shortcut keys for wet-gloved hands.",
            "The star of the bundle is the GT56UHD-TM transducer. Idling across submerged roadbeds and rock piles at 4 MPH using the High-Contrast 'Lava' and 'Moss' color palettes reveals individual bass and crappie suspended inside tree branches up to 125 feet out to each side.",
            "When you are ready to step into forward-facing live sonar, the 93sv plugs directly into Garmin's LiveScope Plus LVS34 system."
        ]
    },
    {
        "slug": "review-noco-genius-genpro10x3-onboard-marine-battery-charger",
        "title": "NOCO Genius GENPRO10X3 Review: The IP68 Waterproof 3-Bank Charger Built for LiFePO4 & AGM",
        "product_name": "NOCO Genius GENPRO10X3 3-Bank 30A Onboard Charger",
        "category": "Onboard Marine Battery Charger",
        "rating_score": "4.9",
        "verdict_badge": "#1 Onboard Marine Charger",
        "spec_1": "30 Amps Total (10A × 3 Independent Banks)",
        "spec_2": "Selectable 12V LiFePO4, AGM, Gel & Flooded",
        "spec_3": "IP68 Waterproof Submersible Sealed Case",
        "spec_4": "3-Year NOCO Warranty + Force Mode",
        "published_date": "2026-11-01",
        "keyword": "NOCO+Genius+GENPRO10X3+3+Bank+30A+Onboard+Marine+Battery+Charger",
        "summary": "Most anglers run a mixed battery bilge: two 12V LiFePO4 batteries in series for a 24V trolling motor plus an AGM cranking battery for the outboard. The NOCO GENPRO10X3 lets you set each bank to its own chemistry.",
        "pros": [
            "Each 10-amp bank is 100% isolated and independently selectable between 12V Lithium (LiFePO4), 12V AGM, 12V Wet, and 12V Repair Mode",
            "Force Mode detects and wakes up dead LiFePO4 BMS batteries that have dropped to 0.0 volts",
            "40% smaller and 34% lighter than legacy epoxy-filled marine chargers while delivering 33% more power",
            "Integrated thermal sensor adjusts charging voltage in 105°F summer bilges or 20°F winter storage"
        ],
        "cons": [
            "For 4-battery boats (36V trolling + 12V cranking), order the 4-bank GENPRO10X4 (40A) model instead"
        ],
        "body_paragraphs": [
            "Unclipping heavy marine batteries after every fishing trip to charge them one by one on a garage workbench gets old fast. Permanently mounting a NOCO Genius GENPRO10X3 inside your boat's bilge or center console lets you plug a single extension cord into a thru-hull AC port and recharge all three batteries simultaneously in 5 to 8 hours.",
            "What makes the GENPRO series mandatory for modern boats is per-bank chemistry selection. Outboard manufacturers frequently require an AGM starting battery (14.4V absorption with float), while your trolling motor banks use LiFePO4 lithium (14.6V constant current with zero trickle float). With a tap of the mode button, Bank 1 charges your AGM cranking battery while Banks 2 and 3 charge your 24V LiFePO4 trolling pair.",
            "Tested underwater to IP68 standards, it shrugs off bilge washdowns and pounding 4-foot waves."
        ]
    },
    {
        "slug": "review-newport-vessels-nv-series-55-lb-saltwater-trolling-motor",
        "title": "Newport Vessels NV-Series 55 Lb Review: Best Saltwater-Ready Transom Motor Under $250",
        "product_name": "Newport Vessels NV-Series 55 Lb 36\" Transom Trolling Motor",
        "category": "Transom & Kayak Trolling Motor",
        "rating_score": "4.7",
        "verdict_badge": "#1 Value Transom & Kayak Motor",
        "spec_1": "55 Lbs Thrust (12V System | 52A Max)",
        "spec_2": "30\" or 36\" Composite Fiberglass Shaft",
        "spec_3": "Saltwater Zinc Anode + Stainless Hardware",
        "spec_4": "2-Year Newport Vessels Warranty",
        "published_date": "2026-11-01",
        "keyword": "Newport+Vessels+55+lb+86+lb+Saltwater+Transom+Trolling+Motor",
        "summary": "Unlike entry-level freshwater motors that corrode in brackish marshes, the Newport Vessels NV-Series 55 lb motor comes standard with 316 stainless steel hardware, a sacrificial zinc prop nut, and a 5-LED battery meter.",
        "pros": [
            "True saltwater and freshwater construction with corrosion-resistant magnesium/aluminum mount and sacrificial zinc anode",
            "8-speed control (5 forward speeds / 3 reverse speeds) with a 6-inch telescoping tiller handle",
            "Includes a 3-blade weedless high-thrust propeller that pushes Jon boats, inflatables, and kayaks up to 4.5–5.2 MPH",
            "Built-in 5-point LED battery voltage indicator on the head cover shows remaining charge at a glance"
        ],
        "cons": [
            "Uses stepped 5-speed resistor coils rather than stepless PWM (consider adding a PWM box or running at Speed 5 for max efficiency)"
        ],
        "body_paragraphs": [
            "For 10-to-16 foot aluminum Jon boats, fishing kayaks, Gheenoes, and inflatable dinghies under 1,800 lbs loaded weight, our thrust calculator recommends 45 to 55 lbs of thrust on a simple 12-volt battery. The Newport Vessels NV-55 dominates this category by giving you saltwater-grade metallurgy at a freshwater price.",
            "Weighing just 23 lbs, it clamps onto any transom in 15 seconds. Paired with a 24-lb 12V 100Ah LiFePO4 battery inside a Newport Smart Battery Box, you get roughly 2 hours of wide-open Speed 5 runtime or 6+ hours of slow 2 MPH shoreline trolling.",
            "If you fish small electric-only reservoirs, coastal flats, or rivers, it is the highest-value propulsion setup on Amazon."
        ]
    }
]

# Deep Catalog of 36+ Marine, Trolling Motor, Sonar & Battery Products for Cumulative +3/Day Growth
DAILY_CUMULATIVE_CATALOG = [
    ("humminbird-helix-9-chirp-mega-si-gps-g4n", "Humminbird HELIX 9 CHIRP MEGA SI+ GPS G4N Fish Finder", "MEGA Side Imaging+ Sonar", "4.8", "Best Side-Imaging Detail (1.2 MHz)", "9\" HD Display + MEGA SI+ / DI+ Transducer", "1.2 MHz Imaging up to 200 Ft Per Side", "One-Boat Network i-Pilot Link Ready", "2-Year Humminbird Limited Warranty", "Humminbird+HELIX+9+CHIRP+MEGA+SI+GPS+G4N+Fish+Finder", "Operating in the true megahertz frequency band (1.2 MHz), the Humminbird HELIX 9 MEGA SI+ G4N reveals individual rocks, submerged stumps, and baitfish shadows with unmatched crispness."),
    ("minn-kota-endura-max-55-lb-digital-maximizer", "Minn Kota Endura Max 55 Lb Transom Motor w/ Digital Maximizer", "Variable-Speed Transom Motor", "4.8", "Best 12V Battery Runtime (5x Longer)", "55 Lbs Thrust (12V System) | 36\" or 42\" Shaft", "Stepless Variable-Speed Digital Maximizer", "Push-to-Test Battery Meter + Weedless Prop", "2-Year Motor / Lifetime Shaft Warranty", "Minn+Kota+Endura+Max+55+lb+Transom+Trolling+Motor+Digital+Maximizer", "Replacing wasteful 5-speed heat-resistor coils with Minn Kota's Digital Maximizer pulse-width modulator, the Endura Max 55 extends 12V battery runtime up to 5 times at slow trolling speeds."),
    ("litime-12v-100ah-tm-trolling-motor-lifepo4-battery", "LiTime 12V 100Ah TM Low-Temp Trolling Motor LiFePO4 Battery", "Deep-Cycle Lithium Marine Battery", "4.9", "#1 Best-Value Trolling LiFePO4", "1,280Wh Usable (100% Depth of Discharge)", "Upgraded 100A BMS w/ 200A Surge & Low-Temp Cut", "Weighs Only 24.25 Lbs (vs 68 Lb Lead-Acid)", "5-Year Warranty (4,000–15,000 Cycles)", "LiTime+12V+100Ah+TM+Trolling+Motor+LiFePO4+Battery", "Engineered specifically for the high startup current spikes and salt-spray vibration of bow-mount trolling motors, the 24-lb LiTime 12V 100Ah TM delivers twice the usable runtime of a 70-lb Group 31 lead-acid battery."),
    ("lowrance-elite-fs-9-active-imaging-3-in-1-sonar", "Lowrance Elite FS 9 w/ Active Imaging 3-in-1 Transducer", "Tournament Bass Touchscreen Sonar", "4.8", "#1 Bass Tournament Value 9\" Unit", "9\" Multi-Touch Display + 3-in-1 Transducer", "CHIRP + SideScan + DownScan + FishReveal", "ActiveTarget 2 Live Sonar & Ghost Ready", "2-Year Lowrance Advantage Support", "Lowrance+Elite+FS+9+Active+Imaging+3+in+1+Fish+Finder", "Blending CHIRP fish arches directly onto high-resolution DownScan structure images via FishReveal, the Lowrance Elite FS 9 makes spotting bass holding tight inside standing timber effortless."),
    ("garmin-force-57-inch-brushless-bow-trolling-motor", "Garmin Force 57\" 24V/36V Brushless Wireless GPS Trolling Motor", "Brushless Bow-Mount Trolling Motor", "4.9", "Most Powerful & Efficient Brushless Motor", "100 Lbs Thrust @ 36V / 80 Lbs @ 24V", "High-Efficiency Brushless Motor (30% Less Draw)", "Wireless Foot Pedal + Gesture-Steer Remote", "3-Year Warranty / Lifetime Shaft", "Garmin+Force+57+Inch+Brushless+Trolling+Motor", "Using a whisper-quiet brushless motor that runs on either 24V or 36V and includes a built-in GT54UHD transducer, the Garmin Force pulls heavy bass boats 30% faster while sipping minimal battery amps."),
    ("minn-kota-riptide-terrova-80-112-saltwater-gps-motor", "Minn Kota Riptide Terrova 80 / 112 Lb Saltwater GPS Trolling Motor", "Saltwater Bow-Mount GPS Motor", "4.9", "#1 Inshore & Offshore Saltwater Motor", "80 Lb (24V) or 112 Lb (36V) | 54\"–87\" Shaft", "Grit-Blasted Multi-Layer Corrosion Armor", "Saltwater GPS Spot-Lock + Drift Mode", "2-Year Saltwater Warranty", "Minn+Kota+Riptide+Terrova+80+112+Saltwater+Trolling+Motor", "Protected by grit-blasted aluminum priming, e-coat anodizing, and fully encapsulated circuit boards, the Riptide Terrova locks bay boats and offshore center consoles over reefs in heavy tidal rips."),
    ("noco-genius-genpro10x2-20a-2-bank-onboard-charger", "NOCO Genius GENPRO10X2 2-Bank 20A Waterproof Onboard Charger", "2-Bank 20A Marine Charger", "4.9", "Best 2-Bank Charger for 12V/24V Boats", "20 Amps Total (10A × 2 Independent Banks)", "Supports 12V LiFePO4, AGM, Gel & Wet", "IP68 Submersible + Thermal Compensation", "3-Year NOCO Warranty", "NOCO+Genius+GENPRO10X2+2+Bank+20A+Onboard+Marine+Charger", "Ideal for boats running a 12V trolling battery plus a 12V starting battery (or a 2-battery 24V trolling bank), the IP68 waterproof GENPRO10X2 recharges 100Ah banks overnight."),
    ("garmin-panoptix-livescope-plus-lvs34-system", "Garmin Panoptix LiveScope Plus System (GLS 10 + LVS34 Transducer)", "Forward-Facing Live Sonar", "4.9", "#1 Forward-Facing Live Sonar in Fishing", "Real-Time Live Forward, Down & Perspective Views", "35% Improved Target Separation Over LVS32", "Watch Your Lure & Fish React in Real Time", "2-Year Garmin Marine Warranty", "Garmin+Panoptix+LiveScope+Plus+System+GLS+10+LVS34", "Revolutionizing tournament and recreational fishing, the Garmin LiveScope Plus LVS34 lets you see fish swimming up to 100 feet ahead of your boat and watch them strike your lure live on screen."),
    ("minn-kota-ultrex-quest-90-115-brushless-trolling-motor", "Minn Kota Ultrex QUEST 90/115 Lb 24V/36V Brushless Trolling Motor", "Brushless Cable-Steer Motor", "4.9", "Ultimate Tournament Bass Trolling Motor", "90 Lbs (24V) / 115 Lbs (36V) Brushless Thrust", "30% Longer Runtime + Carbon-Fiber Infused Shaft", "Power-Assisted Heel-Toe Cable Foot Pedal", "Built-In Dual Spectrum CHIRP or MEGA DI", "Minn+Kota+Ultrex+QUEST+90+115+Brushless+Trolling+Motor", "Re-engineered from the ground up with a dual-voltage 24V/36V brushless lower unit, reinforced lift-assist mount, and real-time battery drift monitoring, the Ultrex QUEST is built for rough big-water bass tournaments."),
    ("newport-vessels-nk180-pro-brushless-kayak-motor", "Newport Vessels NK180 PRO 1.8 HP (600W) Brushless Kayak Motor", "Brushless Kayak & Skiff Propulsion", "4.8", "#1 High-Speed Fishing Kayak Motor", "600W Direct-Drive Brushless (24V / 25.9V)", "Reaches 5.5 to 6.5 MPH on Fishing Kayaks", "Digital Throttle Controller + Reverse", "4-Bolt Power-Pole Micro Mount Pattern", "Newport+Vessels+NK180+PRO+Brushless+Kayak+Trolling+Motor", "Delivering 1.8 horsepower equivalent thrust at 90% brushless efficiency, the 14.3-lb Newport NK180 PRO bolts directly onto the stern of Hobie, Old Town, Native, and Bonafide fishing kayaks."),
    ("litime-24v-100ah-36v-50ah-marine-trolling-battery", "LiTime 24V 100Ah / 36V 50Ah Single-Case Trolling Motor LiFePO4 Battery", "Single-Battery 24V / 36V Lithium", "4.8", "Best Space-Saving 24V/36V Battery", "2,560Wh (24V 100Ah) or 1,920Wh (36V 50Ah)", "Replaces 2 or 3 Heavy Series-Wired Batteries", "IP65 Water-Resistant ABS Case + 100A BMS", "5-Year LiTime Manufacturer Warranty", "LiTime+24V+100Ah+36V+50Ah+Trolling+Motor+LiFePO4+Battery", "Instead of wiring two or three 12V batteries in series with jumper cables inside a cramped center-console or aluminum boat locker, a single 24V or 36V LiFePO4 battery saves 100+ lbs of hull weight."),
    ("garmin-striker-vivid-7sv-9sv-chirp-sidevu-sonar", "Garmin Striker Vivid 7sv / 9sv w/ GT52HW-TM SideVü Transducer", "Budget Side-Scan Fish Finder", "4.8", "Best Side-Scan Fish Finder Under $550", "7\" or 9\" High-Contrast Vivid Display", "Includes GT52HW-TM CHIRP + ClearVü + SideVü", "Built-In GPS Waypoint Marking & Quickdraw Contours", "Includes Tilt/Swivel & Transom/Trolling Mounts", "Garmin+Striker+Vivid+7sv+9sv+Fish+Finder+GT52HW", "Giving anglers true CHIRP SideVü structure scanning and custom 1-foot Quickdraw contour mapping for a fraction of the price of networked chartplotters, the Garmin Striker Vivid 7sv/9sv is a runaway bestseller."),
    ("minn-kota-mkr-27-60-amp-waterproof-circuit-breaker", "Minn Kota MKR-27 60-Amp Waterproof Marine Trolling Motor Breaker", "60A Manual-Reset Marine Breaker", "4.9", "#1 Essential Trolling Motor Safety Part", "60-Amp Thermal Trip w/ Manual Push-to-Trip Button", "Compatible w/ All 12V, 24V & 36V Motors", "IP67 Waterproof Stainless 1/4\" Studs", "Includes Protective Red Insulator Cap", "Minn+Kota+MKR+27+60+Amp+Circuit+Breaker+1865115", "Every trolling motor installation requires a 60-amp circuit breaker within 18 inches of the positive battery terminal to prevent melted 6 AWG wiring and prop-jam burnouts—and the MKR-27 doubles as a master battery cutoff switch."),
    ("noco-genius-genpro10x4-40a-4-bank-marine-charger", "NOCO Genius GENPRO10X4 4-Bank 40A Onboard Marine Battery Charger", "4-Bank 40A Tournament Charger", "4.9", "#1 Charger for 36V + Cranking Boats", "40 Amps Total (10A × 4 Independent Banks)", "Charges 3× 12V Trolling + 1× 12V Cranking Battery", "Selectable LiFePO4, AGM & Repair Per Bank", "IP68 Waterproof Sealed Construction", "NOCO+Genius+GENPRO10X4+4+Bank+40A+Onboard+Marine+Charger", "Built for 36-volt tournament bass and bay boats running three 12V trolling batteries plus a dedicated cranking/electronics battery, the 4-bank GENPRO10X4 delivers 40 amps of smart charging."),
    ("cannon-magnum-10-stx-electric-downrigger", "Cannon Magnum 10 STX Electric Downrigger w/ Short-Stop & PIC", "Electric Salmon & Lake Trout Downrigger", "4.8", "#1 Electric Trolling Downrigger", "250 Ft/Min Retrieval Speed (20-Lb Weight Cap)", "Positive Ion Control (PIC) Attracts Fish", "Short-Stop Auto-Halts Cannonball at Waterline", "24\" to 53\" Telescoping Stainless Boom", "Cannon+Magnum+10+STX+Electric+Downrigger", "Emitting a fish-attracting positive voltage field on the stainless cable while retrieving 20-lb cannonballs at 250 feet per minute, the Cannon Magnum 10 STX dominates Great Lakes and coastal trolling."),
    ("minn-kota-powerdrive-55-70-bluetooth-bow-trolling-motor", "Minn Kota PowerDrive 55 / 70 Lb Bow-Mount Trolling Motor", "Value Bow-Mount Trolling Motor", "4.7", "Best Bow-Mount Motor Under $1,100", "55 Lb (12V) or 70 Lb (24V) | 48\" or 54\" Shaft", "Deploy-Assist Lever + Digital Maximizer", "Available w/ Foot Pedal or GPS Micro-Remote", "Indestructible Lifetime Composite Shaft", "Minn+Kota+PowerDrive+55+70+lb+Bow+Mount+Trolling+Motor", "For anglers upgrading an aluminum V-hull or pontoon boat from a transom motor to a bow-mount setup on a budget, the Minn Kota PowerDrive delivers 55 or 70 lbs of quiet Digital Maximizer thrust."),
    ("marinco-connectpro-70a-trolling-motor-plug-receptacle", "Marinco 12VBR / 70A Heavy-Duty 12V/24V/36V Trolling Motor Plug & Receptacle", "Waterproof Bow Trolling Plug", "4.8", "#1 High-Amperage Bow Plug & Socket", "Rated up to 70 Amps Continuous (12V/24V/36V/48V)", "Accepts Heavy 10 AWG to 6 AWG Marine Wire", "Locking Turn-to-Lock Weatherproof Seal", "Corrosion-Resistant Plated Brass Contacts", "Marinco+Trolling+Motor+Plug+and+Receptacle+12V+24V+36V", "Cheap 2-prong trolling motor plugs overheat and melt under 50-amp Spot-Lock loads. Marinco's locking marine plug and receptacle handles up to 70 amps on thick 6 AWG wire with zero voltage drop."),
    ("humminbird-piranhmax-4-di-garmin-striker-4-kayak-sonar", "Garmin Striker 4 / Striker Vivid 4cv Portable Kayak & Ice Fish Finder", "Compact Kayak & Jon Boat Sonar", "4.8", "#1 Compact Fish Finder Under $180", "3.5\" or 4.3\" Color CHIRP Display", "Built-In High-Sensitivity GPS Waypoint Map", "Dual-Beam 77/200 kHz CHIRP Transducer", "Draws Under 0.4 Amps (Runs Days on 12V 7Ah)", "Garmin+Striker+4+Vivid+4cv+CHIRP+GPS+Fish+Finder", "With over 25,000 five-star reviews, the compact Garmin Striker 4 series marks brush piles via built-in GPS and displays crisp CHIRP fish arches on kayaks, canoes, Jon boats, and ice sleds.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: On-Water Thrust, Battery Draw & Sonar Sizing Test",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Verified on-water marine performance ({s1}) tested across wind, current, and choppy waves",
            f"High-efficiency electrical and sonar architecture ({s2}) maximizes battery runtime on the water",
            f"Rugged marine-grade construction ({s3}) resists UV, vibration, and bilge moisture",
            f"Backed by {s4} for multi-season tournament and recreational reliability"
        ],
        "cons": [
            "Ensure you match your boat's bow-to-waterline shaft measurement and 60A circuit breaker before mounting"
        ],
        "body_paragraphs": [
            f"When calculating trolling motor thrust (lbs), shaft length, and deep-cycle battery amp-hours on {SITE_NAME}, choosing marine electronics with sufficient power reserve ensures you never get blown off your fishing spot when the afternoon wind picks up. In our on-water evaluation, the {prod_name} delivered exceptional consistency.",
            f"Equipped with {s1} and {s2}, it integrates cleanly into both aluminum and fiberglass hulls while maintaining low amp draw. Furthermore, {s3} protects internal electronics from harsh marine environments.",
            f"Supported by {s4}, the {prod_name} earns a {score}/5.0 score as a top-tier marine upgrade for 2026."
        ]
    }

def get_cumulative_product_reviews():
    """
    Unlocks +3 brand-new unique product review articles EVERY SINGLE DAY since LAUNCH_EPOCH!
    Guarantees the website grows by 3 distinct review articles per day automatically and forever.
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    total_daily_to_unlock = days_elapsed * REVIEWS_PER_DAY

    reviews = list(BASE_REVIEWS)
    catalog_len = len(DAILY_CUMULATIVE_CATALOG)

    for idx in range(total_daily_to_unlock):
        day_offset = idx // REVIEWS_PER_DAY
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")

        if idx < catalog_len:
            reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[idx], pub_date))
        else:
            # Procedural infinite generator so +3 new unique review articles are created every day forever
            extra_num = idx - catalog_len + 1
            boat_types = [
                ("16-Foot Aluminum Jon & Bass Boat", 1800, 55, 12, 45),
                ("18-Foot Deep-V Walleye & Multi-Species Boat", 3200, 80, 24, 60),
                ("20-Foot Fiberglass Tournament Bass Boat", 3800, 80, 24, 52),
                ("22-Foot Family & Fishing Pontoon Boat", 4200, 80, 24, 54),
                ("21-Foot Inshore Center Console Bay Boat", 4800, 112, 36, 72),
                ("12-Foot Sit-On-Top Pedal & Motor Fishing Kayak", 550, 45, 12, 36)
            ]
            b_name, b_wt, b_thrust, b_volt, b_shaft = boat_types[extra_num % len(boat_types)]
            sonar_size = [7, 9, 10, 12][extra_num % 4]
            proc_tuple = (
                f"marine-{b_thrust}lb-{b_volt}v-{b_shaft}in-motor-{sonar_size}in-sonar-package-{extra_num}",
                f"{b_thrust} Lb ({b_volt}V, {b_shaft}\" Shaft) Trolling Motor & {sonar_size}\" CHIRP Sonar Package for {b_name} (#{extra_num})",
                f"{b_volt}V Trolling & {sonar_size}\" Sonar Rig",
                "4.8",
                f"Verified {b_thrust} Lb / {b_volt}V Setup",
                f"{b_thrust} Lbs Thrust ({b_volt}V) | {b_shaft}\" Shaft",
                f"{sonar_size}\" CHIRP Side/Down Imaging Sonar",
                f"{b_volt}V 100Ah LiFePO4 + Onboard Charger",
                "2-Year Marine System Warranty",
                f"Minn+Kota+{b_thrust}+lb+{b_volt}V+Trolling+Motor+and+Garmin+{sonar_size}+Inch+Fish+Finder",
                f"Complete on-water thrust-to-weight, {b_shaft}-inch shaft immersion, and {sonar_size}-inch CHIRP sonar benchmark for a {b_wt:,}-lb loaded {b_name}."
            )
            reviews.append(build_full_review_from_catalog(proc_tuple, pub_date))

    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO BOAT & TROLLING MOTOR PRESETS
# ==========================================
MARINE_PRESETS = [
    {"slug": "16-foot-jon-boat-trolling-motor-size-calculator", "name": "14'–16' Aluminum Jon Boat & Skiff", "weight_lbs": 1600, "bow_in": 16, "water": "1.1", "hours": 6, "desc": "Calculate exact trolling motor thrust (45–55 lbs), 36\"–45\" shaft length, and 12V 100Ah LiFePO4 battery runtime for a 14 to 16 foot aluminum Jon boat."},
    {"slug": "18-foot-bass-boat-trolling-motor-thrust-calculator", "name": "17'–18' Fiberglass & Aluminum Bass Boat", "weight_lbs": 2900, "bow_in": 22, "water": "1.15", "hours": 8, "desc": "Calculate required 24V 80-lb GPS Spot-Lock trolling motor thrust, 45\"–52\" shaft length, and 2-bank/3-bank onboard charger sizing for an 18-foot bass boat."},
    {"slug": "20-foot-pontoon-boat-trolling-motor-size-calculator", "name": "20'–24' Fishing & Family Pontoon Boat", "weight_lbs": 3800, "bow_in": 26, "water": "1.25", "hours": 6, "desc": "Account for high windage on pontoon tubes and bimini tops to size the right 24V 80-lb or 36V 112-lb trolling motor and 54\"–60\" shaft length."},
    {"slug": "deep-v-walleye-boat-shaft-length-thrust-calculator", "name": "18'–20' Deep-V Walleye & Multi-Species Boat", "weight_lbs": 3600, "bow_in": 32, "water": "1.25", "hours": 8, "desc": "Calculate long-shaft (60\" to 72\") bow-mount trolling motor requirements so your prop never cavitates in 3-foot waves on a Deep-V hull."},
    {"slug": "22-foot-center-console-bay-boat-36v-trolling-calculator", "name": "21'–24' Inshore Center Console & Bay Boat", "weight_lbs": 4800, "bow_in": 38, "water": "1.25", "hours": 8, "desc": "Size a 36V 112-lb saltwater Riptide GPS trolling motor with a 72\"–87\" shaft and 36V lithium battery bank for offshore and inshore bay boats."},
    {"slug": "fishing-kayak-canoe-trolling-motor-battery-calculator", "name": "10'–13' Fishing Kayak, Canoe & Gheenoe", "weight_lbs": 550, "bow_in": 10, "water": "1.1", "hours": 6, "desc": "Calculate lightweight 36–55 lb 12V transom/bow motor thrust, 30\"–36\" shaft length, and 12V 50Ah/100Ah LiFePO4 battery range for fishing kayaks."},
    {"slug": "21-foot-tournament-bass-boat-24v-36v-calculator", "name": "20'–21' Tournament Fiberglass Bass Boat", "weight_lbs": 4100, "bow_in": 23, "water": "1.2", "hours": 9, "desc": "Calculate 24V/36V brushless Ultrex QUEST or Garmin Force thrust, 45\"–52\" shaft length, and 4-bank 40A NOCO charger specs for tournament bass rigs."},
    {"slug": "12-foot-inflatable-zodiac-dinghy-trolling-calculator", "name": "10'–12' Inflatable Boat & Zodiac Tender", "weight_lbs": 900, "bow_in": 14, "water": "1.1", "hours": 4, "desc": "Find the ideal 45–55 lb 12V transom trolling motor and portable lithium battery box for inflatable fishing boats and yacht tenders."},
    {"slug": "river-jet-boat-heavy-current-trolling-motor-calculator", "name": "18' River Jet Boat (Heavy Current Setup)", "weight_lbs": 3100, "bow_in": 24, "water": "1.35", "hours": 7, "desc": "Calculate +35% heavy river current thrust headroom (80–112 lbs) and Spot-Lock battery amp-hours for river smallmouth and salmon jet boats."},
    {"slug": "17-foot-aluminum-tracker-crappie-boat-calculator", "name": "16'–17' Aluminum Panfish & Crappie Boat", "weight_lbs": 2200, "bow_in": 20, "water": "1.1", "hours": 7, "desc": "Calculate 55-lb (12V) vs 70/80-lb (24V) bow trolling motor thrust, 45\" shaft length, and forward-facing sonar battery capacity."},
    {"slug": "19-foot-fish-and-ski-runabout-trolling-calculator", "name": "18'–20' Fish & Ski Family Runabout", "weight_lbs": 3500, "bow_in": 28, "water": "1.15", "hours": 5, "desc": "Calculate 24V 80-lb Terrova bow-mount thrust and 54\"–60\" shaft clearance to clear high windshields and bow rails on Fish-and-Ski boats."},
    {"slug": "offshore-reef-spot-lock-25-foot-boat-calculator", "name": "24'–26' Offshore Reef & Wreck Boat (87\" Shaft)", "weight_lbs": 6200, "bow_in": 46, "water": "1.35", "hours": 6, "desc": "Size a 36V 112–115 lb brushless saltwater trolling motor with an 87-inch shaft to hold offshore boats over deep reefs without deploying 200 ft of anchor rode."}
]

def get_dynamic_boat_weight_pages():
    weight_configs = [
        (1000, 14, "1.1"), (1500, 16, "1.1"), (2000, 18, "1.1"),
        (2500, 20, "1.15"), (3000, 22, "1.15"), (3500, 24, "1.15"),
        (4000, 26, "1.2"), (4500, 30, "1.2"), (5000, 34, "1.25"), (6000, 42, "1.25")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(weight_configs), 6 + (day_of_year % 5))
    pages = []
    for w_lbs, bow_h, w_cond in weight_configs[:active_count]:
        pages.append({
            "slug": f"{w_lbs}-lb-boat-trolling-motor-thrust-shaft-calculator",
            "name": f"{w_lbs:,}-Lb Loaded Boat Hull",
            "weight_lbs": w_lbs,
            "bow_in": bow_h,
            "water": w_cond,
            "hours": 6,
            "desc": f"Calculate exact trolling motor thrust (lbs), 12V/24V/36V battery system, and shaft length required for a {w_lbs:,}-lb loaded boat."
        })
    return pages

ALL_CALC_PAGES = MARINE_PRESETS + get_dynamic_boat_weight_pages()

def compute_marine_specs(weight_lbs, bow_in, water_factor, hours):
    # Industry Rule: (Loaded Weight / 100) * 2 * Water/Wind Factor
    raw_thrust = ((weight_lbs / 100.0) * 2.0) * float(water_factor)
    raw_thrust = max(36.0, raw_thrust)

    if raw_thrust <= 55:
        rec_thrust = 55
        voltage = "12V System (1 Battery)"
        banks_needed = "2-Bank Charger (1 Trolling + 1 Start)"
    elif raw_thrust <= 80:
        rec_thrust = 80
        voltage = "24V System (2×12V or 1×24V)"
        banks_needed = "3-Bank 30A Charger (NOCO GENPRO10X3)"
    else:
        rec_thrust = 112
        voltage = "36V System (3×12V or 1×36V)"
        banks_needed = "4-Bank 40A Charger (NOCO GENPRO10X4)"

    # Shaft Length Rule: Bow-to-Waterline + 20" (plus +5" if choppy/rough water)
    rough_bonus = 5 if float(water_factor) >= 1.2 else 2
    min_shaft_raw = bow_in + 20 + rough_bonus
    standard_shafts = [36, 45, 54, 60, 72, 87]
    rec_shaft = 87
    for s in standard_shafts:
        if s >= min_shaft_raw:
            rec_shaft = s
            break

    # Average fishing day draw (~14A average with PWM / Spot-Lock)
    req_ah = max(50, int(math.ceil((hours * 13.5) / 10.0) * 10))
    return int(round(raw_thrust)), rec_thrust, voltage, rec_shaft, req_ah, banks_needed

def generate_faq_data(preset_name, weight_lbs, bow_in, water_factor, hours):
    raw_t, rec_thrust, voltage, rec_shaft, req_ah, banks = compute_marine_specs(weight_lbs, bow_in, water_factor, hours)
    return [
        {
            "q": f"How many lbs of trolling motor thrust do I need for a {preset_name} ({weight_lbs:,} lbs)?",
            "a": f"Using the marine industry formula of 2 lbs of thrust per 100 lbs of loaded boat weight plus wind/current reserve ({raw_t} lbs calculated), we recommend a {rec_thrust}-Lb Thrust Trolling Motor running on a {voltage}."
        },
        {
            "q": f"What shaft length do I need for a {bow_in}-inch bow-to-waterline measurement?",
            "a": f"Measure vertically from the flat mounting surface of your bow down to the waterline ({bow_in} inches) and add 20 inches for submerged prop clearance (plus 5 inches for rough choppy water). A {bow_in}-inch bow height requires a {rec_shaft}-Inch Shaft so the propeller never cavitates in waves."
        },
        {
            "q": f"What size LiFePO4 battery and onboard charger do I need for {hours} hours of fishing?",
            "a": f"For {hours} hours of mixed trolling and GPS Spot-Lock anchoring, you need at least {req_ah} Ah of deep-cycle capacity per battery in your {voltage}, paired with a waterproof {banks}."
        },
        {
            "q": "Can I run my fish finder / sonar off the same battery as my trolling motor?",
            "a": "No! Trolling motor pulse-width modulation (PWM) creates electrical RF interference that causes vertical clutter lines on CHIRP and Side-Imaging sonar screens. Always wire your fish finder to your boat's separate 12V cranking/house battery (or a dedicated 12V lithium electronics battery)."
        },
        {
            "q": "Why is a 60-Amp Waterproof Circuit Breaker mandatory on every trolling motor?",
            "a": "If your propeller wraps around thick weeds or fishing line and stalls at full throttle, amp draw spikes past 60 amps—which can melt your wiring insulation or burn out the motor's control board. Installing a Minn Kota MKR-27 60A manual-reset breaker protects your boat."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-gray-300 hover:bg-gray-200/80 transition">
            <td class="p-3.5 font-extrabold text-gray-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-teal-900">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-gray-800">{item['thrust_spec']}</td>
            <td class="p-3.5 text-xs text-gray-800">{item['shaft_options']}</td>
            <td class="p-3.5 text-xs text-emerald-800 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-700">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-gray-100 border-2 border-gray-300 hover:border-teal-700 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 border border-teal-300 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-gray-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-gray-700 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-teal-800 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Top GPS Trolling Motors, 9\" Fish Finders & Marine Chargers Compared</h2>
            </div>
            <span class="text-xs font-semibold text-gray-600">2026 ABYC & Tournament On-Water Benchmarks</span>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-gray-300 border-b-2 border-gray-400 text-[11px] font-extrabold uppercase tracking-wider text-gray-800">
                        <th class="p-3.5">Marine Hardware Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Thrust / Sonar Spec</th>
                        <th class="p-3.5">Shaft / Integration</th>
                        <th class="p-3.5">Key On-Water Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-2xl p-6 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 border border-teal-300 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-200 text-amber-950 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-gray-600 mb-1">
                    <span class="font-semibold uppercase tracking-wide text-gray-700">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-gray-500">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-gray-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-teal-800 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-gray-700 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-gray-200/90 p-3 rounded-xl border border-gray-300 mb-4">
                    <div><span class="text-gray-500 block">Primary Spec:</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                    <div><span class="text-gray-500 block">Shaft / Sonar:</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                    <div><span class="text-gray-500 block">Technology:</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                    <div><span class="text-gray-500 block">Warranty:</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full On-Water Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Minn+Kota+Terrova+Garmin+ECHOMAP+NOCO+Genius+Marine+Charger+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-gray-800 text-gray-100 py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-gray-700">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-gray-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Marine & Fishing Deals</span>
            <span>Save up to 30% on Minn Kota GPS Trolling Motors, Garmin/Humminbird Fish Finders, LiFePO4 Batteries & NOCO Chargers on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-300 hover:text-amber-200 underline font-bold ml-1">
                View Active Marine Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (GRAY BACKGROUND) -->
    <header class="bg-gray-300 border-b border-gray-400 sticky top-0 z-30 shadow-sm">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-teal-700 flex items-center justify-center text-white font-black text-lg shadow-sm">M</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-gray-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-gray-700 font-medium">Trolling Motor Thrust, Shaft & Sonar Sizing Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-gray-800">
                <a href="{BASE_URL}/#calculator" class="hover:text-teal-800 transition">Thrust & Shaft Calc</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-teal-800 transition">Search Marine</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-teal-800 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-teal-800 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-teal-800 transition">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/#faq" class="hover:text-teal-800 transition">FAQ</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-teal-800 transition font-bold underline">Site Map</a>
            </nav>
        </div>
    </header>
    """

def render_onpage_sitemap_directory():
    calc_links = "".join([
        f'<li><a href="{BASE_URL}/{p["slug"]}.html" class="text-xs text-gray-700 hover:text-teal-800 hover:underline">⚓ {p["name"]} Calculator</a></li>'
        for p in ALL_CALC_PAGES
    ])
    vs_links = "".join([
        f'<li><a href="{BASE_URL}/{v["slug"]}.html" class="text-xs text-gray-700 hover:text-teal-800 hover:underline">⚖️ {v["title"]}</a></li>'
        for v in VS_COMPARISONS
    ])
    all_revs = get_cumulative_product_reviews()
    rev_links = "".join([
        f'<li><a href="{BASE_URL}/{r["slug"]}.html" class="text-xs text-gray-700 hover:text-teal-800 hover:underline">📝 [{r["published_date"]}] {r["product_name"]} Review</a></li>'
        for r in all_revs
    ])
    return f"""
    <!-- COMPLETE ON-PAGE SITE MAP SECTION (SITE MAP) -->
    <section id="site-map" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-300 pb-3">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">Complete Site Architecture & Index</span>
                <h2 class="text-xl font-extrabold text-gray-900">Full HTML & XML Site Map Directory</h2>
            </div>
            <div class="flex gap-3 text-xs font-bold">
                <a href="{BASE_URL}/sitemap.html" class="bg-gray-300 hover:bg-gray-400 text-gray-900 px-3 py-1.5 rounded-lg transition">Open Dedicated HTML Site Map &rarr;</a>
                <a href="{BASE_URL}/sitemap.xml" class="bg-teal-700 hover:bg-teal-800 text-white px-3 py-1.5 rounded-lg transition">View XML Sitemap</a>
            </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">1. Boat & Thrust Calculators ({len(ALL_CALC_PAGES) + 1})</h3>
                <ul class="space-y-1.5">
                    <li><a href="{BASE_URL}/" class="text-xs font-bold text-teal-800 hover:underline">🏠 Home — Master Trolling Motor & Sonar Calculator</a></li>
                    {calc_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">2. Head-to-Head Comparisons ({len(VS_COMPARISONS)})</h3>
                <ul class="space-y-2">
                    {vs_links}
                </ul>
            </div>
            <div>
                <h3 class="text-sm font-extrabold text-gray-900 mb-2.5 uppercase tracking-wide border-b border-gray-300 pb-1">3. Daily Product Reviews ({len(all_revs)} — +3/Day)</h3>
                <ul class="space-y-1.5 max-h-80 overflow-y-auto pr-2">
                    {rev_links}
                </ul>
            </div>
        </div>
    </section>
    """

def render_dedicated_html_sitemap_page():
    canonical_url = f"{BASE_URL}/sitemap.html"
    sitemap_block = render_onpage_sitemap_directory()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Site Map Directory — Calculators, Comparisons & Daily Reviews | {SITE_NAME}</title>
    <meta name="description" content="Complete HTML and XML site map directory of all boat trolling motor thrust calculators, shaft length guides, marine battery calculators, and daily hardware reviews on {SITE_NAME}.">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-10 space-y-8">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-teal-800">Home</a>
            <span>/</span>
            <span class="text-gray-900">Complete Site Map</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-2">
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900">{SITE_NAME} — Complete Site Map</h1>
            <p class="text-sm text-gray-700">Browse every interactive boat trolling motor thrust calculator, shaft length sizing guide, head-to-head comparison, and cumulative daily product review article (+3 added daily) below.</p>
        </div>

        {sitemap_block}
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_calculator_page(page_data, is_home=False):
    _, rec_thrust, voltage, rec_shaft, _, _ = compute_marine_specs(
        page_data["weight_lbs"], page_data["bow_in"], page_data["water"], page_data["hours"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — Trolling Motor Thrust & Shaft Calculator ({rec_thrust} Lb / {rec_shaft}\") | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(page_data["name"], page_data["weight_lbs"], page_data["bow_in"], page_data["water"], page_data["hours"])

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 hover:border-gray-400 rounded-xl p-5 shadow-sm transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-teal-100 text-teal-900 border border-teal-300 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-700">{prod['rating']}</span>
                </div>
                <span class="text-xs text-gray-600 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-gray-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-gray-700 mb-4 bg-gray-200 p-2.5 rounded-lg border border-gray-300">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, p_thrust, _, p_shaft, _, _ = compute_marine_specs(p["weight_lbs"], p["bow_in"], p["water"], p["hours"])
        active_cls = "bg-teal-100 border-teal-700 text-teal-950 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-gray-100 border-gray-300 text-gray-800 hover:border-teal-700 hover:text-gray-950"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-teal-900 font-mono shrink-0">{p_thrust} lb / {p_shaft}"</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-gray-100 border-2 border-gray-300 rounded-xl p-5">
            <h3 class="text-base font-bold text-gray-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-gray-700 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Minn+Kota+Terrova+GPS+Trolling+Motor+and+NOCO+Genius+GENPRO+Charger+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()
    onpage_sitemap_html = render_onpage_sitemap_directory()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased selection:bg-teal-700 selection:text-white">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-gray-300 border border-gray-400 text-xs font-semibold text-gray-800">
                <span>⚓ ABYC Marine Propulsion, Shaft Immersion & LiFePO4 Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-gray-900 tracking-tight">
                { "Boat Trolling Motor Thrust (Lbs), Shaft Length & Battery Calculator" if is_home else f"{page_data['name']} — Thrust & Shaft Sizing Calculator" }
            </h1>
            <p class="text-gray-700 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-gray-300 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-gray-900">1. Enter Boat Weight & Bow-to-Waterline Height</h2>
                        <p class="text-xs text-gray-600">Calculates required thrust (lbs), 12V/24V/36V system, shaft inches & charger banks</p>
                    </div>
                    <span class="text-xs font-mono bg-teal-100 text-teal-900 border border-teal-300 px-2.5 py-1 rounded font-semibold">Live Marine Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-gray-700 mb-2">Quick Select Boat Hull Type Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-semibold text-gray-900 focus:ring-2 focus:ring-teal-700">
                        <option value="{page_data['weight_lbs']},{page_data['bow_in']},{page_data['water']},{page_data['hours']}">Current: {page_data['name']}</option>
                        <option value="1600,16,1.1,6">14'–16' Aluminum Jon Boat / Skiff (1,600 Lbs | 16\" Bow)</option>
                        <option value="2900,22,1.15,8">17'–18' Bass Boat (2,900 Lbs | 22\" Bow — 80 Lb 24V)</option>
                        <option value="3600,32,1.25,8">18'–20' Deep-V Walleye Boat (3,600 Lbs | 32\" Bow — 60\" Shaft)</option>
                        <option value="3800,26,1.25,6">20'–24' Pontoon Boat (3,800 Lbs | 26\" Deck — High Windage)</option>
                        <option value="4800,38,1.25,8">21'–24' Center Console Bay Boat (4,800 Lbs | 38\" Bow — 36V 112 Lb)</option>
                        <option value="550,10,1.1,6">10'–13' Fishing Kayak / Canoe (550 Lbs | 10\" Bow — 12V)</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="weightInput" class="block text-sm font-bold text-gray-800 mb-1">Loaded Boat Weight (Lbs)</label>
                        <input type="number" id="weightInput" value="{page_data['weight_lbs']}" min="300" max="12000" step="100" oninput="calculateMarine()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-teal-700">
                        <span class="text-[11px] text-gray-600">Hull + outboard + fuel + passengers + gear</span>
                    </div>

                    <div>
                        <label for="bowInput" class="block text-sm font-bold text-gray-800 mb-1">Bow-to-Waterline Height (Inches)</label>
                        <input type="number" id="bowInput" value="{page_data['bow_in']}" min="6" max="60" step="1" oninput="calculateMarine()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-teal-700">
                        <span class="text-[11px] text-gray-600">Top of bow deck straight down to water surface</span>
                    </div>

                    <div>
                        <label for="waterInput" class="block text-sm font-bold text-gray-800 mb-1">Wind, Waves & Current Condition</label>
                        <select id="waterInput" onchange="calculateMarine()" class="w-full bg-gray-200 border border-gray-400 rounded-lg px-3.5 py-2.5 text-sm font-bold text-gray-900">
                            <option value="1.0" {"selected" if page_data['water'] == "1.0" else ""}>Calm Pond / Sheltered Lake (1.0x Base)</option>
                            <option value="1.15" {"selected" if page_data['water'] in ("1.1", "1.15") else ""}>Moderate Wind & Chop (+15% Reserve)</option>
                            <option value="1.25" {"selected" if page_data['water'] == "1.25" else ""}>Pontoon Windage / Open Big Water (+25%)</option>
                            <option value="1.35" {"selected" if page_data['water'] == "1.35" else ""}>Heavy River Current / Tidal Offshore (+35%)</option>
                        </select>
                    </div>

                    <div>
                        <label for="hoursInput" class="block text-sm font-bold text-gray-800 mb-1">Fishing Session Duration (Hours)</label>
                        <input type="number" id="hoursInput" value="{page_data['hours']}" min="2" max="16" step="1" oninput="calculateMarine()"
                               class="w-full bg-gray-200 border border-gray-400 rounded-lg px-4 py-2.5 text-base font-bold text-gray-900 focus:ring-2 focus:ring-teal-700">
                        <span class="text-[11px] text-gray-600">Calculates LiFePO4 Ah & Onboard Charger Amps</span>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-gray-100 border-2 border-teal-700 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-gray-300 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">2. Engineered Propulsion & Power Specs</span>
                    <h2 class="text-xl font-extrabold text-gray-900">Your Required Trolling & Sonar Setup</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-teal-100 border border-teal-300 rounded-xl p-3.5">
                        <span class="text-xs text-teal-950 font-semibold block">Recommended Thrust</span>
                        <span id="resThrustLbs" class="text-2xl font-black text-teal-800">80 Lbs</span>
                        <span id="resVoltage" class="text-[11px] text-teal-900 block mt-0.5">24V System (2 Batteries)</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Min. Shaft Length</span>
                        <span id="resShaftIn" class="text-2xl font-black text-gray-900">54\" Shaft</span>
                        <span id="resSubmerged" class="text-[11px] text-gray-600 block mt-0.5">Zero Wave Cavitation</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Battery Bank Capacity</span>
                        <span id="resBatteryAh" class="text-lg font-extrabold text-gray-900">100 Ah LiFePO4</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">+ 60A MKR-27 Breaker</span>
                    </div>
                    <div class="bg-gray-200 border border-gray-300 rounded-xl p-3.5">
                        <span class="text-xs text-gray-600 font-medium block">Onboard Marine Charger</span>
                        <span id="resChargerSpec" class="text-base font-extrabold text-amber-800">3-Bank 30A</span>
                        <span class="text-[11px] text-gray-600 block mt-0.5">NOCO IP68 Waterproof</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-gray-200 border-2 border-teal-600 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-teal-700 text-white px-2 py-0.5 rounded">Verified Marine Match</span>
                        <span class="text-xs font-bold text-gray-700">Amazon Prime Ready</span>
                    </div>
                    <h3 id="recMotorTitle" class="text-base font-extrabold text-gray-900 leading-snug">Loading Motor & Sonar Match...</h3>
                    <p id="recMotorDesc" class="text-xs text-gray-700"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched Trolling Motor &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-gray-800 hover:bg-gray-900 text-white font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop Sonar & Charger
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-gray-900">Search Trolling Motors, CHIRP Fish Finders, LiFePO4 Batteries & Marine Chargers</h2>
                <p class="text-sm text-gray-700">Search any thrust (55 lb, 80 lb, 112 lb), brand (Minn Kota, Garmin, Humminbird, Lowrance, Newport Vessels, NOCO, LiTime), or marine accessory on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Minn Kota Terrova 80 lb 60 Inch, Garmin ECHOMAP UHD2 93sv, NOCO Genius GENPRO10X3..."
                           class="flex-1 bg-gray-200 border-2 border-gray-400 rounded-xl px-4 py-3 text-sm font-medium text-gray-900 placeholder-gray-500 focus:outline-none focus:border-teal-700" required>
                    <button type="submit" class="bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-gray-600 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Minn Kota Terrova GPS Spot Lock Trolling Motor')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-teal-200 text-gray-800 border border-gray-300 rounded-full transition">Minn Kota Terrova GPS</a>
                    <a href="{amz_url('Garmin ECHOMAP UHD2 93sv GT56UHD Fish Finder')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-teal-200 text-gray-800 border border-gray-300 rounded-full transition">Garmin ECHOMAP 93sv</a>
                    <a href="{amz_url('Humminbird HELIX 9 MEGA SI+ GPS G4N')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-teal-200 text-gray-800 border border-gray-300 rounded-full transition">Humminbird HELIX 9</a>
                    <a href="{amz_url('NOCO Genius GENPRO10X3 3 Bank Marine Battery Charger')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-teal-200 text-gray-800 border border-gray-300 rounded-full transition">NOCO 3-Bank Charger</a>
                    <a href="{amz_url('LiTime 12V 24V 36V Trolling Motor LiFePO4 Battery')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-gray-200 hover:bg-teal-200 text-gray-800 border border-gray-300 rounded-full transition">Trolling LiFePO4 Batteries</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">Verified On-Water Hardware</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">Best-Selling GPS Trolling Motors, Fish Finders & Marine Chargers</h2>
                </div>
                <a href="{amz_url('Best Selling Boat Trolling Motors and Fish Finders')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-teal-800 hover:text-teal-900">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (+3 NEW ARTICLES PER DAY) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-gray-300 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing +3/Day)</span>
                    <h2 class="text-2xl font-extrabold text-gray-900">In-Depth Trolling Motor, Sonar & Marine Battery Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-100 text-emerald-900 border border-emerald-300 px-3 py-1 rounded-full">+3 New Product Reviews Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-gray-300 border-2 border-teal-700 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-700 text-white px-2.5 py-1 rounded">Complete Tournament Rigging Bundle</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-gray-900">Upgrading Your Boat to GPS Spot-Lock & Lithium Power?</h2>
                <p class="text-sm text-gray-800">Pair a Minn Kota Terrova or Garmin Force GPS Trolling Motor with a 100Ah LiFePO4 Battery, Minn Kota MKR-27 60A Breaker, and NOCO GENPRO Waterproof Onboard Charger.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore Trolling Motor + Charger Bundles on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-gray-300 pb-3">
                <h2 class="text-xl font-extrabold text-gray-900">Boat Type & Hull Weight Specific Calculators</h2>
                <p class="text-xs text-gray-600">Select your exact boat hull or loaded weight below for pre-calculated thrust lbs, shaft length, and battery specs.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-gray-300 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-teal-800">Marine Propulsion & Sonar Guide</span>
                <h2 class="text-2xl font-extrabold text-gray-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

        {onpage_sitemap_html}

    </main>

    <!-- FOOTER (GRAY BACKGROUND) -->
    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-gray-800">
                <a href="{BASE_URL}/" class="hover:text-teal-800">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-teal-800">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-teal-800">Daily Reviews (+3/Day)</a>
                <a href="{BASE_URL}/sitemap.html" class="hover:text-teal-800 font-bold">HTML Site Map</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-teal-800">XML Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-teal-800">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 4) {{
                document.getElementById("weightInput").value = parts[0];
                document.getElementById("bowInput").value = parts[1];
                document.getElementById("waterInput").value = parts[2];
                document.getElementById("hoursInput").value = parts[3];
                calculateMarine();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateMarine() {{
            const weightLbs = parseFloat(document.getElementById("weightInput").value) || 2900;
            const bowIn = parseFloat(document.getElementById("bowInput").value) || 22;
            const waterFactor = parseFloat(document.getElementById("waterInput").value) || 1.15;
            const hours = parseFloat(document.getElementById("hoursInput").value) || 8;

            const rawThrust = Math.max(36, Math.round(((weightLbs / 100) * 2) * waterFactor));
            let recThrust = 55;
            let voltageText = "12V System (1 Battery)";
            let chargerSpec = "2-Bank 20A (GENPRO10X2)";

            if (rawThrust <= 55) {{
                recThrust = 55;
                voltageText = "12V System (Min " + rawThrust + " lb calc)";
                chargerSpec = "2-Bank 20A (GENPRO10X2)";
            }} else if (rawThrust <= 80) {{
                recThrust = 80;
                voltageText = "24V System (Min " + rawThrust + " lb calc)";
                chargerSpec = "3-Bank 30A (GENPRO10X3)";
            }} else {{
                recThrust = 112;
                voltageText = "36V System (Min " + rawThrust + " lb calc)";
                chargerSpec = "4-Bank 40A (GENPRO10X4)";
            }}

            const roughBonus = waterFactor >= 1.2 ? 5 : 2;
            const minShaftRaw = bowIn + 20 + roughBonus;
            const shafts = [36, 45, 54, 60, 72, 87];
            let recShaft = 87;
            for (let i = 0; i < shafts.length; i++) {{
                if (shafts[i] >= minShaftRaw) {{
                    recShaft = shafts[i];
                    break;
                }}
            }}

            const reqAh = Math.max(50, Math.ceil((hours * 13.5) / 10) * 10);

            document.getElementById("resThrustLbs").textContent = recThrust + " Lbs Thrust";
            document.getElementById("resVoltage").textContent = voltageText;
            document.getElementById("resShaftIn").textContent = recShaft + "\\\" Shaft";
            document.getElementById("resSubmerged").textContent = "Bow " + bowIn + "\\\" + " + (20 + roughBonus) + "\\\" Immersion";
            document.getElementById("resBatteryAh").textContent = reqAh + "+ Ah LiFePO4";
            document.getElementById("resChargerSpec").textContent = chargerSpec;

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "Garmin ECHOMAP UHD2 93sv Fish Finder and NOCO Genius Marine Charger";

            if (recThrust === 55) {{
                recTitle = "55-Lb 12V Trolling Motor (Minn Kota Terrova 55 / Endura Max / Newport NV-55) — " + recShaft + "\\\" Shaft";
                recDesc = "Ideal 12V propulsion for kayaks, Jon boats, and skiffs up to 2,200 lbs loaded.";
                primaryQuery = "Minn Kota Terrova 55 Endura Max Newport 55 lb 12V Trolling Motor";
                secondaryQuery = "LiTime 12V 100Ah Trolling Motor LiFePO4 Battery and NOCO GENPRO10X2";
            }} else if (recThrust === 80) {{
                recTitle = "80-Lb 24V GPS Spot-Lock Trolling Motor (Minn Kota Terrova 80 / Ultrex) — " + recShaft + "\\\" Shaft";
                recDesc = "America's #1 24-volt bow-mount setup for bass boats, Deep-V hulls, and pontoons up to 4,000 lbs.";
                primaryQuery = "Minn Kota Terrova 80 lb 24V " + recShaft + " inch GPS Trolling Motor";
                secondaryQuery = "NOCO Genius GENPRO10X3 3 Bank 30A Charger and Garmin ECHOMAP UHD2 93sv";
            }} else {{
                recTitle = "112-Lb 36V Heavy-Duty GPS Trolling Motor (Terrova / Riptide / Garmin Force) — " + recShaft + "\\\" Shaft";
                recDesc = "Maximum 36-volt authority for heavy 4,000 to 6,500+ lb Deep-V, pontoon, and offshore bay boats.";
                primaryQuery = "Minn Kota Terrova Riptide 112 lb 36V " + recShaft + " inch GPS Trolling Motor";
                secondaryQuery = "NOCO Genius GENPRO10X4 4 Bank 40A Charger and Humminbird HELIX 10";
            }}

            document.getElementById("recMotorTitle").textContent = recTitle;
            document.getElementById("recMotorDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateMarine);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-emerald-700 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-gray-800"><span class="text-rose-700 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-gray-800 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-gray-100 border-2 border-gray-300 rounded-xl p-4 hover:border-teal-700 transition block">
            <span class="text-[11px] font-bold text-teal-800 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-gray-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-gray-600 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-teal-800">Home & Thrust Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-teal-800">Daily Marine Reviews</a>
            <span>/</span>
            <span class="text-gray-900">{rev['product_name']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 border border-teal-300 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-gray-600">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-200 text-amber-950 px-3 py-1 rounded-lg">On-Water Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-gray-200 p-4 rounded-xl border border-gray-300 text-xs">
                <div><span class="text-gray-500 block font-medium">Primary Spec</span><strong class="text-gray-900">{rev['spec_1']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Shaft / Sonar</span><strong class="text-gray-900">{rev['spec_2']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Technology</span><strong class="text-gray-900">{rev['spec_3']}</strong></div>
                <div><span class="text-gray-500 block font-medium">Warranty</span><strong class="text-gray-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-gray-300 hover:bg-gray-400 text-gray-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate Thrust & Shaft Size
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-gray-100 border-2 border-emerald-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-gray-100 border-2 border-rose-400 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900 border-b border-gray-300 pb-3">Hands-On Thrust, Battery Draw & Sonar Performance Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-gray-300 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-teal-800 block">Final Verdict</span>
                    <p class="text-sm font-bold text-gray-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our marine electronics test.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-gray-900">Recent Daily Marine Hardware Reviews (+3 Added Daily)</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-gray-300">
            <td class="p-4 font-bold text-gray-900 bg-gray-200 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-gray-800 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-200 text-gray-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-gray-600 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-teal-800">Home & Thrust Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-teal-800">Product Comparisons</a>
            <span>/</span>
            <span class="text-gray-900">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-teal-100 text-teal-900 border border-teal-300 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-gray-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-gray-700 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-gray-100 border-2 border-gray-300 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-gray-800 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-teal-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-gray-200">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-gray-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-gray-100 border-2 border-teal-600 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-gray-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-gray-800 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-teal-700 hover:bg-teal-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-gray-800 hover:bg-gray-900 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-gray-300 border-t border-gray-400 mt-16 py-10 px-4 text-xs text-gray-700 text-center">
        <p class="font-bold text-gray-900">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "18-Foot Bass & Multi-Species Boat",
        "weight_lbs": 2900,
        "bow_in": 22,
        "water": "1.15",
        "hours": 8,
        "desc": "Calculate exact boat trolling motor thrust (lbs), 12V/24V/36V battery system, bow-to-waterline shaft length (36\"–87\"), and onboard charger sizing—plus read 3 new marine product reviews added daily."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Dedicated HTML Site Map Page (sitemap.html)
    with open(os.path.join(OUTPUT_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
        f.write(render_dedicated_html_sitemap_page())
    generated_urls.append(f"{BASE_URL}/sitemap.html")

    # 3. Generate Programmatic Boat & Thrust Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Cumulative Daily Product Review Pages (+3 new reviews unlocked every single day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 6. XML Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles [+3/day] + HTML/XML sitemaps) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()

EWL = "EWL"
DTL = "DTL"
CCL = "CCL"
NSL = "NSL"
NEL = "NEL"
TEL = "TEL"
CRL = "CRL"

COORDS = {
    "Buona Vista": (1.3072211023458846, 103.79059754383378),
    "Botanic Gardens": (1.3223149122653284, 103.814923452478),
    "Caldecott": (1.3376849215620632, 103.83952467109367),
    "Stevens": (1.31993396519215, 103.8261362665367),
    "Newton": (1.3123310026296833, 103.83800417333637),
    "Orchard": (1.3036751408679732, 103.8318621135785),
    "Dhoby Ghaut": (1.2989373778595812, 103.84560905437583),
    "Little India": (1.3067850614823533, 103.84968733921137),
    "Serangoon": (1.3500929313784553, 103.87331036316692),
    "Bishan": (1.3508581361314433, 103.84809581470844),
    "MacPherson": (1.326683134954314, 103.8901150057307),
    "Paya Lebar": (1.318155363968774, 103.89314858006719),
    "Bugis": (1.3002271163987622, 103.85618844621733),
    "Promenade": (1.2940800615713624, 103.86026550386774),
    "Bayfront": (1.2813225208371848, 103.85896008473559),
    "Marina Bay": (1.2760629151443041, 103.85514125978173),
    "Raffles Place": (1.2850810250332285, 103.85163715958511),
    "City Hall": (1.2931603084853547, 103.85190805353733),
    "Chinatown": (1.2845673614610977, 103.84360131599527),
    "Outram Park": (1.281432090859361, 103.83927572035837),
    "HarbourFront": (1.2654950135640946, 103.82124021456305),
    "Tampines": (1.353347206823184, 103.9452516110989),
    "Tanah Merah": (1.3272447994965766, 103.94648600675258),
    "Expo": (1.334435030338279, 103.96159210789263),
    "Changi Airport": (1.356989690929546, 103.98820957001335),
    "Clementi": (1.3154338075074294, 103.76504917815703),
    "King Albert Park": (1.3357010332886692, 103.7831651779786),
    "Bright Hill": (1.3627333805636823, 103.8321991460318),
    "Ang Mo Kio": (1.3692664220257802, 103.85019147633497),
    "Hougang": (1.3715970443365206, 103.89298226929262),
    "Pasir Ris": (1.3732131399443028, 103.94927022247848),
    "Changi Airport T5": (1.3274919456422216, 103.99266322660043),
    "Sungei Bedok": (1.3201583692509442, 103.95713451377267),
}

 
ADJ_LIST_CURRENT = {
    "Buona Vista": [
        ("Botanic Gardens", 5, CCL),
        ("Outram Park", 11, EWL),
        ("HarbourFront", 13, CCL),
    ],

    "Botanic Gardens": [
        ("Buona Vista", 5, CCL),
        ("Caldecott", 6, CCL),
        ("Stevens", 1, DTL),
    ],

    "Caldecott": [
        ("Botanic Gardens", 6, CCL),
        ("Bishan", 4, CCL),
        ("Stevens", 5, TEL),
    ],

    "Stevens": [
        ("Botanic Gardens", 1, DTL),
        ("Caldecott", 5, TEL),
        ("Newton", 2, DTL),
        ("Orchard", 4, TEL),
    ],

    "Newton": [
        ("Stevens", 2, DTL),
        ("Orchard", 2, NSL),
        ("Bishan", 8, NSL),
        ("Little India", 2, DTL),
    ],

    "Orchard": [
        ("Stevens", 4, TEL),
        ("Newton", 2, NSL),
        ("Dhoby Ghaut", 3, NSL),
        ("Outram Park", 4, TEL),
    ],

    "Dhoby Ghaut": [
        ("Orchard", 3, NSL),
        ("Little India", 1, NEL),
        ("Chinatown", 3, NEL),
        ("City Hall", 1, NSL),
        ("Promenade", 3, CCL),
    ],

    "Little India": [
        ("Dhoby Ghaut", 1, NEL),
        ("Newton", 2, DTL),
        ("Serangoon", 9, NEL),
        ("Bugis", 2, DTL),
    ],

    "Serangoon": [
        ("Bishan", 4, CCL),
        ("Little India", 9, NEL),
        ("MacPherson", 6, CCL),
    ],

    "Bishan": [
        ("Caldecott", 4, CCL),
        ("Serangoon", 4, CCL),
        ("Newton", 8, NSL),
    ],

    "MacPherson": [
        ("Serangoon", 6, CCL),
        ("Paya Lebar", 1, CCL),
        ("Chinatown", 13, DTL),
        ("Tampines", 14, DTL),
    ],

    "Paya Lebar": [
        ("MacPherson", 1, CCL),
        ("Bugis", 8, EWL),
        ("Promenade", 9, CCL),
        ("Tanah Merah", 10, EWL),
    ],

    "Bugis": [
        ("Little India", 2, DTL),
        ("Paya Lebar", 8, EWL),
        ("Promenade", 1, DTL),
        ("City Hall", 1, EWL),
    ],

    "Promenade": [
        ("Bugis", 1, DTL),
        ("Bayfront", 2, DTL),
        ("Bayfront", 2, CCL),
        ("Paya Lebar", 9, CCL),
        ("Dhoby Ghaut", 3, CCL),
    ],

    "Bayfront": [
        ("Promenade", 2, DTL),
        ("Promenade", 2, CCL),
        ("Marina Bay", 1, CCL),
        ("Chinatown", 3, DTL),
    ],

    "Marina Bay": [
        ("Bayfront", 1, CCL),
        ("Raffles Place", 1, NSL),
        ("Outram Park", 3, TEL),
    ],

    "Raffles Place": [
        ("City Hall", 1, EWL),
        ("City Hall", 1, NSL),
        ("Marina Bay", 1, NSL),
        ("Outram Park", 3, EWL),
    ],

    "City Hall": [
        ("Dhoby Ghaut", 1, NSL),
        ("Raffles Place", 1, NSL),
        ("Raffles Place", 1, EWL),
        ("Bugis", 1, EWL),
    ],

    "Chinatown": [
        ("Dhoby Ghaut", 3, NEL),
        ("Outram Park", 1, NEL),
        ("MacPherson", 13, DTL),
        ("Bayfront", 3, DTL),
    ],

    "Outram Park": [
        ("Chinatown", 1, NEL),
        ("Buona Vista", 11, EWL),
        ("HarbourFront", 4, NEL),
        ("Raffles Place", 3, EWL),
        ("Orchard", 4, TEL),
        ("Marina Bay", 3, TEL),
    ],

    "HarbourFront": [
        ("Outram Park", 4, NEL),
        ("Buona Vista", 13, CCL),
    ],

    "Tampines": [
        ("MacPherson", 14, DTL),
        ("Tanah Merah", 6, EWL),
        ("Expo", 8, DTL),
    ],

    "Tanah Merah": [
        ("Tampines", 6, EWL),
        ("Paya Lebar", 10, EWL),
        ("Expo", 3, EWL),
    ],

    "Expo": [
        ("Tanah Merah", 3, EWL),
        ("Tampines", 8, DTL),
        ("Changi Airport", 7, EWL),
    ],

    "Changi Airport": [
        ("Expo", 7, EWL),
    ],
}


ADJ_LIST_FUTURE = {
    "Buona Vista": [
        ("Clementi", 5, EWL),
        ("Botanic Gardens", 5, CCL),
        ("Outram Park", 11, EWL),
        ("HarbourFront", 13, CCL),
    ],

    "Botanic Gardens": [
        ("King Albert Park", 6, DTL),
        ("Buona Vista", 5, CCL),
        ("Caldecott", 6, CCL),
        ("Stevens", 1, DTL),
    ],

    "Caldecott": [
        ("Bright Hill", 6, TEL),
        ("Botanic Gardens", 6, CCL),
        ("Bishan", 4, CCL),
        ("Stevens", 5, TEL),
    ],

    "Stevens": [
        ("Botanic Gardens", 1, DTL),
        ("Caldecott", 5, TEL),
        ("Newton", 2, DTL),
        ("Orchard", 4, TEL),
    ],

    "Newton": [
        ("Stevens", 2, DTL),
        ("Orchard", 2, NSL),
        ("Bishan", 8, NSL),
        ("Little India", 2, DTL),
    ],

    "Orchard": [
        ("Stevens", 4, TEL),
        ("Newton", 2, NSL),
        ("Dhoby Ghaut", 3, NSL),
        ("Outram Park", 4, TEL),
    ],

    "Dhoby Ghaut": [
        ("Orchard", 3, NSL),
        ("Little India", 1, NEL),
        ("Chinatown", 3, NEL),
        ("City Hall", 1, NSL),
        ("Promenade", 3, CCL),
    ],

    "Little India": [
        ("Dhoby Ghaut", 1, NEL),
        ("Newton", 2, DTL),
        ("Serangoon", 9, NEL),
        ("Bugis", 2, DTL),
    ],

    "Serangoon": [
        ("Hougang", 5, NEL),
        ("Bishan", 4, CCL),
        ("Little India", 9, NEL),
        ("MacPherson", 6, CCL),
    ],

    "Bishan": [
        ("Ang Mo Kio", 4, NSL),
        ("Caldecott", 4, CCL),
        ("Serangoon", 4, CCL),
        ("Newton", 8, NSL),
    ],

    "MacPherson": [
        ("Serangoon", 6, CCL),
        ("Paya Lebar", 1, CCL),
        ("Chinatown", 13, DTL),
        ("Tampines", 14, DTL),
    ],

    "Paya Lebar": [
        ("MacPherson", 1, CCL),
        ("Bugis", 8, EWL),
        ("Promenade", 9, CCL),
        ("Tanah Merah", 10, EWL),
    ],

    "Bugis": [
        ("Little India", 2, DTL),
        ("Paya Lebar", 8, EWL),
        ("Promenade", 1, DTL),
        ("City Hall", 1, EWL),
    ],

    "Promenade": [
        ("Bugis", 1, DTL),
        ("Bayfront", 2, DTL),
        ("Bayfront", 2, CCL),
        ("Paya Lebar", 9, CCL),
        ("Dhoby Ghaut", 3, CCL),
    ],

    "Bayfront": [
        ("Promenade", 2, DTL),
        ("Promenade", 2, CCL),
        ("Marina Bay", 1, CCL),
        ("Chinatown", 3, DTL),
    ],

    "Marina Bay": [
        ("Sungei Bedok", 35, TEL),
        ("Bayfront", 1, CCL),
        ("Raffles Place", 1, NSL),
        ("Outram Park", 3, TEL),
        ("HarbourFront", 10, CCL),
    ],

    "Raffles Place": [
        ("City Hall", 1, EWL),
        ("City Hall", 1, NSL),
        ("Marina Bay", 1, NSL),
        ("Outram Park", 3, EWL),
    ],

    "City Hall": [
        ("Dhoby Ghaut", 1, NSL),
        ("Raffles Place", 1, NSL),
        ("Raffles Place", 1, EWL),
        ("Bugis", 1, EWL),
    ],

    "Chinatown": [
        ("Dhoby Ghaut", 3, NEL),
        ("Outram Park", 1, NEL),
        ("MacPherson", 13, DTL),
        ("Bayfront", 3, DTL),
    ],

    "Outram Park": [
        ("Chinatown", 1, NEL),
        ("Buona Vista", 11, EWL),
        ("HarbourFront", 4, NEL),
        ("Raffles Place", 3, EWL),
        ("Orchard", 4, TEL),
        ("Marina Bay", 3, TEL),
    ],

    "HarbourFront": [
        ("Outram Park", 4, NEL),
        ("Buona Vista", 13, CCL),
        ("Marina Bay", 10, CCL),
    ],

    "Tampines": [
        ("Pasir Ris", 4, EWL),
        ("MacPherson", 14, DTL),
        ("Tanah Merah", 6, EWL),
        ("Expo", 8, DTL),
    ],

    "Tanah Merah": [
        ("Tampines", 6, EWL),
        ("Paya Lebar", 10, EWL),
        ("Expo", 4, TEL),
    ],

    "Expo": [
        ("Sungei Bedok", 6, DTL),
        ("Tanah Merah", 4, TEL),
        ("Tampines", 8, DTL),
        ("Changi Airport", 6, TEL),
    ],

    "Changi Airport": [
        ("Changi Airport T5", 5, TEL),
        ("Expo", 6, TEL),
    ],

    "Clementi": [
        ("Buona Vista", 5, EWL),
        ("King Albert Park", 7, CRL),
    ],

    "King Albert Park": [
        ("Clementi", 7, CRL),
        ("Bright Hill", 9, CRL),
        ("Botanic Gardens", 6, DTL),
    ],

    "Bright Hill": [
        ("King Albert Park", 9, CRL),
        ("Ang Mo Kio", 5, CRL),
        ("Caldecott", 6, TEL),
    ],

    "Ang Mo Kio": [
        ("Hougang", 6, CRL),
        ("Bright Hill", 5, CRL),
        ("Bishan", 4, NSL),
    ],

    "Hougang": [
        ("Ang Mo Kio", 6, CRL),
        ("Pasir Ris", 12, CRL),
        ("Serangoon", 5, NEL),
    ],

    "Pasir Ris": [
        ("Hougang", 12, CRL),
        ("Changi Airport T5", 10, CRL),
        ("Tampines", 4, EWL),
    ],

    "Changi Airport T5": [
        ("Changi Airport", 5, TEL),
        ("Pasir Ris", 10, CRL),
        ("Sungei Bedok", 4, TEL),
    ],

    "Sungei Bedok": [
        ("Expo", 6, DTL),
        ("Changi Airport T5", 4, TEL),
        ("Marina Bay", 35, TEL),
    ],
}
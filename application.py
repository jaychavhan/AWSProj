import random
from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

numberOfQuestions = 10
application = Flask(__name__)

# adding configuration for using a sqlite database
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin1234@flagadroitdb.c9pp3gwuqypj.us-east-1.rds.amazonaws.com:3306/flagscores'
db = SQLAlchemy(application)
migrate = Migrate(application, db)


# Models
class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    correctAns = db.Column(db.Integer, nullable=False)

    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Name : {self.name}, Score: {self.score}"


class Quiz:
    queId = ""
    que_image = ""
    option1 = ""
    option2 = ""
    option3 = ""
    option4 = ""
    correctOption = ""

    def __init__(self, queId, que_image, option1, option2, option3, option4, correctOption):
        self.queId = queId
        self.que_image = que_image
        self.option1 = option1
        self.option2 = option2
        self.option3 = option3
        self.option4 = option4
        self.correctOption = correctOption

    def getCorrectAnswer(self):
        if self.correctOption == self.option1:
            return self.option1
        if self.correctOption == self.option2:
            return self.option2
        if self.correctOption == self.option3:
            return self.option3
        if self.correctOption == self.option4:
            return self.option4


codeDict = {
    "ad": "Andorra",
    "ae": "United Arab Emirates",
    "af": "Afghanistan",
    "ag": "Antigua and Barbuda",
    "ai": "Anguilla",
    "al": "Albania",
    "am": "Armenia",
    "ao": "Angola",
    "aq": "Antarctica",
    "ar": "Argentina",
    "as": "American Samoa",
    "at": "Austria",
    "au": "Australia",
    "aw": "Aruba",
    "ax": "Åland Islands",
    "az": "Azerbaijan",
    "ba": "Bosnia and Herzegovina",
    "bb": "Barbados",
    "bd": "Bangladesh",
    "be": "Belgium",
    "bf": "Burkina Faso",
    "bg": "Bulgaria",
    "bh": "Bahrain",
    "bi": "Burundi",
    "bj": "Benin",
    "bl": "Saint Barthélemy",
    "bm": "Bermuda",
    "bn": "Brunei",
    "bo": "Bolivia",
    "bq": "Caribbean Netherlands",
    "br": "Brazil",
    "bs": "Bahamas",
    "bt": "Bhutan",
    "bv": "Bouvet Island",
    "bw": "Botswana",
    "by": "Belarus",
    "bz": "Belize",
    "ca": "Canada",
    "cc": "Cocos (Keeling) Islands",
    "cd": "DR Congo",
    "cf": "Central African Republic",
    "cg": "Republic of the Congo",
    "ch": "Switzerland",
    "ci": "Côte d'Ivoire (Ivory Coast)",
    "ck": "Cook Islands",
    "cl": "Chile",
    "cm": "Cameroon",
    "cn": "China",
    "co": "Colombia",
    "cr": "Costa Rica",
    "cu": "Cuba",
    "cv": "Cape Verde",
    "cw": "Curaçao",
    "cx": "Christmas Island",
    "cy": "Cyprus",
    "cz": "Czechia",
    "de": "Germany",
    "dj": "Djibouti",
    "dk": "Denmark",
    "dm": "Dominica",
    "do": "Dominican Republic",
    "dz": "Algeria",
    "ec": "Ecuador",
    "ee": "Estonia",
    "eg": "Egypt",
    "eh": "Western Sahara",
    "er": "Eritrea",
    "es": "Spain",
    "et": "Ethiopia",
    "eu": "European Union",
    "fi": "Finland",
    "fj": "Fiji",
    "fk": "Falkland Islands",
    "fm": "Micronesia",
    "fo": "Faroe Islands",
    "fr": "France",
    "ga": "Gabon",
    "gb": "United Kingdom",
    "gb-eng": "England",
    "gb-nir": "Northern Ireland",
    "gb-sct": "Scotland",
    "gb-wls": "Wales",
    "gd": "Grenada",
    "ge": "Georgia",
    "gf": "French Guiana",
    "gg": "Guernsey",
    "gh": "Ghana",
    "gi": "Gibraltar",
    "gl": "Greenland",
    "gm": "Gambia",
    "gn": "Guinea",
    "gp": "Guadeloupe",
    "gq": "Equatorial Guinea",
    "gr": "Greece",
    "gs": "South Georgia",
    "gt": "Guatemala",
    "gu": "Guam",
    "gw": "Guinea-Bissau",
    "gy": "Guyana",
    "hk": "Hong Kong",
    "hm": "Heard Island and McDonald Islands",
    "hn": "Honduras",
    "hr": "Croatia",
    "ht": "Haiti",
    "hu": "Hungary",
    "id": "Indonesia",
    "ie": "Ireland",
    "il": "Israel",
    "im": "Isle of Man",
    "in": "India",
    "io": "British Indian Ocean Territory",
    "iq": "Iraq",
    "ir": "Iran",
    "is": "Iceland",
    "it": "Italy",
    "je": "Jersey",
    "jm": "Jamaica",
    "jo": "Jordan",
    "jp": "Japan",
    "ke": "Kenya",
    "kg": "Kyrgyzstan",
    "kh": "Cambodia",
    "ki": "Kiribati",
    "km": "Comoros",
    "kn": "Saint Kitts and Nevis",
    "kp": "North Korea",
    "kr": "South Korea",
    "kw": "Kuwait",
    "ky": "Cayman Islands",
    "kz": "Kazakhstan",
    "la": "Laos",
    "lb": "Lebanon",
    "lc": "Saint Lucia",
    "li": "Liechtenstein",
    "lk": "Sri Lanka",
    "lr": "Liberia",
    "ls": "Lesotho",
    "lt": "Lithuania",
    "lu": "Luxembourg",
    "lv": "Latvia",
    "ly": "Libya",
    "ma": "Morocco",
    "mc": "Monaco",
    "md": "Moldova",
    "me": "Montenegro",
    "mf": "Saint Martin",
    "mg": "Madagascar",
    "mh": "Marshall Islands",
    "mk": "North Macedonia",
    "ml": "Mali",
    "mm": "Myanmar",
    "mn": "Mongolia",
    "mo": "Macau",
    "mp": "Northern Mariana Islands",
    "mq": "Martinique",
    "mr": "Mauritania",
    "ms": "Montserrat",
    "mt": "Malta",
    "mu": "Mauritius",
    "mv": "Maldives",
    "mw": "Malawi",
    "mx": "Mexico",
    "my": "Malaysia",
    "mz": "Mozambique",
    "na": "Namibia",
    "nc": "New Caledonia",
    "ne": "Niger",
    "nf": "Norfolk Island",
    "ng": "Nigeria",
    "ni": "Nicaragua",
    "nl": "Netherlands",
    "no": "Norway",
    "np": "Nepal",
    "nr": "Nauru",
    "nu": "Niue",
    "nz": "New Zealand",
    "om": "Oman",
    "pa": "Panama",
    "pe": "Peru",
    "pf": "French Polynesia",
    "pg": "Papua New Guinea",
    "ph": "Philippines",
    "pk": "Pakistan",
    "pl": "Poland",
    "pm": "Saint Pierre and Miquelon",
    "pn": "Pitcairn Islands",
    "pr": "Puerto Rico",
    "ps": "Palestine",
    "pt": "Portugal",
    "pw": "Palau",
    "py": "Paraguay",
    "qa": "Qatar",
    "re": "Réunion",
    "ro": "Romania",
    "rs": "Serbia",
    "ru": "Russia",
    "rw": "Rwanda",
    "sa": "Saudi Arabia",
    "sb": "Solomon Islands",
    "sc": "Seychelles",
    "sd": "Sudan",
    "se": "Sweden",
    "sg": "Singapore",
    "sh": "Saint Helena, Ascension and Tristan da Cunha",
    "si": "Slovenia",
    "sj": "Svalbard and Jan Mayen",
    "sk": "Slovakia",
    "sl": "Sierra Leone",
    "sm": "San Marino",
    "sn": "Senegal",
    "so": "Somalia",
    "sr": "Suriname",
    "ss": "South Sudan",
    "st": "São Tomé and Príncipe",
    "sv": "El Salvador",
    "sx": "Sint Maarten",
    "sy": "Syria",
    "sz": "Eswatini (Swaziland)",
    "tc": "Turks and Caicos Islands",
    "td": "Chad",
    "tf": "French Southern and Antarctic Lands",
    "tg": "Togo",
    "th": "Thailand",
    "tj": "Tajikistan",
    "tk": "Tokelau",
    "tl": "Timor-Leste",
    "tm": "Turkmenistan",
    "tn": "Tunisia",
    "to": "Tonga",
    "tr": "Turkey",
    "tt": "Trinidad and Tobago",
    "tv": "Tuvalu",
    "tw": "Taiwan",
    "tz": "Tanzania",
    "ua": "Ukraine",
    "ug": "Uganda",
    "um": "United States Minor Outlying Islands",
    "un": "United Nations",
    "us": "United States",
    "us-ak": "Alaska",
    "us-al": "Alabama",
    "us-ar": "Arkansas",
    "us-az": "Arizona",
    "us-ca": "California",
    "us-co": "Colorado",
    "us-ct": "Connecticut",
    "us-de": "Delaware",
    "us-fl": "Florida",
    "us-ga": "Georgia",
    "us-hi": "Hawaii",
    "us-ia": "Iowa",
    "us-id": "Idaho",
    "us-il": "Illinois",
    "us-in": "Indiana",
    "us-ks": "Kansas",
    "us-ky": "Kentucky",
    "us-la": "Louisiana",
    "us-ma": "Massachusetts",
    "us-md": "Maryland",
    "us-me": "Maine",
    "us-mi": "Michigan",
    "us-mn": "Minnesota",
    "us-mo": "Missouri",
    "us-ms": "Mississippi",
    "us-mt": "Montana",
    "us-nc": "North Carolina",
    "us-nd": "North Dakota",
    "us-ne": "Nebraska",
    "us-nh": "New Hampshire",
    "us-nj": "New Jersey",
    "us-nm": "New Mexico",
    "us-nv": "Nevada",
    "us-ny": "New York",
    "us-oh": "Ohio",
    "us-ok": "Oklahoma",
    "us-or": "Oregon",
    "us-pa": "Pennsylvania",
    "us-ri": "Rhode Island",
    "us-sc": "South Carolina",
    "us-sd": "South Dakota",
    "us-tn": "Tennessee",
    "us-tx": "Texas",
    "us-ut": "Utah",
    "us-va": "Virginia",
    "us-vt": "Vermont",
    "us-wa": "Washington",
    "us-wi": "Wisconsin",
    "us-wv": "West Virginia",
    "us-wy": "Wyoming",
    "uy": "Uruguay",
    "uz": "Uzbekistan",
    "va": "Vatican City (Holy See)",
    "vc": "Saint Vincent and the Grenadines",
    "ve": "Venezuela",
    "vg": "British Virgin Islands",
    "vi": "United States Virgin Islands",
    "vn": "Vietnam",
    "vu": "Vanuatu",
    "wf": "Wallis and Futuna",
    "ws": "Samoa",
    "xk": "Kosovo",
    "ye": "Yemen",
    "yt": "Mayotte",
    "za": "South Africa",
    "zm": "Zambia",
    "zw": "Zimbabwe"
}

keys = list(codeDict.keys())
random.shuffle(keys)

ShuffledCodeDict = dict()
for key in keys:
    ShuffledCodeDict.update({key: codeDict[key]})

listOfCountries = ['Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola',
                   'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia',
                   'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium',
                   'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of',
                   'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil',
                   'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi',
                   'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad',
                   'Chile', 'China', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo',
                   'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia',
                   'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica',
                   'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia',
                   'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France',
                   'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia',
                   'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala',
                   'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands',
                   'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia',
                   'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan',
                   'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of",
                   'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia',
                   'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao',
                   'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta',
                   'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico',
                   'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro',
                   'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands',
                   'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island',
                   'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied',
                   'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal',
                   'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy',
                   'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia',
                   'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines',
                   'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles',
                   'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands',
                   'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka',
                   'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland',
                   'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of',
                   'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey',
                   'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates',
                   'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan',
                   'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British',
                   'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']

listOfQuestions = []

queCount = 0

for key, value in ShuffledCodeDict.items():
    queCount = queCount + 1
    if queCount == numberOfQuestions + 1:
        break
    choice1 = random.choice(listOfCountries)
    choice2 = random.choice(listOfCountries)
    choice3 = random.choice(listOfCountries)
    choice4 = value
    listOfChoices = [choice1, choice2, choice3, choice4]
    firstOption = random.choice(listOfChoices)
    listOfChoices.remove(firstOption)
    secondOption = random.choice(listOfChoices)
    listOfChoices.remove(secondOption)
    thirdOption = random.choice(listOfChoices)
    listOfChoices.remove(thirdOption)
    listOfQuestions.append(Quiz(key, key, firstOption, secondOption, thirdOption, listOfChoices[0], value))

usernameDict = {}


@application.route("/")
def user():
    return render_template("username.html")


@application.route("/quiz", methods=['POST', 'GET'])
def index():
    username = request.form['user']
    print(username)
    usernameDict.update({username: 0})
    return render_template("quiz.html", questions_list=listOfQuestions, username=username)


def getComments(numberOfCorrectAns):
    percentage = (numberOfCorrectAns / numberOfQuestions) * 100
    comments = ""
    if 80 <= percentage < 101:
        comments = "Awesome Work!!!"
    elif 60 <= percentage < 80:
        comments = "Good Job!!!"
    elif 40 <= percentage < 60:
        comments = "Keep trying harder"
    elif 0 <= percentage < 40:
            comments = "Better luck next time..."
    return comments


@application.route("/result", methods=['POST', 'GET'])
def result():
    num_CorrectAnswers = 0
    for que in listOfQuestions:
        selectedOption = request.form[que.queId]
        correctOption = que.getCorrectAnswer()
        if selectedOption == correctOption:
            num_CorrectAnswers += 1

    username = request.form['username']
    record = Scores.query.filter_by(name=username).first()
    if record:
        record.score = num_CorrectAnswers * 10
        record.correctAns = num_CorrectAnswers
        db.session.merge(record)
        db.session.commit()
        print("Updated record")
    else:
        provider = Scores(name=username, score=num_CorrectAnswers * 10, correctAns=num_CorrectAnswers)
        db.session.add(provider)
        db.session.commit()
        print("New record")

    userScoreRecord = Scores.query.filter_by(name=username).first()
    allUserRecords = Scores.query.all()
    count = 0
    sumScores = 0
    for u in allUserRecords:
        sumScores += u.score
        count += 1
    averageScore = sumScores / count
    return render_template("result.html", username=userScoreRecord.name, score=userScoreRecord.score,
                           correctAns=userScoreRecord.correctAns, numberOfQuestions=numberOfQuestions,
                           averageScore=averageScore, comments=getComments(userScoreRecord.correctAns))


if __name__ == "__main__":
    application.run(debug=True)

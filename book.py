import RioStatLib
import json
# yo. anyone reading this be prepared to die looking at this code. unironically not joking its that bad.
# the code specifically for the box score is alright imo, but the rest is kinda :face_vomiting:. good luck out there
# i tried to document a bit, its not enough lmao

# creates usable stats from the json listed
def create_json(file: str):
    with open(file, "r") as jsonStr:
        jsonObj = json.load(jsonStr)
        stats = RioStatLib.StatObj(jsonObj)
    return stats
# finds the offset needed to make the list look nice
def find_offset(characters: list):
    long = 0
    for char in characters:
        if len(char) > long:
            long = len(char)
    return long

# checks for what to print
def score_changes(option: str):
    if option == "0":
        return [True, False]
    elif option == "1":
        return [False, True]
    elif option == "2":
        return [True, True]
    else:
        print("invalid number, please use 0 1 or 2.")
        return

# buffer used
def ten_buffer(stat: int):
    if stat < 10:
        return " "
    return ""

#prints box
def box_print(pc: bool, mobile: bool):
    last_inn = 1
    last_half = 0
    ascore = 0
    hscore = 0
    homescores = []
    awayscores = []
    max_innings = statfile.inningsPlayed()
    for x in range(1, max_innings * 2 + 1):
        # gets the inning we are lookin for
        if last_half == 1:
            new_inn = last_inn + 1
            new_half = 0
        else:
            new_inn = last_inn
            new_half = 1

        for event in events:
            if new_inn == event["Inning"] and new_half == event["Half Inning"]:
                new_ascore = event["Away Score"]
                new_hscore = event["Home Score"]
        if new_half == 0:
            # walkoff checker (if ending in a walkoff then will allocate the correct score since events dont cover that)
            if last_inn == max_innings:
                homescores.append(statfile.score(0) - hscore)
            else:
                homescores.append(new_hscore - hscore)
            hscore = new_hscore
        else:
            awayscores.append(new_ascore - ascore)
            ascore = new_ascore
        last_inn = new_inn
        last_half = new_half

    # adding hits, runs
    ahits = statfile.hits(0)
    aruns = statfile.runsAllowed(1)
    hhits = statfile.hits(1)
    hruns = statfile.runsAllowed(0)
    # formatting
    hoffset = ""
    aoffset = ""
    numlist = ""
    format = abs(len(aplayer) - len(hplayer))
    if len(aplayer) > len(hplayer):
        buffernum = len(aplayer)
        if format == 1:
            hoffset = " "
        else:
            for num in range(0, format):
                hoffset += " "
    else:
        buffernum = len(hplayer)
        if format == 1:
            aoffset = " "
        else:
            for num in range(0, format):
                aoffset += " "
    for number in range(1, max_innings + 1):
        if number >= 10:
            tempnum = number - 10
        else:
            tempnum = number
        numlist += str(tempnum) + " "
    rbuffer = " "
    abuffer = ""
    hbuffer = ""
    if aruns >= 10 or hruns >= 10:
        rbuffer = "  "
        if aruns < 10:
            abuffer = " "
        elif hruns < 10:
            hbuffer = " "
    mobile_buffer = ""

    if max_innings > 9:
        sub = 6
    else:
        sub = 5

    for num in range(0, buffernum - sub):
        mobile_buffer += " "
    #fixes scorebook so it doesnt have commas
    trueascores = ""
    truehscores = ""
    for score in awayscores:
        trueascores += str(score) + " "
    for score in homescores:
        truehscores += str(score) + " "

    #pc print
    if pc:
        print()
        print("IP: " + str(max_innings) + " "+  mobile_buffer + " " + numlist + " R" + rbuffer + "H")
        print(aplayer + " " + aoffset, trueascores + " " + str(aruns) + abuffer, ahits)
        print(hplayer + " " + hoffset, truehscores + " " +  str(hruns) + hbuffer, hhits)
    #mobile print
    if mobile:
        print()
        print("IP: " + str(max_innings) + mobile_buffer + "  R" + rbuffer + "H")
        print(aplayer, aoffset, str(aruns) + abuffer, ahits)
        print(hplayer, hoffset, str(hruns) + hbuffer, hhits)
    return

# input your json file location here
# ex. "path/to/RioStatFile.json"
jason = "C:/MSSB StatFiles/NCL S4/BigNick at Super63.json"
statfile = create_json(jason)
aplayer = statfile.player(0)
hplayer = statfile.player(1)
events = statfile.events()
# can swap line below with: choice = "2"
# so it will print both always and not ask (or: choice = 0 | for only pc, and: choice = 2 | for only mobile
choice = input("PC Box, Mobile Box, or Both? 0/1/2: ")
book = input('Do you want the book printed? 0/1: ')
box = score_changes(choice)
box_print(box[0], box[1])


# just warning you: the code below is absolutely held together by one SINGLE string its that bad. glhf
if book == "0":
    exit()

for x in range(0,2):
    print()
    if x == 0:
        print("Away Player:", aplayer)
    else:
        print("Home Player:", hplayer)
    chars = statfile.characterName(x)
    offset = find_offset(chars)

    for y in range(0,2):
        title_offset = ""
        for num in range(-1, offset - 4):
            title_offset += " "
        if y == 0:
            print("Batter Stats")
            print("    ", title_offset, "Hits /", "RBI /", "HR /", "Steals /", "Stars /", "Batting Avg.")
            for z in range(0, 9):
                # these are spaces to add to make formatting good if the value is >= 10
                hits = statfile.hits(x,z)
                rbi = statfile.rbi(x, z)
                hr = statfile.homeruns(x, z)
                sb = statfile.basesStolen(x, z)
                stars = statfile.starHitsUsed(x, z)
                hoff = ten_buffer(hits)
                roff = ten_buffer(rbi)
                hroff = ten_buffer(hr)
                soff = ten_buffer(sb)
                stoff = ten_buffer(stars)

                try:
                    ba = round(statfile.battingAvg(x,z), 3)
                except ZeroDivisionError:
                    if statfile.atBats(x, z) == 0:
                        ba = "-"
                    else:
                        ba = 0
                real_offset = ""
                for num in range(-1, offset - len(chars[z])):
                    real_offset += " "
                print(chars[z], real_offset, hits, "   " + hoff, rbi, "  " + roff, hr, " " + hroff, sb, "     " + soff, stars, "    " + stoff, "{:.3f}".format(ba))
            # these are spaces to add to make formatting good if the value is >= 10
            hits = statfile.hits(x)
            rbi = statfile.rbi(x)
            hr = statfile.homeruns(x)
            sb = statfile.basesStolen(x)
            stars = statfile.starHitsUsed(x)
            hoff = ten_buffer(hits)
            roff = ten_buffer(rbi)
            hroff = ten_buffer(hr)
            soff = ten_buffer(sb)
            stoff = ten_buffer(stars)

            try:
                ba = statfile.battingAvg(x)
            except ZeroDivisionError:
                ba = 0
            real_offset = ""
            for num in range(-1, offset - 5):
                real_offset += " "
            print("TOTAL", real_offset, hits, "   " + hoff, rbi, "  " + roff, hr, " " + hroff, sb, "     " + soff, stars, "    " + stoff, "{:.3f}".format(round(ba, 3)))
        else:
            print()
            print("Pitcher Stats")
            print("    ", title_offset, "Big Plays /", "HA /", "K /", "RA /", "Stars /", "ERA")
            for z in range(0, 9):
                # these are spaces to add to make formatting good if the value is >= 10
                bp = statfile.bigPlays(x, z)
                ha = statfile.hitsAllowed(x, z)
                k = statfile.strikeoutsPitched(x, z)
                ra = statfile.runsAllowed(x, z)
                stars = statfile.starPitchesThrown(x, z)
                bpoff = ten_buffer(bp)
                haoff = ten_buffer(ha)
                koff = ten_buffer(k)
                raoff = ten_buffer(ra)
                stoff = ten_buffer(stars)
                real_offset = ""
                for num in range(-1, offset - len(chars[z])):
                    real_offset += " "

                if statfile.wasPitcher(x, z) == 1:
                    real_era = "{:.2f}".format(round(statfile.era(x, z), 2))
                else:
                    real_era = "-"
                print(chars[z], real_offset, bp, "        " + bpoff, ha, " " + haoff, k, "" + koff, ra, " " + raoff,
                      stars, "    " + stoff, real_era)
            # these are spaces to add to make formatting good if the value is >= 10
            bp = statfile.bigPlays(x)
            ha = statfile.hitsAllowed(x)
            k = statfile.strikeoutsPitched(x)
            ra = statfile.runsAllowed(x)
            stars = statfile.starPitchesThrown(x)
            bpoff = ten_buffer(bp)
            haoff = ten_buffer(ha)
            koff = ten_buffer(k)
            raoff = ten_buffer(ra)
            stoff = ten_buffer(stars)

            try:
                era = int(statfile.era(x))
            except ZeroDivisionError:
                era = 0
            real_offset = ""
            for num in range(0, offset - 4):
                real_offset += " "
            print("TOTAL", real_offset, bp, "        " + bpoff, ha, " " + haoff, k, "" + koff, ra, " " + raoff,
                  stars, "    " + stoff, "{:.2f}".format(round(era, 2)))

import os
def process_file(filename):
    input_file='P:\\bba\\' + filename
    output_file = 'P:\\bba-summary\\' + filename[:-4] + '.txt'
    print("writing " + str(output_file))
    f = open(output_file, 'w')
    
    f.write(input_file+'\n')

    f.write('\n                        -- Sorted by Board Number --\n')
    with open(input_file, 'r') as i_file:
        # Split the string into individual lines
        content = i_file.read()
        lines = content.strip().split('\n')

        results = {}
        notes = {}
        this_note = ''
        this_auction = ''
        auction = False
        par = ''
        optimum = False
        f.write('brd# dlr contract score  par     north            east             south            west             | auction...   | notes\n')
        f.write('---- --- -------- -----  ------  ---------------- ---------------- ---------------- ---------------- | ------------------------- \n')
        for line in lines:
            if line.startswith('[Board'):
                board_number = line[8:-2]
            if line.startswith('[Dealer'):
                dealer = ' ' + line[9] 
            if line.startswith('[Deal'):
                the_deal = line[9:-2]
            if line.startswith('[Declarer'):
                declarer = line[11:-2]
            if line.startswith('[Contract'):
                contract = line[11:-2]
            if line.startswith('[Score'):
                score = line[11:-2]
            if auction == True:
                if line.startswith('['):
                    # this marks the end of this auction; save the bidding.'
                    this_auction = this_auction.replace(' =','=')
                    this_auction = this_auction.replace('Pass', 'P')
                    bidding = '-'.join(this_auction.split()).replace('-P-P-P','')
                    auction = False
                else:
                    this_auction = this_auction + ' ' + line
            if line.startswith('[Auction'):
                # the next line(s) are the auction
                auction = True
            if line.startswith('[Note'):
                note = line[9].upper() + line[10:-2]   # upper case the first letter
                if note not in notes:
                    notes[note] = 1
                else:
                    notes[note] += 1
                this_note = this_note + ' | ' + note
            if optimum == True:
                txt = line.replace('NT', 'N')
                par = txt[0:3] + txt[4:6].rjust(3)
                optimum = False
            if line.startswith('[Optimum'):
                optimum = True
            if line.strip() == '':
                # I've got everything needed; so, write it out.
                summary = board_number.ljust(5) + dealer.ljust(4)  + (contract + '-' + declarer).ljust(9) + score.rjust(5) + '  ' + par.ljust(8) + the_deal + ' | ' + bidding + this_note
                f.write(summary + '\n')
                result = bidding + this_note
                if result not in results:
                    results[result] = 1
                else:
                    results[result] += 1
                
                this_note = ''
                this_auction = ''

    if this_auction != '':
        summary = board_number.ljust(5) + dealer.ljust(4)  + (contract + '-' + declarer).ljust(9) + score.rjust(5) + '  ' + par.ljust(8) + the_deal + ' | ' + bidding + this_note
        f.write(summary + '\n')
        result = bidding + this_note
        if result not in results:
            results[result] = 1
        else:
            results[result] += 1
    
    f.write('\n             -- Sorted Summary of Bidding Sequences --\n\n')
    for result in dict(sorted(results.items())):
        txt = str(results[result])
        f.write(txt.rjust(5) + '  ' + result +'\n')

    f.write('\n   -- Sorted Summary of Notes (the first character is forced to upper case) --\n\n')
    for note in dict(sorted(notes.items())):
        txt = str(notes[note])
        f.write(txt.rjust(5) + '  ' + note +'\n')

for file in os.listdir('P:\\bba\\'):
    n_files = 0
    if file.endswith(".pbn"):
        process_file(file)
        n_files += 1
        if n_files > 2:
            break
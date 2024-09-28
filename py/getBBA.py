import argparse
import sys
import re

parser = argparse.ArgumentParser(description="get BBA Stats")
parser.add_argument("--input", help="Name of input file")
args = parser.parse_args()
input = args.input

if input[-4:] != '.pbn':
    sys.exit("Input file must be .pbn")
input_file  = '/Users/adavidbailey/Practice-Bidding-Scenarios/bba/' + input

print("reading " + str(input_file))
output_file = input_file + '.txt'
print("writing " + str(output_file))
f = open(output_file, 'w')
f.write(input_file+'\n')


f.write('\n -- Sorted Board Number --\n')
with open(input_file, 'r') as i_file:
    # Split the string into individual lines
    content = i_file.read()
    lines = content.strip().split('\n')

    nBoards = 0  
    nDeals = 0
    nGames = 0
    results = {}
    this_note = ''
    this_auction = ''
    auction = False
    par = ''
    optimum = False
    f.write('board declarer contract score  par    | auction... notes' + '\n')
    for line in lines:
        if line.startswith('[Board'):
            board_number = line[8:-2]
            nBoards += 1
        if line.startswith('[Declarer'):
            declarer = line[11:-2]
        if line.startswith('[Contract'):
            contract = line[11:-2]
        if line.startswith('[Score'):
            score = line[11:-2]
            if declarer == 'N' or declarer == 'S': 
                nDeals = nDeals + 1
                if int(score)>150:
                    nGames = nGames + 1
        if auction == True:
            if line.startswith('['):
                # this marks the end of this auction; save the bidding.'
                bidding = '-'.join(this_auction.split()).replace('Pass', 'P').replace('-P-P-P','')
                auction = False
            else:
                this_auction = this_auction + ' ' + line
        if line.startswith('[Auction'):
            # the next line(s) are the auction
            auction = True
        if line.startswith('[Note'):
            note = line[9:-2].capitalize()
            this_note = this_note + ' | ' + note
        if optimum == True:
            par = line.strip()
            optimum = False
        if line.startswith('[Optimum'):
            optimum = True
        if line.startswith('[Play'):
            # I've got everything needed; so; write it out.
            result = bidding + ' ' + this_note
            f.write(board_number.rjust(5) + declarer.rjust(6) + contract.rjust(9) + score.rjust(9) + '  ' + par.ljust(7) + ' ' + result + '\n')
            
            if result not in results:
                results[result] = 1
            else:
                results[result] += 1
            this_note = ''
            this_auction = ''
   
    f.write('\n -- Sorted Bidding Sequences --\n')
    for result in dict(sorted(results.items())):
        txt = str(results[result])
        f.write(txt.rjust(5) + '  ' + result +'\n')
    
    f.write('\nSummary for ' + input_file + '\n')
    f.write('Deals N/S = ' + str(nDeals) + '\n')
    f.write('Games N/S = ' + str(nGames) + ' or ' + str(round(nGames/nDeals * 100, 2)) + '%\n')

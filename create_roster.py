import json


def create_roster(roster):
    event_roster = {}
    competitors = {}

    for line in roster.split('\n'):
        if 'Status,' in line:
            for index, competitor in enumerate(line.split(',')):
                if competitor != 'Status':
                    competitors[index] = competitor
                    event_roster[competitor] = []
        else:
            players = line.split(',')
            if players == ['']:
                continue
            status = players[0].lower()
            for index, competitor in competitors.items():
                player_name = players[index].split(' [')[0]
                pdga_num = players[index].split('[')[1][:-1]
                event_roster[competitor].append({
                    'name': player_name,
                    'pdga': int(pdga_num),
                    'status': status
                })

        # print(line)
    with open('event_roster.json', 'w') as f:
        json.dump(event_roster, f, indent=4)
    print(json.dumps(event_roster, indent=4))
    return event_roster

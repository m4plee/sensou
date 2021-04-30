from django.shortcuts import render
from . import sensou


def card_path(cards):
    path = []
    for card in cards:
        path.append(str(card[0]) + '_' + str(card[1]) + '.png')
    return path


def point(card):
    tup = card[0]
    point = tup[0]
    if point == 1:
        return 11
    else:
        return point


def game(request):
    if request.method == 'GET':
        is_gameover = False
        deck = sensou.Deck()
        cnt = 0
        player_get_num = 0
        com_get_num = 0
        plus = 0
        hand_num = 24 - int(cnt)

        request.session['deck'] = deck
        request.session['is_gameover'] = is_gameover
        request.session['plus'] = plus
        request.session['player_get_num'] = player_get_num
        request.session['com_get_num'] = com_get_num
        request.session['cnt'] = cnt

        d = {
            'message': '始めましょう！',
            'player_card': ['0_u.png'],
            'com_card': ['0_u.png'],
            'player_get_num': 0,
            'com_get_num': 0,
            'cnt': 0,
            'hands': ['0_u.png'] * hand_num,
        }

        return render(request, 'game.html', d)

    if request.method == 'POST':
        plus = request.session['plus']
        deck = request.session['deck']
        player_get_num = request.session['player_get_num']
        com_get_num = request.session['com_get_num']
        is_gameover = request.session['is_gameover']
        cnt = request.session['cnt']

        if 'your' in request.POST:
            player_card = [deck.emission()]
            com_card = [deck.emission()]
            player_get_num += 0
            com_get_num += 0

            if point(player_card) > point(com_card):
                deck = request.session['deck']
                is_gameover = request.session['is_gameover']
                player_get_num += 1 + plus
                com_get_num += 0
                cnt += 1
                plus = 0
                hand_num = 24 - int(cnt)
                if cnt == 26:
                    is_gameover = True
                else:
                    d = {
                        'message': 'プレイヤーに１ポイント入ります！',
                        'player_card': card_path(player_card),
                        'com_card': card_path(com_card),
                        'player_get_num': player_get_num,
                        'com_get_num': com_get_num,
                        'cnt': cnt,
                        'hands': ['0_u.png'] * hand_num,
                    }
                    player_card = list(player_card)
                    player_card.clear()
                    com_card = list(com_card)
                    com_card.clear()
                    return render(request, 'game.html', d)

            if point(com_card) > point(player_card):
                deck = request.session['deck']
                is_gameover = request.session['is_gameover']
                com_get_num += 1 + plus
                player_get_num += 0
                cnt += 1
                hand_num = 24 - int(cnt)
                plus = 0
                if cnt == 26:
                    is_gameover = True
                else:
                    d = {
                        'message': 'NPCに１ポイント入ります！',
                        'player_card': card_path(player_card),
                        'com_card': card_path(com_card),
                        'player_get_num': player_get_num,
                        'com_get_num': com_get_num,
                        'cnt': cnt,
                        'hands': ['0_u.png'] * hand_num,
                    }
                    player_card = list(player_card)
                    player_card.clear()
                    com_card = list(com_card)
                    com_card.clear()
                    return render(request, 'game.html', d)

            if point(com_card) == point(player_card):
                deck = request.session['deck']
                is_gameover = request.session['is_gameover']
                cnt += 1
                plus += 1
                hand_num = 24 - int(cnt)
                if cnt == 26:
                    is_gameover = True

                else:
                    d = {
                        'message': '引き分けです！もう一度カードを選んでください',
                        'player_card': card_path(player_card),
                        'com_card': card_path(com_card),
                        'player_get_num': player_get_num,
                        'com_get_num': com_get_num,
                        'cnt': cnt,
                        'hands': ['0_u.png'] * hand_num,
                    }
                    player_card = list(player_card)
                    player_card.clear()
                    com_card = list(com_card)
                    com_card.clear()
                    return render(request, 'game.html', d)

                if is_gameover:
                    player_get_num = request.session['player_get_num']
                    com_get_num = request.session['com_get_num']

                    if player_get_num > com_get_num:
                        msg = f'{player_get_num - com_get_num}ポイント差であなたの勝ちです！'
                    elif com_get_num > player_get_num:
                        msg = f'{com_get_num - player_get_num}ポイント差でNPCの勝ちです！'
                    else:
                        msg = '引き分けです！'

                    d = {
                        'message': msg,
                        'player_card': card_path(player_card),
                        'com_card': card_path(com_card),
                        'player_get_num': player_get_num,
                        'com_get_num': com_get_num,
                        'cnt': cnt,
                        'hands': ['0_u.png']
                    }
                    return render(request, 'game.html', d)

from django.shortcuts import render
from . import sensou


def card_path(cards):
    path = []
    for card in cards:
        path.append(str(card[0]) + '_' + str(card[1]) + '.png')
    return path


def game(request):
    if request.method == 'GET':
        is_gamestart = True
        is_gameover = False
        deck = sensou.Deck()
        cnt = 0
        player_get_num = 0
        com_get_num = 0
        plus = 0
        hand_num = 24 - int(cnt)

        request.session['deck'] = deck
        request.session['is_gameover'] = is_gameover
        request.session['is_gamestart'] = is_gamestart
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
            'hands': ['0_u.png'] * hand_num
        }

        return render(request, 'game.html', d)

    elif request.method == 'POST':
        plus = request.session['plus']
        deck = request.session['deck']
        player_get_num = request.session['player_get_num']
        com_get_num = request.session['com_get_num']
        is_gameover = request.session['is_gameover']
        cnt = request.session['cnt']

        if request.method == 'POST':
            is_gamestart = False
            player_card = [deck.emission()]
            com_card = [deck.emission()]
            player_get_num += 0
            com_get_num += 0

            if sensou.point(player_card) > sensou.point(com_card):
                player_get_num += 1 + plus
                com_get_num += 0
                cnt += 1
                plus = 0
                hand_num = 24 - int(cnt)
                deck = request.session['deck']
                is_gameover = request.session['is_gameover']
                d = {
                    'message': 'プレイヤーに１ポイント入ります！',
                    'player_card': card_path(player_card),
                    'com_card': card_path(com_card),
                    'player_get_num': player_get_num,
                    'com_get_num': com_get_num,
                    'cnt': cnt,
                    'hands': ['0_u.png'] * hand_num,
                }
                return render(request, 'game.html', d)

            elif sensou.point(com_card) > sensou.point(player_card):
                com_get_num += 1 + plus
                player_get_num += 0
                cnt += 1
                hand_num = 24 - int(cnt)
                deck = request.session['deck']
                is_gameover = request.session['is_gameover']
                plus = 0
                d = {
                    'message': 'NPCに１ポイント入ります！',
                    'player_card': card_path(player_card),
                    'com_card': card_path(com_card),
                    'player_get_num': player_get_num,
                    'com_get_num': com_get_num,
                    'cnt': cnt,
                    'hands': ['0_u.png'] * hand_num
                }
                return render(request, 'game.html', d)

            elif sensou.point(com_card) == sensou.point(player_card):
                cnt += 1
                plus += 1
                hand_num = 24 - int(cnt)
                player_card = player_card.clear()
                com_card = com_card.clear()
                player_card = [deck.emission()]
                com_card = [deck.emission()]

                d = {
                    'message': 'もう一度カードを選んでください',
                    'player_card': card_path(player_card),
                    'com_card': card_path(com_card),
                    'player_get_num': player_get_num,
                    'com_get_num': com_get_num,
                    'cnt': cnt,
                    'hands': ['0_u.png'] * hand_num
                }
                return render(request, 'game.html', d)

        if cnt == 26:
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
                'hands': ['0_u.png'] * hand_num
            }
            return render(request, 'game.html', d)

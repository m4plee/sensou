from django.shortcuts import render
from . import sensou


def str_card(card):
    path = []
    for i in card:
        path.append(str(card[0]) + '_' + str(card[1] + '.png'))


def game(request):
    if request.method == 'GET':
        is_gameover = False
        is_win = False
        deck = sensou.Deck()

        request.session['deck'] = deck
        request.session['is_gameover'] = is_gameover
        request.session['is_win'] = is_win

        d = {
            message = '始めましょう！',
            player_card = ['0_u.png'],
            com_card = ['0_u.png'],
            player_num = 0,
            com_num = 0,
        }

        return render(request, 'game.html', d)

    elif request.method == 'POST':
        deck = request.session['deck']
        is_gameover = request.session['is_gameover']
        is_win = request.session['is_win']

        if not is_gameover:
            player_card = [deck.emission()]
            com_card = [deck.emission()]

            if sensou.point(player_card) > sensou.point(com_card):
                player_num += 2
                d = {
                    message = 'プレイヤーの勝ちです！',
                    player_card = ['str_card(player_card)'],
                    com_card = ['str_card(com_card)'],
                    player_num = player_num,
                    com_num = com_num,
                }   
                return render(request, 'game.html', d)

            elif sensou.point(com_card) > sensou.point(player_card):
                com_num += 2
                d = {
                    message = 'コンピューターの勝ちです！',
                    player_card = ['str_card(player_card)'],
                    com_card = ['str_card(com_card)'],
                    player_num = player_num,
                    com_num = com_num,
                }   
                return render(request, 'game.html', d)

            else:
                cnt = 2
                difference = sensou.point(com_card) - sensou.point(player_card)
                while difference > 1:
                    player_card = player_card.clear()
                    com_card = com_card.clear()
                    player_card = [deck.emission()]
                    com_card = [deck.emission()]
                    cnt += 2
                    d = {
                        message = '引き分けです！',
                        player_card = ['str_card(player_card)'],
                        com_card = ['str_card(com_card)'],
                        player_num = player_num,
                        com_num = com_num,
                    } 

    


            